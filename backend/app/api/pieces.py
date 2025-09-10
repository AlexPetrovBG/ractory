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
from app.services.sync_service import SyncService

router = APIRouter()

@router.get("", response_model=List[PieceResponse])
async def list_pieces(
    request: Request,
    project_guid: Optional[UUID] = None,
    component_guid: Optional[UUID] = None,
    assembly_guid: Optional[UUID] = None,
    company_guid: Optional[UUID] = None,
    include_inactive: bool = Query(False, description="Include soft-deleted pieces"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_tenant_session),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    List pieces, optionally filtered by project, component, assembly, or company.
    - By default, only active (not soft-deleted) pieces are returned.
    - Set `include_inactive=true` to include soft-deleted pieces (where is_active is False).
    - Each piece includes `is_active` and `deleted_at` fields to indicate soft deletion status.
    """
    # Validate company access if company_guid parameter is provided
    if company_guid:
        await validate_company_access(request, company_guid, current_user["company_guid"], current_user["role"])

    # Determine the tenant_id to use for filtering based on role and provided company_guid
    filter_tenant_id = str(company_guid) if company_guid and current_user["role"] == UserRole.SYSTEM_ADMIN else current_user["company_guid"]
    effective_tenant_check_id = filter_tenant_id if current_user["role"] == UserRole.SYSTEM_ADMIN else current_user["company_guid"]

    # Create base query
    query = select(Piece)
    
    # Validate and apply project_guid filter
    if project_guid:
        project_stmt = select(Project).where(Project.guid == project_guid)
        project_stmt = add_tenant_filter(project_stmt, effective_tenant_check_id, current_user["role"])
        project_result = await session.execute(project_stmt)
        project = project_result.scalar_one_or_none()
        if not project:
            raise HTTPException(status_code=404, detail=f"Project with GUID {project_guid} not found or not accessible.")
        query = query.where(Piece.project_guid == project_guid)

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
        query = query.where(Piece.component_guid == component_guid)

    # Validate and apply assembly_guid filter
    if assembly_guid:
        assembly_stmt = select(Assembly).where(Assembly.guid == assembly_guid)
        assembly_stmt = add_tenant_filter(assembly_stmt, effective_tenant_check_id, current_user["role"])
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
    query = add_tenant_filter(query, filter_tenant_id, current_user["role"])
    
    # Add pagination
    if not include_inactive:
        query = query.where(Piece.is_active == True)
    query = query.limit(limit).offset(offset)
    
    # Execute query
    result = await session.execute(query)
    pieces = result.scalars().all()
    
    # Convert to response model
    return [PieceResponse.model_validate(piece) for piece in pieces]

@router.get("/{piece_guid}", response_model=PieceDetail)
async def get_piece(
    piece_guid: UUID,
    include_inactive: bool = Query(False, description="Include soft-deleted piece"),
    session: AsyncSession = Depends(get_tenant_session),
    current_user: CurrentUser = Depends(get_current_user)
):
    """Get a specific piece by GUID."""
    # Create base query 
    stmt = select(Piece).where(Piece.guid == piece_guid)
    
    # Add explicit tenant filtering as defense-in-depth
    stmt = add_tenant_filter(stmt, current_user["company_guid"], current_user["role"])
    
    # PATCH: Only filter for active if include_inactive is False
    if not include_inactive:
        stmt = stmt.where(Piece.is_active == True)
    
    # Execute query
    result = await session.execute(stmt)
    piece = result.scalar_one_or_none()
    
    if not piece:
        raise HTTPException(status_code=404, detail="Piece not found")

    if current_user["role"] != UserRole.SYSTEM_ADMIN and str(piece.company_guid) != str(current_user["company_guid"]):
        raise HTTPException(status_code=403, detail="Access to this piece is forbidden.")
    
    # Build response dict explicitly to avoid getattr/annotation issues
    piece_data = {
        "guid": piece.guid,
        "piece_id": piece.piece_id,
        "project_guid": piece.project_guid,
        "component_guid": piece.component_guid,
        "assembly_guid": piece.assembly_guid,
        "barcode": piece.barcode,
        "outer_length": piece.outer_length,
        "angle_left": piece.angle_left,
        "angle_right": piece.angle_right,
        "company_guid": piece.company_guid,
        "created_at": piece.created_at,
        "updated_at": getattr(piece, "updated_at", None),
        "is_active": piece.is_active,
        "deleted_at": piece.deleted_at,
        # Add all other optional fields as needed
    }
    # Add all other PieceDetail fields if present
    for key in PieceDetail.__annotations__.keys():
        if key not in piece_data:
            piece_data[key] = getattr(piece, key, None)
    
    # Check for missing required (non-Optional) fields
    required_fields = [
        "guid", "piece_id", "project_guid", "component_guid", "company_guid", "created_at"
    ]
    missing = [f for f in required_fields if piece_data.get(f) is None]
    if missing:
        raise HTTPException(status_code=500, detail=f"Piece missing required fields: {missing}")

    return PieceDetail.model_validate(piece_data)

@router.delete("/{piece_guid}", status_code=204)
async def soft_delete_piece(
    piece_guid: UUID,
    session: AsyncSession = Depends(get_tenant_session),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Soft delete a piece by GUID.
    - Sets `is_active` to False and `deleted_at` to the current timestamp.
    - Returns 204 No Content on success.
    - Cascades soft delete to all active children (if any).
    """
    stmt = select(Piece).where(Piece.guid == piece_guid)
    stmt = add_tenant_filter(stmt, current_user["company_guid"], current_user["role"])
    result = await session.execute(stmt)
    piece = result.scalar_one_or_none()
    if not piece:
        raise HTTPException(status_code=404, detail="Piece not found or forbidden")
    await SyncService.cascade_soft_delete('piece', piece_guid, session)
    return None

@router.post("/{piece_guid}/restore", status_code=204)
async def restore_piece(
    piece_guid: UUID,
    session: AsyncSession = Depends(get_tenant_session),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Restore a soft-deleted piece by GUID.
    - Sets `is_active` to True and `deleted_at` to NULL for the piece.
    - Returns 204 No Content on success.
    - Restores only children with `deleted_at` matching the parent's original `deleted_at` (if any).
    """
    stmt = select(Piece).where(Piece.guid == piece_guid)
    stmt = add_tenant_filter(stmt, current_user["company_guid"], current_user["role"])
    result = await session.execute(stmt)
    piece = result.scalar_one_or_none()
    if not piece:
        raise HTTPException(status_code=404, detail="Piece not found or forbidden")
    await SyncService.cascade_restore('piece', piece_guid, session)
    return None 