import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base
from app.models.enums import Role

class User(Base):
    """User model for authentication and authorization."""
    __tablename__ = "users"

    guid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_guid = Column(UUID(as_uuid=True), ForeignKey("companies.guid"), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    pwd_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)
    pin = Column(String(6), nullable=True)  # 6-digit PIN for operators
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<User {self.email}>" 