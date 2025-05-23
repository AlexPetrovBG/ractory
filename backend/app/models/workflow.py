from sqlalchemy import Column, String, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.models.base import Base, TimestampMixin
from app.models.enums import WorkflowActionType

class Workflow(Base, TimestampMixin):
    __tablename__ = "workflow"

    guid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_guid = Column(UUID(as_uuid=True), ForeignKey("companies.guid"), nullable=False)
    company_name = Column(String, nullable=True)
    workstation_guid = Column(UUID(as_uuid=True), ForeignKey("workstations.guid"), nullable=True)
    workstation_name = Column(String, nullable=True)
    api_key_guid = Column(UUID(as_uuid=True), nullable=True)
    user_guid = Column(UUID(as_uuid=True), ForeignKey("users.guid"), nullable=True)
    user_name = Column(String, nullable=True)
    action_type = Column(Enum(WorkflowActionType), nullable=False)
    action_value = Column(String, nullable=True)

    # Relationships
    company = relationship("Company", back_populates="workflows")
    workstation = relationship("Workstation", back_populates="workflows")
    user = relationship("User", back_populates="workflows")

    def __repr__(self):
        return f"<Workflow(guid={self.guid}, company_guid={self.company_guid}, action_type={self.action_type})>" 