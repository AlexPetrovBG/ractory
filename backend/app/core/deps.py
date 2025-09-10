from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select

from app.utils.security import decode_token
from app.core.database import get_db
from app.models.enums import UserRole
from app.models.user import User

# Type alias for current user data
CurrentUser = Dict[str, Any]

# Define the OAuth2 scheme for JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

async def get_user_by_id(db: AsyncSession, user_id: str):
    """Get a user by ID from the database."""
    try:
        # Query the actual user from the database
        result = await db.execute(
            select(User).where(User.guid == user_id)
        )
        user = result.scalars().first()
        
        if user:
            return {
                "guid": str(user.guid),
                "email": user.email,
                "role": UserRole(user.role),
                "company_guid": str(user.company_guid),
                "is_active": user.is_active,
            }
        return None
    except Exception as e:
        print(f"Database error in get_user_by_id: {e}")
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
            print(f"Auth error: {e}")
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
    """Set the tenant context for a database session using row-level security."""
    await db.execute(text(f"SET rls.tenant_id = '{tenant_id}'"))
    await db.commit()

async def tenant_middleware(
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Middleware to set tenant context for the database session."""
    if current_user and "company_guid" in current_user:
        await set_tenant_for_session(db, str(current_user["company_guid"]))
    return db

async def get_tenant_session(
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AsyncSession:
    """Get a database session with tenant context set."""
    if current_user and "company_guid" in current_user:
        await set_tenant_for_session(db, str(current_user["company_guid"]))
    return db

async def verify_workstation(
    workstation_id: str,
    current_user: CurrentUser = Depends(get_current_user),
):
    """Verify that the current user has access to the specified workstation."""
    # For now, just return True - implement actual verification logic
    return True

# Additional dependency to get a database session with proper tenant context
async def get_session():
    """Get a database session without authentication for internal use."""
    async for session in get_db():
        yield session
        break  # Only get one session

async def get_db_user(user_id: str, db: AsyncSession = Depends(get_db)):
    """Get a user from the database by ID."""
    return await get_user_by_id(db, user_id) 