from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.brand import BrandDetailOut, BrandListOut, BrandOut
from app.services.brand_service import get_brand_detail, get_brands

router = APIRouter(prefix="/brands", tags=["brands"])


@router.get("", response_model=BrandListOut)
def list_brands(
    country: str | None = Query(None),
    search: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items, total = get_brands(db, country=country, search=search, page=page, page_size=page_size)
    return BrandListOut(items=[BrandOut.model_validate(b) for b in items], total=total)


@router.get("/{brand_id}", response_model=BrandDetailOut)
def brand_detail(brand_id: int, db: Session = Depends(get_db)):
    return get_brand_detail(db, brand_id)
