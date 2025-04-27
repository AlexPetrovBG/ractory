import uuid
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

# Base schema for company properties
class CompanyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Name of the company")
    short_name: Optional[str] = Field(None, max_length=50, description="Optional short name for the company")
    logo_path: Optional[str] = Field(None, max_length=255, description="Optional path to the company logo")
    is_active: Optional[bool] = Field(True, description="Whether the company is active")
    # Add other relevant company fields here as needed
    # e.g., address: Optional[str] = None
    # e.g., contact_email: Optional[EmailStr] = None

# Schema for creating a new company (input)
class CompanyCreate(CompanyBase):
    pass

# Schema for reading company data (output), includes fields from the model
class CompanyRead(CompanyBase):
    guid: uuid.UUID = Field(..., description="Unique identifier for the company")
    created_at: datetime = Field(..., description="Timestamp when the company was created")
    updated_at: datetime = Field(..., description="Timestamp when the company was last updated")

    class Config:
        orm_mode = True # Allows mapping from SQLAlchemy models 