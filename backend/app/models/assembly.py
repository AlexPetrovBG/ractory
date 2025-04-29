from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .base import Base

class Assembly(Base):
    __tablename__ = "assemblies"
    
    id = Column(Integer, primary_key=True) # From RaConnect
    id_project = Column(Integer, ForeignKey("projects.id"), nullable=False)
    id_component = Column(Integer, ForeignKey("components.id"), nullable=False)
    trolley_cell = Column(String, nullable=True)
    trolley = Column(String, nullable=True)
    cell_number = Column(Integer, nullable=True)
    picture = Column(LargeBinary, nullable=True)
    company_guid = Column(UUID(as_uuid=True), ForeignKey("companies.guid"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    project = relationship("Project", back_populates="assemblies")
    component = relationship("Component", back_populates="assemblies")
    pieces = relationship("Piece", back_populates="assembly")
    company = relationship("Company", back_populates="assemblies")
    
    def __repr__(self):
        return f"<Assembly id={self.id}, component_id={self.id_component}>" 