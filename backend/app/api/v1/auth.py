from fastapi import APIRouter, HTTPException, status, Depends, Response, Cookie
from typing import Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import (
    LoginRequest, TokenResponse, RefreshRequest, QrLoginRequest, ErrorResponse
)
from app.services.auth_service import AuthService
from app.utils.security import decode_token
from app.models.enums import UserRole
from app.core.rbac import require_system_admin
from app.core.deps import get_current_user, CurrentUser, get_session

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    }
)

@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest, session: AsyncSession = Depends(get_session)):
    """
    Authenticate a user with email and password.
    
    Returns JWT access and refresh tokens on success.
    """
    try:
        # Authenticate user
        user = await AuthService.authenticate_user(login_data.email, login_data.password, session)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Generate tokens
        tokens = await AuthService.create_tokens(user)
        
        return TokenResponse(**tokens)
    except Exception as e:
        # Log the error for debugging
        print(f"Authentication error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    response: Response,
    refresh_data: Optional[RefreshRequest] = None,
    refresh_token: Optional[str] = Cookie(None)
):
    """
    Refresh an access token using a refresh token.
    
    The refresh token can be provided either in the request body or as a cookie.
    """
    # Get token from either body or cookie
    token = None
    if refresh_data and refresh_data.refresh_token:
        token = refresh_data.refresh_token
    elif refresh_token:
        token = refresh_token
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is required"
        )
    
    try:
        # Decode and validate the refresh token
        payload = decode_token(token)
        
        # In a real implementation, we would validate against the database
        # and check if the token has been revoked
        
        # Create new access token
        user = {
            "user_id": payload["sub"],
            "tenant": payload["tenant"],
            "role": payload["role"]
        }
        
        tokens = await AuthService.create_tokens(user)
        
        # Set refresh token as HttpOnly cookie
        response.set_cookie(
            key="refresh_token",
            value=tokens["refresh_token"],
            httponly=True,
            secure=True,  # Requires HTTPS
            samesite="strict",
            max_age=604800  # 7 days in seconds
        )
        
        return TokenResponse(**tokens)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired refresh token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/qr", response_model=TokenResponse)
async def qr_login(qr_data: QrLoginRequest, session: AsyncSession = Depends(get_session)):
    """
    Authenticate an operator using QR code (user_guid) and PIN.
    
    Returns a workstation-scoped JWT valid for 1 hour.
    """
    result = await AuthService.validate_qr_login(
        qr_data.user_guid, 
        qr_data.workstation_guid, 
        qr_data.pin,
        session
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid QR login credentials"
        )
    
    return TokenResponse(**result)

@router.get("/protected", dependencies=[Depends(require_system_admin)])
async def protected_route(current_user: CurrentUser = Depends(get_current_user)):
    """
    A test protected endpoint that requires SystemAdmin role.
    """
    return {
        "message": "You have access to this protected route",
        "user_id": current_user.user_id,
        "role": current_user.role,
        "tenant": current_user.tenant
    }

@router.get("/me")
async def get_current_user_info(current_user: CurrentUser = Depends(get_current_user)):
    """
    Get information about the current authenticated user.
    """
    return {
        "guid": current_user.user_id,
        "email": current_user.email if hasattr(current_user, "email") else None,
        "role": current_user.role,
        "company_guid": current_user.tenant,
    } 