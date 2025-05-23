from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, DateTime, Column
from sqlalchemy.sql import func
import os
from datetime import datetime
from typing import Optional

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

class TimestampMixin:
    """Mixin that adds created_at and updated_at columns to a model.
    
    This mixin should be used with all models that need to track creation
    and modification timestamps. It automatically sets created_at on insert
    and updated_at is handled by a database trigger.
    """
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

# Session dependency
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session 