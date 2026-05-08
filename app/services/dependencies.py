from sqlalchemy.orm import Session

from app.core.config import settings
from app.infrastructure.external_clients import CourseClient, StudentClient
from app.infrastructure.pdf_generator import PdfGenerator
from app.infrastructure.repository import CertificateRepository
from app.infrastructure.s3_storage import S3Storage
from app.services.certification_service import CertificationService


def get_certification_service(db: Session) -> CertificationService:
    return CertificationService(
        repository=CertificateRepository(db),
        student_client=StudentClient(settings.student_service_url),
        course_client=CourseClient(settings.course_service_url),
        pdf_generator=PdfGenerator(),
        s3_storage=S3Storage(
            endpoint_url=settings.s3_endpoint_url,
            region=settings.s3_region,
            access_key=settings.s3_access_key,
            secret_key=settings.s3_secret_key,
            bucket=settings.s3_bucket,
        ),
    )
