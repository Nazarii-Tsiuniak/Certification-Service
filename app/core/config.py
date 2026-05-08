from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "certification-service"
    app_env: str = "dev"
    database_url: str = Field(
        default="postgresql+psycopg://cert_user:cert_pass@postgres:5432/certdb"
    )

    rabbitmq_url: str = "amqp://guest:guest@rabbitmq:5672/"
    rabbitmq_queue: str = "course.events"

    s3_endpoint_url: str = "http://localstack:4566"
    s3_region: str = "us-east-1"
    s3_access_key: str = "test"
    s3_secret_key: str = "test"
    s3_bucket: str = "certificates"

    jwt_secret: str = "super-secret"
    jwt_algorithm: str = "HS256"

    student_service_url: str = "http://student-service:8000"
    course_service_url: str = "http://course-service:8000"

    presigned_url_expiration_seconds: int = 900

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
