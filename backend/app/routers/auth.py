from fastapi import APIRouter, Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.database import get_db
from app.models.enums import UserRole
from app.schemas.auth import Token, TokenRefresh, Login, QRAuth
from app.utils.security import verify_password, create_token, decode_token
from app.repositories import users as users_repo

# Router setup
router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login", response_model=Token)
async def login(login_data: Login, db: AsyncSession = Depends(get_db)):
    """Login with email and password."""
    print(f"Login attempt: {login_data.email}")
    try:
        # Get user from the database by email
        user = await users_repo.get_user_by_email(db, login_data.email)
        print(f"User found: {user is not None}")
        
        # Validate user exists and password is correct
        if not user:
            print("User not found")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check if user is active
        if not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is inactive",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        pwd_match = verify_password(login_data.password, user["pwd_hash"])
        print(f"Password match: {pwd_match}")
        print(f"User role: {user['role']}")
        print(f"User company: {user['company_guid']}")
        
        if not pwd_match:
            print("Password does not match")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Generate access token
        access_token = create_token(
            subject=str(user["guid"]),
            tenant=str(user["company_guid"]) if user["company_guid"] else None,
            role=str(user["role"]),
        )
        
        # Generate refresh token with longer expiry
        refresh_token = create_token(
            subject=str(user["guid"]),
            tenant=str(user["company_guid"]) if user["company_guid"] else None,
            role=str(user["role"]),
            expires_min=7 * 24 * 60,  # 7 days
            extra_data={"token_type": "refresh"}
        )
        
        print("Returning response")
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "role": str(user["role"]),
            "expires_in": 15 * 60  # 15 minutes in seconds
        }
    except Exception as e:
        print(f"Login error: {e}")
        import traceback
        traceback.print_exc()
        raise

@router.post("/refresh", response_model=Token)
async def refresh(
    refresh_data: TokenRefresh = None,
    refresh_token: str = Cookie(None),
    db: AsyncSession = Depends(get_db)
):
    """Refresh access token using a refresh token."""
    # Use either the body refresh token or the cookie
    token = refresh_data.refresh_token if refresh_data else refresh_token
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        # Decode and validate refresh token
        payload = decode_token(token)
        
        # Check if it's a refresh token
        if payload.get("token_type") != "refresh":
            raise ValueError("Not a refresh token")
        
        # Get user ID, tenant and role from token
        user_id = payload.get("sub")
        tenant = payload.get("tenant")
        role = payload.get("role")
        
        # Create new access token
        access_token = create_token(
            subject=user_id,
            tenant=tenant,
            role=role,
        )
        
        return {
            "access_token": access_token,
            "role": role,
            "expires_in": 15 * 60  # 15 minutes in seconds
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid refresh token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/qr", response_model=Token)
async def qr_auth(auth_data: QRAuth, db: AsyncSession = Depends(get_db)):
    """Authenticate using QR code + PIN."""
    try:
        # Parse UUIDs
        user_guid = UUID(auth_data.user_guid)
        workstation_guid = UUID(auth_data.workstation_guid)
        
        # Get user by GUID and verify PIN
        user = await users_repo.get_user_by_guid_pin(
            db, 
            user_guid,
            auth_data.pin
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user ID, PIN, or workstation",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verify user is an operator
        if user["role"] != UserRole.OPERATOR:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="QR authentication is only for operators",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verify user is active
        if not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is inactive",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Generate operator-specific token with workstation claim
        access_token = create_token(
            subject=str(user["guid"]),
            tenant=str(user["company_guid"]),
            role=str(user["role"]),
            expires_min=60,  # 1 hour
            extra_data={"ws": str(workstation_guid)}
        )
        
        return {
            "access_token": access_token,
            "role": str(user["role"]),
            "expires_in": 60 * 60  # 1 hour in seconds
        }
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format",
        )
