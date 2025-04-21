from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, Optional, List
from uuid import UUID

from app.core.database import get_db
from app.core.deps import get_current_user, require_roles, tenant_middleware
from app.models.enums import Role
from app.repositories import companies as companies_repo
from app.schemas.companies import CompanyCreate, CompanyUpdate, CompanyRead

# Router setup
router = APIRouter(prefix="/companies", tags=["companies"])

@router.get("", response_model=List[CompanyRead])
async def list_companies(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(tenant_middleware)
):
    """
    List companies.
    
    - System Admins see all companies
    - Other roles see only their own company
    """
    user_role = current_user["role"]
    company_guid = current_user["company_guid"]
    
    # For System Admins, return all companies
    if user_role == Role.SYSTEM_ADMIN:
        companies, total = await companies_repo.get_companies(db, page, size)
        return companies
    
    # For other roles, return just their company as a list
    company = await companies_repo.get_company_by_guid(db, company_guid)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    return [company]

@router.get("/current", response_model=CompanyRead)
async def get_current_company(
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(tenant_middleware)
):
    """
    Get information about the current user's company.
    
    All authenticated users can access this endpoint to get basic info about their company.
    """
    company_guid = current_user["company_guid"]
    
    company = await companies_repo.get_company_by_guid(db, company_guid)
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    return company

@router.get("/{company_guid}", response_model=CompanyRead)
async def get_company(
    company_guid: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get information about a specific company.
    
    Only System Admins can view companies other than their own.
    Company Admins can only view their own company.
    """
    user_role = current_user["role"]
    user_company_guid = current_user["company_guid"]
    
    # Check permissions
    if user_role != Role.SYSTEM_ADMIN and str(company_guid) != user_company_guid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view other companies"
        )
    
    company = await companies_repo.get_company_by_guid(db, company_guid)
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    return company

@router.post("", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
async def create_company(
    company_data: CompanyCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(tenant_middleware)
):
    """
    Create a new company.
    
    Only System Admins can create companies.
    """
    # Check permissions
    if current_user["role"] != Role.SYSTEM_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only System Admins can create companies"
        )
    
    # Create company in database
    try:
        company = await companies_repo.create_company(db, company_data.dict())
        return company
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating company: {str(e)}"
        )

@router.patch("/{company_guid}", response_model=CompanyRead)
async def update_company(
    company_guid: UUID,
    company_data: CompanyUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(tenant_middleware)
):
    """
    Update company information.
    
    - System Admins can update any company
    - Company Admins can only update their own company
    """
    user_role = current_user["role"]
    user_company_guid = current_user["company_guid"]
    
    # Check permissions
    if user_role != Role.SYSTEM_ADMIN and str(company_guid) != user_company_guid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this company"
        )
    
    # Update company in database
    company = await companies_repo.update_company(db, company_guid, company_data.dict(exclude_unset=True))
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    return company

@router.delete("/{company_guid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_guid: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(tenant_middleware)
):
    """
    Delete a company.
    
    Only System Admins can delete companies.
    """
    # Check permissions
    if current_user["role"] != Role.SYSTEM_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only System Admins can delete companies"
        )
    
    # Delete company from database
    success = await companies_repo.delete_company(db, company_guid)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    return None 