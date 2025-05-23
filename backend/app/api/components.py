from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import get_session
from app.models.component import Component
from app.schemas.sync.components import ComponentResponse, ComponentDetail
from app.core.deps import get_current_user, CurrentUser, get_tenant_session
from app.models.enums import UserRole
from app.core.tenant_utils import add_tenant_filter, verify_tenant_access, validate_company_access
from app.models.project import Project

router = APIRouter()

@router.get("", response_model=List[ComponentResponse])
async def list_components(
    request: Request,
    project_guid: Optional[UUID] = None,
    company_guid: Optional[UUID] = None,
    session: AsyncSession = Depends(get_tenant_session),
    current_user: CurrentUser = Depends(get_current_user)
):
    """List all components, optionally filtered by project_guid or company_guid."""
    # Validate company access if company_guid parameter is provided
    if company_guid:
        await validate_company_access(request, company_guid, current_user.tenant, current_user.role)
        # If validated, this company_guid can be used for filtering if user is SystemAdmin
        # Otherwise, filtering is implicitly by current_user.tenant via add_tenant_filter

    # Create base query
    query = select(Component)

    # Filter by project if specified
    if project_guid:
        # Before filtering by project_guid, ensure the project itself is accessible
        project_stmt = select(Project).where(Project.guid == project_guid)
        project_stmt = add_tenant_filter(project_stmt, current_user.tenant, current_user.role)
        project_result = await session.execute(project_stmt)
        project = project_result.scalar_one_or_none()
        if not project:
            raise HTTPException(status_code=404, detail=f"Project with GUID {project_guid} not found or not accessible.")
        query = query.where(Component.project_guid == project_guid)
    
    # Add explicit tenant filtering as defense-in-depth
    # If company_guid was provided and validated for a SystemAdmin, use that for filtering
    # Otherwise, current_user.tenant is used (which is the default for non-SystemAdmins)
    filter_tenant_id = str(company_guid) if company_guid and current_user.role == UserRole.SYSTEM_ADMIN else current_user.tenant
    query = add_tenant_filter(query, filter_tenant_id, current_user.role)
    
    # Execute query
    result = await session.execute(query)
    components = result.scalars().all()
    
    # Convert to response model
    return [ComponentResponse.model_validate(component) for component in components]

@router.get("/{component_guid}", response_model=ComponentDetail)
async def get_component(
    component_guid: UUID,
    session: AsyncSession = Depends(get_tenant_session),
    current_user: CurrentUser = Depends(get_current_user)
):
    """Get a specific component by GUID."""
    # Create base query 
    stmt = select(Component).where(Component.guid == component_guid)
    
    # Add explicit tenant filtering as defense-in-depth
    stmt = add_tenant_filter(stmt, current_user.tenant, current_user.role)
    
    # Execute query
    result = await session.execute(stmt)
    component = result.scalar_one_or_none()
    
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")

    # ADD THIS: Explicit company check for non-SystemAdmins
    if current_user.role != UserRole.SYSTEM_ADMIN and str(component.company_guid) != str(current_user.tenant):
        # This case should ideally not be hit if RLS and add_tenant_filter work,
        # but it's a strong safeguard.
        raise HTTPException(status_code=403, detail="Access to this component is forbidden.")
    # END ADD
    
    # Get assembly and piece counts
    assembly_count = 0  # Replace with actual count logic
    piece_count = 0     # Replace with actual count logic
    
    # Create a dict with component attributes
    component_data = {
        key: getattr(component, key) 
        for key in ComponentDetail.__annotations__.keys() 
        if hasattr(component, key)
    }
    
    # Add the count fields
    component_data["assembly_count"] = assembly_count
    component_data["piece_count"] = piece_count
    
    # Use model_validate
    return ComponentDetail.model_validate(component_data) 