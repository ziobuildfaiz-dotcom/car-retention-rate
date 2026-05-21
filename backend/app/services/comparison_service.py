from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.brand import Brand
from app.models.brand_series import BrandSeries
from app.models.car_model import CarModel
from app.models.retention_rate import RetentionRate


def compare_models(db: Session, model_ids: list[int]) -> dict:
    subq = (
        db.query(
            RetentionRate.model_id,
            func.max(RetentionRate.scrape_date).label("max_date"),
        )
        .group_by(RetentionRate.model_id)
        .subquery()
    )

    rates = (
        db.query(RetentionRate)
        .join(
            subq,
            (subq.c.model_id == RetentionRate.model_id)
            & (subq.c.max_date == RetentionRate.scrape_date),
        )
        .filter(RetentionRate.model_id.in_(model_ids))
        .all()
    )

    models = (
        db.query(CarModel)
        .join(BrandSeries, CarModel.series_id == BrandSeries.id)
        .join(Brand, BrandSeries.brand_id == Brand.id)
        .filter(CarModel.id.in_(model_ids))
        .all()
    )

    radar_data = {"models": [], "dimensions": ["1年保值率", "3年保值率", "5年保值率", "指导价指数", "样本量指数"]}

    for model in models:
        rate = next((r for r in rates if r.model_id == model.id), None)
        entry = {
            "name": f"{model.series.name if model.series else ''} {model.specific_model}",
            "guide_price": model.guide_price,
        }
        if rate:
            max_price = max((m.guide_price or 1 for m in models), default=1)
            max_samples = max((r.sample_count or 1 for r in rates), default=1)
            entry["values"] = [
                rate.retention_1yr or 0,
                rate.retention_3yr or 0,
                rate.retention_5yr or 0,
                round((model.guide_price or 0) / max_price * 100, 1),
                round((rate.sample_count or 0) / max_samples * 100, 1),
            ]
        else:
            entry["values"] = [0, 0, 0, 0, 0]
        radar_data["models"].append(entry)

    return radar_data


def compare_brands(
    db: Session,
    brand_ids: list[int],
    year_start: int | None = None,
    year_end: int | None = None,
):
    subq = (
        db.query(
            RetentionRate.model_id,
            func.max(RetentionRate.scrape_date).label("max_date"),
        )
        .group_by(RetentionRate.model_id)
        .subquery()
    )

    query = (
        db.query(
            Brand.name.label("brand_name"),
            CarModel.model_year,
            func.avg(RetentionRate.retention_3yr).label("avg_3yr"),
        )
        .join(BrandSeries, BrandSeries.brand_id == Brand.id)
        .join(CarModel, CarModel.series_id == BrandSeries.id)
        .join(RetentionRate, RetentionRate.model_id == CarModel.id)
        .join(
            subq,
            (subq.c.model_id == RetentionRate.model_id)
            & (subq.c.max_date == RetentionRate.scrape_date),
        )
        .filter(Brand.id.in_(brand_ids))
        .filter(RetentionRate.retention_3yr.isnot(None))
    )

    if year_start:
        query = query.filter(CarModel.model_year >= year_start)
    if year_end:
        query = query.filter(CarModel.model_year <= year_end)

    rows = (
        query.group_by(Brand.name, CarModel.model_year)
        .order_by(Brand.name, CarModel.model_year)
        .all()
    )

    brand_data: dict[str, list[dict]] = {}
    for brand_name, year, avg_3yr in rows:
        if brand_name not in brand_data:
            brand_data[brand_name] = []
        brand_data[brand_name].append({"year": year, "avg_3yr": round(float(avg_3yr), 1)})

    return {"brands": [{"name": k, "yearly": v} for k, v in brand_data.items()]}
