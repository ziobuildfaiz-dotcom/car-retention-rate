from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.brand import Brand
from app.models.brand_series import BrandSeries
from app.models.car_model import CarModel
from app.models.retention_rate import RetentionRate
from app.schemas.model import BrandRankingItem, FilterMeta, RankingItem


def get_model_rankings(
    db: Session,
    retention_period: str = "3yr",
    vehicle_type: str | None = None,
    model_year: int | None = None,
    brand_id: int | None = None,
    top_n: int = 20,
):
    retention_col = getattr(RetentionRate, f"retention_{retention_period}")

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
            CarModel,
            Brand.name.label("brand_name"),
            BrandSeries.name.label("series_name"),
            retention_col.label("retention"),
        )
        .join(BrandSeries, CarModel.series_id == BrandSeries.id)
        .join(Brand, BrandSeries.brand_id == Brand.id)
        .join(RetentionRate, RetentionRate.model_id == CarModel.id)
        .join(
            subq,
            (subq.c.model_id == RetentionRate.model_id)
            & (subq.c.max_date == RetentionRate.scrape_date),
        )
        .filter(retention_col.isnot(None))
    )

    if vehicle_type:
        query = query.filter(BrandSeries.vehicle_type == vehicle_type)
    if model_year:
        query = query.filter(CarModel.model_year == model_year)
    if brand_id:
        query = query.filter(Brand.id == brand_id)

    rows = query.order_by(retention_col.desc()).limit(top_n).all()

    results = []
    for idx, (model, brand_name, series_name, retention) in enumerate(rows, 1):
        results.append(
            RankingItem(
                rank=idx,
                model_id=model.id,
                model_name=model.specific_model,
                series_name=series_name,
                brand_name=brand_name,
                model_year=model.model_year,
                guide_price=model.guide_price,
                retention=round(float(retention), 1),
            )
        )
    return results


def get_brand_rankings(
    db: Session,
    retention_period: str = "3yr",
    top_n: int = 10,
):
    retention_col = getattr(RetentionRate, f"retention_{retention_period}")

    subq = (
        db.query(
            RetentionRate.model_id,
            func.max(RetentionRate.scrape_date).label("max_date"),
        )
        .group_by(RetentionRate.model_id)
        .subquery()
    )

    rows = (
        db.query(
            Brand.id.label("brand_id"),
            Brand.name.label("brand_name"),
            func.avg(retention_col).label("avg_retention"),
            func.count(func.distinct(CarModel.id)).label("model_count"),
        )
        .join(BrandSeries, BrandSeries.brand_id == Brand.id)
        .join(CarModel, CarModel.series_id == BrandSeries.id)
        .join(RetentionRate, RetentionRate.model_id == CarModel.id)
        .join(
            subq,
            (subq.c.model_id == RetentionRate.model_id)
            & (subq.c.max_date == RetentionRate.scrape_date),
        )
        .filter(retention_col.isnot(None))
        .group_by(Brand.id)
        .order_by(func.avg(retention_col).desc())
        .limit(top_n)
        .all()
    )

    return [
        BrandRankingItem(
            rank=idx,
            brand_id=row.brand_id,
            brand_name=row.brand_name,
            avg_retention=round(float(row.avg_retention), 1),
            model_count=row.model_count,
        )
        for idx, row in enumerate(rows, 1)
    ]


def get_filter_meta(db: Session):
    vehicle_types = [
        r[0]
        for r in db.query(BrandSeries.vehicle_type)
        .filter(BrandSeries.vehicle_type.isnot(None))
        .distinct()
        .all()
    ]

    fuel_types = [
        r[0]
        for r in db.query(CarModel.fuel_type)
        .filter(CarModel.fuel_type.isnot(None))
        .distinct()
        .all()
    ]

    countries = [
        r[0]
        for r in db.query(Brand.country).filter(Brand.country.isnot(None)).distinct().all()
    ]

    year_range = db.query(
        func.min(CarModel.model_year), func.max(CarModel.model_year)
    ).first()

    price_range = db.query(
        func.min(CarModel.guide_price), func.max(CarModel.guide_price)
    ).filter(CarModel.guide_price.isnot(None)).first()

    return FilterMeta(
        vehicle_types=vehicle_types,
        fuel_types=fuel_types,
        countries=countries,
        year_range=(year_range[0] or 2000, year_range[1] or 2025),
        price_range=(price_range[0] or 5.0, price_range[1] or 200.0),
    )
