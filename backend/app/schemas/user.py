from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
import uuid
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    role: str
    is_active: Optional[bool] = True
    pin: Optional[str] = None
    name: Optional[str] = Field(None, max_length=100)
    surname: Optional[str] = Field(None, max_length=100)
    picture_path: Optional[str] = Field(None, max_length=255)

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

    @validator('picture_path')
    def validate_picture_path(cls, v):
        if v is not None:
            # Basic URL or path validation
            if not any([
                v.startswith('/'),                     # Absolute path
                v.startswith('./'),                    # Relative path
                v.startswith('http://'),               # HTTP URL
                v.startswith('https://'),              # HTTPS URL
                v.startswith('data:image/')            # Data URL
            ]):
                raise ValueError('Picture path must be a valid URL or file path')
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
    name: Optional[str] = Field(None, max_length=100)
    surname: Optional[str] = Field(None, max_length=100)
    picture_path: Optional[str] = Field(None, max_length=255)

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

    @validator('picture_path')
    def validate_picture_path(cls, v):
        if v is not None:
            # Basic URL or path validation
            if not any([
                v.startswith('/'),                     # Absolute path
                v.startswith('./'),                    # Relative path
                v.startswith('http://'),               # HTTP URL
                v.startswith('https://'),              # HTTPS URL
                v.startswith('data:image/')            # Data URL
            ]):
                raise ValueError('Picture path must be a valid URL or file path')
        return v


class UserInDB(UserBase):
    guid: uuid.UUID
    company_guid: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    guid: uuid.UUID
    email: EmailStr
    role: str
    is_active: bool
    pin: Optional[str]
    name: Optional[str]
    surname: Optional[str]
    picture_path: Optional[str]
    company_guid: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True 