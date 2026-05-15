import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import HTTPException, status

from app.core.config import settings
from app.domain.models import Certificate
from app.domain.schemas import LifecycleEvent
from app.infrastructure.external_clients import CourseClient, StudentClient
from app.infrastructure.pdf_generator import PdfGenerator
from app.infrastructure.repository import CertificateRepository
from app.infrastructure.s3_storage import S3Storage


class CertificationService:
    def __init__(
        self,
        repository: CertificateRepository,
        student_client: StudentClient,
        course_client: CourseClient,
        pdf_generator: PdfGenerator,
        s3_storage: S3Storage,
    ):
        self.repository = repository
        self.student_client = student_client
        self.course_client = course_client
        self.pdf_generator = pdf_generator
        self.s3_storage = s3_storage

    def issue_from_course_completed(self, user_id: uuid.UUID, course_id: uuid.UUID) -> Certificate:
        student_name = self.student_client.get_student_name(str(user_id))
        course_title = self.course_client.get_course_title(str(course_id))
        issued_at = datetime.now(timezone.utc)
        certificate_uuid = uuid.uuid4()

        pdf_content = self.pdf_generator.generate_certificate_pdf(
            certificate_uuid=str(certificate_uuid),
            student_name=student_name,
            course_title=course_title,
            issued_at=issued_at.isoformat(),
        )

        s3_key = f"certificates/{user_id}/{course_id}/{certificate_uuid}.pdf"
        self.s3_storage.upload_pdf(s3_key, pdf_content)

        certificate = Certificate(
            certificate_uuid=certificate_uuid,
            user_id=user_id,
            course_id=course_id,
            student_name_snapshot=student_name,
            course_title_snapshot=course_title,
            issued_at=issued_at,
            pdf_s3_key=s3_key,
        )
        return self.repository.create(certificate)

    def handle_lifecycle_event(self, event: LifecycleEvent) -> dict[str, Any]:
        if event.event_type == "course.completed":
            cert = self.issue_from_course_completed(
                user_id=event.user_id,
                course_id=event.course_id,
            )
            return {
                "status": "processed",
                "event_type": event.event_type,
                "certificate_id": str(cert.id),
            }

        return {"status": "processed", "event_type": event.event_type}

    def verify_certificate(self, certificate_uuid: uuid.UUID) -> Certificate:
        certificate = self.repository.get_by_certificate_uuid(certificate_uuid)
        if not certificate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Certificate not found",
            )
        return certificate

    def get_download_url(self, certificate_id: uuid.UUID, request_user_id: uuid.UUID) -> str:
        certificate = self.repository.get_by_id(certificate_id)
        if not certificate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Certificate not found",
            )

        if certificate.user_id != request_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot access this certificate",
            )

        return self.s3_storage.generate_presigned_url(
            key=certificate.pdf_s3_key,
            expires_in=settings.presigned_url_expiration_seconds,
        )
