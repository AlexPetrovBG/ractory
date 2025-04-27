from fastapi import Depends, HTTPException, status
from typing import List, Callable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.deps import CurrentUser, get_current_user, get_tenant_session
from app.models.enums import UserRole

def require_roles(*allowed_roles: str) -> Callable:
    """
    Dependency factory to require specific roles for an endpoint.
    
    Args:
        *allowed_roles: Variadic list of allowed roles (from UserRole enum)
        
    Returns:
        Dependency function that validates user roles
        
    Example:
        @app.get("/admin-only", dependencies=[Depends(require_roles(UserRole.SYSTEM_ADMIN))])
    """
    async def _require_roles(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required one of: {', '.join(allowed_roles)}"
            )
        return current_user
    
    return _require_roles

# Convenience dependencies for common role checks
require_system_admin = require_roles("SystemAdmin")
require_company_admin = require_roles("SystemAdmin", "CompanyAdmin")
require_project_manager = require_roles(
    "SystemAdmin", "CompanyAdmin", "ProjectManager"
)

async def set_tenant_context(
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_tenant_session)
) -> AsyncSession:
    """
    Middleware-like dependency to set the PostgreSQL tenant context.
    
    This enables RLS policies by setting the app.tenant parameter.
    SystemAdmin users bypass RLS via app.bypass_rls.
    
    Args:
        current_user: The authenticated user from JWT
        session: Database session
        
    Returns:
        Session with tenant context set
    """
    # For SystemAdmin, bypass RLS
    if current_user.role == "SystemAdmin":
        await session.execute(text("SET app.bypass_rls = true"))
    else:
        # For other roles, set tenant context
        await session.execute(text(f"SET app.tenant = '{current_user.tenant}'"))
    
    return session

def scope_guard(resource_company_guid_field: str):
    """
    Ensures the current user can only access resources in their own company.
    
    SystemAdmin users bypass this check.
    
    Args:
        resource_company_guid_field: Name of the field in the resource containing company_guid
        
    Returns:
        Dependency function that validates tenant access
    """
    async def _scope_guard(
        current_user: CurrentUser = Depends(get_current_user),
        resource: dict = Depends()
    ):
        # SystemAdmin can access all resources
        if current_user.role == "SystemAdmin":
            return resource
            
        # For other users, ensure resource.company_guid matches user's tenant
        if resource_company_guid_field not in resource or resource[resource_company_guid_field] != current_user.tenant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found"
            )
            
        return resource
    
    return _scope_guard 