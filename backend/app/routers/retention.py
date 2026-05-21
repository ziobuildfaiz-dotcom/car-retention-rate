from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.model import BrandRankingItem, FilterMeta, RankingItem
from app.services.retention_service import (
    get_brand_rankings,
    get_filter_meta,
    get_model_rankings,
)

router = APIRouter(tags=["retention"])


@router.get("/rankings", response_model=list[RankingItem])
def model_rankings(
    retention_period: str = Query("3yr", pattern=r"^(1yr|2yr|3yr|4yr|5yr)$"),
    vehicle_type: str | None = Query(None),
    model_year: int | None = Query(None),
    brand_id: int | None = Query(None),
    top_n: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return get_model_rankings(
        db,
        retention_period=retention_period,
        vehicle_type=vehicle_type,
        model_year=model_year,
        brand_id=brand_id,
        top_n=top_n,
    )


@router.get("/rankings/brands", response_model=list[BrandRankingItem])
def brand_rankings(
    retention_period: str = Query("3yr", pattern=r"^(1yr|2yr|3yr|4yr|5yr)$"),
    top_n: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    return get_brand_rankings(db, retention_period=retention_period, top_n=top_n)


@router.get("/meta/filters", response_model=FilterMeta)
def filter_metadata(db: Session = Depends(get_db)):
    return get_filter_meta(db)
