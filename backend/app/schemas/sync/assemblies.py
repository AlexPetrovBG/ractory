from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

class AssemblyBase(BaseModel):
    """Base schema for Assembly fields."""
    project_guid: uuid.UUID
    component_guid: uuid.UUID
    trolley_cell: Optional[str] = None
    trolley: Optional[str] = None
    cell_number: Optional[int] = None
    
class AssemblyCreate(AssemblyBase):
    """Schema for creating an Assembly."""
    guid: uuid.UUID = Field(default_factory=uuid.uuid4)
    picture: Optional[bytes] = None
    company_guid: Optional[uuid.UUID] = None  # Will be set from token if not provided

class AssemblyBulkInsert(BaseModel):
    """Schema for bulk inserting Assemblies."""
    assemblies: List[AssemblyCreate]

class AssemblyResponse(AssemblyBase):
    """Schema for Assembly responses."""
    guid: uuid.UUID
    company_guid: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True

class AssemblyDetail(AssemblyResponse):
    """Detailed Assembly schema with piece count."""
    piece_count: int = 0
    
    class Config:
        from_attributes = True 