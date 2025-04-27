from typing import List, Dict, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, update
import uuid

from app.models.project import Project
from app.models.component import Component
from app.models.assembly import Assembly
from app.models.piece import Piece
from app.models.article import Article
from app.schemas.sync.main import (
    ProjectCreate, ComponentCreate, AssemblyCreate, PieceCreate, ArticleCreate, SyncResult
)

class SyncService:
    """
    Service for synchronizing data from RaConnect.
    
    Handles bulk inserts and updates for production entities.
    """
    
    @staticmethod
    async def sync_projects(projects_data: List[Dict[str, Any]], company_guid: str, session: AsyncSession) -> Dict[str, int]:
        # Add company_guid to each record
        for p in projects_data:
            p['company_guid'] = company_guid
            
        stmt = insert(Project).values(projects_data)
        stmt = stmt.on_conflict_do_update(
            index_elements=[Project.id], # Assuming 'id' is the RaConnect primary key
            set_={c.name: getattr(stmt.excluded, c.name) 
                  for c in Project.__table__.columns if c.name != 'id'}
        )
        result = await session.execute(stmt)
        # rowcount might not be reliable for inserts/updates with ON CONFLICT in asyncpg
        # We might need a more sophisticated way to count inserts vs updates if needed
        # For now, returning a placeholder
        await session.commit()
        return {"inserted_or_updated": len(projects_data)} # Placeholder count
    
    @staticmethod
    async def sync_components(components_data: List[Dict[str, Any]], company_guid: str, session: AsyncSession) -> Dict[str, int]:
        for c in components_data:
            c['company_guid'] = company_guid
            
        stmt = insert(Component).values(components_data)
        stmt = stmt.on_conflict_do_update(
            index_elements=[Component.id],
            set_={col.name: getattr(stmt.excluded, col.name) 
                  for col in Component.__table__.columns if col.name != 'id'}
        )
        await session.execute(stmt)
        await session.commit()
        return {"inserted_or_updated": len(components_data)}
    
    @staticmethod
    async def sync_assemblies(assemblies_data: List[Dict[str, Any]], company_guid: str, session: AsyncSession) -> Dict[str, int]:
        for a in assemblies_data:
            a['company_guid'] = company_guid
            
        stmt = insert(Assembly).values(assemblies_data)
        stmt = stmt.on_conflict_do_update(
            index_elements=[Assembly.id],
            set_={c.name: getattr(stmt.excluded, c.name) 
                  for c in Assembly.__table__.columns if c.name != 'id'}
        )
        await session.execute(stmt)
        await session.commit()
        return {"inserted_or_updated": len(assemblies_data)}
    
    @staticmethod
    async def sync_pieces(pieces_data: List[Dict[str, Any]], company_guid: str, session: AsyncSession) -> Dict[str, int]:
        for p in pieces_data:
            p['company_guid'] = company_guid
            
        stmt = insert(Piece).values(pieces_data)
        stmt = stmt.on_conflict_do_update(
            index_elements=[Piece.id],
            set_={c.name: getattr(stmt.excluded, c.name) 
                  for c in Piece.__table__.columns if c.name != 'id'}
        )
        await session.execute(stmt)
        await session.commit()
        return {"inserted_or_updated": len(pieces_data)}
    
    @staticmethod
    async def sync_articles(articles_data: List[Dict[str, Any]], company_guid: str, session: AsyncSession) -> Dict[str, int]:
        for a in articles_data:
            a['company_guid'] = company_guid
            
        stmt = insert(Article).values(articles_data)
        stmt = stmt.on_conflict_do_update(
            index_elements=[Article.id],
            set_={c.name: getattr(stmt.excluded, c.name) 
                  for c in Article.__table__.columns if c.name != 'id'}
        )
        await session.execute(stmt)
        await session.commit()
        return {"inserted_or_updated": len(articles_data)} 