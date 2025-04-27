from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

class ProjectBase(BaseModel):
    """Base schema for Project fields."""
    code: str
    creation_date: datetime
    modified_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    check_sum: Optional[str] = None
    in_production: bool = False
    company_name: Optional[str] = None

class ProjectCreate(ProjectBase):
    """Schema for creating a Project."""
    id: int
    company_guid: Optional[str] = None  # Will be set from token if not provided

class ProjectBulkInsert(BaseModel):
    """Schema for bulk inserting Projects."""
    projects: List[ProjectCreate]

class ProjectResponse(ProjectBase):
    """Schema for Project responses."""
    id: int
    company_guid: str
    created_at: datetime

    class Config:
        orm_mode = True

class ProjectDetail(ProjectResponse):
    """Detailed Project schema with component counts."""
    component_count: int = 0
    piece_count: int = 0
    
    class Config:
        orm_mode = True

class SyncResult(BaseModel):
    """Result of a sync operation."""
    inserted: int
    updated: int 