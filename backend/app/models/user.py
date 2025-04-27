import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base

class User(Base):
    __tablename__ = "users"
    
    guid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_guid = Column(UUID(as_uuid=True), ForeignKey("companies.guid"), nullable=False)
    email = Column(String, unique=True, nullable=False)
    pwd_hash = Column(String, nullable=False)
    role = Column(String, nullable=False) # Consider using Enum type here
    pin = Column(String(6), nullable=True)  # For operators
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    company = relationship("Company", back_populates="users")
    
    def __repr__(self):
        return f"<User guid={self.guid}, email={self.email}, role={self.role}>" 