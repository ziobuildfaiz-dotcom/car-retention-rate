from pydantic import BaseModel


class BrandOut(BaseModel):
    id: int
    name: str
    name_en: str | None
    country: str | None
    logo_url: str | None

    model_config = {"from_attributes": True}


class BrandListOut(BaseModel):
    items: list[BrandOut]
    total: int


class SeriesOut(BaseModel):
    id: int
    brand_id: int
    name: str
    vehicle_type: str | None

    model_config = {"from_attributes": True}


class BrandDetailOut(BrandOut):
    series_list: list[SeriesOut] = []
