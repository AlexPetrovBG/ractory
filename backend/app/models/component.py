import uuid
from sqlalchemy import Column, String, Integer, LargeBinary, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy as sa

from app.core.database import Base

class Component(Base):
    """Component model representing data synced from RaWorkshop."""
    __tablename__ = "components"

    guid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_id = Column(Integer, nullable=False, index=True, comment="RaWorkshop ID")
    company_guid = Column(UUID(as_uuid=True), ForeignKey("companies.guid"), nullable=False, index=True)
    
    code = Column(String, index=True, comment="Component code identifier")
    designation = Column(String, comment="Name or description of the component")
    id_project = Column(Integer, ForeignKey("projects.original_id"), index=True, comment="Foreign key to Projects.Id") 
    quantity = Column(Integer, comment="Number of components")
    picture = Column(LargeBinary, comment="Visual representation of the component")
    created_date = Column(DateTime(timezone=True), comment="When the component was created")
    
    synced_at = Column(DateTime(timezone=True), server_default=func.now(), comment="When the component was last synced")
    
    # Add unique constraint on original_id and company_guid
    __table_args__ = (sa.UniqueConstraint('original_id', 'company_guid', name='uq_component_original_id_company'),)

    def __repr__(self):
        return f"<Component {self.code or self.original_id} (Project: {self.id_project}, Company: {self.company_guid})>" 