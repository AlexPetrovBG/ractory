import uuid
from sqlalchemy import Column, String, DateTime, func, UUID as pgUUID, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from .base import Base # Corrected import path
# Import related models for relationship definition
# from .user import User # Avoid direct import loop, use string reference
# from .project import Project
# from .apikey import ApiKey
# from .workstation import Workstation

class Company(Base):
    __tablename__ = "companies"
    __table_args__ = {'extend_existing': True}

    guid = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, index=True)
    short_name = Column(String(50), nullable=True)
    logo_path = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Define relationships (uncommented and added)
    users = relationship("User", back_populates="company")
    projects = relationship("Project", back_populates="company")
    api_keys = relationship("ApiKey", back_populates="company") # Added from tables.py
    workstations = relationship("Workstation", back_populates="company") # Added from tables.py

    def __repr__(self):
        return f"<Company(guid={self.guid}, name='{self.name}')>" 