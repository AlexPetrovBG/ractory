from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_active_user, RoleChecker
from app.core.database import get_db
from app.models import Workstation, User
from app.schemas import WorkstationCreate, WorkstationUpdate, WorkstationResponse

router = APIRouter()

# Permission requirements
allow_system_or_company_admin = RoleChecker(["SystemAdmin", "CompanyAdmin"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=WorkstationResponse)
async def create_workstation(
    workstation_data: WorkstationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Create a new workstation.
    Only SystemAdmin and CompanyAdmin can create workstations.
    """
    allow_system_or_company_admin(current_user.role)
    
    # Set company_guid from current user if not provided
    if not workstation_data.company_guid:
        workstation_data.company_guid = current_user.company_guid
    
    # Allow SystemAdmin to create workstations for other companies
    if current_user.role != "SystemAdmin" and workstation_data.company_guid != current_user.company_guid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create workstation for another company"
        )
    
    # Create workstation object
    workstation = Workstation(
        location=workstation_data.location,
        type=workstation_data.type,
        company_guid=workstation_data.company_guid,
        is_active=workstation_data.is_active
    )
    
    # Add and commit to database
    db.add(workstation)
    await db.commit()
    await db.refresh(workstation)
    
    return workstation


@router.get("/", response_model=List[WorkstationResponse])
async def get_workstations(
    type: Optional[str] = Query(None, description="Filter by workstation type"),
    active: Optional[bool] = Query(None, description="Filter by active status"),
    location: Optional[str] = Query(None, description="Filter by location (substring match)"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get all workstations from the current user's company.
    Can be filtered by type, active status, and location.
    """
    stmt = select(Workstation).where(Workstation.company_guid == current_user.company_guid)
    if type:
        stmt = stmt.where(Workstation.type == type)
    if active is not None:
        stmt = stmt.where(Workstation.is_active == active)
    if location:
        stmt = stmt.where(Workstation.location.ilike(f"%{location}%"))
    result = await db.execute(stmt)
    workstations = result.scalars().all()
    return workstations


@router.get("/{guid}", response_model=WorkstationResponse)
async def get_workstation(
    guid: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get a specific workstation by GUID."""
    workstation = await db.get(Workstation, guid)
    
    if not workstation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workstation not found"
        )
    
    # Non-system admins can only view workstations from their company
    if current_user.role != "SystemAdmin" and workstation.company_guid != current_user.company_guid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view workstations from other companies"
        )
    
    return workstation


@router.put("/{guid}", response_model=WorkstationResponse)
async def update_workstation(
    guid: UUID,
    workstation_data: WorkstationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Update a workstation's information.
    Only SystemAdmin and CompanyAdmin can update workstations.
    """
    allow_system_or_company_admin(current_user.role)
    
    # Get the workstation to update
    workstation = await db.get(Workstation, guid)
    
    if not workstation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workstation not found"
        )
    
    # CompanyAdmin can only update workstations in their company
    if current_user.role == "CompanyAdmin" and workstation.company_guid != current_user.company_guid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update workstations from other companies"
        )
    
    # Update fields
    if workstation_data.location is not None:
        workstation.location = workstation_data.location
    
    if workstation_data.type is not None:
        workstation.type = workstation_data.type
    
    if workstation_data.is_active is not None:
        workstation.is_active = workstation_data.is_active
    
    # Commit changes
    await db.commit()
    await db.refresh(workstation)
    
    return workstation


@router.delete("/{guid}", status_code=status.HTTP_200_OK)
async def delete_workstation(
    guid: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Soft delete a workstation by setting is_active to False.
    Only SystemAdmin and CompanyAdmin can deactivate workstations.
    """
    allow_system_or_company_admin(current_user.role)
    
    # Get the workstation to delete
    workstation = await db.get(Workstation, guid)
    
    if not workstation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workstation not found"
        )
    
    # CompanyAdmin can only delete workstations in their company
    if current_user.role == "CompanyAdmin" and workstation.company_guid != current_user.company_guid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete workstations from other companies"
        )
    
    # Soft delete by setting is_active to False
    workstation.is_active = False
    await db.commit()
    
    return {
        "message": "Workstation deactivated successfully",
        "guid": workstation.guid
    } 