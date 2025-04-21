from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any, Optional
from uuid import UUID

from app.core.database import get_db
from app.core.deps import get_current_user, require_roles, tenant_middleware
from app.models.enums import Role
from app.repositories import users as users_repo

# Router setup
router = APIRouter(prefix="/users", tags=["users"])

@router.get("", response_model=List[Dict[str, Any]])
async def list_users(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    role: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(tenant_middleware)
):
    """
    List users for the current company.
    
    - Operators can only see themselves
    - Project Managers can see all operators and themselves
    - Company Admins can see all users in their company
    - System Admins can see all users in all companies
    """
    company_guid = current_user["company_guid"]
    user_role = current_user["role"]
    
    # Only Company Admins and System Admins can list all users
    if user_role not in [Role.COMPANY_ADMIN, Role.SYSTEM_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to list users"
        )
    
    # System admins can see all users, others only see their company
    if user_role == Role.SYSTEM_ADMIN:
        users, total = await users_repo.get_users(db, None, page, size, role)
    else:
        users, total = await users_repo.get_users(db, UUID(company_guid), page, size, role)
    
    return users

@router.get("/{user_guid}", response_model=Dict[str, Any])
async def get_user(
    user_guid: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(tenant_middleware)
):
    """
    Get a specific user by GUID.
    
    - Users can view their own profile
    - Company Admins can view any user in their company
    - System Admins can view any user
    """
    company_guid = current_user["company_guid"]
    user_role = current_user["role"]
    current_user_guid = current_user["sub"]
    
    # Get the requested user
    user = await users_repo.get_user_by_guid(db, user_guid)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check permissions - allow only if it's the user's own profile
    # or if they are an admin of the same company or a system admin
    if (current_user_guid != str(user_guid) and 
        (user_role != Role.SYSTEM_ADMIN and 
         (user_role != Role.COMPANY_ADMIN or str(user["company_guid"]) != company_guid))):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this user"
        )
    
    return user

@router.post("", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: Dict[str, Any],
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(tenant_middleware)
):
    """
    Create a new user.
    
    - Company Admins can create users in their company
    - System Admins can create users in any company
    """
    company_guid = current_user["company_guid"]
    user_role = current_user["role"]
    
    # Check permissions
    if user_role not in [Role.COMPANY_ADMIN, Role.SYSTEM_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create users"
        )
    
    # Set the company GUID for the new user
    target_company_guid = user_data.get("company_guid", company_guid)
    
    # Company admins can only create users in their own company
    if user_role == Role.COMPANY_ADMIN and target_company_guid != company_guid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Company admins can only create users in their own company"
        )
    
    # Create user
    try:
        user = await users_repo.create_user(db, user_data)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )

@router.patch("/{user_guid}", response_model=Dict[str, Any])
async def update_user(
    user_guid: UUID,
    user_data: Dict[str, Any],
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(tenant_middleware)
):
    """
    Update user information.
    
    - Users can update their own profile (limited fields)
    - Company Admins can update any user in their company
    - System Admins can update any user
    """
    company_guid = current_user["company_guid"]
    user_role = current_user["role"]
    current_user_guid = current_user["sub"]
    
    # Get the user to update
    user = await users_repo.get_user_by_guid(db, user_guid)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check permissions
    is_self_update = current_user_guid == str(user_guid)
    is_same_company = str(user["company_guid"]) == company_guid
    
    # Regular users can only update themselves and not change role or company
    if is_self_update and user_role not in [Role.COMPANY_ADMIN, Role.SYSTEM_ADMIN]:
        # Remove protected fields
        for field in ["role", "company_guid", "is_active"]:
            if field in user_data:
                del user_data[field]
    # Company admins can update users in their company
    elif user_role == Role.COMPANY_ADMIN and not is_same_company:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )
    # If not self, company admin of same company, or system admin, reject
    elif not is_self_update and user_role != Role.SYSTEM_ADMIN and (user_role != Role.COMPANY_ADMIN or not is_same_company):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )
    
    # Update user
    updated_user = await users_repo.update_user(db, user_guid, user_data)
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating user"
        )
    
    return updated_user 