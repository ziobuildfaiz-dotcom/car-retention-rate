from pydantic import BaseModel


class CarModelOut(BaseModel):
    id: int
    series_id: int
    model_year: int
    specific_model: str
    guide_price: float | None
    displacement: str | None
    fuel_type: str | None
    transmission: str | None
    brand_name: str | None = None
    series_name: str | None = None

    model_config = {"from_attributes": True}


class CarModelListOut(BaseModel):
    items: list[CarModelOut]
    total: int


class RetentionOut(BaseModel):
    id: int
    model_id: int
    source: str
    scrape_date: str
    retention_1yr: float | None
    retention_2yr: float | None
    retention_3yr: float | None
    retention_4yr: float | None
    retention_5yr: float | None
    avg_listed_price: float | None
    sample_count: int | None

    model_config = {"from_attributes": True}


class ModelDetailOut(CarModelOut):
    retention_rates: list[RetentionOut] = []


class RankingItem(BaseModel):
    rank: int
    model_id: int
    model_name: str
    series_name: str
    brand_name: str
    model_year: int
    guide_price: float | None
    retention: float


class BrandRankingItem(BaseModel):
    rank: int
    brand_id: int
    brand_name: str
    avg_retention: float
    model_count: int


class FilterMeta(BaseModel):
    vehicle_types: list[str]
    fuel_types: list[str]
    countries: list[str]
    year_range: tuple[int, int]
    price_range: tuple[float, float]


class ComparisonRequest(BaseModel):
    model_ids: list[int]


class ComparisonBrandRequest(BaseModel):
    brand_ids: list[int]
    year_start: int | None = None
    year_end: int | None = None
