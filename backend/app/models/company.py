import uuid
from sqlalchemy import Column, String, Boolean, Integer, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from .base import Base, TimestampMixin
# Import related models for relationship definition
# from .user import User # Avoid direct import loop, use string reference
# from .project import Project
# from .apikey import ApiKey
# from .workstation import Workstation

class Company(Base, TimestampMixin):
    __tablename__ = "companies"
    __table_args__ = (
        CheckConstraint('company_index >= 0 AND company_index <= 99', name='company_index_range'),
        {'extend_existing': True}
    )

    guid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, index=True)
    short_name = Column(String(50), nullable=True)
    logo_path = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    company_index = Column(Integer, nullable=True, unique=True)

    # Define relationships
    users = relationship("User", back_populates="company")
    projects = relationship("Project", back_populates="company")
    api_keys = relationship("ApiKey", back_populates="company")
    workstations = relationship("Workstation", back_populates="company")
    articles = relationship("Article", back_populates="company")
    assemblies = relationship("Assembly", back_populates="company")
    components = relationship("Component", back_populates="company")
    pieces = relationship("Piece", back_populates="company")
    workflows = relationship("Workflow", back_populates="company")

    def __repr__(self):
        return f"<Company(guid={self.guid}, name='{self.name}')>" 