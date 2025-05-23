from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import get_session
from app.models.piece import Piece
from app.schemas.sync.pieces import PieceResponse, PieceDetail
from app.core.deps import get_current_user, CurrentUser, get_tenant_session
from app.models.enums import UserRole
from app.core.tenant_utils import add_tenant_filter, verify_tenant_access, validate_company_access
from app.models.project import Project
from app.models.component import Component
from app.models.assembly import Assembly

router = APIRouter()

@router.get("", response_model=List[PieceResponse])
async def list_pieces(
    request: Request,
    project_guid: Optional[UUID] = None,
    component_guid: Optional[UUID] = None,
    assembly_guid: Optional[UUID] = None,
    company_guid: Optional[UUID] = None,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_tenant_session),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    List pieces, optionally filtered by project, component, assembly, or company.
    Supports pagination.
    """
    # Validate company access if company_guid parameter is provided
    if company_guid:
        await validate_company_access(request, company_guid, current_user.tenant, current_user.role)

    # Determine the tenant_id to use for filtering based on role and provided company_guid
    filter_tenant_id = str(company_guid) if company_guid and current_user.role == UserRole.SYSTEM_ADMIN else current_user.tenant
    effective_tenant_check_id = filter_tenant_id if current_user.role == UserRole.SYSTEM_ADMIN else current_user.tenant

    # Create base query
    query = select(Piece)
    
    # Validate and apply project_guid filter
    if project_guid:
        project_stmt = select(Project).where(Project.guid == project_guid)
        project_stmt = add_tenant_filter(project_stmt, effective_tenant_check_id, current_user.role)
        project_result = await session.execute(project_stmt)
        project = project_result.scalar_one_or_none()
        if not project:
            raise HTTPException(status_code=404, detail=f"Project with GUID {project_guid} not found or not accessible.")
        query = query.where(Piece.project_guid == project_guid)

    # Validate and apply component_guid filter
    if component_guid:
        component_stmt = select(Component).where(Component.guid == component_guid)
        component_stmt = add_tenant_filter(component_stmt, effective_tenant_check_id, current_user.role)
        component_result = await session.execute(component_stmt)
        component = component_result.scalar_one_or_none()
        if not component:
            raise HTTPException(status_code=404, detail=f"Component with GUID {component_guid} not found or not accessible.")
        if project_guid and component.project_guid != project_guid: # Check consistency if project_guid also given
            raise HTTPException(status_code=400, detail=f"Component {component_guid} does not belong to project {project_guid}.")
        query = query.where(Piece.component_guid == component_guid)

    # Validate and apply assembly_guid filter
    if assembly_guid:
        assembly_stmt = select(Assembly).where(Assembly.guid == assembly_guid)
        assembly_stmt = add_tenant_filter(assembly_stmt, effective_tenant_check_id, current_user.role)
        assembly_result = await session.execute(assembly_stmt)
        assembly = assembly_result.scalar_one_or_none()
        if not assembly:
            raise HTTPException(status_code=404, detail=f"Assembly with GUID {assembly_guid} not found or not accessible.")
        if component_guid and assembly.component_guid != component_guid: # Check consistency
            raise HTTPException(status_code=400, detail=f"Assembly {assembly_guid} does not belong to component {component_guid}.")
        if project_guid and assembly.project_guid != project_guid: # Check consistency
            raise HTTPException(status_code=400, detail=f"Assembly {assembly_guid} does not belong to project {project_guid}.")
        query = query.where(Piece.assembly_guid == assembly_guid)
    
    # Add tenant filtering for pieces themselves
    query = add_tenant_filter(query, filter_tenant_id, current_user.role)
    
    # Add pagination
    query = query.limit(limit).offset(offset)
    
    # Execute query
    result = await session.execute(query)
    pieces = result.scalars().all()
    
    # Convert to response model
    return [PieceResponse.model_validate(piece) for piece in pieces]

@router.get("/{piece_guid}", response_model=PieceDetail)
async def get_piece(
    piece_guid: UUID,
    session: AsyncSession = Depends(get_tenant_session),
    current_user: CurrentUser = Depends(get_current_user)
):
    """Get a specific piece by GUID."""
    # Create base query 
    stmt = select(Piece).where(Piece.guid == piece_guid)
    
    # Add explicit tenant filtering as defense-in-depth
    stmt = add_tenant_filter(stmt, current_user.tenant, current_user.role)
    
    # Execute query
    result = await session.execute(stmt)
    piece = result.scalar_one_or_none()
    
    if not piece:
        raise HTTPException(status_code=404, detail="Piece not found")

    # ADD THIS: Explicit company check for non-SystemAdmins
    if current_user.role != UserRole.SYSTEM_ADMIN and str(piece.company_guid) != str(current_user.tenant):
        # This case should ideally not be hit if RLS and add_tenant_filter work,
        # but it's a strong safeguard.
        raise HTTPException(status_code=403, detail="Access to this piece is forbidden.")
    # END ADD
    
    # Use model_validate
    return PieceDetail.model_validate(piece) 