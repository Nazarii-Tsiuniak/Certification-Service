from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.orm import Session

from app.domain.schemas import LifecycleEvent
from app.infrastructure.db import get_db_session
from app.services.dependencies import get_certification_service

events_router = APIRouter(prefix="/api/v1/events", tags=["events"])


@events_router.post("/lifecycle", status_code=status.HTTP_202_ACCEPTED)
def ingest_lifecycle_event(
    event: Annotated[LifecycleEvent, Body(discriminator="event_type")],
    db: Session = Depends(get_db_session),
):
    service = get_certification_service(db)
    return service.handle_lifecycle_event(event)
