from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.security import get_current_active_user, hash_password
from app.core.database import get_db
from app.models import User
from app.schemas import UserCreate, UserUpdate, UserResponse
from app.core.security import RoleChecker
from app.utils.role_utils import can_manage_role

router = APIRouter()

# Permission requirements
allow_system_or_company_admin = RoleChecker(["SystemAdmin", "CompanyAdmin"])
allow_system_admin = RoleChecker(["SystemAdmin"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Create a new user.
    - SystemAdmin can create users with any role
    - CompanyAdmin can only create users with lower roles (ProjectManager, Operator)
    - Other roles cannot create users
    """
    # Check if email already exists
    result = await db.execute(select(User).filter(User.email == user_data.email))
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Only SystemAdmin and CompanyAdmin can create users
    if current_user.role not in ["SystemAdmin", "CompanyAdmin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create users"
        )
    
    # Check role creation permissions using the role hierarchy
    if not can_manage_role(current_user.role, user_data.role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create users with this role"
        )
    
    # Non-SystemAdmin can only create users in their own company
    if current_user.role != "SystemAdmin" and user_data.company_guid != current_user.company_guid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create users in other companies"
        )
    
    # Create user
    user = User(
        email=user_data.email,
        pwd_hash=hash_password(user_data.password),
        role=user_data.role,
        company_guid=user_data.company_guid,
        is_active=True,
        pin=user_data.pin,
        name=user_data.name,
        surname=user_data.surname,
        picture_path=user_data.picture_path
    )
    
    # Add and commit to database
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return user


@router.get("", response_model=List[UserResponse])
async def get_users(
    role: Optional[str] = Query(None, description="Filter by role"),
    active: Optional[bool] = Query(None, description="Filter by active status"),
    company_guid: Optional[UUID] = Query(None, description="Filter by company GUID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get users based on filters and permissions.
    - SystemAdmin can view all users or filter by company
    - Other roles can only view users from their own company
    """
    # Start with base query
    query = select(User)
    
    # Handle company access based on role
    if current_user.role != "SystemAdmin":
        # Non-SystemAdmin users can only see their own company's users
        query = query.filter(User.company_guid == current_user.company_guid)
        if company_guid and company_guid != current_user.company_guid:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view users from other companies"
            )
    elif company_guid:
        # SystemAdmin can filter by company if requested
        query = query.filter(User.company_guid == company_guid)
    
    # Apply additional filters if provided
    if role:
        query = query.filter(User.role == role)
    if active is not None:
        query = query.filter(User.is_active == active)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{guid}", response_model=UserResponse)
async def get_user(
    guid: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get a specific user by GUID."""
    result = await db.execute(select(User).filter(User.guid == guid))
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Non-system admins can only view users from their company
    if current_user.role != "SystemAdmin" and user.company_guid != current_user.company_guid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view users from other companies"
        )
    
    return user


@router.put("/{guid}", response_model=UserResponse)
async def update_user(
    guid: UUID,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Update a user's information. 
    - SystemAdmin can update any user
    - CompanyAdmin can only update users from their company and only to lower roles
    - Users can update their own information except role
    """
    # Get the user to update
    result = await db.execute(select(User).filter(User.guid == guid))
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    is_updating_self = (current_user.guid == user.guid)

    # Role change attempt?
    changing_role = hasattr(user_data, 'role') and user_data.role is not None and user_data.role != user.role

    if current_user.role == "SystemAdmin":
        # SystemAdmin: Check role management logic if changing role
        if changing_role:
            if not (can_manage_role(current_user.role, user.role) and \
                    can_manage_role(current_user.role, user_data.role)):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="SystemAdmin: Not authorized to make this role transition."
                )
    elif current_user.role == "CompanyAdmin":
        # CompanyAdmin: Must be within the same company
        if user.company_guid != current_user.company_guid:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="CompanyAdmin: Not authorized to update users from other companies."
            )
        if changing_role:
            if is_updating_self:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="CompanyAdmin: You cannot change your own role."
                )
            # Check role management for updating another user
            if not (can_manage_role(current_user.role, user.role) and \
                    can_manage_role(current_user.role, user_data.role)):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="CompanyAdmin: Not authorized to make this role transition for the user."
                )
    else: # ProjectManager, Operator, etc.
        if not is_updating_self:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your own account."
            )
        if changing_role: 
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot change your own role."
            )
    
    # Update fields
    if hasattr(user_data, 'email') and user_data.email is not None:
        # Check if email exists for another user
        result = await db.execute(select(User).filter(User.email == user_data.email, User.guid != guid))
        existing = result.scalars().first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered to another user"
            )
        user.email = user_data.email
    
    if hasattr(user_data, 'password') and user_data.password is not None:
        user.pwd_hash = hash_password(user_data.password)
    
    if hasattr(user_data, 'role') and user_data.role is not None:
        user.role = user_data.role
    
    if hasattr(user_data, 'is_active') and user_data.is_active is not None:
        user.is_active = user_data.is_active
    
    if hasattr(user_data, 'pin') and user_data.pin is not None:
        user.pin = user_data.pin
        
    if 'name' in user_data.__dict__:
        user.name = user_data.name
        
    if 'surname' in user_data.__dict__:
        user.surname = user_data.surname
        
    if 'picture_path' in user_data.__dict__:
        user.picture_path = user_data.picture_path
    
    # Commit changes
    await db.commit()
    await db.refresh(user)
    
    return user


@router.delete("/{guid}", status_code=status.HTTP_200_OK)
async def delete_user(
    guid: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Soft delete a user by setting is_active to False.
    Only SystemAdmin and CompanyAdmin can deactivate users.
    """
    allow_system_or_company_admin(current_user.role)
    
    # Get the user to delete
    result = await db.execute(select(User).filter(User.guid == guid))
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Authorization checks
    if current_user.role != "SystemAdmin":
        # Non-SystemAdmin can only delete users in their company
        if user.company_guid != current_user.company_guid:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete users from other companies"
            )
        
        # Non-SystemAdmin can't delete SystemAdmins
        if user.role == "SystemAdmin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete SystemAdmin users"
            )
        
        # Non-SystemAdmin can't delete Integration users
        if user.role == "Integration":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete Integration users"
            )
    
    # Self-deletion check
    if user.guid == current_user.guid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    # Instead of hard deletion, set is_active to False
    user.is_active = False
    await db.commit()
    
    return {"message": "User deactivated successfully", "guid": str(user.guid)} 