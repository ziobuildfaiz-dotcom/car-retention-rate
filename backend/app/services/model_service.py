from sqlalchemy.orm import Session

from app.models.brand import Brand
from app.models.brand_series import BrandSeries
from app.models.car_model import CarModel


def get_models(
    db: Session,
    series_id: int | None = None,
    model_year: int | None = None,
    fuel_type: str | None = None,
    sort_by: str = "id",
    order: str = "desc",
    page: int = 1,
    page_size: int = 20,
):
    query = (
        db.query(CarModel)
        .join(BrandSeries, CarModel.series_id == BrandSeries.id)
        .join(Brand, BrandSeries.brand_id == Brand.id)
    )

    if series_id:
        query = query.filter(CarModel.series_id == series_id)
    if model_year:
        query = query.filter(CarModel.model_year == model_year)
    if fuel_type:
        query = query.filter(CarModel.fuel_type == fuel_type)

    total = query.count()

    sort_col = getattr(CarModel, sort_by, CarModel.id)
    if order == "desc":
        query = query.order_by(sort_col.desc())
    else:
        query = query.order_by(sort_col.asc())

    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return items, total


def get_model_detail(db: Session, model_id: int) -> CarModel | None:
    return db.query(CarModel).filter(CarModel.id == model_id).first()
