from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from app.core.database import get_db
from app.core.deps import get_current_user, require_roles, tenant_middleware
from app.models.enums import Role
from app.schemas.raconnect import (
    PieceCreate, ProjectCreate, ComponentCreate, AssemblyCreate, ArticleCreate, SyncResponse
)
from app.repositories.sync import (
    bulk_upsert_pieces, bulk_upsert_projects, bulk_upsert_components, 
    bulk_upsert_assemblies, bulk_upsert_articles
)

MAX_SYNC_CHUNK_SIZE = 1000

router = APIRouter(prefix="/sync", tags=["sync"])

@router.post(
    "/pieces", 
    response_model=SyncResponse, 
    dependencies=[Depends(require_roles(Role.COMPANY_ADMIN, Role.INTEGRATION))]
)
async def sync_pieces(
    pieces: List[PieceCreate] = Body(..., max_length=MAX_SYNC_CHUNK_SIZE),
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(tenant_middleware)
):
    """Bulk upsert pieces. Limited to 1000 pieces per request."""
    if len(pieces) > MAX_SYNC_CHUNK_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Payload too large. Maximum {MAX_SYNC_CHUNK_SIZE} pieces allowed per request."
        )
        
    # Get tenant ID from authenticated user
    tenant_id = current_user["company_guid"]
    print(f"Syncing pieces for tenant: {tenant_id}")
    print(f"User role: {current_user['role']}")
    
    # Validate or set company_guid for each piece
    for p in pieces:
        if p.company_guid and p.company_guid != tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Payload contains pieces for a different company."
            )
        p.company_guid = tenant_id  # Ensure company_guid is set

    try:
        result = await bulk_upsert_pieces(db, pieces, tenant_id)
        return result
    except Exception as e:
        print(f"Error in sync_pieces: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing piece sync request"
        )

@router.post(
    "/projects", 
    response_model=SyncResponse, 
    dependencies=[Depends(require_roles(Role.COMPANY_ADMIN, Role.INTEGRATION))]
)
async def sync_projects(
    projects: List[ProjectCreate] = Body(..., max_length=MAX_SYNC_CHUNK_SIZE),
    db: AsyncSession = Depends(get_db), 
    current_user: Dict[str, Any] = Depends(tenant_middleware)
):
    """Bulk upsert projects. Limited to 1000 projects per request."""
    if len(projects) > MAX_SYNC_CHUNK_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Payload too large. Maximum {MAX_SYNC_CHUNK_SIZE} projects allowed per request."
        )
        
    # Get tenant ID from authenticated user
    tenant_id = current_user["company_guid"]
    print(f"Syncing projects for tenant: {tenant_id}")
    
    # Validate or set company_guid for each project
    for p in projects:
        if p.company_guid and p.company_guid != tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Payload contains projects for a different company."
            )
        p.company_guid = tenant_id  # Ensure company_guid is set

    try:
        result = await bulk_upsert_projects(db, projects, tenant_id)
        return result
    except Exception as e:
        print(f"Error in sync_projects: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing project sync request"
        )

@router.post(
    "/components", 
    response_model=SyncResponse, 
    dependencies=[Depends(require_roles(Role.COMPANY_ADMIN, Role.INTEGRATION))]
)
async def sync_components(
    components: List[ComponentCreate] = Body(..., max_length=MAX_SYNC_CHUNK_SIZE),
    db: AsyncSession = Depends(get_db), 
    current_user: Dict[str, Any] = Depends(tenant_middleware)
):
    """Bulk upsert components. Limited to 1000 components per request."""
    if len(components) > MAX_SYNC_CHUNK_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Payload too large. Maximum {MAX_SYNC_CHUNK_SIZE} components allowed per request."
        )
        
    # Get tenant ID from authenticated user
    tenant_id = current_user["company_guid"]
    print(f"Syncing components for tenant: {tenant_id}")
    
    # Validate or set company_guid for each component
    for c in components:
        if c.company_guid and c.company_guid != tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Payload contains components for a different company."
            )
        c.company_guid = tenant_id  # Ensure company_guid is set

    try:
        result = await bulk_upsert_components(db, components, tenant_id)
        return result
    except Exception as e:
        print(f"Error in sync_components: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing component sync request"
        )

@router.post(
    "/assemblies", 
    response_model=SyncResponse, 
    dependencies=[Depends(require_roles(Role.COMPANY_ADMIN, Role.INTEGRATION))]
)
async def sync_assemblies(
    assemblies: List[AssemblyCreate] = Body(..., max_length=MAX_SYNC_CHUNK_SIZE),
    db: AsyncSession = Depends(get_db), 
    current_user: Dict[str, Any] = Depends(tenant_middleware)
):
    """Bulk upsert assemblies. Limited to 1000 assemblies per request."""
    if len(assemblies) > MAX_SYNC_CHUNK_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Payload too large. Maximum {MAX_SYNC_CHUNK_SIZE} assemblies allowed per request."
        )
        
    # Get tenant ID from authenticated user
    tenant_id = current_user["company_guid"]
    print(f"Syncing assemblies for tenant: {tenant_id}")
    
    # Validate or set company_guid for each assembly
    for a in assemblies:
        if a.company_guid and a.company_guid != tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Payload contains assemblies for a different company."
            )
        a.company_guid = tenant_id  # Ensure company_guid is set

    try:
        result = await bulk_upsert_assemblies(db, assemblies, tenant_id)
        return result
    except Exception as e:
        print(f"Error in sync_assemblies: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing assembly sync request"
        )

@router.post(
    "/articles", 
    response_model=SyncResponse, 
    dependencies=[Depends(require_roles(Role.COMPANY_ADMIN, Role.INTEGRATION))]
)
async def sync_articles(
    articles: List[ArticleCreate] = Body(..., max_length=MAX_SYNC_CHUNK_SIZE),
    db: AsyncSession = Depends(get_db), 
    current_user: Dict[str, Any] = Depends(tenant_middleware)
):
    """Bulk upsert articles. Limited to 1000 articles per request."""
    if len(articles) > MAX_SYNC_CHUNK_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Payload too large. Maximum {MAX_SYNC_CHUNK_SIZE} articles allowed per request."
        )
        
    # Get tenant ID from authenticated user
    tenant_id = current_user["company_guid"]
    print(f"Syncing articles for tenant: {tenant_id}")
    
    # Validate or set company_guid for each article
    for a in articles:
        if a.company_guid and a.company_guid != tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Payload contains articles for a different company."
            )
        a.company_guid = tenant_id  # Ensure company_guid is set

    try:
        result = await bulk_upsert_articles(db, articles, tenant_id)
        return result
    except Exception as e:
        print(f"Error in sync_articles: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing article sync request"
        ) 