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

router = APIRouter()

@router.get("", response_model=List[ProjectResponse])
async def list_projects(
    request: Request,
    company_guid: Optional[UUID] = None,
    code: Optional[str] = None,
    search: Optional[str] = None,
    session: AsyncSession = Depends(get_tenant_session),
    current_user: CurrentUser = Depends(get_current_user)
):
    """List all projects for the current company."""
    # Validate company access if company_guid parameter is provided
    if company_guid:
        await validate_company_access(request, company_guid, current_user.tenant, current_user.role)
    
    # Create base query
    query = select(Project)
    
    # Add filter by code if provided
    if code:
        query = query.filter(Project.code == code)
    
    # Add search functionality if provided
    if search:
        query = query.filter(Project.code.ilike(f"%{search}%"))
    
    # Add explicit tenant filtering as defense-in-depth
    query = add_tenant_filter(query, current_user.tenant, current_user.role)
    
    # Execute query
    result = await session.execute(query)
    projects = result.scalars().all()
    
    # Updated to use model_validate instead of from_orm
    return [ProjectResponse.model_validate(project) for project in projects]

@router.get("/{project_guid}", response_model=ProjectDetail)
async def get_project(
    project_guid: UUID,
    session: AsyncSession = Depends(get_tenant_session),
    current_user: CurrentUser = Depends(get_current_user)
):
    """Get a specific project by GUID."""
    # Create base query 
    stmt = select(Project).where(Project.guid == project_guid)
    
    # Add explicit tenant filtering as defense-in-depth
    stmt = add_tenant_filter(stmt, current_user.tenant, current_user.role)
    
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
        "piece_count": piece_count
    }
    
    # Use model_validate
    return ProjectDetail.model_validate(project_data) 