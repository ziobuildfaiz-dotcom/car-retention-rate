from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.model import (
    CarModelOut,
    ComparisonBrandRequest,
    ComparisonRequest,
    RetentionOut,
)
from app.services.comparison_service import compare_brands, compare_models
from app.services.model_service import get_model_detail

router = APIRouter(prefix="/comparison", tags=["comparison"])


@router.post("")
def model_comparison(body: ComparisonRequest, db: Session = Depends(get_db)):
    models = []
    for mid in body.model_ids:
        m = get_model_detail(db, mid)
        if m:
            models.append(m)
    if len(models) < 2:
        return {"models": models, "message": "Need at least 2 models for comparison"}

    radar_data = compare_models(db, body.model_ids)
    return {
        "models": [CarModelOut.model_validate(m) for m in models],
        "radar_data": radar_data,
    }


@router.post("/brands")
def brand_comparison(body: ComparisonBrandRequest, db: Session = Depends(get_db)):
    return compare_brands(db, body.brand_ids, body.year_start, body.year_end)
