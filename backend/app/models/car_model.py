from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class CarModel(Base):
    __tablename__ = "car_model"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    series_id: Mapped[int] = mapped_column(Integer, ForeignKey("brand_series.id"), nullable=False)
    model_year: Mapped[int] = mapped_column(Integer, nullable=False)
    specific_model: Mapped[str] = mapped_column(String(300), nullable=False)
    guide_price: Mapped[float | None] = mapped_column(Float)
    displacement: Mapped[str | None] = mapped_column(String(50))
    fuel_type: Mapped[str | None] = mapped_column(String(50))
    transmission: Mapped[str | None] = mapped_column(String(50))

    series = relationship("BrandSeries", back_populates="models")
    retention_rates = relationship("RetentionRate", back_populates="model", lazy="selectin")
