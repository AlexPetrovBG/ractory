from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import uuid

class LoginRequest(BaseModel):
    """
    Schema for login request with email and password.
    """
    email: EmailStr
    password: str
    
class TokenResponse(BaseModel):
    """
    Schema for token response after successful login.
    """
    access_token: str
    refresh_token: str
    role: str
    expires_in: int = 900  # 15 minutes in seconds
    
class RefreshRequest(BaseModel):
    """
    Schema for token refresh request.
    """
    refresh_token: str
    
class QrLoginRequest(BaseModel):
    """
    Schema for operator QR code login.
    """
    user_guid: uuid.UUID
    workstation_guid: uuid.UUID
    pin: str = Field(..., min_length=6, max_length=6)
    
class ErrorResponse(BaseModel):
    """
    Standardized error response format.
    """
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None 