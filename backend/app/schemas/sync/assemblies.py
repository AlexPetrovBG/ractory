from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

class AssemblyBase(BaseModel):
    """Base schema for Assembly fields."""
    id_project: int
    id_component: int
    trolley_cell: Optional[str] = None
    trolley: Optional[str] = None
    cell_number: Optional[int] = None
    
class AssemblyCreate(AssemblyBase):
    """Schema for creating an Assembly."""
    id: int
    picture: Optional[bytes] = None
    company_guid: Optional[str] = None  # Will be set from token if not provided

class AssemblyBulkInsert(BaseModel):
    """Schema for bulk inserting Assemblies."""
    assemblies: List[AssemblyCreate]

class AssemblyResponse(AssemblyBase):
    """Schema for Assembly responses."""
    id: int
    company_guid: str
    created_at: datetime

    class Config:
        orm_mode = True

class AssemblyDetail(AssemblyResponse):
    """Detailed Assembly schema with piece count."""
    piece_count: int = 0
    
    class Config:
        orm_mode = True 