from typing import Optional, List, Dict, Any
from sqlalchemy import select, update, delete, func, text
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from uuid import UUID

from app.models.user import User
from app.models.enums import UserRole

async def get_user_by_email(db: AsyncSession, email: str) -> Optional[Dict[str, Any]]:
    """
    Get a user by email.
    
    Args:
        db: Database session
        email: The email address of the user to retrieve
        
    Returns:
        User data as a dictionary if found, None otherwise
    """
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    user = result.scalars().first()
    
    if not user:
        return None
    
    return {
        "guid": user.guid,
        "email": user.email,
        "pwd_hash": user.pwd_hash,
        "role": user.role,
        "company_guid": user.company_guid,
        "is_active": user.is_active,
        "pin": user.pin
    }

async def get_user_by_guid(db: AsyncSession, user_guid: UUID) -> Optional[Dict[str, Any]]:
    """
    Get a user by GUID.
    
    Args:
        db: Database session
        user_guid: The GUID of the user to retrieve
        
    Returns:
        User data as a dictionary if found, None otherwise
    """
    query = select(User).where(User.guid == user_guid)
    result = await db.execute(query)
    user = result.scalars().first()
    
    if not user:
        return None
    
    return {
        "guid": user.guid,
        "email": user.email,
        "role": user.role,
        "company_guid": user.company_guid,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None
    }

async def get_users(
    db: AsyncSession, 
    company_guid: UUID = None, 
    page: int = 1, 
    size: int = 10,
    role: str = None
) -> Tuple[List[Dict[str, Any]], int]:
    """
    Get a paginated list of users with optional filtering.
    
    Args:
        db: Database session
        company_guid: Optional company GUID filter
        page: Page number (starting from 1)
        size: Number of items per page
        role: Optional role filter
        
    Returns:
        Tuple containing the list of users and the total count
    """
    # Calculate offset
    offset = (page - 1) * size
    
    # Base query
    query = select(User)
    count_query = select(func.count()).select_from(User)
    
    # Apply filters
    if company_guid:
        query = query.where(User.company_guid == company_guid)
        count_query = count_query.where(User.company_guid == company_guid)
    
    if role:
        query = query.where(User.role == role)
        count_query = count_query.where(User.role == role)
    
    # Get total count
    total = await db.scalar(count_query)
    
    # Get users with pagination
    query = query.offset(offset).limit(size)
    result = await db.execute(query)
    users = result.scalars().all()
    
    # Convert to dictionaries
    user_dicts = []
    for user in users:
        user_dicts.append({
            "guid": user.guid,
            "email": user.email,
            "role": user.role,
            "company_guid": user.company_guid,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat() if user.created_at else None
        })
    
    return user_dicts, total

async def get_user_by_guid_pin(
    db: AsyncSession, 
    user_guid: UUID, 
    pin: str
) -> Optional[Dict[str, Any]]:
    """
    Get a user by GUID and verify PIN.
    
    Args:
        db: Database session
        user_guid: The GUID of the user to retrieve
        pin: The user's PIN to verify
        
    Returns:
        User data as a dictionary if found and PIN matches, None otherwise
    """
    query = select(User).where(User.guid == user_guid, User.pin == pin)
    result = await db.execute(query)
    user = result.scalars().first()
    
    if not user:
        return None
    
    return {
        "guid": user.guid,
        "email": user.email,
        "role": user.role,
        "company_guid": user.company_guid,
        "is_active": user.is_active
    }

async def create_user(db: AsyncSession, user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new user.
    
    Args:
        db: Database session
        user_data: Dictionary containing user data
        
    Returns:
        The created user as a dictionary
    """
    # Create new user instance
    user = User(
        email=user_data.get("email"),
        pwd_hash=user_data.get("pwd_hash"),
        company_guid=user_data.get("company_guid"),
        role=user_data.get("role"),
        pin=user_data.get("pin"),
        is_active=user_data.get("is_active", True)
    )
    
    # Add to session and commit
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return {
        "guid": user.guid,
        "email": user.email,
        "role": user.role,
        "company_guid": user.company_guid,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }

async def update_user(
    db: AsyncSession, 
    user_guid: UUID, 
    user_data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Update an existing user.
    
    Args:
        db: Database session
        user_guid: The GUID of the user to update
        user_data: Dictionary containing updated user data
        
    Returns:
        The updated user as a dictionary if found, None otherwise
    """
    # Get the user
    query = select(User).where(User.guid == user_guid)
    result = await db.execute(query)
    user = result.scalars().first()
    
    if not user:
        return None
    
    # Update fields
    for key, value in user_data.items():
        if hasattr(user, key) and value is not None:
            setattr(user, key, value)
    
    # Commit changes
    await db.commit()
    await db.refresh(user)
    
    return {
        "guid": user.guid,
        "email": user.email,
        "role": user.role,
        "company_guid": user.company_guid,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None
    } 