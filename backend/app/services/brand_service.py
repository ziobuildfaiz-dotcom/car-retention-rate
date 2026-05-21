from sqlalchemy.orm import Session

from app.models.brand import Brand


def get_brands(
    db: Session,
    country: str | None = None,
    search: str | None = None,
    page: int = 1,
    page_size: int = 20,
):
    query = db.query(Brand)

    if country:
        query = query.filter(Brand.country == country)
    if search:
        query = query.filter(Brand.name.contains(search))

    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return items, total


def get_brand_detail(db: Session, brand_id: int) -> Brand | None:
    return db.query(Brand).filter(Brand.id == brand_id).first()
