import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.models import Certificate


class CertificateRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_certificate_uuid(self, certificate_uuid: uuid.UUID) -> Optional[Certificate]:
        stmt = select(Certificate).where(Certificate.certificate_uuid == certificate_uuid)
        return self.db.scalar(stmt)

    def get_by_id(self, certificate_id: uuid.UUID) -> Optional[Certificate]:
        stmt = select(Certificate).where(Certificate.id == certificate_id)
        return self.db.scalar(stmt)

    def create(self, certificate: Certificate) -> Certificate:
        self.db.add(certificate)
        self.db.commit()
        self.db.refresh(certificate)
        return certificate
