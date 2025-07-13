from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import get_session
from app.models.article import Article
from app.schemas.sync.articles import ArticleResponse, ArticleDetail
from app.core.deps import get_current_user, CurrentUser, get_tenant_session
from app.models.enums import UserRole
from app.core.tenant_utils import add_tenant_filter, verify_tenant_access, validate_company_access
from app.models.project import Project
from app.models.component import Component
from app.services.sync_service import SyncService

router = APIRouter()

@router.get("", response_model=List[ArticleResponse])
async def list_articles(
    request: Request,
    project_guid: Optional[UUID] = None,
    component_guid: Optional[UUID] = None,
    company_guid: Optional[UUID] = None,
    include_inactive: bool = Query(False, description="Include soft-deleted articles"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_tenant_session),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    List articles, with optional filtering by project, component, or company.
    - By default, only active (not soft-deleted) articles are returned.
    - Set `include_inactive=true` to include soft-deleted articles (where is_active is False).
    - Each article includes `is_active` and `deleted_at` fields to indicate soft deletion status.
    """
    # Validate company access if company_guid parameter is provided
    if company_guid:
        await validate_company_access(request, company_guid, current_user.tenant, current_user.role)

    # Determine the tenant_id to use for filtering based on role and provided company_guid
    filter_tenant_id = str(company_guid) if company_guid and current_user.role == UserRole.SYSTEM_ADMIN else current_user.tenant

    # Create base query
    query = select(Article)

    # Validate and apply project_guid filter
    if project_guid:
        project_stmt = select(Project).where(Project.guid == project_guid)
        # SystemAdmin uses filter_tenant_id which could be different from current_user.tenant
        # Non-SystemAdmins implicitly use current_user.tenant
        project_stmt = add_tenant_filter(project_stmt, filter_tenant_id if current_user.role == UserRole.SYSTEM_ADMIN else current_user.tenant, current_user.role)
        project_result = await session.execute(project_stmt)
        project = project_result.scalar_one_or_none()
        if not project:
            raise HTTPException(status_code=404, detail=f"Project with GUID {project_guid} not found or not accessible.")
        query = query.where(Article.project_guid == project_guid)

    # Validate and apply component_guid filter
    if component_guid:
        component_stmt = select(Component).where(Component.guid == component_guid)
        component_stmt = add_tenant_filter(component_stmt, filter_tenant_id if current_user.role == UserRole.SYSTEM_ADMIN else current_user.tenant, current_user.role)
        component_result = await session.execute(component_stmt)
        component = component_result.scalar_one_or_none()
        if not component:
            raise HTTPException(status_code=404, detail=f"Component with GUID {component_guid} not found or not accessible.")
        
        # If project_guid was also provided, ensure component belongs to that project
        if project_guid and component.project_guid != project_guid:
            raise HTTPException(status_code=400, detail=f"Component {component_guid} does not belong to project {project_guid}.")
        query = query.where(Article.component_guid == component_guid)
    
    # Add tenant filtering for articles themselves
    query = add_tenant_filter(query, filter_tenant_id, current_user.role)
    
    # Add pagination
    query = query.limit(limit).offset(offset)
    
    # Execute query
    result = await session.execute(query)
    articles = result.scalars().all()
    
    # Convert to response model
    return [ArticleResponse.model_validate(article) for article in articles]

@router.get("/{article_guid}", response_model=ArticleDetail)
async def get_article(
    article_guid: UUID,
    include_inactive: bool = Query(False, description="Include soft-deleted article"),
    session: AsyncSession = Depends(get_tenant_session),
    current_user: CurrentUser = Depends(get_current_user)
):
    """Get a specific article by GUID."""
    # Create base query 
    stmt = select(Article).where(Article.guid == article_guid)
    
    # Add explicit tenant filtering as defense-in-depth
    stmt = add_tenant_filter(stmt, current_user.tenant, current_user.role)
    
    # PATCH: Only filter for active if include_inactive is False
    if not include_inactive:
        stmt = stmt.where(Article.is_active == True)
    
    # Execute query
    result = await session.execute(stmt)
    article = result.scalar_one_or_none()
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    if current_user.role != UserRole.SYSTEM_ADMIN and str(article.company_guid) != str(current_user.tenant):
        raise HTTPException(status_code=403, detail="Access to this article is forbidden.")
    
    # Build response dict explicitly to avoid getattr/annotation issues
    article_data = {
        "guid": article.guid,
        "code": article.code,
        "project_guid": article.project_guid,
        "component_guid": article.component_guid,
        "designation": article.designation,
        "company_guid": article.company_guid,
        "created_at": article.created_at,
        "updated_at": getattr(article, "updated_at", None),
        "is_active": article.is_active,
        "deleted_at": article.deleted_at,
        # Add all other optional fields as needed
    }
    # Add all other ArticleDetail fields if present
    for key in ArticleDetail.__annotations__.keys():
        if key not in article_data:
            article_data[key] = getattr(article, key, None)
    
    # Check for missing required (non-Optional) fields
    required_fields = [
        "guid", "code", "project_guid", "component_guid", "company_guid", "created_at"
    ]
    missing = [f for f in required_fields if article_data.get(f) is None]
    if missing:
        raise HTTPException(status_code=500, detail=f"Article missing required fields: {missing}")

    return ArticleDetail.model_validate(article_data)

@router.delete("/{article_guid}", status_code=204)
async def soft_delete_article(
    article_guid: UUID,
    session: AsyncSession = Depends(get_tenant_session),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Soft delete an article by GUID.
    - Sets `is_active` to False and `deleted_at` to the current timestamp.
    - Returns 204 No Content on success.
    """
    stmt = select(Article).where(Article.guid == article_guid)
    stmt = add_tenant_filter(stmt, current_user.tenant, current_user.role)
    result = await session.execute(stmt)
    article = result.scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found or forbidden")
    await SyncService.cascade_soft_delete('article', article_guid, session)
    return None

@router.post("/{article_guid}/restore", status_code=204)
async def restore_article(
    article_guid: UUID,
    session: AsyncSession = Depends(get_tenant_session),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Restore a soft-deleted article by GUID.
    - Sets `is_active` to True and `deleted_at` to NULL for the article.
    - Returns 204 No Content on success.
    - Restores only children with `deleted_at` matching the parent's original `deleted_at` (if any).
    """
    stmt = select(Article).where(Article.guid == article_guid)
    stmt = add_tenant_filter(stmt, current_user.tenant, current_user.role)
    result = await session.execute(stmt)
    article = result.scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found or forbidden")
    await SyncService.cascade_restore('article', article_guid, session)
    return None 