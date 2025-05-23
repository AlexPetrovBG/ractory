from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from .base import Base, TimestampMixin

class Project(Base, TimestampMixin):
    __tablename__ = "projects"
    
    guid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String, nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=True)
    in_production = Column(Boolean, default=False)
    company_name = Column(String, nullable=True) # Denormalized for easier access?
    company_guid = Column(UUID(as_uuid=True), ForeignKey("companies.guid"), nullable=False)
    
    # Relationships
    company = relationship("Company", back_populates="projects")
    components = relationship("Component", back_populates="project")
    assemblies = relationship("Assembly", back_populates="project")
    pieces = relationship("Piece", back_populates="project")
    articles = relationship("Article", back_populates="project")
    
    def __repr__(self):
        return f"<Project guid={self.guid}, code={self.code}>" 