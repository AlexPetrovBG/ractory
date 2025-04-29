from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.models.base import get_session
from app.core.deps import get_current_user, CurrentUser, get_tenant_session
from app.core.rbac import require_scopes
from app.schemas.sync.main import (
    ProjectBulkInsert, ComponentBulkInsert, AssemblyBulkInsert, 
    PieceBulkInsert, ArticleBulkInsert, SyncResult
)
from app.services.sync_service import SyncService
from app.models.enums import UserRole

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
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_tenant_session)
):
    """
    Bulk insert or update projects from RaConnect.
    
    Requires API key with sync:write scope or SystemAdmin/CompanyAdmin/Integration role.
    """
    # Perform bulk upsert using service
    result = await SyncService.sync_projects(data.projects, current_user.tenant, session)
    
    return SyncResult(**result)

@router.post("/components", response_model=SyncResult, dependencies=[Depends(require_scopes("sync:write"))])
async def sync_components(
    data: ComponentBulkInsert,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_tenant_session)
):
    """
    Bulk insert or update components from RaConnect.
    
    Requires API key with sync:write scope or SystemAdmin/CompanyAdmin/Integration role.
    """
    # Perform bulk upsert using service
    result = await SyncService.upsert_components(data.components, current_user.tenant, session)
    
    return SyncResult(**result)

@router.post("/assemblies", response_model=SyncResult, dependencies=[Depends(require_scopes("sync:write"))])
async def sync_assemblies(
    data: AssemblyBulkInsert,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_tenant_session)
):
    """
    Bulk insert or update assemblies from RaConnect.
    
    Requires API key with sync:write scope or SystemAdmin/CompanyAdmin/Integration role.
    """
    # Perform bulk upsert using service
    result = await SyncService.upsert_assemblies(data.assemblies, current_user.tenant, session)
    
    return SyncResult(**result)

@router.post("/pieces", response_model=SyncResult, dependencies=[Depends(require_scopes("sync:write"))])
async def sync_pieces(
    data: PieceBulkInsert,
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
    
    # Perform bulk upsert using service
    result = await SyncService.upsert_pieces(data.pieces, current_user.tenant, session)
    
    return SyncResult(**result)

@router.post("/articles", response_model=SyncResult, dependencies=[Depends(require_scopes("sync:write"))])
async def sync_articles(
    data: ArticleBulkInsert,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_tenant_session)
):
    """
    Bulk insert or update articles from RaConnect.
    
    Requires API key with sync:write scope or SystemAdmin/CompanyAdmin/Integration role.
    """
    # Perform bulk upsert using service
    result = await SyncService.upsert_articles(data.articles, current_user.tenant, session)
    
    return SyncResult(**result) 