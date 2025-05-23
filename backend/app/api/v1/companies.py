from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import uuid

from app.schemas.company import CompanyCreate, CompanyRead, CompanyUpdate
from app.services.company_service import CompanyService
from app.core.deps import get_session, get_current_user
from app.core.rbac import require_roles # Assuming require_roles checks for one or more roles
from app.models.enums import UserRole

router = APIRouter(
    prefix="/companies",
    tags=["companies"],
    dependencies=[Depends(require_roles(UserRole.SYSTEM_ADMIN))] # Temporarily commented out for testing
)

@router.post("", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
async def create_company(
    company_in: CompanyCreate,
    db: AsyncSession = Depends(get_session),
    # current_user: CurrentUser = Depends(get_current_user) # Inject if needed for logging/audit
):
    """
    Create a new company. Only accessible by System Administrators.
    """
    # Check if company already exists by name
    existing_company = await CompanyService.get_company_by_name(db, name=company_in.name)
    if existing_company:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Company with name '{company_in.name}' already exists."
        )
    
    # Check if company_index is provided and if it's unique
    if company_in.company_index is not None:
        existing_with_index = await CompanyService.get_company_by_index(db, index=company_in.company_index)
        if existing_with_index:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Company index {company_in.company_index} is already in use."
            )
    
    # Create company
    try:
        new_company = await CompanyService.create_company(db=db, company=company_in)
        return new_company
    except ValueError as e:
        # Handle validation errors from Pydantic
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        # Log the error properly in a real application
        print(f"Error creating company: {e}") 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create company."
        )

@router.get("", response_model=List[CompanyRead])
async def list_companies(
    db: AsyncSession = Depends(get_session),
    skip: int = 0, 
    limit: int = 100
):
    """
    List all companies. Only accessible by System Administrators.
    """
    try:
        companies = await CompanyService.get_companies(db, skip=skip, limit=limit)
        return companies
    except Exception as e:
        print(f"Error listing companies: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not retrieve companies."
        )

@router.get("/{company_guid}", response_model=CompanyRead)
async def get_company(
    company_guid: uuid.UUID = Path(..., description="The UUID of the company to retrieve"),
    db: AsyncSession = Depends(get_session)
):
    """
    Get a specific company by GUID. Only accessible by System Administrators.
    """
    company = await CompanyService.get_company(db, company_guid=company_guid)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with GUID {company_guid} not found."
        )
    return company

@router.patch("/{company_guid}", response_model=CompanyRead)
async def update_company(
    company_guid: uuid.UUID = Path(..., description="The UUID of the company to update"),
    company_update: CompanyUpdate = None,
    db: AsyncSession = Depends(get_session)
):
    """
    Update a specific company by GUID. Only accessible by System Administrators.
    This is a partial update - only fields included in the request will be updated.
    """
    # First check if the company exists
    existing_company = await CompanyService.get_company(db, company_guid=company_guid)
    if not existing_company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with GUID {company_guid} not found."
        )
    
    # If update data is empty, return the existing company
    if not company_update or not company_update.dict(exclude_unset=True):
        return existing_company
    
    try:
        # Only pass fields that were actually provided
        update_data = company_update.dict(exclude_unset=True)
        
        # Check if company_index is being updated and validate uniqueness
        if 'company_index' in update_data and update_data['company_index'] is not None:
            # Check if another company already has this index
            existing_with_index = await CompanyService.get_company_by_index(db, update_data['company_index'])
            if existing_with_index and existing_with_index.guid != company_guid:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Company index {update_data['company_index']} is already in use."
                )
        
        updated_company = await CompanyService.update_company(
            db, 
            company_guid=company_guid, 
            company_data=update_data
        )
        return updated_company
    except ValueError as e:
        # Handle input validation errors
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except HTTPException:
        # Re-raise HTTP exceptions without wrapping them
        raise
    except Exception as e:
        print(f"Error updating company: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not update company: {str(e)}"
        )

@router.put("/{company_guid}", response_model=CompanyRead)
async def put_company(
    company_guid: uuid.UUID = Path(..., description="The UUID of the company to update"),
    company_update: CompanyUpdate = None,
    db: AsyncSession = Depends(get_session)
):
    """
    Full update of a company. Only accessible by System Administrators.
    This is implemented as an alias to the PATCH endpoint to solve the 405 Method Not Allowed error.
    """
    # Use the same implementation as PATCH
    return await update_company(company_guid, company_update, db)

@router.delete("/{company_guid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_guid: uuid.UUID = Path(..., description="The UUID of the company to delete"),
    db: AsyncSession = Depends(get_session)
):
    """
    Delete a specific company by GUID. Only accessible by System Administrators.
    """
    # First check if the company exists
    existing_company = await CompanyService.get_company(db, company_guid=company_guid)
    if not existing_company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with GUID {company_guid} not found."
        )
    
    try:
        await CompanyService.delete_company(db, company_guid=company_guid)
        return None
    except Exception as e:
        print(f"Error deleting company: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not delete company: {str(e)}"
        )

# Add other company endpoints here (GET, PUT, DELETE) as needed
# Remember to apply appropriate role checks (e.g., CompanyAdmin for GET/PUT within their own company) 