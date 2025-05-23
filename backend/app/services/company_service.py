from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
import uuid
from typing import List, Dict, Any, Optional

from app.models.company import Company
from app.schemas.company import CompanyCreate

class CompanyService:
    @staticmethod
    async def create_company(db: AsyncSession, company: CompanyCreate) -> Company:
        """Create a new company in the database."""
        db_company = Company(**company.dict())
        db.add(db_company)
        await db.commit()
        await db.refresh(db_company)
        return db_company
    
    @staticmethod
    async def get_company_by_name(db: AsyncSession, name: str) -> Optional[Company]:
        """Get a company by its name."""
        result = await db.execute(select(Company).filter(Company.name == name))
        return result.scalars().first()
    
    @staticmethod
    async def get_company_by_index(db: AsyncSession, index: int) -> Optional[Company]:
        """Get a company by its index."""
        result = await db.execute(select(Company).filter(Company.company_index == index))
        return result.scalars().first()
    
    @staticmethod
    async def get_company(db: AsyncSession, company_guid: uuid.UUID) -> Optional[Company]:
        """Get a company by its GUID."""
        result = await db.execute(select(Company).filter(Company.guid == company_guid))
        return result.scalars().first()
    
    @staticmethod
    async def get_companies(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Company]:
        """Get a list of companies with pagination."""
        result = await db.execute(select(Company).offset(skip).limit(limit))
        return result.scalars().all()
    
    @staticmethod
    async def update_company(db: AsyncSession, company_guid: uuid.UUID, company_data: Dict[str, Any]) -> Optional[Company]:
        """
        Update a company with the provided data.
        Only fields included in company_data will be updated.
        """
        # Execute update query
        await db.execute(
            update(Company)
            .where(Company.guid == company_guid)
            .values(**company_data)
        )
        
        # Commit the transaction
        await db.commit()
        
        # Get and return the updated company
        return await CompanyService.get_company(db, company_guid)
    
    @staticmethod
    async def delete_company(db: AsyncSession, company_guid: uuid.UUID) -> bool:
        """Delete a company by its GUID."""
        # Execute delete query
        result = await db.execute(
            delete(Company).where(Company.guid == company_guid)
        )
        
        # Commit the transaction
        await db.commit()
        
        # Return True if a company was deleted
        return result.rowcount > 0

    # Add other service methods as needed (e.g., get_all_companies) 