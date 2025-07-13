from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import ValidationError

from app.models.base import get_session
from app.core.deps import get_current_user, CurrentUser, get_tenant_session
from app.core.rbac import require_scopes
from app.schemas.sync.main import (
    ProjectBulkInsert, ComponentBulkInsert, AssemblyBulkInsert, 
    PieceBulkInsert, ArticleBulkInsert, SyncResult
)
from app.services.sync_service import SyncService
from app.models.enums import UserRole
from app.core.tenant_utils import verify_tenant_access, validate_company_access

router = APIRouter(
    prefix="/sync",
    tags=["synchronization"],
    responses={
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        422: {"description": "Validation Error"},
    }
)

@router.post("/projects", response_model=SyncResult, dependencies=[Depends(require_scopes("sync:write"))])
async def sync_projects(
    data: ProjectBulkInsert,
    request: Request,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_tenant_session)
):
    """
    Bulk insert or update projects from RaConnect.
    
    Requires API key with sync:write scope or SystemAdmin/CompanyAdmin/Integration role.
    """
    # Verify all projects belong to the user's company before processing the data
    # This ensures company validation happens before other validation errors
    for project in data.projects:
        await validate_company_access(
            request, 
            project.company_guid, 
            current_user.tenant, 
            current_user.role
        )
    
    # Perform bulk upsert using service
    result = await SyncService.sync_projects(data.projects, current_user.tenant, session)
    
    return SyncResult(**result)

@router.post("/components", response_model=SyncResult, dependencies=[Depends(require_scopes("sync:write"))])
async def sync_components(
    data: ComponentBulkInsert,
    request: Request,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_tenant_session)
):
    """
    Bulk insert or update components from RaConnect.
    
    Requires API key with sync:write scope or SystemAdmin/CompanyAdmin/Integration role.
    """
    # Verify all components belong to the user's company
    for component in data.components:
        await validate_company_access(
            request, 
            component.company_guid, 
            current_user.tenant, 
            current_user.role
        )
    
    # Perform bulk upsert using service
    result = await SyncService.sync_components(data.components, current_user.tenant, session)
    
    return SyncResult(**result)

@router.post("/assemblies", response_model=SyncResult, dependencies=[Depends(require_scopes("sync:write"))])
async def sync_assemblies(
    data: AssemblyBulkInsert,
    request: Request,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_tenant_session)
):
    """
    Bulk insert or update assemblies from RaConnect.
    
    Requires API key with sync:write scope or SystemAdmin/CompanyAdmin/Integration role.
    """
    # Verify all assemblies belong to the user's company
    for assembly in data.assemblies:
        await validate_company_access(
            request, 
            assembly.company_guid, 
            current_user.tenant, 
            current_user.role
        )
    
    # Perform bulk upsert using service
    result = await SyncService.sync_assemblies(data.assemblies, current_user.tenant, session)
    
    return SyncResult(**result)

@router.post("/pieces", response_model=SyncResult, dependencies=[Depends(require_scopes("sync:write"))])
async def sync_pieces(
    data: PieceBulkInsert,
    request: Request,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_tenant_session)
):
    """
    Bulk insert or update pieces from RaConnect.
    
    Requires API key with sync:write scope or SystemAdmin/CompanyAdmin/Integration role.
    Maximum of 1000 pieces per request due to size.
    """
    # Check if batch size is too large
    if len(data.pieces) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum batch size is 1000 pieces"
        )
    
    # Verify all pieces belong to the user's company
    for piece in data.pieces:
        await validate_company_access(
            request, 
            piece.company_guid, 
            current_user.tenant, 
            current_user.role
        )
    
    # Perform bulk upsert using service
    result = await SyncService.sync_pieces(data.pieces, current_user.tenant, session)
    
    return SyncResult(**result)

@router.post("/articles", response_model=SyncResult, dependencies=[Depends(require_scopes("sync:write"))])
async def sync_articles(
    data: ArticleBulkInsert,
    request: Request,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_tenant_session)
):
    """
    Bulk insert or update articles from RaConnect.
    
    Requires API key with sync:write scope or SystemAdmin/CompanyAdmin/Integration role.
    """
    # Verify all articles belong to the user's company
    for article in data.articles:
        await validate_company_access(
            request, 
            article.company_guid, 
            current_user.tenant, 
            current_user.role
        )
    
    # Perform bulk upsert using service
    result = await SyncService.sync_articles(data.articles, current_user.tenant, session)
    
    return SyncResult(**result) 