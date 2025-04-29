from fastapi import APIRouter, HTTPException, status, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import uuid

from app.schemas.api_key import (
    ApiKeyCreate, ApiKeyCreated, ApiKeyResponse, 
    ApiKeyList, ApiKeyUpdate
)
from app.services.api_key_service import ApiKeyService
from app.core.deps import get_current_user, CurrentUser, get_tenant_session
from app.core.rbac import require_company_admin, require_system_admin
from app.models.enums import UserRole

router = APIRouter(
    prefix="/api-keys",
    tags=["api-keys"],
    dependencies=[Depends(require_company_admin)]  # Minimum required role: CompanyAdmin
)

@router.post("", response_model=ApiKeyCreated, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    api_key: ApiKeyCreate,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_tenant_session)
):
    """
    Create a new API key for the current company.
    
    Only CompanyAdmin and SystemAdmin can create API keys.
    The raw API key is only returned once in the response.
    """
    company_guid = uuid.UUID(current_user.tenant)
    
    try:
        result = await ApiKeyService.create_api_key(
            company_guid=company_guid,
            description=api_key.description,
            scopes=api_key.scopes,
            session=session
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create API key: {str(e)}"
        )

@router.get("", response_model=ApiKeyList)
async def get_api_keys(
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_tenant_session)
):
    """
    Get all API keys for the current company.
    
    Only CompanyAdmin and SystemAdmin can view API keys.
    Note that the actual key values are not returned, only metadata.
    """
    company_guid = uuid.UUID(current_user.tenant)
    
    try:
        api_keys = await ApiKeyService.get_api_keys_for_company(
            company_guid=company_guid,
            session=session
        )
        return {"api_keys": api_keys}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve API keys: {str(e)}"
        )

@router.get("/{guid}", response_model=ApiKeyResponse)
async def get_api_key(
    guid: uuid.UUID,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_tenant_session)
):
    """
    Get an API key by its GUID.
    
    Only CompanyAdmin and SystemAdmin can view API keys.
    Note that the actual key value is not returned, only metadata.
    """
    try:
        api_key = await ApiKeyService.get_api_key_by_guid(guid, session)
        
        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"API key with GUID {guid} not found"
            )
            
        return api_key
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve API key: {str(e)}"
        )

@router.put("/{guid}", response_model=ApiKeyResponse)
async def update_api_key(
    guid: uuid.UUID,
    api_key_update: ApiKeyUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_tenant_session)
):
    """
    Update an API key's description, scopes, or active status.
    
    Only CompanyAdmin and SystemAdmin can update API keys.
    """
    try:
        # Check if the API key exists
        existing_key = await ApiKeyService.get_api_key_by_guid(guid, session)
        
        if not existing_key:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"API key with GUID {guid} not found"
            )
        
        # Update the API key
        updated_key = await ApiKeyService.update_api_key(
            guid=guid,
            description=api_key_update.description,
            scopes=api_key_update.scopes,
            is_active=api_key_update.is_active,
            session=session
        )
        
        return updated_key
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update API key: {str(e)}"
        )

@router.delete("/{guid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_api_key(
    guid: uuid.UUID,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_tenant_session)
):
    """
    Delete an API key.
    
    Only CompanyAdmin and SystemAdmin can delete API keys.
    """
    try:
        # Check if the API key exists
        existing_key = await ApiKeyService.get_api_key_by_guid(guid, session)
        
        if not existing_key:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"API key with GUID {guid} not found"
            )
        
        # Delete the API key
        success = await ApiKeyService.delete_api_key(guid, session)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete API key"
            )
        
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete API key: {str(e)}"
        ) 