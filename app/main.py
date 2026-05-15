import time
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.events_routes import events_router
from app.api.v1.private_routes import private_router
from app.api.v1.public_routes import public_router
from app.core.config import settings
from app.domain.models import Certificate
from app.infrastructure.db import Base, engine
from app.infrastructure.s3_storage import S3Storage


@asynccontextmanager
async def lifespan(app: FastAPI):
    max_attempts = 20
    attempt = 0
    last_error = None

    while attempt < max_attempts:
        attempt += 1
        try:
            Base.metadata.create_all(bind=engine, tables=[Certificate.__table__])

            s3 = S3Storage(
                endpoint_url=settings.s3_endpoint_url,
                region=settings.s3_region,
                access_key=settings.s3_access_key,
                secret_key=settings.s3_secret_key,
                bucket=settings.s3_bucket,
            )
            s3.ensure_bucket()
            last_error = None
            break
        except Exception as exc:
            last_error = exc
            time.sleep(3)

    if last_error is not None:
        raise last_error

    yield


app = FastAPI(title="Certification Service", version="1.0.0", lifespan=lifespan)
app.include_router(public_router)
app.include_router(private_router)
app.include_router(events_router)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}
