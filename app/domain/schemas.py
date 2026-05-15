import uuid
from datetime import datetime
from typing import Literal, Union

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


class UserOnboardedEvent(BaseModel):
    event_type: Literal["user.onboarded"]
    user_id: uuid.UUID
    email: str
    full_name: str
    registered_at: datetime


class UserDetailsUpdatedEvent(BaseModel):
    event_type: Literal["user.details.updated"]
    user_id: uuid.UUID
    email: str | None = None
    full_name: str | None = None
    updated_at: datetime


class CourseStartedEvent(BaseModel):
    event_type: Literal["course.started"]
    user_id: uuid.UUID
    course_id: uuid.UUID
    started_at: datetime


class CourseIntermediateControlPassedEvent(BaseModel):
    event_type: Literal["course.intermediate_control.passed"]
    user_id: uuid.UUID
    course_id: uuid.UUID
    control_id: uuid.UUID
    score: float
    passed_at: datetime


class CourseUpdatedEvent(BaseModel):
    event_type: Literal["course.updated"]
    course_id: uuid.UUID
    title: str | None = None
    description: str | None = None
    updated_at: datetime


class CourseCompletedLifecycleEvent(BaseModel):
    event_type: Literal["course.completed"]
    user_id: uuid.UUID
    course_id: uuid.UUID


LifecycleEvent = Union[
    UserOnboardedEvent,
    UserDetailsUpdatedEvent,
    CourseStartedEvent,
    CourseIntermediateControlPassedEvent,
    CourseUpdatedEvent,
    CourseCompletedLifecycleEvent,
]
