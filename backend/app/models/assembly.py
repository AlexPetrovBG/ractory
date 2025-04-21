import uuid
from sqlalchemy import Column, String, Integer, LargeBinary, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy as sa

from app.core.database import Base

class Assembly(Base):
    """Assembly model representing data synced from RaWorkshop."""
    __tablename__ = "assemblies"

    guid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_id = Column(Integer, nullable=False, index=True, comment="RaWorkshop ID")
    company_guid = Column(UUID(as_uuid=True), ForeignKey("companies.guid"), nullable=False, index=True)
    
    id_project = Column(Integer, ForeignKey("projects.original_id"), index=True, comment="Foreign key to Projects.Id")
    id_component = Column(Integer, ForeignKey("components.original_id"), index=True, comment="Foreign key to Components.Id")
    trolley_cell = Column(String, comment="Identifies the trolley and cell position")
    trolley = Column(String, comment="Identifies the trolley")
    cell_number = Column(Integer, comment="Cell number within the trolley")
    picture = Column(LargeBinary, comment="Visual representation of the assembly")
    
    synced_at = Column(DateTime(timezone=True), server_default=func.now(), comment="When the assembly was last synced")
    
    # Add unique constraint on original_id and company_guid
    __table_args__ = (sa.UniqueConstraint('original_id', 'company_guid', name='uq_assembly_original_id_company'),)

    def __repr__(self):
        return f"<Assembly {self.original_id} (Component: {self.id_component}, Company: {self.company_guid})>" 