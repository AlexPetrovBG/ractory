import uuid
import secrets
import string
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from datetime import datetime
from typing import Optional, List, Dict, Any

from app.models.apikey import ApiKey
from app.utils.security import hash_password


class ApiKeyService:
    @staticmethod
    def generate_api_key() -> str:
        """
        Generate a secure API key with a prefix.
        
        Returns:
            A string in the format "rfk_<random_string>"
        """
        # Generate 32 characters of randomness
        charset = string.ascii_letters + string.digits
        random_part = ''.join(secrets.choice(charset) for _ in range(32))
        
        # Add prefix to make it easily identifiable
        return f"rfk_{random_part}"
    
    @staticmethod
    def hash_api_key(api_key: str) -> str:
        """
        Hash an API key for storage in the database.
        
        Args:
            api_key: The raw API key
            
        Returns:
            Hashed API key string
        """
        # We can use the same hashing mechanism as for passwords
        return hash_password(api_key)
    
    @staticmethod
    async def create_api_key(
        company_guid: uuid.UUID,
        description: Optional[str] = None,
        scopes: Optional[str] = None,
        session: AsyncSession = None
    ) -> Dict[str, Any]:
        """
        Create a new API key for a company.
        
        Args:
            company_guid: The company this key belongs to
            description: Optional description of what this key is for
            scopes: Optional comma-separated list of permission scopes
            session: Database session
            
        Returns:
            Dictionary with the created API key details, including the raw key
        """
        # Generate a new API key
        raw_key = ApiKeyService.generate_api_key()
        hashed_key = ApiKeyService.hash_api_key(raw_key)
        
        # Create the API key model
        new_key = ApiKey(
            guid=uuid.uuid4(),
            company_guid=company_guid,
            key_hash=hashed_key,
            description=description,
            scopes=scopes,
            is_active=True
        )
        
        # Save to database
        session.add(new_key)
        await session.commit()
        await session.refresh(new_key)
        
        # Return the details including the raw key (which won't be retrievable again)
        return {
            "guid": new_key.guid,
            "key": raw_key,
            "description": new_key.description,
            "scopes": new_key.scopes,
            "created_at": new_key.created_at,
            "company_guid": new_key.company_guid
        }
    
    @staticmethod
    async def get_api_keys_for_company(
        company_guid: uuid.UUID,
        session: AsyncSession = None
    ) -> List[ApiKey]:
        """
        Get all API keys for a company.
        
        Args:
            company_guid: The company GUID to get keys for
            session: Database session
            
        Returns:
            List of API key objects
        """
        query = select(ApiKey).where(ApiKey.company_guid == company_guid)
        result = await session.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def get_api_key_by_guid(
        guid: uuid.UUID,
        session: AsyncSession = None
    ) -> Optional[ApiKey]:
        """
        Get an API key by its GUID.
        
        Args:
            guid: The API key GUID
            session: Database session
            
        Returns:
            API key object if found, None otherwise
        """
        query = select(ApiKey).where(ApiKey.guid == guid)
        result = await session.execute(query)
        return result.scalars().first()
    
    @staticmethod
    async def update_api_key(
        guid: uuid.UUID,
        description: Optional[str] = None,
        scopes: Optional[str] = None,
        is_active: Optional[bool] = None,
        session: AsyncSession = None
    ) -> Optional[ApiKey]:
        """
        Update an API key's details.
        
        Args:
            guid: The API key GUID to update
            description: New description (None to keep current)
            scopes: New scopes (None to keep current)
            is_active: New active status (None to keep current)
            session: Database session
            
        Returns:
            Updated API key object if found, None otherwise
        """
        # Prepare update values (only non-None values)
        values = {}
        if description is not None:
            values["description"] = description
        if scopes is not None:
            values["scopes"] = scopes
        if is_active is not None:
            values["is_active"] = is_active
        
        # No values to update
        if not values:
            return await ApiKeyService.get_api_key_by_guid(guid, session)
        
        # Update the key
        query = update(ApiKey).where(ApiKey.guid == guid).values(**values).returning(ApiKey)
        result = await session.execute(query)
        await session.commit()
        
        return result.scalars().first()
    
    @staticmethod
    async def delete_api_key(
        guid: uuid.UUID,
        session: AsyncSession = None
    ) -> bool:
        """
        Delete an API key.
        
        Args:
            guid: The API key GUID to delete
            session: Database session
            
        Returns:
            True if deleted, False if not found
        """
        query = delete(ApiKey).where(ApiKey.guid == guid)
        result = await session.execute(query)
        await session.commit()
        
        return result.rowcount > 0
    
    @staticmethod
    async def validate_api_key(
        api_key: str,
        session: AsyncSession = None
    ) -> Optional[Dict[str, Any]]:
        """
        Validate an API key and update its last_used_at timestamp.
        
        Args:
            api_key: The raw API key to validate
            session: Database session
            
        Returns:
            Dictionary with company and scope info if validated, None otherwise
        """
        # We need to query all API keys as we don't know the hash upfront
        query = select(ApiKey).where(ApiKey.is_active == True)
        result = await session.execute(query)
        keys = result.scalars().all()
        
        # Try to find a matching key
        from app.utils.security import verify_password
        
        for key in keys:
            if verify_password(api_key, key.key_hash):
                # Update last_used_at
                key.last_used_at = datetime.utcnow()
                await session.commit()
                
                # Return key info
                return {
                    "company_guid": str(key.company_guid),
                    "scopes": key.scopes,
                    "guid": str(key.guid)
                }
        
        return None 