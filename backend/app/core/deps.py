from fastapi import Depends, HTTPException, status, Request, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from typing import Optional, List, Dict, Any, Generator, AsyncGenerator, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.utils.security import decode_token
from app.models.enums import UserRole
from app.models.base import get_session
from app.models.user import User
from app.models.apikey import ApiKey
from app.services.api_key_service import ApiKeyService
from app.core.tenant_utils import set_tenant_context, add_tenant_filter

# Security scheme for JWT Bearer token
security = HTTPBearer(auto_error=False)

class CurrentUser:
    """
    Class representing the authenticated user from a JWT token.
    """
    def __init__(self, user_id: str, tenant: str, role: str, extras: Optional[Dict[str, Any]] = None):
        self.user_id = user_id  # 'sub' claim from JWT
        self.tenant = tenant    # 'tenant' claim from JWT (company_guid)
        self.role = role        # 'role' claim from JWT
        self.extras = extras or {}  # Additional claims (workstation, scope, etc.)

async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    x_api_key: Optional[str] = Header(None),
    session: AsyncSession = Depends(get_session)
) -> CurrentUser:
    """
    Dependency to extract and validate the current user from JWT token or API key.
    
    Args:
        request: The incoming request
        credentials: The HTTP Bearer token from Authorization header
        x_api_key: API key from X-API-Key header
        session: Database session
        
    Returns:
        CurrentUser object with user information
        
    Raises:
        HTTPException: 401 if authentication fails
    """
    # First try JWT token authentication
    if credentials and credentials.scheme.lower() == "bearer":
        try:
            token = credentials.credentials
            payload = decode_token(token)
            
            # Extract required claims
            user_id = payload.get("sub")
            tenant = payload.get("tenant")
            role = payload.get("role")
            
            if not all([user_id, tenant, role]):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token claims",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Extract additional claims that aren't the standard ones
            extras = {k: v for k, v in payload.items() 
                    if k not in ["sub", "tenant", "role", "exp", "iat"]}
            
            return CurrentUser(user_id, tenant, role, extras)
        except jwt.PyJWTError:
            # Fall through to API key authentication if JWT token is invalid
            pass
    
    # Try API key authentication
    api_key = None
    
    # Check X-API-Key header
    if x_api_key:
        api_key = x_api_key
    # Check Authorization: ApiKey header
    elif credentials and credentials.scheme.lower() == "apikey":
        api_key = credentials.credentials
    
    if api_key:
        try:
            # Validate API key
            api_key_info = await ApiKeyService.validate_api_key(api_key, session)
            
            if api_key_info:
                # Create CurrentUser from API key info
                return CurrentUser(
                    user_id=api_key_info["guid"],
                    tenant=str(api_key_info["company_guid"]),  # Convert UUID to string for consistency
                    role=UserRole.INTEGRATION,  # API keys always have Integration role
                    extras={"scopes": api_key_info.get("scopes", ""), "auth_type": "api_key"}
                )
        except Exception as e:
            # Log the error but don't expose it
            print(f"API key authentication error: {str(e)}")
    
    # If we get here, authentication failed
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": 'Bearer realm="rafactory"'},
    )

async def get_tenant_session(
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> AsyncSession:
    """
    Get a database session with tenant context set for RLS.
    
    Args:
        current_user: The authenticated user from JWT
        session: SQLAlchemy async session
        
    Returns:
        Session with tenant context set
    """
    # Set tenant context using the new utility
    await set_tenant_context(session, current_user.tenant, current_user.role)
    
    return session

async def get_db_user(
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_tenant_session)
) -> User:
    """
    Get the database User object for the current authenticated user.
    
    Args:
        current_user: The authenticated user from JWT
        session: SQLAlchemy async session with tenant context
        
    Returns:
        User database model instance
        
    Raises:
        HTTPException: 404 if user not found in database
    """
    from sqlalchemy import select
    
    # Skip for API key authentication since there's no user
    if current_user.extras.get("auth_type") == "api_key":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User object not available for API key authentication"
        )
    
    # Query the user from database
    result = await session.execute(
        select(User).where(User.guid == current_user.user_id)
    )
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in database"
        )
    
    return user 