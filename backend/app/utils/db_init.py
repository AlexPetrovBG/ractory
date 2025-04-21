import asyncio
from datetime import datetime
import os
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, async_session_factory
from app.models import company, user
from app.models.company import Company

# Create a direct engine for the script
DB_URL = "postgresql+asyncpg://rafactory_rw:StrongP@ss!@db/rafactory"
engine = create_async_engine(DB_URL, echo=False)

async def create_tables():
    """Create all tables in the database."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created.")

async def seed_sample_data():
    """Seed sample data for development."""
    async with async_session_factory() as session:
        # Check if we already have companies
        query = "SELECT COUNT(*) FROM companies"
        result = await session.execute(query)
        count = result.scalar()
        
        if count and count > 0:
            print(f"Sample data already exists. Found {count} companies.")
            return
            
        # Sample companies
        sample_companies = [
            Company(
                name="Test Company Ltd.",
                short_name="TestCo",
                logo_path="/logos/testco.png",
                subscription_tier="Professional",
                subscription_status="active",
                user_count=4,
                projects_count=12,
                workstations_count=8,
            ),
            Company(
                name="Another Corp",
                short_name="AC",
                logo_path="/logos/ac.png",
                subscription_tier="Basic",
                subscription_status="active",
                user_count=2,
                projects_count=5,
                workstations_count=3,
            ),
            Company(
                name="Inactive Example",
                short_name="IE",
                logo_path="/logos/ie.png",
                subscription_tier="Basic",
                subscription_status="inactive",
                user_count=1,
                projects_count=0,
                workstations_count=0,
                is_active=False,
            )
        ]
        
        # Create companies
        for company in sample_companies:
            session.add(company)
        
        await session.commit()
        print("Sample data seeded.")

async def init_db():
    """Initialize database schema and seed data."""
    await create_tables()
    await seed_sample_data()

if __name__ == "__main__":
    asyncio.run(init_db()) 