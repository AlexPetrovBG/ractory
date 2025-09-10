from fastapi import APIRouter, Depends, HTTPException, Query, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
import uuid
from datetime import datetime

from app.core.deps import get_current_user, CurrentUser, get_tenant_session
from app.core.rbac import require_company_admin, require_project_manager
from app.services.workflow_service import WorkflowService
from app.schemas.workflow import (
    WorkflowCreate, WorkflowResponse, WorkflowList, 
    WorkflowFilter, WorkflowStatistics
)
from app.models.enums import WorkflowActionType, UserRole
from app.core.tenant_utils import validate_company_access

# Create router with prefix and tag
router = APIRouter(
    prefix="/workflow",
    tags=["workflow"],
    dependencies=[Depends(require_project_manager)]  # Minimum required role: ProjectManager
)


@router.post("", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
async def create_workflow_entry(
    workflow: WorkflowCreate,
    request: Request,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_tenant_session)
):
    """
    Create a new workflow entry.
    
    This endpoint records a workflow action such as barcode scanning, piece cutting, etc.
    """
    try:
        # Validate action_type (should be automatically validated by Pydantic)
        if workflow.action_type not in WorkflowActionType.__members__.values():
            valid_types = [str(t) for t in WorkflowActionType.__members__.values()]
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "error": "Invalid action_type provided",
                    "valid_types": valid_types
                }
            )
        
        target_company_guid: uuid.UUID
        if workflow.company_guid:
            # If company_guid is provided in payload, validate it
            await validate_company_access(request, workflow.company_guid, current_user["company_guid"], current_user["role"])
            target_company_guid = workflow.company_guid
        else:
            # Otherwise, use the tenant from the current user's token
            target_company_guid = uuid.UUID(current_user["company_guid"])
        
        # Create the workflow entry
        entry = await WorkflowService.create_workflow_entry(
            action_type=workflow.action_type,
            company_guid=target_company_guid,
            workstation_guid=workflow.workstation_guid,
            user_guid=workflow.user_guid or current_user["guid"],  # Use the current user if not specified
            api_key_guid=workflow.api_key_guid,
            action_value=workflow.action_value,
            session=session
        )
        
        await session.commit()
        return entry
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create workflow entry: {str(e)}"
        )


@router.get("", response_model=WorkflowList)
async def get_workflow_entries(
    action_type: Optional[WorkflowActionType] = None,
    workstation_guid: Optional[uuid.UUID] = None,
    user_guid: Optional[uuid.UUID] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_tenant_session)
):
    """
    Get workflow entries with optional filtering.
    
    This endpoint supports filtering by action type, workstation, user, and date range.
    Results are paginated and sorted by creation date (newest first).
    """
    try:
        company_guid = uuid.UUID(current_user["company_guid"])
        
        entries = await WorkflowService.get_workflow_entries(
            company_guid=company_guid,
            action_type=action_type,
            workstation_guid=workstation_guid,
            user_guid=user_guid,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            offset=offset,
            session=session
        )
        
        return {"workflows": entries}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve workflow entries: {str(e)}"
        )


@router.get("/statistics", response_model=WorkflowStatistics)
async def get_workflow_statistics(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_tenant_session)
):
    """
    Get statistics about workflow entries.
    
    This endpoint provides counts and aggregated data about workflow entries,
    optionally filtered by date range.
    """
    try:
        company_guid = uuid.UUID(current_user["company_guid"])
        
        stats = await WorkflowService.get_workflow_statistics(
            company_guid=company_guid,
            start_date=start_date,
            end_date=end_date,
            session=session
        )
        
        return stats
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve workflow statistics: {str(e)}"
        )


@router.get("/{guid}", response_model=WorkflowResponse)
async def get_workflow_entry(
    guid: uuid.UUID,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_tenant_session)
):
    """
    Get a workflow entry by GUID.
    
    This endpoint retrieves a specific workflow entry by its GUID.
    """
    try:
        entry = await WorkflowService.get_workflow_by_guid(guid, session)
        
        if not entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Workflow entry with GUID {guid} not found"
            )
        
        # Check company access (RLS should handle this, but double-check)
        if entry.company_guid != uuid.UUID(current_user["company_guid"]) and current_user["role"] != UserRole.SYSTEM_ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this workflow entry"
            )
        
        return entry
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve workflow entry: {str(e)}"
        ) 