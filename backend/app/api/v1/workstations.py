from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_active_user, RoleChecker
from app.core.database import get_db
from app.models import Workstation, User, Company
from app.schemas import WorkstationCreate, WorkstationUpdate, WorkstationResponse
from app.schemas.workstation import WorkstationType

router = APIRouter()

# Permission requirements
allow_system_or_company_admin = RoleChecker(["SystemAdmin", "CompanyAdmin"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=WorkstationResponse)
async def create_workstation(
    workstation_data: WorkstationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Create a new workstation.
    
    Requires SystemAdmin or CompanyAdmin role.
    
    Args:
        workstation_data: Data for the new workstation
        
    Returns:
        The created workstation
        
    Raises:
        403: If CompanyAdmin tries to create workstation for another company
        422: If validation fails
        404: If the company_guid is not found
        400: If invalid company_guid format
    """
    allow_system_or_company_admin(current_user.role)
    
    # Set company_guid from current user if not provided
    if not workstation_data.company_guid:
        workstation_data.company_guid = current_user.company_guid
    
    # Allow SystemAdmin to create workstations for other companies
    if current_user.role != "SystemAdmin" and workstation_data.company_guid != current_user.company_guid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": "Cannot create workstation for another company",
                "company_guid": str(workstation_data.company_guid),
                "your_company": str(current_user.company_guid)
            }
        )
    
    # Verify that company exists
    company = await db.get(Company, workstation_data.company_guid)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Company not found",
                "company_guid": str(workstation_data.company_guid)
            }
        )
    
    try:
        # Create workstation object
        workstation = Workstation(
            location=workstation_data.location,
            type=workstation_data.type.value,  # Use enum value
            company_guid=workstation_data.company_guid,
            is_active=workstation_data.is_active
        )
        
        # Add and commit to database
        db.add(workstation)
        await db.commit()
        await db.refresh(workstation)
        
        return workstation
    except ValueError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid input data: {str(e)}"
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create workstation: {str(e)}"
        )


@router.get("", response_model=List[WorkstationResponse])
async def get_workstations(
    type: Optional[WorkstationType] = Query(None, description="Filter by workstation type"),
    active: Optional[bool] = Query(None, description="Filter by active status"),
    location: Optional[str] = Query(None, min_length=3, description="Filter by location (substring match)"),
    company_guid: Optional[UUID] = Query(None, description="Filter by company GUID (SystemAdmin only)"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get all workstations from the current user's company.
    
    Args:
        type: Optional filter by workstation type
        active: Optional filter by active status
        location: Optional filter by location substring
        company_guid: Optional company GUID to filter by (only for SystemAdmin)
        
    Returns:
        List of workstations matching the filters
        
    Note:
        - Results are limited to the user's company unless SystemAdmin
        - Empty list if no workstations match the filters
    """
    # Validate company access
    if company_guid and company_guid != current_user.company_guid and current_user.role != "SystemAdmin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access resources from another company"
        )
    
    # Use either the provided company_guid or the user's company_guid
    effective_company_guid = company_guid if company_guid and current_user.role == "SystemAdmin" else current_user.company_guid
    
    try:
        stmt = select(Workstation).where(Workstation.company_guid == effective_company_guid)
        if type:
            stmt = stmt.where(Workstation.type == type.value)
        if active is not None:
            stmt = stmt.where(Workstation.is_active == active)
        if location:
            stmt = stmt.where(Workstation.location.ilike(f"%{location}%"))
        
        result = await db.execute(stmt)
        workstations = result.scalars().all()
        return workstations
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve workstations: {str(e)}"
        )


@router.get("/{guid}", response_model=WorkstationResponse)
async def get_workstation(
    guid: UUID = Path(..., description="The GUID of the workstation to retrieve"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get a specific workstation by GUID.
    
    Args:
        guid: The unique identifier of the workstation
        
    Returns:
        The requested workstation
        
    Raises:
        404: If workstation not found
        403: If user tries to access workstation from another company
    """
    workstation = await db.get(Workstation, guid)
    
    if not workstation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Workstation not found",
                "guid": str(guid)
            }
        )
    
    # Non-system admins can only view workstations from their company
    if current_user.role != "SystemAdmin" and workstation.company_guid != current_user.company_guid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": "Not authorized to view workstations from other companies",
                "workstation_company": str(workstation.company_guid),
                "your_company": str(current_user.company_guid)
            }
        )
    
    return workstation


@router.put("/{guid}", response_model=WorkstationResponse)
async def update_workstation(
    guid: UUID = Path(..., description="The GUID of the workstation to update"),
    workstation_data: WorkstationUpdate = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Update a workstation's information.
    
    Requires SystemAdmin or CompanyAdmin role.
    
    Args:
        guid: The unique identifier of the workstation
        workstation_data: The fields to update
        
    Returns:
        The updated workstation
        
    Raises:
        404: If workstation not found
        403: If CompanyAdmin tries to update workstation from another company
        422: If validation fails
    """
    allow_system_or_company_admin(current_user.role)
    
    try:
        # Get the workstation to update
        workstation = await db.get(Workstation, guid)
        
        if not workstation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "Workstation not found",
                    "guid": str(guid)
                }
            )
        
        # CompanyAdmin can only update workstations in their company
        if current_user.role == "CompanyAdmin" and workstation.company_guid != current_user.company_guid:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "message": "Not authorized to update workstations from other companies",
                    "workstation_company": str(workstation.company_guid),
                    "your_company": str(current_user.company_guid)
                }
            )
        
        # Update fields
        if workstation_data.location is not None:
            workstation.location = workstation_data.location
        
        if workstation_data.type is not None:
            workstation.type = workstation_data.type.value
        
        if workstation_data.is_active is not None:
            workstation.is_active = workstation_data.is_active
        
        # Commit changes
        await db.commit()
        await db.refresh(workstation)
        
        return workstation
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update workstation: {str(e)}"
        )


@router.delete("/{guid}", status_code=status.HTTP_200_OK)
async def delete_workstation(
    guid: UUID = Path(..., description="The GUID of the workstation to deactivate"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Soft delete a workstation by setting is_active to False.
    
    Requires SystemAdmin or CompanyAdmin role.
    
    Args:
        guid: The unique identifier of the workstation
        
    Returns:
        Confirmation message with the workstation GUID
        
    Raises:
        404: If workstation not found
        403: If CompanyAdmin tries to delete workstation from another company
    """
    allow_system_or_company_admin(current_user.role)
    
    try:
        # Get the workstation to delete
        workstation = await db.get(Workstation, guid)
        
        if not workstation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "Workstation not found",
                    "guid": str(guid)
                }
            )
        
        # CompanyAdmin can only delete workstations in their company
        if current_user.role == "CompanyAdmin" and workstation.company_guid != current_user.company_guid:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "message": "Not authorized to delete workstations from other companies",
                    "workstation_company": str(workstation.company_guid),
                    "your_company": str(current_user.company_guid)
                }
            )
        
        # Soft delete by setting is_active to False
        workstation.is_active = False
        await db.commit()
        
        return {
            "message": "Workstation deactivated successfully",
            "guid": workstation.guid,
            "location": workstation.location
        }
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to deactivate workstation: {str(e)}"
        ) 