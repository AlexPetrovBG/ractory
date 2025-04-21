from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime


class CompanyBase(BaseModel):
    """Base schema with fields common to all company-related schemas."""
    name: str = Field(..., description="Full company name")
    short_name: str = Field(..., description="Abbreviated company name")
    logo_path: Optional[str] = Field(None, description="Path to company logo file")
    subscription_tier: Optional[str] = Field("Basic", description="Company subscription tier")
    subscription_status: Optional[str] = Field("trial", description="Current subscription status")
    is_active: Optional[bool] = Field(True, description="Whether the company account is active")


class CompanyCreate(CompanyBase):
    """Schema for creating a new company."""
    pass


class CompanyUpdate(BaseModel):
    """Schema for updating an existing company."""
    name: Optional[str] = Field(None, description="Full company name")
    short_name: Optional[str] = Field(None, description="Abbreviated company name")
    logo_path: Optional[str] = Field(None, description="Path to company logo file")
    subscription_tier: Optional[str] = Field(None, description="Company subscription tier")
    subscription_status: Optional[str] = Field(None, description="Current subscription status")
    is_active: Optional[bool] = Field(None, description="Whether the company account is active")


class CompanyInDB(CompanyBase):
    """Schema representing a company as stored in the database."""
    guid: UUID = Field(..., description="Unique identifier for the company")
    user_count: int = Field(..., description="Number of users in the company")
    projects_count: int = Field(..., description="Number of projects in the company")
    workstations_count: int = Field(..., description="Number of workstations in the company")
    created_at: datetime = Field(..., description="When the company was created")
    updated_at: Optional[datetime] = Field(None, description="When the company was last updated")

    class Config:
        from_attributes = True


class CompanyRead(CompanyInDB):
    """Schema for returning company information in API responses."""
    pass 