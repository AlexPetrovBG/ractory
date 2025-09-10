from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...models.base import get_session
from ...models.project import Project
from ...models.component import Component
from ...models.piece import Piece
from ...schemas.sync.projects import ProjectResponse, ProjectDetail
from ...core.deps import get_current_user, CurrentUser, get_tenant_session
from ...models.enums import UserRole
from ...core.tenant_utils import add_tenant_filter, validate_company_access
from ...services.sync_service import SyncService

router = APIRouter()

@router.get("", response_model=List[ProjectResponse])
async def list_projects(
    request: Request,
    company_guid: Optional[UUID] = None,
    code: Optional[str] = None,
    search: Optional[str] = None,
    include_inactive: bool = Query(False, description="Include soft-deleted projects"),
    session: AsyncSession = Depends(get_tenant_session),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    List all projects for the current company.
    - By default, only active (not soft-deleted) projects are returned.
    - Set `include_inactive=true` to include soft-deleted projects (where is_active is False).
    - Each project includes `is_active` and `deleted_at` fields to indicate soft deletion status.
    """
    # Validate company access if company_guid parameter is provided
    if company_guid:
        await validate_company_access(request, company_guid, current_user["company_guid"], current_user["role"])
    
    # Create base query
    query = select(Project)
    
    # If company_guid is provided by any user (including SystemAdmin),
    # it should be used as the primary filter.
    if company_guid:
        query = query.filter(Project.company_guid == company_guid)
    else:
        # If no specific company_guid is given in the request,
        # then apply the standard tenant filtering (which allows SystemAdmin to see all
        # or regular users to see their own company's projects).
        query = add_tenant_filter(query, current_user["company_guid"], current_user["role"])
    
    # Add filter by code if provided
    if code:
        query = query.filter(Project.code == code)
    
    # Add search functionality if provided
    if search:
        query = query.filter(Project.code.ilike(f"%{search}%"))
    
    # Add explicit tenant filtering as defense-in-depth
    # query = add_tenant_filter(query, current_user["company_guid"], current_user["role"]) # This line is now handled by the conditional logic above
    
    # Add filter for active projects if include_inactive is False
    if not include_inactive:
        query = query.where(Project.is_active == True)
    
    # Execute query
    result = await session.execute(query)
    projects = result.scalars().all()
    
    # Updated to use model_validate instead of from_orm
    return [ProjectResponse.model_validate(project) for project in projects]

@router.get("/{project_guid}", response_model=ProjectDetail)
async def get_project(
    project_guid: UUID,
    include_inactive: bool = Query(False, description="Include soft-deleted project"),
    session: AsyncSession = Depends(get_tenant_session),
    current_user: CurrentUser = Depends(get_current_user)
):
    """Get a specific project by GUID."""
    # Create base query 
    stmt = select(Project).where(Project.guid == project_guid)
    
    # Add explicit tenant filtering as defense-in-depth
    stmt = add_tenant_filter(stmt, current_user["company_guid"], current_user["role"])
    
    # PATCH: Only filter for active if include_inactive is False
    if not include_inactive:
        stmt = stmt.where(Project.is_active == True)
    
    # Execute query
    result = await session.execute(stmt)
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Get component and piece counts
    component_count = 0  # Replace with actual count logic
    piece_count = 0      # Replace with actual count logic
    
    # Create project data dictionary directly from the project attributes
    project_data = {
        "code": project.code,
        "guid": project.guid,
        "company_guid": project.company_guid,
        "created_at": project.created_at,
        "updated_at": project.updated_at,
        "due_date": project.due_date,
        "in_production": project.in_production,
        "company_name": project.company_name,
        "component_count": component_count,
        "piece_count": piece_count,
        "is_active": project.is_active,
        "deleted_at": project.deleted_at
    }
    
    # Use model_validate
    return ProjectDetail.model_validate(project_data)

@router.delete("/{project_guid}", status_code=204)
async def soft_delete_project(
    project_guid: UUID,
    session: AsyncSession = Depends(get_tenant_session),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Soft delete a project by GUID.
    - Sets `is_active` to False and `deleted_at` to the current timestamp.
    - Cascades soft delete to all active children (components, assemblies, pieces, articles).
    - Returns 204 No Content on success.
    """
    # Check project exists and belongs to tenant
    stmt = select(Project).where(Project.guid == project_guid)
    stmt = add_tenant_filter(stmt, current_user["company_guid"], current_user["role"])
    result = await session.execute(stmt)
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or forbidden")
    await SyncService.cascade_soft_delete('project', project_guid, session)
    return None

@router.post("/{project_guid}/restore", status_code=204)
async def restore_project(
    project_guid: UUID,
    session: AsyncSession = Depends(get_tenant_session),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Restore a soft-deleted project by GUID.
    - Sets `is_active` to True and `deleted_at` to NULL for the project.
    - Restores only children with `deleted_at` matching the parent's original `deleted_at`.
    - Returns 204 No Content on success.
    """
    stmt = select(Project).where(Project.guid == project_guid)
    stmt = add_tenant_filter(stmt, current_user["company_guid"], current_user["role"])
    result = await session.execute(stmt)
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or forbidden")
    await SyncService.cascade_restore('project', project_guid, session)
    return None 