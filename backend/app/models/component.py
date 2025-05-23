from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from .base import Base, TimestampMixin

class Component(Base, TimestampMixin):
    __tablename__ = "components"
    
    guid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String, nullable=False)
    designation = Column(String, nullable=True)
    project_guid = Column(UUID(as_uuid=True), ForeignKey("projects.guid"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    picture = Column(LargeBinary, nullable=True)
    company_guid = Column(UUID(as_uuid=True), ForeignKey("companies.guid"), nullable=False)
    
    # Relationships
    project = relationship("Project", back_populates="components")
    assemblies = relationship("Assembly", back_populates="component")
    articles = relationship("Article", back_populates="component")
    pieces = relationship("Piece", back_populates="component")
    company = relationship("Company", back_populates="components")
    
    def __repr__(self):
        return f"<Component guid={self.guid}, code={self.code}, project_guid={self.project_guid}>" 