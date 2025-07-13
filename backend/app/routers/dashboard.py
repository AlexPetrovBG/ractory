from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List
from uuid import UUID

from app.core.database import get_db
from app.core.deps import tenant_middleware
from app.models.enums import UserRole
from app.models.user import User
from app.models.company import Company
from app.repositories import users as users_repo
from app.repositories import companies as companies_repo

# Router setup
router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/counts", response_model=Dict[str, int])
async def get_dashboard_counts(
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(tenant_middleware)
):
    """
    Get counts for dashboard widgets.
    
    - For System Admins: Returns total counts across all companies
    - For Company Admins: Returns counts for their company only
    """
    result = {}
    user_role = current_user["role"]
    company_guid = current_user["company_guid"]
    
    # Get user count
    user_query = select(func.count()).select_from(User)
    if user_role != UserRole.SYSTEM_ADMIN and company_guid:
        user_query = user_query.where(User.company_guid == UUID(company_guid))
    result["users"] = await db.scalar(user_query) or 0
    
    # Get company count (for system admins only)
    if user_role == UserRole.SYSTEM_ADMIN:
        company_query = select(func.count()).select_from(Company)
        result["companies"] = await db.scalar(company_query) or 0
    else:
        # Regular users only see 1 company - their own
        result["companies"] = 1
    
    # Projects and workstations - placeholder counts
    # These would be actual database queries in a complete implementation
    result["projects"] = 0
    result["workstations"] = 0
    
    # For company admins and system admins, try to get the actual counts from company record
    if user_role in [UserRole.COMPANY_ADMIN, UserRole.SYSTEM_ADMIN] and company_guid:
        try:
            company = await companies_repo.get_company_by_guid(db, UUID(company_guid))
            if company:
                result["projects"] = company.get("projects_count", 0)
                result["workstations"] = company.get("workstations_count", 0)
        except Exception as e:
            print(f"Error getting company details: {e}")
    
    return result

@router.get("/recent-activity", response_model=List[Dict[str, Any]])
async def get_recent_activity(
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(tenant_middleware)
):
    """
    Get recent activity for the dashboard.
    
    - For System Admins: Returns system-wide activity
    - For Company Admins: Returns activity for their company only
    """
    # In a real implementation, this would query an audit_log or similar table
    # For now, we'll return placeholder data
    
    # Mock data - would be replaced with actual database query
    activity = [
        {
            "id": 1,
            "user": "system",
            "action": "System Status",
            "details": "All services operational",
            "timestamp": "2025-04-20T12:00:00Z"
        }
    ]
    
    return activity

@router.get("/company-info", response_model=Dict[str, Any])
async def get_company_info(
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(tenant_middleware)
):
    """
    Get information about the user's company.
    
    - For all users: Returns details about their company
    - For System Admins without a company: Returns system overview
    """
    company_guid = current_user.get("company_guid")
    user_role = current_user["role"]
    
    # If user has a company, get company details
    if company_guid:
        try:
            company = await companies_repo.get_company_by_guid(db, UUID(company_guid))
            if company:
                return company
        except Exception as e:
            print(f"Error getting company details: {e}")
    
    # For System Admins without a company, return system info
    if user_role == UserRole.SYSTEM_ADMIN:
        company_count = await db.scalar(select(func.count()).select_from(Company))
        user_count = await db.scalar(select(func.count()).select_from(User))
        
        return {
            "name": "System Administration",
            "short_name": "SYS",
            "subscription_tier": "Enterprise",
            "subscription_status": "active",
            "user_count": user_count,
            "companies_count": company_count,
            "is_active": True
        }
    
    # Fallback for users without company info
    return {
        "name": "Ra Factory",
        "short_name": "RF",
        "subscription_tier": "Basic",
        "subscription_status": "trial",
        "is_active": True
    } 