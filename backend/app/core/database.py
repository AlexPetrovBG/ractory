from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os

# Database connection parameters
DB_HOST = os.getenv("DB_HOST", "db_dev")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "rafactory_dev")
DB_USER = os.getenv("DB_USER", "rafactory_rw")
DB_PASS = os.getenv("DB_PASS", "R4fDBP4ssw0rd9X")

# Construct the connection URL for asyncpg
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create the async engine
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create a session factory for async sessions
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Import the Base from the models directory to ensure we use the same Base
from app.models.base import Base

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get an async database session.
    
    This function is used as a dependency in FastAPI route functions to
    ensure each request gets its own session, which is closed after the
    request is processed.
    
    Returns:
        AsyncGenerator[AsyncSession, None]: A SQLAlchemy AsyncSession object
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close() 