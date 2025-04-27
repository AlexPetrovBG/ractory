from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
import os

# Get environment - default to development if not specified
ENV = os.getenv("ENV", "development")

# Set the appropriate database URL based on environment
if ENV == "production":
    DATABASE_URL = os.getenv(
        "DATABASE_URL", 
        "postgresql+asyncpg://rafactory_rw:R4fDBP4ssw0rd9X@localhost/rafactory_prod"
    )
else:
    DATABASE_URL = os.getenv(
        "DATABASE_URL", 
        "postgresql+asyncpg://rafactory_rw:R4fDBP4ssw0rd9X@db_dev/rafactory_dev"
    )

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Create a single metadata instance
metadata = MetaData()

# Base class for all models, using the shared metadata
Base = declarative_base(metadata=metadata)

# Session dependency
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session 