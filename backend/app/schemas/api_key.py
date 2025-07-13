from pydantic import BaseModel, Field, UUID4
from typing import Optional, List, Dict, Any
from datetime import datetime


class ApiKeyBase(BaseModel):
    description: Optional[str] = Field(None, example="Integration with ERP system", description="A description of what this API key is used for")
    scopes: Optional[str] = Field(None, example="sync:read,sync:write", description="Comma-separated list of scopes this key has access to")


class ApiKeyCreate(ApiKeyBase):
    key: Optional[str] = Field(None, example="rfk_customkey123456789", description="Optional custom API key. Must start with 'rfk_' and be unique")
    company_guid: Optional[UUID4] = Field(None, description="Company GUID (for SystemAdmin only). If not provided, uses the authenticated user's company")


class ApiKeyCreated(BaseModel):
    guid: UUID4
    key: str = Field(..., example="rfk_12345abcdef", description="The actual API key that should be securely stored (only shown once)")
    description: Optional[str] = None
    scopes: Optional[str] = None
    created_at: datetime
    company_guid: UUID4


class ApiKeyResponse(BaseModel):
    guid: UUID4
    description: Optional[str] = None
    scopes: Optional[str] = None
    created_at: datetime
    last_used_at: Optional[datetime] = None
    is_active: bool
    company_guid: UUID4

    class Config:
        orm_mode = True


class ApiKeyList(BaseModel):
    api_keys: List[ApiKeyResponse]


class ApiKeyUpdate(BaseModel):
    description: Optional[str] = None
    scopes: Optional[str] = None
    is_active: Optional[bool] = None 