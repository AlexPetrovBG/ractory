from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .base import Base

class Component(Base):
    __tablename__ = "components"
    
    id = Column(Integer, primary_key=True) # From RaConnect
    code = Column(String, nullable=False)
    designation = Column(String, nullable=True)
    id_project = Column(Integer, ForeignKey("projects.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    picture = Column(LargeBinary, nullable=True)
    created_date = Column(DateTime(timezone=True), nullable=False)
    company_guid = Column(UUID(as_uuid=True), ForeignKey("companies.guid"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="components")
    assemblies = relationship("Assembly", back_populates="component")
    articles = relationship("Article", back_populates="component")
    # pieces = relationship("Piece", back_populates="component") # Direct relation might not be needed
    
    def __repr__(self):
        return f"<Component id={self.id}, code={self.code}, project_id={self.id_project}>" 