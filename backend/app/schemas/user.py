from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
import uuid
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    role: str
    is_active: Optional[bool] = True
    pin: Optional[str] = None

    @validator('pin')
    def validate_pin(cls, v):
        if v is not None and (not v.isdigit() or len(v) != 6):
            raise ValueError('PIN must be a 6-digit number')
        return v

    @validator('role')
    def validate_role(cls, v):
        valid_roles = ['SystemAdmin', 'CompanyAdmin', 'ProjectManager', 'Operator', 'Integration']
        if v not in valid_roles:
            raise ValueError(f'Role must be one of: {", ".join(valid_roles)}')
        return v


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    company_guid: Optional[uuid.UUID] = None  # Will be set from JWT token in most cases


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    role: Optional[str] = None
    is_active: Optional[bool] = None
    pin: Optional[str] = None

    @validator('pin')
    def validate_pin(cls, v):
        if v is not None and (not v.isdigit() or len(v) != 6):
            raise ValueError('PIN must be a 6-digit number')
        return v

    @validator('role')
    def validate_role(cls, v):
        if v is not None:
            valid_roles = ['SystemAdmin', 'CompanyAdmin', 'ProjectManager', 'Operator', 'Integration']
            if v not in valid_roles:
                raise ValueError(f'Role must be one of: {", ".join(valid_roles)}')
        return v


class UserInDB(UserBase):
    guid: uuid.UUID
    company_guid: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class UserResponse(UserInDB):
    # Remove sensitive fields
    pass 