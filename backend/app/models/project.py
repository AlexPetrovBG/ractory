import uuid
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy as sa

from app.core.database import Base
from .base import TimestampMixin

class Project(Base, TimestampMixin):
    """Project model representing data synced from RaWorkshop."""
    __tablename__ = "projects"

    guid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_id = Column(Integer, nullable=False, index=True, comment="RaWorkshop ID")
    company_guid = Column(UUID(as_uuid=True), ForeignKey("companies.guid"), nullable=False, index=True)
    
    code = Column(String, index=True, comment="Project code identifier")
    creation_date = Column(DateTime(timezone=True), comment="When the project was created")
    modified_date = Column(DateTime(timezone=True), comment="When the project was last modified")
    due_date = Column(DateTime(timezone=True), comment="Project deadline")
    check_sum = Column(String, comment="Validation checksum")
    in_production = Column(Boolean, default=True, comment="Flag indicating if project is in production")
    company_name = Column(String, comment="Name of the company associated with the project")
    
    synced_at = Column(DateTime(timezone=True), server_default=func.now(), comment="When the project was last synced")
    
    # Add unique constraint on original_id and company_guid
    __table_args__ = (sa.UniqueConstraint('original_id', 'company_guid', name='uq_project_original_id_company'),)

    def __repr__(self):
        return f"<Project {self.code or self.original_id} (Company: {self.company_guid})>" 