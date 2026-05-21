from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, SessionLocal, engine
from app.models import Brand
from app.routers import brands, comparison, models, retention


def auto_seed_if_empty():
    db = SessionLocal()
    try:
        if db.query(Brand).count() == 0:
            from seed_data_large import seed
            seed()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    auto_seed_if_empty()
    yield


app = FastAPI(title="汽车保值率可视化平台", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(brands.router, prefix=settings.api_prefix)
app.include_router(models.router, prefix=settings.api_prefix)
app.include_router(retention.router, prefix=settings.api_prefix)
app.include_router(comparison.router, prefix=settings.api_prefix)


@app.get("/health")
def health():
    return {"status": "ok"}
