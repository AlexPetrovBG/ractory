from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import uuid

from app.models.company import Company
from app.schemas.company import CompanyCreate

class CompanyService:
    @staticmethod
    async def get_company_by_guid(db: AsyncSession, company_guid: uuid.UUID) -> Company | None:
        result = await db.execute(select(Company).filter(Company.guid == company_guid))
        return result.scalars().first()

    @staticmethod
    async def get_company_by_name(db: AsyncSession, name: str) -> Company | None:
        result = await db.execute(select(Company).filter(Company.name == name))
        return result.scalars().first()

    @staticmethod
    async def create_company(db: AsyncSession, company: CompanyCreate) -> Company:
        db_company = Company(**company.dict())
        db.add(db_company)
        await db.commit()
        await db.refresh(db_company)
        return db_company

    # Add other service methods as needed (e.g., update_company, delete_company, get_all_companies) 