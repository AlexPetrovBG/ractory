from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

class ArticleBase(BaseModel):
    """Base schema for Article fields."""
    code: str
    id_project: int
    id_component: int
    designation: Optional[str] = None
    
class ArticleCreate(ArticleBase):
    """Schema for creating an Article."""
    id: int
    created_date: datetime
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
    modified_date: Optional[datetime] = None
    company_guid: Optional[str] = None  # Will be set from token if not provided

class ArticleBulkInsert(BaseModel):
    """Schema for bulk inserting Articles."""
    articles: List[ArticleCreate]

class ArticleResponse(ArticleBase):
    """Schema for Article responses."""
    id: int
    company_guid: str
    created_at: datetime

    class Config:
        orm_mode = True 