from fastapi import Depends, HTTPException, status
from typing import List, Optional, Dict, Any

from app.core.deps import get_current_user, CurrentUser
from app.utils.security import hash_password as utils_hash_password
from app.models.user import User
from app.models.base import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Re-export hash_password from utils for consistency
hash_password = utils_hash_password

# get_current_active_user function removed - use get_current_user instead
# which already provides the same functionality with better consistency

class RoleChecker:
    """
    Callable class to check if a user has one of the required roles.
    """
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles
    
    def __call__(self, role: str):
        if role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required one of: {', '.join(self.allowed_roles)}"
            )
        return True 