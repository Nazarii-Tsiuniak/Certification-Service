import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CertificateVerificationResponse(BaseModel):
    certificate_uuid: uuid.UUID
    user_id: uuid.UUID
    course_id: uuid.UUID
    student_name: str
    course_title: str
    issued_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DownloadUrlResponse(BaseModel):
    certificate_id: uuid.UUID
    download_url: str
    expires_in_seconds: int


class CourseCompletedEvent(BaseModel):
    user_id: uuid.UUID
    course_id: uuid.UUID
