import uuid
from datetime import datetime, timezone

import pytest
from fastapi import HTTPException

from app.services.certification_service import CertificationService


class FakeRepo:
    def __init__(self):
        self.by_uuid = {}
        self.by_id = {}

    def get_by_certificate_uuid(self, certificate_uuid):
        return self.by_uuid.get(certificate_uuid)

    def get_by_id(self, certificate_id):
        return self.by_id.get(certificate_id)

    def create(self, certificate):
        if not getattr(certificate, "id", None):
            certificate.id = uuid.uuid4()
        self.by_uuid[certificate.certificate_uuid] = certificate
        self.by_id[certificate.id] = certificate
        return certificate


class FakeStudentClient:
    def get_student_name(self, _):
        return "John Doe"


class FakeCourseClient:
    def get_course_title(self, _):
        return "Distributed Systems"


class FakePdfGenerator:
    def generate_certificate_pdf(self, **kwargs):
        return f"pdf-{kwargs['certificate_uuid']}".encode()


class FakeS3:
    def __init__(self):
        self.uploaded = {}

    def upload_pdf(self, key, content):
        self.uploaded[key] = content

    def generate_presigned_url(self, key, expires_in):
        return f"https://s3.local/{key}?exp={expires_in}"


class CertObj:
    pass


@pytest.fixture
def service():
    repo = FakeRepo()
    s3 = FakeS3()

    svc = CertificationService(
        repository=repo,
        student_client=FakeStudentClient(),
        course_client=FakeCourseClient(),
        pdf_generator=FakePdfGenerator(),
        s3_storage=s3,
    )
    return svc, repo, s3


def test_issue_from_course_completed_creates_snapshot_and_pdf(service):
    svc, _, s3 = service
    user_id = uuid.uuid4()
    course_id = uuid.uuid4()

    cert = svc.issue_from_course_completed(user_id=user_id, course_id=course_id)

    assert cert.student_name_snapshot == "John Doe"
    assert cert.course_title_snapshot == "Distributed Systems"
    assert cert.user_id == user_id
    assert cert.course_id == course_id
    assert cert.pdf_s3_key in s3.uploaded


def test_verify_certificate_not_found(service):
    svc, _, _ = service
    with pytest.raises(HTTPException) as exc:
        svc.verify_certificate(uuid.uuid4())
    assert exc.value.status_code == 404


def test_get_download_url_forbidden(service):
    svc, repo, _ = service

    cert = CertObj()
    cert.id = uuid.uuid4()
    cert.certificate_uuid = uuid.uuid4()
    cert.user_id = uuid.uuid4()
    cert.course_id = uuid.uuid4()
    cert.student_name_snapshot = "Jane"
    cert.course_title_snapshot = "Python"
    cert.issued_at = datetime.now(timezone.utc)
    cert.pdf_s3_key = "certificates/a.pdf"

    repo.by_id[cert.id] = cert

    with pytest.raises(HTTPException) as exc:
        svc.get_download_url(cert.id, uuid.uuid4())
    assert exc.value.status_code == 403
