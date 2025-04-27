import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, UUID as pgUUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base

class ApiKey(Base):
    __tablename__ = "api_keys"
    
    guid = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_guid = Column(pgUUID(as_uuid=True), ForeignKey("companies.guid"), nullable=False)
    key_hash = Column(String, nullable=False, unique=True) # Store hash, not the key itself
    description = Column(String, nullable=True)
    scopes = Column(String, nullable=True) # Comma-separated scopes or JSON? Start simple.
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    company = relationship("Company", back_populates="api_keys")
    
    def __repr__(self):
        return f"<ApiKey guid={self.guid}, company_guid={self.company_guid}, description={self.description}>" 