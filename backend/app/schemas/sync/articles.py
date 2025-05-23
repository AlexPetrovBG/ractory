from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

class ArticleBase(BaseModel):
    """Base schema for Article fields."""
    code: str
    project_guid: uuid.UUID
    component_guid: uuid.UUID
    designation: Optional[str] = None
    
class ArticleCreate(ArticleBase):
    """Schema for creating an Article."""
    guid: uuid.UUID = Field(default_factory=uuid.uuid4)
    # Including all optional fields
    consume_group_designation: Optional[str] = None
    consume_group_priority: Optional[int] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    category_designation: Optional[str] = None
    position: Optional[str] = None
    short_position: Optional[str] = None
    code_no_color: Optional[str] = None
    component_code: Optional[str] = None
    is_extra: Optional[bool] = False
    length: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    surface: Optional[float] = None
    angle1: Optional[float] = None
    angle2: Optional[float] = None
    unit_weight: Optional[float] = None
    bar_length: Optional[float] = None
    company_guid: Optional[uuid.UUID] = None  # Will be set from token if not provided

class ArticleBulkInsert(BaseModel):
    """Schema for bulk inserting Articles."""
    articles: List[ArticleCreate]

class ArticleResponse(ArticleBase):
    """Schema for Article responses."""
    guid: uuid.UUID
    company_guid: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True

class ArticleDetail(ArticleResponse):
    """Detailed schema for Article responses with all available fields."""
    # Including all additional fields from ArticleCreate
    consume_group_designation: Optional[str] = None
    consume_group_priority: Optional[int] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    category_designation: Optional[str] = None
    position: Optional[str] = None
    short_position: Optional[str] = None
    code_no_color: Optional[str] = None
    component_code: Optional[str] = None
    is_extra: Optional[bool] = None
    length: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    surface: Optional[float] = None
    angle1: Optional[float] = None
    angle2: Optional[float] = None
    unit_weight: Optional[float] = None
    bar_length: Optional[float] = None
    updated_at: Optional[datetime] = None 