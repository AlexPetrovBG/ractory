from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db
from app.core.config import settings
import os

router = APIRouter()

@router.get("/health")
async def health_check_v1(db: AsyncSession = Depends(get_db)):
    """Comprehensive health check endpoint for API v1."""
    
    # Check database connectivity
    db_status = "connected"
    try:
        await db.execute(text("SELECT 1"))
    except Exception:
        db_status = "disconnected"
    
    # Get environment info
    environment = os.getenv("ENVIRONMENT", "production")
    
    return {
        "status": "healthy" if db_status == "connected" else "unhealthy",
        "version": "0.1.0",
        "api_version": "v1", 
        "environment": environment,
        "database": db_status
    } 