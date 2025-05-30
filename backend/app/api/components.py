from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import get_session
from app.models.component import Component
from app.schemas.sync.components import ComponentResponse, ComponentDetail
from app.core.deps import get_current_user, CurrentUser, get_tenant_session
from app.models.enums import UserRole
from app.core.tenant_utils import add_tenant_filter, verify_tenant_access, validate_company_access
from app.models.project import Project
from app.services.sync_service import SyncService

router = APIRouter()

@router.get("", response_model=List[ComponentResponse])
async def list_components(
    request: Request,
    project_guid: Optional[UUID] = None,
    company_guid: Optional[UUID] = None,
    include_inactive: bool = Query(False, description="Include soft-deleted components"),
    session: AsyncSession = Depends(get_tenant_session),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    List all components, optionally filtered by project_guid or company_guid.
    - By default, only active (not soft-deleted) components are returned.
    - Set `include_inactive=true` to include soft-deleted components (where is_active is False).
    - Each component includes `is_active` and `deleted_at` fields to indicate soft deletion status.
    """
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
    
    # Add inactive filtering
    if not include_inactive:
        query = query.where(Component.is_active == True)
    
    # Execute query
    result = await session.execute(query)
    components = result.scalars().all()
    
    # Convert to response model
    return [ComponentResponse.model_validate(component) for component in components]

@router.get("/{component_guid}", response_model=ComponentDetail)
async def get_component(
    component_guid: UUID,
    include_inactive: bool = Query(False, description="Include soft-deleted component"),
    session: AsyncSession = Depends(get_tenant_session),
    current_user: CurrentUser = Depends(get_current_user)
):
    """Get a specific component by GUID."""
    # Create base query 
    stmt = select(Component).where(Component.guid == component_guid)
    
    # Add explicit tenant filtering as defense-in-depth
    stmt = add_tenant_filter(stmt, current_user.tenant, current_user.role)
    
    # PATCH: Only filter for active if include_inactive is False
    if not include_inactive:
        stmt = stmt.where(Component.is_active == True)
    
    # Execute query
    result = await session.execute(stmt)
    component = result.scalar_one_or_none()

    print(f"DEBUG: component type={type(component)}, repr={component!r}")
    print(f"DEBUG: component.__dict__={getattr(component, '__dict__', str(component))}")
    
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")

    if current_user.role != UserRole.SYSTEM_ADMIN and str(component.company_guid) != str(current_user.tenant):
        raise HTTPException(status_code=403, detail="Access to this component is forbidden.")
    
    assembly_count = 0
    piece_count = 0
    # Build response dict explicitly to avoid getattr/annotation issues
    component_data = {
        "guid": component.guid,
        "code": component.code,
        "designation": component.designation,
        "project_guid": component.project_guid,
        "quantity": component.quantity,
        "company_guid": component.company_guid,
        "created_at": component.created_at,
        "updated_at": getattr(component, "updated_at", None),
        "is_active": component.is_active,
        "deleted_at": component.deleted_at,
        "assembly_count": assembly_count,
        "piece_count": piece_count,
        # Add any other required fields here
    }
    
    # Check for missing required (non-Optional) fields
    required_fields = [
        "guid", "code", "project_guid", "quantity", "company_guid", "created_at"
    ]
    missing = [f for f in required_fields if component_data.get(f) is None]
    if missing:
        raise HTTPException(status_code=500, detail=f"Component missing required fields: {missing}")

    return ComponentDetail.model_validate(component_data)

@router.delete("/{component_guid}", status_code=204)
async def soft_delete_component(
    component_guid: UUID,
    session: AsyncSession = Depends(get_tenant_session),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Soft delete a component by GUID.
    - Sets `is_active` to False and `deleted_at` to the current timestamp.
    - Cascades soft delete to all active children (assemblies, pieces, articles).
    - Returns 204 No Content on success.
    """
    stmt = select(Component).where(Component.guid == component_guid)
    stmt = add_tenant_filter(stmt, current_user.tenant, current_user.role)
    result = await session.execute(stmt)
    component = result.scalar_one_or_none()
    if not component:
        raise HTTPException(status_code=404, detail="Component not found or forbidden")
    await SyncService.cascade_soft_delete('component', component_guid, session)
    return None

@router.post("/{component_guid}/restore", status_code=204)
async def restore_component(
    component_guid: UUID,
    session: AsyncSession = Depends(get_tenant_session),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Restore a soft-deleted component by GUID.
    - Sets `is_active` to True and `deleted_at` to NULL for the component.
    - Restores only children with `deleted_at` matching the parent's original `deleted_at`.
    - Returns 204 No Content on success.
    """
    stmt = select(Component).where(Component.guid == component_guid)
    stmt = add_tenant_filter(stmt, current_user.tenant, current_user.role)
    result = await session.execute(stmt)
    component = result.scalar_one_or_none()
    if not component:
        raise HTTPException(status_code=404, detail="Component not found or forbidden")
    await SyncService.cascade_restore('component', component_guid, session)
    return None 