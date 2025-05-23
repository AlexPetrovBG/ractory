from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from .base import Base, TimestampMixin

class Assembly(Base, TimestampMixin):
    __tablename__ = "assemblies"
    
    guid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_guid = Column(UUID(as_uuid=True), ForeignKey("projects.guid"), nullable=False)
    component_guid = Column(UUID(as_uuid=True), ForeignKey("components.guid"), nullable=False)
    trolley_cell = Column(String, nullable=True)
    trolley = Column(String, nullable=True)
    cell_number = Column(Integer, nullable=True)
    picture = Column(LargeBinary, nullable=True)
    company_guid = Column(UUID(as_uuid=True), ForeignKey("companies.guid"), nullable=False)
    
    # Relationships
    project = relationship("Project", back_populates="assemblies")
    component = relationship("Component", back_populates="assemblies")
    pieces = relationship("Piece", back_populates="assembly")
    company = relationship("Company", back_populates="assemblies")
    
    def __repr__(self):
        return f"<Assembly guid={self.guid}, component_guid={self.component_guid}>" 