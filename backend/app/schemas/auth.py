from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str
    refresh_token: str = None
    role: str
    expires_in: int

class TokenData(BaseModel):
    """Token data schema for decoded JWT payload."""
    sub: str
    email: EmailStr
    role: str
    company_guid: Optional[UUID] = None
    exp: int

class RefreshRequest(BaseModel):
    """Token refresh request schema."""
    refresh_token: str

class LoginRequest(BaseModel):
    """Login request schema."""
    email: EmailStr
    password: str

class QrLoginRequest(BaseModel):
    """QR code authentication request schema."""
    user_guid: str
    workstation_guid: str
    pin: str

class ErrorResponse(BaseModel):
    """Error response schema."""
    detail: str 