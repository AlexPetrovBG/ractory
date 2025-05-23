from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

class ProjectBase(BaseModel):
    """Base schema for Project fields."""
    code: str
    updated_at: Optional[datetime] = None
    due_date: Optional[datetime] = None
    in_production: bool = False
    company_name: Optional[str] = None

class ProjectCreate(ProjectBase):
    """Schema for creating a Project."""
    guid: uuid.UUID = Field(default_factory=uuid.uuid4)
    company_guid: Optional[uuid.UUID] = None  # Will be set from token if not provided
    updated_at: Optional[datetime] = None

class ProjectBulkInsert(BaseModel):
    """Schema for bulk inserting Projects."""
    projects: List[ProjectCreate]

class ProjectResponse(ProjectBase):
    """Schema for Project responses."""
    guid: uuid.UUID
    company_guid: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }

class ProjectDetail(ProjectResponse):
    """Detailed Project schema with component counts."""
    component_count: int = 0
    piece_count: int = 0
    
    model_config = {
        "from_attributes": True
    }

class SyncResult(BaseModel):
    """Result of a sync operation."""
    inserted: int
    updated: int 