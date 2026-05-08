import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.domain.schemas import CertificateVerificationResponse
from app.infrastructure.db import get_db_session
from app.services.dependencies import get_certification_service

public_router = APIRouter(prefix="/api/v1/certificates", tags=["certificates-public"])


@public_router.get("/verify/{certificate_uuid}", response_model=CertificateVerificationResponse)
def verify_certificate(certificate_uuid: uuid.UUID, db: Session = Depends(get_db_session)):
    service = get_certification_service(db)
    cert = service.verify_certificate(certificate_uuid)
    return CertificateVerificationResponse(
        certificate_uuid=cert.certificate_uuid,
        user_id=cert.user_id,
        course_id=cert.course_id,
        student_name=cert.student_name_snapshot,
        course_title=cert.course_title_snapshot,
        issued_at=cert.issued_at,
    )
