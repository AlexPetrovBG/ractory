import uuid
from sqlalchemy import Column, String, DateTime, func, UUID as pgUUID, ForeignKey, JSON, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from .base import Base

class UiTemplate(Base):
    __tablename__ = "ui_templates"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_guid = Column(pgUUID(as_uuid=True), ForeignKey("companies.guid"), nullable=False)
    workstation_guid = Column(pgUUID(as_uuid=True), ForeignKey("workstations.guid"), nullable=True)
    name = Column(String(255), nullable=False)
    json_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)
    
    # Define relationships
    company = relationship("Company")
    workstation = relationship("Workstation", back_populates="ui_templates")

    def __repr__(self):
        return f"<UiTemplate(id={self.id}, name='{self.name}')>" 