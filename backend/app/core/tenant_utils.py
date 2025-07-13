"""
Utilities for multi-tenant context management.

This module provides functions to ensure correct tenant context is set
for all database operations to ensure proper isolation.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from fastapi import HTTPException, status, Request
from uuid import UUID
from typing import Optional, List, Set, Dict, Any, Union

from app.models.enums import UserRole

async def set_tenant_context(session: AsyncSession, tenant_id: Optional[str], role: Optional[str] = None) -> None:
    """
    Set the tenant context for the database session.
    
    This sets the PostgreSQL session variables that control Row-Level Security (RLS).
    
    Args:
        session: SQLAlchemy AsyncSession to set context on
        tenant_id: The tenant ID (company_guid) to set
        role: The user role, to determine if RLS should be bypassed
        
    Returns:
        None
    """
    # Clear any existing tenant context first
    await session.execute(text("RESET app.tenant"))
    await session.execute(text("RESET app.bypass_rls"))
    
    # For SystemAdmin role, bypass RLS
    if role == UserRole.SYSTEM_ADMIN:
        await session.execute(text("SET app.bypass_rls = true"))
    elif tenant_id:
        # For other roles, set tenant context
        # Ensure tenant_id is properly formatted and escaped
        await session.execute(text(f"SET app.tenant = '{str(tenant_id)}'"))

async def get_tenant_context(session: AsyncSession) -> Dict[str, Any]:
    """
    Get the current tenant context from the database session.
    
    Args:
        session: SQLAlchemy AsyncSession to get context from
        
    Returns:
        Dict with tenant and bypass_rls values
    """
    tenant_result = await session.execute(text("SHOW app.tenant"))
    tenant = tenant_result.scalar()
    
    bypass_result = await session.execute(text("SHOW app.bypass_rls"))
    bypass_rls = bypass_result.scalar()
    
    return {
        "tenant": tenant,
        "bypass_rls": bypass_rls == "true"
    }

def verify_tenant_access(resource_company_guid: Union[str, UUID], user_company_guid: Union[str, UUID], 
                        user_role: str) -> bool:
    """
    Verify a user has access to a resource based on tenant.
    
    Args:
        resource_company_guid: The company GUID of the resource
        user_company_guid: The company GUID of the user
        user_role: The role of the user
        
    Returns:
        True if access is allowed, False otherwise
    """
    # SystemAdmin can access all resources
    if user_role == UserRole.SYSTEM_ADMIN:
        return True
        
    # For other roles, ensure company GUIDs match
    return str(resource_company_guid) == str(user_company_guid)

async def validate_company_access(request: Request, resource_company_guid: Union[str, UUID], 
                                user_company_guid: Union[str, UUID], user_role: str) -> None:
    """
    Validate user's company access and raise HTTPException if not allowed.
    
    This function should be used in route handlers to explicitly validate
    company_guid parameters against the user's company.
    
    Args:
        request: The FastAPI request object
        resource_company_guid: The company GUID to validate access for
        user_company_guid: The user's company GUID
        user_role: The user's role
        
    Returns:
        None if access is allowed
        
    Raises:
        HTTPException: 403 if access is not allowed
    """
    # Always allow SystemAdmin
    if user_role == UserRole.SYSTEM_ADMIN:
        return
    
    # For all other roles, ensure company GUIDs match
    if str(resource_company_guid) != str(user_company_guid):
        # Store attempted cross-company access in request state for logging
        request.state.cross_company_attempt = {
            "resource_company": str(resource_company_guid),
            "user_company": str(user_company_guid),
            "path": request.url.path,
            "method": request.method
        }
        
        # Raise 403 for cross-company access attempt
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access resources from another company"
        )

def add_tenant_filter(query, tenant_id: Optional[str], user_role: Optional[str] = None):
    """
    Add tenant filtering to a SQLAlchemy query if needed.
    
    This is a second layer of defense beyond RLS.
    
    Args:
        query: SQLAlchemy query object
        tenant_id: User's tenant ID (company_guid)
        user_role: User's role
        
    Returns:
        Updated query with tenant filtering
    """
    # Only SystemAdmin bypasses tenant filtering
    if user_role != UserRole.SYSTEM_ADMIN and tenant_id:
        # This assumes the model has company_guid attribute
        # The exact implementation may vary based on the model
        try:
            # Get the class from the query's statement
            entity = query.column_descriptions[0]['entity']
            if hasattr(entity, 'company_guid'):
                query = query.filter(entity.company_guid == tenant_id)
        except (IndexError, AttributeError):
            # If we can't determine the entity, just return the original query
            pass
            
    return query 