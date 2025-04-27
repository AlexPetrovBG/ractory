from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .base import Base

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True) # From RaConnect
    code = Column(String, nullable=False)
    creation_date = Column(DateTime(timezone=True), nullable=False)
    modified_date = Column(DateTime(timezone=True), nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    check_sum = Column(String, nullable=True)
    in_production = Column(Boolean, default=False)
    company_name = Column(String, nullable=True) # Denormalized for easier access?
    company_guid = Column(UUID(as_uuid=True), ForeignKey("companies.guid"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    company = relationship("Company", back_populates="projects")
    components = relationship("Component", back_populates="project")
    # assemblies = relationship("Assembly", back_populates="project") # Direct relation might not be needed if through component
    # pieces = relationship("Piece", back_populates="project") # Direct relation might not be needed
    # articles = relationship("Article", back_populates="project") # Direct relation might not be needed
    
    def __repr__(self):
        return f"<Project id={self.id}, code={self.code}>" 