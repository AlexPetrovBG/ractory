import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base, TimestampMixin
from .enums import UserRole

class User(Base, TimestampMixin):
    __tablename__ = "users"
    
    guid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_guid = Column(UUID(as_uuid=True), ForeignKey("companies.guid"), nullable=False)
    email = Column(String, unique=True, nullable=False)
    pwd_hash = Column(String, nullable=False)
    role = Column(String, nullable=False) # Consider using Enum type here
    pin = Column(String(6), nullable=True)  # For operators
    is_active = Column(Boolean, default=True, nullable=False)
    name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    picture_path = Column(String, nullable=True)
    
    # Relationships
    company = relationship("Company", back_populates="users")
    workflows = relationship("Workflow", back_populates="user")
    
    def __repr__(self):
        return f"<User guid={self.guid}, email={self.email}, role={self.role}>" 