import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_current_user_id
from app.domain.schemas import DownloadUrlResponse
from app.infrastructure.db import get_db_session
from app.services.dependencies import get_certification_service

private_router = APIRouter(prefix="/api/v1/certificates", tags=["certificates-private"])


@private_router.get("/{certificate_id}/download", response_model=DownloadUrlResponse)
def download_certificate(
    certificate_id: uuid.UUID,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db_session),
):
    service = get_certification_service(db)
    url = service.get_download_url(certificate_id=certificate_id, request_user_id=user_id)
    return DownloadUrlResponse(
        certificate_id=certificate_id,
        download_url=url,
        expires_in_seconds=settings.presigned_url_expiration_seconds,
    )
