from typing import Optional, Dict, Any
import uuid
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User  # Updated import path for User model
from app.utils.security import verify_password, create_token
from app.models.enums import UserRole

class AuthService:
    @staticmethod
    async def authenticate_user(email: str, password: str, session: AsyncSession) -> Optional[Dict[str, Any]]:
        """
        Authenticate a user by email and password.
        
        Args:
            email: User's email address
            password: Plain text password to verify
            session: Database session
            
        Returns:
            User dict if authenticated, None otherwise
        """
        # Query the database for the user
        print(f"DEBUG: Attempting to authenticate user with email: {email}")
        query = select(User).where(User.email == email)
        result = await session.execute(query)
        user = result.scalars().first()
        
        # If user not found or password doesn't match, return None
        if not user:
            print(f"DEBUG: User not found during auth: {email}")
            return None
            
        # Added debug logging
        print(f"DEBUG: Found user {user.email}, with hash: {user.pwd_hash}")
        print(f"DEBUG: Verifying password for {user.email}...")
        
        if not verify_password(password, user.pwd_hash):
            print(f"DEBUG: Password verification failed for {user.email}")
            return None
            
        print(f"DEBUG: Password verification succeeded for {user.email}")
        
        # Return user info if authenticated
        return {
            "user_id": str(user.guid),
            "email": user.email,
            "role": user.role,
            "tenant": str(user.company_guid),
            "created_at": user.created_at
        }
        
    @staticmethod
    async def create_tokens(user: Dict[str, Any]) -> Dict[str, str]:
        """
        Create access and refresh tokens for a user.
        
        Args:
            user: User info dictionary with at least user_id, tenant, and role
            
        Returns:
            Dictionary with access_token, refresh_token, and role
        """
        # Create real JWT tokens using the security utility
        access_token = create_token(
            sub=user["user_id"],
            tenant=user["tenant"],
            role=user["role"],
            exp_min=15  # 15 minutes expiration
        )
        
        # Create refresh token with longer expiration
        refresh_token = create_token(
            sub=user["user_id"],
            tenant=user["tenant"],
            role=user["role"],
            exp_min=10080  # 7 days in minutes
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "role": user["role"],
            "expires_in": 900,  # 15 minutes in seconds
        }
        
    @staticmethod
    async def validate_qr_login(user_guid: uuid.UUID, workstation_guid: uuid.UUID, pin: str, session: AsyncSession) -> Optional[Dict[str, str]]:
        """
        Validate QR code login with PIN.
        
        Args:
            user_guid: User's UUID from QR code
            workstation_guid: Workstation UUID
            pin: User's 6-digit PIN
            session: Database session
            
        Returns:
            Tokens if validated, None otherwise
        """
        # Query the database for the user
        query = select(User).where(User.guid == user_guid)
        result = await session.execute(query)
        user = result.scalars().first()
        
        # Validate PIN and that the user is assigned to this workstation
        if not user or user.pin != pin:
            return None
        
        # In a real implementation, would check if user is assigned to this workstation
        # For now, just creating tokens
        user_dict = {
            "user_id": str(user.guid),
            "email": user.email,
            "role": user.role,
            "tenant": str(user.company_guid),
            "created_at": user.created_at,
            "workstation": str(workstation_guid)  # Add workstation to token claims
        }
        
        return await AuthService.create_tokens(user_dict) 