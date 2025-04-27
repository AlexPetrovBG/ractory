from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from typing import Optional, List, Dict, Any, Generator, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.utils.security import decode_token
from app.models.enums import UserRole
from app.models.base import get_session
from app.models.user import User
# from app.models.apikey import ApiKey # TODO: Create apikey.py and uncomment

# Security scheme for JWT Bearer token
security = HTTPBearer()

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
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> CurrentUser:
    """
    Dependency to extract and validate the current user from JWT token.
    
    Args:
        credentials: The HTTP Bearer token from Authorization header
        
    Returns:
        CurrentUser object with user information
        
    Raises:
        HTTPException: 401 if token is invalid or expired
    """
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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
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
    # Set PostgreSQL session variables for RLS
    # For SystemAdmin, we optionally bypass RLS with app.bypass_rls
    if current_user.role == UserRole.SYSTEM_ADMIN:
        await session.execute("SET app.bypass_rls = true")
    else:
        # For all other roles, set the tenant context
        await session.execute(f"SET app.tenant = '{current_user.tenant}'")
    
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