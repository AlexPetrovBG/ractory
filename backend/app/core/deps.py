from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.utils.security import decode_token
from app.core.database import get_db
from app.models.enums import UserRole

# Type alias for current user data
CurrentUser = Dict[str, Any]

# Define the OAuth2 scheme for JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

# We'll implement this in a future checkpoint with actual DB models
async def get_user_by_id(db: AsyncSession, user_id: str):
    """Get a user by ID (placeholder)."""
    # Placeholder implementation
    if user_id == "00000000-0000-0000-0000-000000000000":
        return {
            "guid": user_id,
            "email": "admin@example.com",
            "role": UserRole.SYSTEM_ADMIN,
            "company_guid": "11111111-1111-1111-1111-111111111111",
        }
    elif user_id == "22222222-2222-2222-2222-222222222222":
        return {
            "guid": user_id,
            "email": "admin@testcompany.com",
            "role": UserRole.COMPANY_ADMIN,
            "company_guid": "11111111-1111-1111-1111-111111111111",
        }
    return None

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    x_api_key: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db)
) -> CurrentUser:
    """Get the current user from JWT token or API key."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # First try with JWT token
    if token:
        try:
            # Decode the JWT token
            payload = decode_token(token)
            user_id = payload.get("sub")
            if user_id is None:
                raise credentials_exception
                
            # Get the user from the database
            user = await get_user_by_id(db, user_id)
            if user is None:
                raise credentials_exception
                
            # Add token payload to user object
            user["token_data"] = payload
            
            # Important: Make sure role is correctly set from token payload
            role_str = payload.get("role")
            if role_str:
                # Convert string role to enum
                try:
                    user["role"] = UserRole(role_str)
                except ValueError:
                    # If role in token doesn't match any valid UserRole enum
                    user["role"] = UserRole.OPERATOR  # Default fallback
            
            # Set tenant in db session for RLS
            await set_tenant_for_session(db, user["company_guid"])
            
            return user
        except Exception as e:
            print(f"Auth error: {str(e)}")
            raise credentials_exception
    
    # Then try with API key (if implemented)
    elif x_api_key:
        # Simple placeholder implementation for API key auth
        if x_api_key == "test-integration-key":
            user = {
                "guid": "integration-user",
                "email": "integration@testcompany.com",
                "role": UserRole.INTEGRATION,
                "company_guid": "11111111-1111-1111-1111-111111111111",
                "token_data": {"scope": "sync:true"}
            }
            
            # Set tenant in db session for RLS
            await set_tenant_for_session(db, user["company_guid"])
            
            return user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    
    # If no authentication method provided
    raise credentials_exception

def require_roles(*roles: UserRole):
    """Dependency for requiring specific roles."""
    async def role_checker(
        current_user: CurrentUser = Depends(get_current_user),
    ):
        if current_user["role"] not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role {current_user['role']} not authorized. Required: {', '.join(str(r) for r in roles)}",
            )
        return current_user
    return role_checker

async def set_tenant_for_session(db: AsyncSession, tenant_id: str):
    """Set the tenant ID for the current database session (RLS)."""
    # This would set the PostgreSQL RLS policy at the session level
    try:
        await db.execute(text(f"SET app.tenant = '{tenant_id}'"))
    except Exception as e:
        print(f"Error setting tenant: {str(e)}")
    
# Middleware to automatically set the tenant based on the authenticated user
async def tenant_middleware(
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Set the tenant ID for the current database session based on user."""
    tenant_id = current_user["company_guid"]
    if tenant_id:
        await set_tenant_for_session(db, tenant_id)
    return current_user

# Workstation verification for operator sessions
async def verify_workstation(
    workstation_id: str,
    current_user: CurrentUser = Depends(get_current_user),
):
    """Verify that operator has access to this workstation."""
    # Check if token has workstation claim
    token_data = current_user.get("token_data", {})
    ws_claim = token_data.get("ws")
    
    # Operators must have ws claim matching the requested workstation
    if current_user["role"] == UserRole.OPERATOR and ws_claim != workstation_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operator not authorized for this workstation",
        )
    
    return current_user

# Added: Provide a tenant-aware session for RBAC and other dependencies
async def get_tenant_session(
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AsyncSession:
    tenant_id = current_user.get("company_guid")
    if tenant_id:
        await set_tenant_for_session(db, tenant_id)
    return db 