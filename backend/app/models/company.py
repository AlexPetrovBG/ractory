import uuid
from sqlalchemy import Column, String, Boolean, DateTime, func, Integer
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base

class Company(Base):
    """Company model representing an organization in the multi-tenant system."""
    __tablename__ = "companies"

    guid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    logo_path = Column(String, nullable=True)
    subscription_tier = Column(String, nullable=False, default="Basic")
    subscription_status = Column(String, nullable=False, default="trial")
    user_count = Column(Integer, nullable=False, default=0)
    projects_count = Column(Integer, nullable=False, default=0)
    workstations_count = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Company {self.name}>"

    @property
    def as_dict(self):
        """Convert model to dictionary for API responses."""
        return {
            "guid": str(self.guid),
            "name": self.name,
            "short_name": self.short_name,
            "logo_path": self.logo_path,
            "subscription_tier": self.subscription_tier,
            "subscription_status": self.subscription_status,
            "user_count": self.user_count,
            "projects_count": self.projects_count,
            "workstations_count": self.workstations_count,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        } 