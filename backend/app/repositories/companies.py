from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, Tuple, List, Optional
from uuid import UUID

from app.models.company import Company
from app.schemas.companies import CompanyInDB

async def get_companies(
    db: AsyncSession, 
    page: int = 1, 
    size: int = 10
) -> Tuple[List[Dict[str, Any]], int]:
    """
    Get a paginated list of companies.
    
    Args:
        db: Database session
        page: Page number (starting from 1)
        size: Number of items per page
        
    Returns:
        Tuple containing the list of companies and the total count
    """
    # Calculate offset
    offset = (page - 1) * size
    
    # Get total count
    count_query = select(func.count()).select_from(Company)
    total = await db.scalar(count_query)
    
    # Get companies with pagination
    query = select(Company).offset(offset).limit(size)
    result = await db.execute(query)
    companies = result.scalars().all()
    
    # Convert to dictionaries
    company_dicts = [company.as_dict for company in companies]
    
    return company_dicts, total

async def get_company_by_guid(
    db: AsyncSession, 
    company_guid: UUID
) -> Optional[Dict[str, Any]]:
    """
    Get a company by GUID.
    
    Args:
        db: Database session
        company_guid: The GUID of the company to retrieve
        
    Returns:
        Company data as a dictionary if found, None otherwise
    """
    query = select(Company).where(Company.guid == company_guid)
    result = await db.execute(query)
    company = result.scalars().first()
    
    if not company:
        return None
    
    return company.as_dict

async def create_company(
    db: AsyncSession, 
    company_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create a new company.
    
    Args:
        db: Database session
        company_data: Dictionary containing company data
        
    Returns:
        The created company as a dictionary
    """
    # Create new company instance
    company = Company(
        name=company_data.get("name"),
        short_name=company_data.get("short_name"),
        logo_path=company_data.get("logo_path"),
        subscription_tier=company_data.get("subscription_tier", "Basic"),
        subscription_status=company_data.get("subscription_status", "trial"),
        is_active=company_data.get("is_active", True)
    )
    
    # Add to session and commit
    db.add(company)
    await db.commit()
    await db.refresh(company)
    
    return company.as_dict

async def update_company(
    db: AsyncSession, 
    company_guid: UUID, 
    company_data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Update an existing company.
    
    Args:
        db: Database session
        company_guid: The GUID of the company to update
        company_data: Dictionary containing updated company data
        
    Returns:
        The updated company as a dictionary if found, None otherwise
    """
    # Get the company
    query = select(Company).where(Company.guid == company_guid)
    result = await db.execute(query)
    company = result.scalars().first()
    
    if not company:
        return None
    
    # Update fields
    for key, value in company_data.items():
        if hasattr(company, key) and value is not None:
            setattr(company, key, value)
    
    # Commit changes
    await db.commit()
    await db.refresh(company)
    
    return company.as_dict

async def delete_company(
    db: AsyncSession, 
    company_guid: UUID
) -> bool:
    """
    Delete a company.
    
    Args:
        db: Database session
        company_guid: The GUID of the company to delete
        
    Returns:
        True if the company was deleted, False if not found
    """
    # Get the company
    query = select(Company).where(Company.guid == company_guid)
    result = await db.execute(query)
    company = result.scalars().first()
    
    if not company:
        return False
    
    # Delete the company
    await db.delete(company)
    await db.commit()
    
    return True 