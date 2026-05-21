from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class RetentionRate(Base):
    __tablename__ = "retention_rate"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    model_id: Mapped[int] = mapped_column(Integer, ForeignKey("car_model.id"), nullable=False)
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    scrape_date: Mapped[date] = mapped_column(Date, nullable=False)
    retention_1yr: Mapped[float | None] = mapped_column(Float)
    retention_2yr: Mapped[float | None] = mapped_column(Float)
    retention_3yr: Mapped[float | None] = mapped_column(Float)
    retention_4yr: Mapped[float | None] = mapped_column(Float)
    retention_5yr: Mapped[float | None] = mapped_column(Float)
    avg_listed_price: Mapped[float | None] = mapped_column(Float)
    sample_count: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    model = relationship("CarModel", back_populates="retention_rates")
