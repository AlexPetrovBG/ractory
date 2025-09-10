from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, DateTime, Column, Boolean
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from datetime import datetime
from typing import Optional, AsyncGenerator

# Create a single metadata instance
metadata = MetaData()

# Base class for all models, using the shared metadata
Base = declarative_base(metadata=metadata)

class TimestampMixin:
    """Mixin that adds created_at, updated_at, is_active, and deleted_at columns to a model.
    This mixin should be used with all models that need to track creation, modification, and soft deletion timestamps.
    Automatically sets created_at on insert and updated_at is handled by a database trigger.
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
    is_active = Column(Boolean, nullable=False, default=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

# Session dependency
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    # Note: async_session_factory should be defined in database.py
    # Import the correct session factory
    from app.core.database import async_session_factory
    async with async_session_factory() as session:
        yield session 