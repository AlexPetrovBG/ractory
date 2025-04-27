from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

class ComponentBase(BaseModel):
    """Base schema for Component fields."""
    code: str
    designation: Optional[str] = None
    id_project: int
    quantity: int = 1
    
class ComponentCreate(ComponentBase):
    """Schema for creating a Component."""
    id: int
    created_date: datetime
    picture: Optional[bytes] = None
    company_guid: Optional[str] = None  # Will be set from token if not provided

class ComponentBulkInsert(BaseModel):
    """Schema for bulk inserting Components."""
    components: List[ComponentCreate]

class ComponentResponse(ComponentBase):
    """Schema for Component responses."""
    id: int
    company_guid: str
    created_at: datetime

    class Config:
        orm_mode = True

class ComponentDetail(ComponentResponse):
    """Detailed Component schema with assembly counts."""
    assembly_count: int = 0
    piece_count: int = 0
    
    class Config:
        orm_mode = True 