from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import get_session
from app.models.assembly import Assembly
from app.schemas.sync.assemblies import AssemblyResponse, AssemblyDetail
from app.core.deps import get_current_user, CurrentUser, get_tenant_session
from app.models.enums import UserRole
from app.core.tenant_utils import add_tenant_filter, verify_tenant_access, validate_company_access
from app.models.project import Project
from app.models.component import Component
from app.services.sync_service import SyncService

router = APIRouter()

@router.get("", response_model=List[AssemblyResponse])
async def list_assemblies(
    request: Request,
    project_guid: Optional[UUID] = None,
    component_guid: Optional[UUID] = None,
    company_guid: Optional[UUID] = None,
    include_inactive: bool = Query(False, description="Include soft-deleted assemblies"),
    session: AsyncSession = Depends(get_tenant_session),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    List all assemblies, optionally filtered by project, component, or company.
    - By default, only active (not soft-deleted) assemblies are returned.
    - Set `include_inactive=true` to include soft-deleted assemblies (where is_active is False).
    - Each assembly includes `is_active` and `deleted_at` fields to indicate soft deletion status.
    """
    # Validate company access if company_guid parameter is provided
    if company_guid:
        await validate_company_access(request, company_guid, current_user["company_guid"], current_user["role"])

    # Determine the tenant_id to use for filtering based on role and provided company_guid
    filter_tenant_id = str(company_guid) if company_guid and current_user["role"] == UserRole.SYSTEM_ADMIN else current_user["company_guid"]
    effective_tenant_check_id = filter_tenant_id if current_user["role"] == UserRole.SYSTEM_ADMIN else current_user["company_guid"]

    # Create base query
    query = select(Assembly)
    
    # Validate and apply project_guid filter
    if project_guid:
        project_stmt = select(Project).where(Project.guid == project_guid)
        project_stmt = add_tenant_filter(project_stmt, effective_tenant_check_id, current_user["role"])
        project_result = await session.execute(project_stmt)
        project = project_result.scalar_one_or_none()
        if not project:
            raise HTTPException(status_code=404, detail=f"Project with GUID {project_guid} not found or not accessible.")
        query = query.where(Assembly.project_guid == project_guid)

    # Validate and apply component_guid filter
    if component_guid:
        component_stmt = select(Component).where(Component.guid == component_guid)
        component_stmt = add_tenant_filter(component_stmt, effective_tenant_check_id, current_user["role"])
        component_result = await session.execute(component_stmt)
        component = component_result.scalar_one_or_none()
        if not component:
            raise HTTPException(status_code=404, detail=f"Component with GUID {component_guid} not found or not accessible.")
        if project_guid and component.project_guid != project_guid: # Check consistency if project_guid also given
            raise HTTPException(status_code=400, detail=f"Component {component_guid} does not belong to project {project_guid}.")
        query = query.where(Assembly.component_guid == component_guid)
    
    # Add tenant filtering for assemblies themselves
    query = add_tenant_filter(query, filter_tenant_id, current_user["role"])
    
    # Add is_active filter
    if not include_inactive:
        query = query.where(Assembly.is_active == True)
    
    # Execute query
    result = await session.execute(query)
    assemblies = result.scalars().all()
    
    # Convert to response model
    return [AssemblyResponse.model_validate(assembly) for assembly in assemblies]

@router.get("/{assembly_guid}", response_model=AssemblyDetail)
async def get_assembly(
    assembly_guid: UUID,
    include_inactive: bool = Query(False, description="Include soft-deleted assembly"),
    session: AsyncSession = Depends(get_tenant_session),
    current_user: CurrentUser = Depends(get_current_user)
):
    """Get a specific assembly by GUID."""
    # Create base query 
    stmt = select(Assembly).where(Assembly.guid == assembly_guid)
    
    # Add explicit tenant filtering as defense-in-depth
    stmt = add_tenant_filter(stmt, current_user["company_guid"], current_user["role"])
    
    # PATCH: Only filter for active if include_inactive is False
    if not include_inactive:
        stmt = stmt.where(Assembly.is_active == True)
    
    # Execute query
    result = await session.execute(stmt)
    assembly = result.scalar_one_or_none()
    
    if not assembly:
        raise HTTPException(status_code=404, detail="Assembly not found")

    if current_user["role"] != UserRole.SYSTEM_ADMIN and str(assembly.company_guid) != str(current_user["company_guid"]):
        raise HTTPException(status_code=403, detail="Access to this assembly is forbidden.")
    
    piece_count = 0
    # Build response dict explicitly to avoid getattr/annotation issues
    assembly_data = {
        "guid": assembly.guid,
        "project_guid": assembly.project_guid,
        "component_guid": assembly.component_guid,
        "trolley_cell": assembly.trolley_cell,
        "trolley": assembly.trolley,
        "cell_number": assembly.cell_number,
        "company_guid": assembly.company_guid,
        "created_at": assembly.created_at,
        "updated_at": getattr(assembly, "updated_at", None),
        "is_active": assembly.is_active,
        "deleted_at": assembly.deleted_at,
        "piece_count": piece_count,
        # Add any other required fields here
    }
    
    # Check for missing required (non-Optional) fields
    required_fields = [
        "guid", "project_guid", "component_guid", "company_guid", "created_at"
    ]
    missing = [f for f in required_fields if assembly_data.get(f) is None]
    if missing:
        raise HTTPException(status_code=500, detail=f"Assembly missing required fields: {missing}")

    return AssemblyDetail.model_validate(assembly_data)

@router.delete("/{assembly_guid}", status_code=204)
async def soft_delete_assembly(
    assembly_guid: UUID,
    session: AsyncSession = Depends(get_tenant_session),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Soft delete an assembly by GUID.
    - Sets `is_active` to False and `deleted_at` to the current timestamp.
    - Cascades soft delete to all active children (pieces, articles).
    - Returns 204 No Content on success.
    """
    stmt = select(Assembly).where(Assembly.guid == assembly_guid)
    stmt = add_tenant_filter(stmt, current_user["company_guid"], current_user["role"])
    result = await session.execute(stmt)
    assembly = result.scalar_one_or_none()
    if not assembly:
        raise HTTPException(status_code=404, detail="Assembly not found or forbidden")
    await SyncService.cascade_soft_delete('assembly', assembly_guid, session)
    return None 

@router.post("/{assembly_guid}/restore", status_code=204)
async def restore_assembly(
    assembly_guid: UUID,
    session: AsyncSession = Depends(get_tenant_session),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Restore a soft-deleted assembly by GUID.
    - Sets `is_active` to True and `deleted_at` to NULL for the assembly.
    - Restores only children with `deleted_at` matching the parent's original `deleted_at`.
    - Returns 204 No Content on success.
    """
    stmt = select(Assembly).where(Assembly.guid == assembly_guid)
    stmt = add_tenant_filter(stmt, current_user["company_guid"], current_user["role"])
    result = await session.execute(stmt)
    assembly = result.scalar_one_or_none()
    if not assembly:
        raise HTTPException(status_code=404, detail="Assembly not found or forbidden")
    await SyncService.cascade_restore('assembly', assembly_guid, session)
    return None 