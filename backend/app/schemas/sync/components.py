from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

class ComponentBase(BaseModel):
    """Base schema for Component fields."""
    code: str
    designation: Optional[str] = None
    project_guid: uuid.UUID
    quantity: int = 1
    is_active: bool = True
    deleted_at: Optional[datetime] = None
    
class ComponentCreate(ComponentBase):
    """Schema for creating a Component."""
    guid: uuid.UUID = Field(default_factory=uuid.uuid4)
    picture: Optional[bytes] = None
    company_guid: Optional[uuid.UUID] = None  # Will be set from token if not provided

class ComponentBulkInsert(BaseModel):
    """Schema for bulk inserting Components."""
    components: List[ComponentCreate]

class ComponentResponse(ComponentBase):
    """Schema for Component responses."""
    guid: uuid.UUID
    company_guid: uuid.UUID
    created_at: datetime
    is_active: bool = True
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ComponentDetail(ComponentResponse):
    """Detailed Component schema with assembly counts."""
    assembly_count: int = 0
    piece_count: int = 0
    
    class Config:
        from_attributes = True 