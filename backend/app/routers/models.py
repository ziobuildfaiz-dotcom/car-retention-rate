from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.model import CarModelListOut, CarModelOut, ModelDetailOut
from app.services.model_service import get_model_detail, get_models

router = APIRouter(prefix="/models", tags=["models"])


@router.get("", response_model=CarModelListOut)
def list_models(
    series_id: int | None = Query(None),
    model_year: int | None = Query(None),
    fuel_type: str | None = Query(None),
    sort_by: str = Query("id"),
    order: str = Query("desc"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items, total = get_models(
        db,
        series_id=series_id,
        model_year=model_year,
        fuel_type=fuel_type,
        sort_by=sort_by,
        order=order,
        page=page,
        page_size=page_size,
    )
    return CarModelListOut(items=[CarModelOut.model_validate(m) for m in items], total=total)


@router.get("/{model_id}", response_model=ModelDetailOut)
def model_detail(model_id: int, db: Session = Depends(get_db)):
    model = get_model_detail(db, model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model
