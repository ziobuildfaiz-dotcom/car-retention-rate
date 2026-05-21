from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class BrandSeries(Base):
    __tablename__ = "brand_series"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    brand_id: Mapped[int] = mapped_column(Integer, ForeignKey("brand.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    vehicle_type: Mapped[str | None] = mapped_column(String(50))

    brand = relationship("Brand", back_populates="series_list")
    models = relationship("CarModel", back_populates="series", lazy="selectin")
