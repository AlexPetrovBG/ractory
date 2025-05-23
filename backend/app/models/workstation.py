import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from .base import Base, TimestampMixin
from .enums import WorkstationType

class Workstation(Base, TimestampMixin):
    __tablename__ = "workstations"
    __table_args__ = {'extend_existing': True}

    guid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_guid = Column(UUID(as_uuid=True), ForeignKey("companies.guid"), nullable=False)
    location = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)  # Should match WorkstationType enum
    is_active = Column(Boolean, default=True, nullable=False)

    # Define relationship to Company
    company = relationship("Company", back_populates="workstations")
    # Define relationship to UI templates
    ui_templates = relationship("UiTemplate", back_populates="workstation")
    # Define relationship to workflows
    workflows = relationship("Workflow", back_populates="workstation")

    def __repr__(self):
        return f"<Workstation(guid={self.guid}, location='{self.location}', type='{self.type}')>" 