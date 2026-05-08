# Certification Service

Certification Service for a microservice-based E-Learning platform.

## Features

- FastAPI REST API
- PostgreSQL persistence (UUID PKs)
- RabbitMQ consumer for `CourseCompleted` events
- Snapshot storage of Student/Course data
- PDF generation with ReportLab
- S3 upload and presigned URLs (LocalStack in local env)
- JWT Bearer auth for private endpoint

## Architecture

Layered architecture:

- Controller: `app/api/v1/*.py`
- Service: `app/services/*.py`
- Domain: `app/domain/*.py`
- Infrastructure: `app/infrastructure/*.py`, `app/worker/*.py`

## API Endpoints

- Public: `GET /api/v1/certificates/verify/{uuid}`
- Private: `GET /api/v1/certificates/{id}/download` (JWT required)

OpenAPI spec: `docs/swagger.yaml`

AsyncAPI spec: `docs/asyncapi.yaml`

## Run with Docker Compose

```bash
docker-compose up --build
```

Services:

- `certification-service` on `http://localhost:8000`
- PostgreSQL on `localhost:5432`
- RabbitMQ on `localhost:5672` (management UI `http://localhost:15672`)
- LocalStack S3 on `localhost:4566`

## Run tests

```bash
pip install -r requirements.txt
pytest
```

## Environment Variables

Configured via docker-compose by default.

Important keys:

- `DATABASE_URL`
- `RABBITMQ_URL`
- `RABBITMQ_QUEUE`
- `S3_ENDPOINT_URL`, `S3_BUCKET`, `S3_REGION`
- `JWT_SECRET`, `JWT_ALGORITHM`
- `STUDENT_SERVICE_URL`, `COURSE_SERVICE_URL`
