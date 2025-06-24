from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os

# Database connection parameters (match .env and compose)
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Construct the connection URL for asyncpg
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

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