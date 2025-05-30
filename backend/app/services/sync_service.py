from typing import List, Dict, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, update, func
import uuid
from fastapi import HTTPException, status
import logging
import datetime

from app.models.project import Project
from app.models.component import Component
from app.models.assembly import Assembly
from app.models.piece import Piece
from app.models.article import Article
from app.schemas.sync.main import (
    ProjectCreate, ComponentCreate, AssemblyCreate, PieceCreate, ArticleCreate, SyncResult
)
from app.services.workflow_service import WorkflowService
from app.models.enums import WorkflowActionType

# Set up logging
logger = logging.getLogger("app.services.sync_service")

class SyncService:
    """
    Service for synchronizing data from RaConnect.
    
    Handles bulk inserts and updates for production entities.
    """
    
    @staticmethod
    async def sync_projects(projects_data: List[ProjectCreate], company_guid: uuid.UUID, session: AsyncSession) -> Dict[str, int]:
        # Convert company_guid to UUID if it's a string
        if isinstance(company_guid, str):
            company_guid = uuid.UUID(company_guid)
        
        # Validate company isolation for all projects
        for i, project in enumerate(projects_data):
            if project.company_guid is not None and project.company_guid != company_guid:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Project at index {i} has company_guid that doesn't match the authenticated user's company"
                )
        
        # Check for duplicate GUIDs in the input data
        guid_set = set()
        for i, project in enumerate(projects_data):
            if project.guid:
                if project.guid in guid_set:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"Duplicate GUID found in input data: {project.guid}"
                    )
                guid_set.add(project.guid)
        
        # Check which GUIDs already exist in the database
        existing_guids = set()
        if guid_set:
            query = select(Project.guid, Project.is_active, Project.deleted_at).where(Project.guid.in_(guid_set))
            result = await session.execute(query)
            existing_db = {row[0]: (row[1], row[2]) for row in result.all()}
            existing_guids = set(existing_db.keys())
        else:
            existing_db = {}
        
        # Convert ProjectCreate objects to dicts
        insert_dicts = []
        update_dicts = []
        reactivated_dicts = []
        input_guids = set()
        for p in projects_data:
            d = p.dict()
            d['company_guid'] = company_guid
            input_guids.add(p.guid)
            if p.guid:
                if p.guid in existing_guids:
                    # If soft-deleted, reactivate and update
                    is_active, deleted_at = existing_db[p.guid]
                    if not is_active:
                        d['is_active'] = True
                        d['deleted_at'] = None
                        reactivated_dicts.append(d)
                    else:
                        update_dicts.append(d)
                else:
                    insert_dicts.append(d)
            else:
                d['guid'] = uuid.uuid4()
                insert_dicts.append(d)
        
        # Handle inserts
        inserted_count = 0
        if insert_dicts:
            insert_stmt = insert(Project).values(insert_dicts)
            await session.execute(insert_stmt)
            inserted_count = len(insert_dicts)
        
        # Handle updates
        updated_count = 0
        for update_dict in update_dicts:
            guid = update_dict.pop('guid')
            update_stmt = update(Project).where(Project.guid == guid).values(**update_dict)
            update_result = await session.execute(update_stmt)
            updated_count += update_result.rowcount
        
        # Handle reactivations
        for reactivate_dict in reactivated_dicts:
            guid = reactivate_dict.pop('guid')
            update_stmt = update(Project).where(Project.guid == guid).values(**reactivate_dict)
            await session.execute(update_stmt)
            updated_count += 1
        
        # Soft delete children not present in payload
        # (This requires a list of all project GUIDs for this company in DB)
        db_query = select(Project.guid).where(Project.company_guid == company_guid, Project.is_active == True)
        db_result = await session.execute(db_query)
        db_guids = {row[0] for row in db_result.all()}
        missing_guids = db_guids - input_guids
        for missing_guid in missing_guids:
            await SyncService.cascade_soft_delete('project', missing_guid, session)
        
        await session.commit()
        return {"inserted": inserted_count, "updated": updated_count}
    
    @staticmethod
    async def sync_components(components_data: List[ComponentCreate], company_guid: uuid.UUID, session: AsyncSession) -> Dict[str, int]:
        if isinstance(company_guid, str):
            company_guid = uuid.UUID(company_guid)
        project_guids = set()
        for component in components_data:
            if component.project_guid:
                project_guids.add(component.project_guid)
        if project_guids:
            query = select(Project.guid).where(
                Project.guid.in_(project_guids),
                Project.company_guid == company_guid
            )
            result = await session.execute(query)
            valid_project_guids = {str(row[0]).lower() for row in result.all()}
            logger.debug(f"Valid project GUIDs: {valid_project_guids}")
        else:
            valid_project_guids = set()
        for i, component in enumerate(components_data):
            if component.company_guid is not None and component.company_guid != company_guid:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Component at index {i} has company_guid that doesn't match the authenticated user's company"
                )
            if component.project_guid and str(component.project_guid).lower() not in valid_project_guids:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Component at index {i} references a project that doesn't exist or doesn't belong to your company"
                )
        guid_set = set()
        for i, component in enumerate(components_data):
            if component.guid:
                if component.guid in guid_set:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"Duplicate GUID found in input data: {component.guid}"
                    )
                guid_set.add(component.guid)
        existing_guids = set()
        if guid_set:
            query = select(Component.guid, Component.is_active, Component.deleted_at).where(Component.guid.in_(guid_set))
            result = await session.execute(query)
            existing_db = {row[0]: (row[1], row[2]) for row in result.all()}
            existing_guids = set(existing_db.keys())
        else:
            existing_db = {}
        insert_dicts = []
        update_dicts = []
        reactivated_dicts = []
        input_guids = set()
        for c in components_data:
            d = c.dict()
            d['company_guid'] = company_guid
            input_guids.add(c.guid)
            if c.guid:
                if c.guid in existing_guids:
                    is_active, deleted_at = existing_db[c.guid]
                    if not is_active:
                        d['is_active'] = True
                        d['deleted_at'] = None
                        reactivated_dicts.append(d)
                    else:
                        update_dicts.append(d)
                else:
                    insert_dicts.append(d)
            else:
                d['guid'] = uuid.uuid4()
                insert_dicts.append(d)
        inserted_count = 0
        if insert_dicts:
            insert_stmt = insert(Component).values(insert_dicts)
            await session.execute(insert_stmt)
            inserted_count = len(insert_dicts)
        updated_count = 0
        for update_dict in update_dicts:
            guid = update_dict.pop('guid')
            update_stmt = update(Component).where(Component.guid == guid).values(**update_dict)
            update_result = await session.execute(update_stmt)
            updated_count += update_result.rowcount
        for reactivate_dict in reactivated_dicts:
            guid = reactivate_dict.pop('guid')
            update_stmt = update(Component).where(Component.guid == guid).values(**reactivate_dict)
            await session.execute(update_stmt)
            updated_count += 1
        db_query = select(Component.guid).where(Component.company_guid == company_guid, Component.is_active == True)
        db_result = await session.execute(db_query)
        db_guids = {row[0] for row in db_result.all()}
        missing_guids = db_guids - input_guids
        for missing_guid in missing_guids:
            await SyncService.cascade_soft_delete('component', missing_guid, session)
        await session.commit()
        return {"inserted": inserted_count, "updated": updated_count}
    
    @staticmethod
    async def sync_assemblies(assemblies_data: List[AssemblyCreate], company_guid: uuid.UUID, session: AsyncSession) -> Dict[str, int]:
        if isinstance(company_guid, str):
            company_guid = uuid.UUID(company_guid)
        project_guids = set()
        component_guids = set()
        project_component_pairs = []
        for assembly in assemblies_data:
            if assembly.project_guid:
                project_guids.add(assembly.project_guid)
            if assembly.component_guid:
                component_guids.add(assembly.component_guid)
            if assembly.project_guid and assembly.component_guid:
                project_component_pairs.append((assembly.project_guid, assembly.component_guid))
        if project_guids:
            query = select(Project.guid).where(
                Project.guid.in_(project_guids),
                Project.company_guid == company_guid
            )
            result = await session.execute(query)
            valid_project_guids = {str(row[0]).lower() for row in result.all()}
            logger.debug(f"Valid project GUIDs: {valid_project_guids}")
        else:
            valid_project_guids = set()
        valid_component_guids = set()
        component_project_map = {}
        if component_guids:
            query = select(Component.guid, Component.project_guid).where(
                Component.guid.in_(component_guids),
                Component.company_guid == company_guid
            )
            result = await session.execute(query)
            rows = result.all()
            for row in rows:
                component_guid_str = str(row[0]).lower()
                valid_component_guids.add(component_guid_str)
                if row[1] is not None:
                    component_project_map[component_guid_str] = str(row[1]).lower()
                else:
                    logger.warning(f"Component {component_guid_str} has NULL project_guid")
            logger.debug(f"Valid component GUIDs: {valid_component_guids}")
            logger.debug(f"Component->Project map: {component_project_map}")
        for i, assembly in enumerate(assemblies_data):
            if assembly.company_guid is not None and assembly.company_guid != company_guid:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Assembly at index {i} has company_guid that doesn't match the authenticated user's company"
                )
            if assembly.project_guid and str(assembly.project_guid).lower() not in valid_project_guids:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Assembly at index {i} references a project that doesn't exist or doesn't belong to your company"
                )
            component_guid_str = str(assembly.component_guid).lower()
            if assembly.component_guid and component_guid_str not in valid_component_guids:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Assembly at index {i} references a component that doesn't exist or doesn't belong to your company"
                )
            if assembly.project_guid and assembly.component_guid:
                project_guid_str = str(assembly.project_guid).lower()
                if component_guid_str not in component_project_map:
                    direct_query = select(Component.project_guid).where(
                        Component.guid == assembly.component_guid,
                        Component.company_guid == company_guid
                    )
                    direct_result = await session.execute(direct_query)
                    direct_project_guid = direct_result.scalar_one_or_none()
                    if direct_project_guid is None:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Assembly at index {i} references a component that has no project association"
                        )
                    else:
                        logger.error(f"Assembly validation error: Component {component_guid_str} has project_guid={direct_project_guid} but wasn't in the component_project_map")
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Assembly at index {i} references a component with inconsistent project data. Please verify the component's project association."
                        )
                component_project_guid = component_project_map[component_guid_str]
                if component_project_guid != project_guid_str:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Assembly at index {i} has mismatched project/component relationship. Component '{component_guid_str}' belongs to project '{component_project_guid}', not '{project_guid_str}'."
                    )
        guid_set = set()
        for i, assembly in enumerate(assemblies_data):
            if assembly.guid:
                if assembly.guid in guid_set:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"Duplicate GUID found in input data: {assembly.guid}"
                    )
                guid_set.add(assembly.guid)
        existing_guids = set()
        if guid_set:
            query = select(Assembly.guid, Assembly.is_active, Assembly.deleted_at).where(Assembly.guid.in_(guid_set))
            result = await session.execute(query)
            existing_db = {row[0]: (row[1], row[2]) for row in result.all()}
            existing_guids = set(existing_db.keys())
        else:
            existing_db = {}
        insert_dicts = []
        update_dicts = []
        reactivated_dicts = []
        input_guids = set()
        for a in assemblies_data:
            d = a.dict()
            d['company_guid'] = company_guid
            input_guids.add(a.guid)
            if a.guid:
                if a.guid in existing_guids:
                    is_active, deleted_at = existing_db[a.guid]
                    if not is_active:
                        d['is_active'] = True
                        d['deleted_at'] = None
                        reactivated_dicts.append(d)
                    else:
                        update_dicts.append(d)
                else:
                    insert_dicts.append(d)
            else:
                d['guid'] = uuid.uuid4()
                insert_dicts.append(d)
        inserted_count = 0
        if insert_dicts:
            insert_stmt = insert(Assembly).values(insert_dicts)
            await session.execute(insert_stmt)
            inserted_count = len(insert_dicts)
        updated_count = 0
        for update_dict in update_dicts:
            guid = update_dict.pop('guid')
            update_stmt = update(Assembly).where(Assembly.guid == guid).values(**update_dict)
            update_result = await session.execute(update_stmt)
            updated_count += update_result.rowcount
        for reactivate_dict in reactivated_dicts:
            guid = reactivate_dict.pop('guid')
            update_stmt = update(Assembly).where(Assembly.guid == guid).values(**reactivate_dict)
            await session.execute(update_stmt)
            updated_count += 1
        db_query = select(Assembly.guid).where(Assembly.company_guid == company_guid, Assembly.is_active == True)
        db_result = await session.execute(db_query)
        db_guids = {row[0] for row in db_result.all()}
        missing_guids = db_guids - input_guids
        for missing_guid in missing_guids:
            await SyncService.cascade_soft_delete('assembly', missing_guid, session)
        await session.commit()
        return {"inserted": inserted_count, "updated": updated_count}
    
    @staticmethod
    async def sync_pieces(pieces_data: List[PieceCreate], company_guid: uuid.UUID, session: AsyncSession) -> Dict[str, int]:
        if isinstance(company_guid, str):
            company_guid = uuid.UUID(company_guid)
        project_guids = set()
        component_guids = set()
        assembly_guids = set()
        for piece in pieces_data:
            if piece.project_guid:
                project_guids.add(piece.project_guid)
            if piece.component_guid:
                component_guids.add(piece.component_guid)
            if piece.assembly_guid:
                assembly_guids.add(piece.assembly_guid)
        valid_project_guids = set()
        if project_guids:
            query = select(Project.guid).where(
                Project.guid.in_(project_guids),
                Project.company_guid == company_guid
            )
            result = await session.execute(query)
            valid_project_guids = {str(row[0]).lower() for row in result.all()}
        valid_component_guids = set()
        if component_guids:
            query = select(Component.guid).where(
                Component.guid.in_(component_guids),
                Component.company_guid == company_guid
            )
            result = await session.execute(query)
            valid_component_guids = {str(row[0]).lower() for row in result.all()}
        valid_assembly_guids = set()
        if assembly_guids:
            query = select(Assembly.guid).where(
                Assembly.guid.in_(assembly_guids),
                Assembly.company_guid == company_guid
            )
            result = await session.execute(query)
            valid_assembly_guids = {str(row[0]).lower() for row in result.all()}
        for i, piece in enumerate(pieces_data):
            if piece.company_guid is not None and piece.company_guid != company_guid:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Piece at index {i} has company_guid that doesn't match the authenticated user's company"
                )
            if piece.project_guid and str(piece.project_guid).lower() not in valid_project_guids:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Piece at index {i} references a project that doesn't exist or doesn't belong to your company"
                )
            if piece.component_guid and str(piece.component_guid).lower() not in valid_component_guids:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Piece at index {i} references a component that doesn't exist or doesn't belong to your company"
                )
            if piece.assembly_guid and str(piece.assembly_guid).lower() not in valid_assembly_guids:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Piece at index {i} references an assembly that doesn't exist or doesn't belong to your company"
                )
        guid_set = set()
        for i, piece in enumerate(pieces_data):
            if piece.guid:
                if piece.guid in guid_set:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"Duplicate GUID found in input data: {piece.guid}"
                    )
                guid_set.add(piece.guid)
        existing_guids = set()
        if guid_set:
            query = select(Piece.guid, Piece.is_active, Piece.deleted_at).where(Piece.guid.in_(guid_set))
            result = await session.execute(query)
            existing_db = {row[0]: (row[1], row[2]) for row in result.all()}
            existing_guids = set(existing_db.keys())
        else:
            existing_db = {}
        insert_dicts = []
        update_dicts = []
        reactivated_dicts = []
        input_guids = set()
        for p in pieces_data:
            d = p.dict()
            d['company_guid'] = company_guid
            input_guids.add(p.guid)
            if p.guid:
                if p.guid in existing_guids:
                    is_active, deleted_at = existing_db[p.guid]
                    if not is_active:
                        d['is_active'] = True
                        d['deleted_at'] = None
                        reactivated_dicts.append(d)
                    else:
                        update_dicts.append(d)
                else:
                    insert_dicts.append(d)
            else:
                d['guid'] = uuid.uuid4()
                insert_dicts.append(d)
        inserted_count = 0
        if insert_dicts:
            insert_stmt = insert(Piece).values(insert_dicts)
            await session.execute(insert_stmt)
            inserted_count = len(insert_dicts)
        updated_count = 0
        for update_dict in update_dicts:
            guid = update_dict.pop('guid')
            update_stmt = update(Piece).where(Piece.guid == guid).values(**update_dict)
            update_result = await session.execute(update_stmt)
            updated_count += update_result.rowcount
        for reactivate_dict in reactivated_dicts:
            guid = reactivate_dict.pop('guid')
            update_stmt = update(Piece).where(Piece.guid == guid).values(**reactivate_dict)
            await session.execute(update_stmt)
            updated_count += 1
        db_query = select(Piece.guid).where(Piece.company_guid == company_guid, Piece.is_active == True)
        db_result = await session.execute(db_query)
        db_guids = {row[0] for row in db_result.all()}
        missing_guids = db_guids - input_guids
        for missing_guid in missing_guids:
            await SyncService.cascade_soft_delete('piece', missing_guid, session)
        await session.commit()
        return {"inserted": inserted_count, "updated": updated_count}
    
    @staticmethod
    async def sync_articles(articles_data: List[ArticleCreate], company_guid: uuid.UUID, session: AsyncSession) -> Dict[str, int]:
        if isinstance(company_guid, str):
            company_guid = uuid.UUID(company_guid)
        project_guids = set()
        component_guids = set()
        for article in articles_data:
            if article.project_guid:
                project_guids.add(article.project_guid)
            if article.component_guid:
                component_guids.add(article.component_guid)
        valid_project_guids = set()
        if project_guids:
            query = select(Project.guid).where(
                Project.guid.in_(project_guids),
                Project.company_guid == company_guid
            )
            result = await session.execute(query)
            valid_project_guids = {str(row[0]).lower() for row in result.all()}
        valid_component_guids = set()
        if component_guids:
            query = select(Component.guid).where(
                Component.guid.in_(component_guids),
                Component.company_guid == company_guid
            )
            result = await session.execute(query)
            valid_component_guids = {str(row[0]).lower() for row in result.all()}
        for i, article in enumerate(articles_data):
            if article.company_guid is not None and article.company_guid != company_guid:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Article at index {i} has company_guid that doesn't match the authenticated user's company"
                )
            if article.project_guid and str(article.project_guid).lower() not in valid_project_guids:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Article at index {i} references a project that doesn't exist or doesn't belong to your company"
                )
            if article.component_guid and str(article.component_guid).lower() not in valid_component_guids:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Article at index {i} references a component that doesn't exist or doesn't belong to your company"
                )
        guid_set = set()
        for i, article in enumerate(articles_data):
            if article.guid:
                if article.guid in guid_set:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"Duplicate GUID found in input data: {article.guid}"
                    )
                guid_set.add(article.guid)
        existing_guids = set()
        if guid_set:
            query = select(Article.guid, Article.is_active, Article.deleted_at).where(Article.guid.in_(guid_set))
            result = await session.execute(query)
            existing_db = {row[0]: (row[1], row[2]) for row in result.all()}
            existing_guids = set(existing_db.keys())
        else:
            existing_db = {}
        insert_dicts = []
        update_dicts = []
        reactivated_dicts = []
        input_guids = set()
        for a in articles_data:
            d = a.dict()
            d['company_guid'] = company_guid
            input_guids.add(a.guid)
            if a.guid:
                if a.guid in existing_guids:
                    is_active, deleted_at = existing_db[a.guid]
                    if not is_active:
                        d['is_active'] = True
                        d['deleted_at'] = None
                        reactivated_dicts.append(d)
                    else:
                        update_dicts.append(d)
                else:
                    insert_dicts.append(d)
            else:
                d['guid'] = uuid.uuid4()
                insert_dicts.append(d)
        inserted_count = 0
        if insert_dicts:
            insert_stmt = insert(Article).values(insert_dicts)
            await session.execute(insert_stmt)
            inserted_count = len(insert_dicts)
        updated_count = 0
        for update_dict in update_dicts:
            guid = update_dict.pop('guid')
            update_stmt = update(Article).where(Article.guid == guid).values(**update_dict)
            update_result = await session.execute(update_stmt)
            updated_count += update_result.rowcount
        for reactivate_dict in reactivated_dicts:
            guid = reactivate_dict.pop('guid')
            update_stmt = update(Article).where(Article.guid == guid).values(**reactivate_dict)
            await session.execute(update_stmt)
            updated_count += 1
        db_query = select(Article.guid).where(Article.company_guid == company_guid, Article.is_active == True)
        db_result = await session.execute(db_query)
        db_guids = {row[0] for row in db_result.all()}
        missing_guids = db_guids - input_guids
        for missing_guid in missing_guids:
            await SyncService.cascade_soft_delete('article', missing_guid, session)
        await session.commit()
        return {"inserted": inserted_count, "updated": updated_count}
    
    @staticmethod
    async def run_full_sync(
        data: Dict[str, Any], 
        company_guid: uuid.UUID,
        session: AsyncSession
    ) -> Dict[str, Dict[str, int]]:
        """Run a full synchronization for all entity types."""
        result = SyncResult()
        
        # Synchronize all provided entity types
        if "projects" in data and data["projects"]:
            result.projects = await SyncService.sync_projects(data["projects"], company_guid, session)
        
        if "components" in data and data["components"]:
            result.components = await SyncService.sync_components(data["components"], company_guid, session)
        
        if "assemblies" in data and data["assemblies"]:
            result.assemblies = await SyncService.sync_assemblies(data["assemblies"], company_guid, session)
        
        if "pieces" in data and data["pieces"]:
            result.pieces = await SyncService.sync_pieces(data["pieces"], company_guid, session)
        
        if "articles" in data and data["articles"]:
            result.articles = await SyncService.sync_articles(data["articles"], company_guid, session)
        
        return result.dict()
    
    @staticmethod
    async def cascade_soft_delete(entity_type: str, guid: uuid.UUID, session: AsyncSession, deleted_at=None):
        """
        Recursively soft delete the entity and all its active children.
        entity_type: one of 'project', 'component', 'assembly', 'piece', 'article'
        guid: the guid of the entity to soft delete
        session: SQLAlchemy AsyncSession
        deleted_at: timestamp to use for deleted_at (if None, use a single utcnow() for the whole cascade)
        """
        if deleted_at is None:
            deleted_at = datetime.datetime.utcnow()
        # Map entity_type to model and children
        entity_map = {
            'project': (Project, [Component, Assembly, Piece, Article], 'project_guid'),
            'component': (Component, [Assembly, Piece, Article], 'component_guid'),
            'assembly': (Assembly, [Piece], 'assembly_guid'),
            'piece': (Piece, [], None),
            'article': (Article, [], None),
        }
        if entity_type not in entity_map:
            raise ValueError(f"Unknown entity_type: {entity_type}")
        model, children, fk_field = entity_map[entity_type]
        # Soft delete the parent (always execute for the given guid)
        await session.execute(
            update(model)
            .where(model.guid == guid)
            .values(is_active=False, deleted_at=deleted_at)
        )
        # Audit log: fetch company_guid
        result = await session.execute(select(model.company_guid).where(model.guid == guid))
        company_guid = result.scalar_one_or_none()
        if company_guid:
            await WorkflowService.create_workflow_entry(
                action_type=WorkflowActionType.SoftDelete,
                company_guid=company_guid,
                action_value=f"Soft deleted {entity_type} {guid}",
                session=session
            )
        # Cascade to children
        table_to_entity_type = {
            "projects": "project",
            "components": "component",
            "assemblies": "assembly",
            "pieces": "piece",
            "articles": "article"
        }
        for child_model in children:
            child_fk = fk_field
            if child_fk is None:
                continue
            # Find all active children
            result = await session.execute(
                select(child_model.guid)
                .where(getattr(child_model, child_fk) == guid, child_model.is_active == True)
            )
            child_guids = [row[0] for row in result.all()]
            for child_guid in child_guids:
                child_type = table_to_entity_type[child_model.__tablename__]
                await SyncService.cascade_soft_delete(child_type, child_guid, session, deleted_at=deleted_at)
        await session.commit()

    @staticmethod
    async def cascade_restore(entity_type: str, guid: uuid.UUID, session: AsyncSession, deleted_at=None):
        """
        Recursively restore the entity and all its children that were deleted in the same operation (matching deleted_at).
        entity_type: one of 'project', 'component', 'assembly', 'piece', 'article'
        guid: the guid of the entity to restore
        session: SQLAlchemy AsyncSession
        deleted_at: timestamp to match for children (if None, fetch from parent)
        """
        # Map entity_type to model and children
        entity_map = {
            'project': (Project, [Component, Assembly, Piece, Article], 'project_guid'),
            'component': (Component, [Assembly, Piece, Article], 'component_guid'),
            'assembly': (Assembly, [Piece], 'assembly_guid'),
            'piece': (Piece, [], None),
            'article': (Article, [], None),
        }
        if entity_type not in entity_map:
            raise ValueError(f"Unknown entity_type: {entity_type}")
        model, children, fk_field = entity_map[entity_type]

        # Fetch parent's deleted_at if not provided
        if deleted_at is None:
            result = await session.execute(
                select(model.deleted_at).where(model.guid == guid)
            )
            parent_deleted_at = result.scalar_one_or_none()
            if parent_deleted_at is None:
                # Already restored or not found
                return
            deleted_at = parent_deleted_at

        # Restore the parent
        await session.execute(
            update(model)
            .where(model.guid == guid, model.is_active == False)
            .values(is_active=True, deleted_at=None)
        )
        # Audit log: fetch company_guid
        result = await session.execute(select(model.company_guid).where(model.guid == guid))
        company_guid = result.scalar_one_or_none()
        if company_guid:
            await WorkflowService.create_workflow_entry(
                action_type=WorkflowActionType.Restore,
                company_guid=company_guid,
                action_value=f"Restored {entity_type} {guid}",
                session=session
            )

        # Cascade restore to children with matching deleted_at
        table_to_entity_type = {
            "projects": "project",
            "components": "component",
            "assemblies": "assembly",
            "pieces": "piece",
            "articles": "article"
        }
        for child_model in children:
            child_fk = fk_field
            if child_fk is None:
                continue
            # Find all children with matching deleted_at
            result = await session.execute(
                select(child_model.guid)
                .where(getattr(child_model, child_fk) == guid,
                       child_model.is_active == False,
                       child_model.deleted_at == deleted_at)
            )
            child_guids = [row[0] for row in result.all()]
            for child_guid in child_guids:
                child_type = table_to_entity_type[child_model.__tablename__]
                await SyncService.cascade_restore(child_type, child_guid, session, deleted_at=deleted_at)
        await session.commit() 