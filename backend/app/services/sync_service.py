from typing import List, Dict, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, update
import uuid
from fastapi import HTTPException, status
import logging

from app.models.project import Project
from app.models.component import Component
from app.models.assembly import Assembly
from app.models.piece import Piece
from app.models.article import Article
from app.schemas.sync.main import (
    ProjectCreate, ComponentCreate, AssemblyCreate, PieceCreate, ArticleCreate, SyncResult
)

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
            query = select(Project.guid).where(Project.guid.in_(guid_set))
            result = await session.execute(query)
            existing_guids = {row[0] for row in result.all()}
        
        # Convert ProjectCreate objects to dicts
        insert_dicts = []
        update_dicts = []
        
        for p in projects_data:
            d = p.dict()
            d['company_guid'] = company_guid
            
            # If guid is provided, we need to determine if this is an insert or update
            if p.guid:
                if p.guid in existing_guids:
                    # This is an update
                    update_dicts.append(d)
                else:
                    # This is a new record with provided GUID
                    insert_dicts.append(d)
            else:
                # Auto-generate GUID for new records without GUID
                d['guid'] = uuid.uuid4()
                insert_dicts.append(d)
        
        # Handle inserts
        inserted_count = 0
        if insert_dicts:
            insert_stmt = insert(Project).values(insert_dicts)
            insert_result = await session.execute(insert_stmt)
            inserted_count = len(insert_dicts)
        
        # Handle updates
        updated_count = 0
        for update_dict in update_dicts:
            guid = update_dict.pop('guid')
            update_stmt = update(Project).where(Project.guid == guid).values(**update_dict)
            update_result = await session.execute(update_stmt)
            updated_count += update_result.rowcount
        
        await session.commit()
        return {"inserted": inserted_count, "updated": updated_count}
    
    @staticmethod
    async def sync_components(components_data: List[ComponentCreate], company_guid: uuid.UUID, session: AsyncSession) -> Dict[str, int]:
        # Convert company_guid to UUID if it's a string
        if isinstance(company_guid, str):
            company_guid = uuid.UUID(company_guid)
        
        # First, collect all project GUIDs referenced by the components
        project_guids = set()
        for component in components_data:
            if component.project_guid:
                project_guids.add(component.project_guid)
        
        # Get all the projects referenced by these components that belong to this company
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
        
        # Validate company isolation and project references for all components
        for i, component in enumerate(components_data):
            # Validate company_guid matches authenticated user's company
            if component.company_guid is not None and component.company_guid != company_guid:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Component at index {i} has company_guid that doesn't match the authenticated user's company"
                )
            
            # Validate project_guid exists and belongs to this company
            if component.project_guid and str(component.project_guid).lower() not in valid_project_guids:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Component at index {i} references a project that doesn't exist or doesn't belong to your company"
                )
        
        # Check for duplicate GUIDs in the input data
        guid_set = set()
        for i, component in enumerate(components_data):
            if component.guid:
                if component.guid in guid_set:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"Duplicate GUID found in input data: {component.guid}"
                    )
                guid_set.add(component.guid)
        
        # Check which GUIDs already exist in the database
        existing_guids = set()
        if guid_set:
            query = select(Component.guid).where(Component.guid.in_(guid_set))
            result = await session.execute(query)
            existing_guids = {row[0] for row in result.all()}
        
        # Convert ComponentCreate objects to dicts
        insert_dicts = []
        update_dicts = []
        
        for c in components_data:
            d = c.dict()
            d['company_guid'] = company_guid
            
            # If guid is provided, we need to determine if this is an insert or update
            if c.guid:
                if c.guid in existing_guids:
                    # This is an update
                    update_dicts.append(d)
                else:
                    # This is a new record with provided GUID
                    insert_dicts.append(d)
            else:
                # Auto-generate GUID for new records without GUID
                d['guid'] = uuid.uuid4()
                insert_dicts.append(d)
        
        # Handle inserts
        inserted_count = 0
        if insert_dicts:
            insert_stmt = insert(Component).values(insert_dicts)
            insert_result = await session.execute(insert_stmt)
            inserted_count = len(insert_dicts)
        
        # Handle updates
        updated_count = 0
        for update_dict in update_dicts:
            guid = update_dict.pop('guid')
            update_stmt = update(Component).where(Component.guid == guid).values(**update_dict)
            update_result = await session.execute(update_stmt)
            updated_count += update_result.rowcount
        
        await session.commit()
        return {"inserted": inserted_count, "updated": updated_count}
    
    @staticmethod
    async def sync_assemblies(assemblies_data: List[AssemblyCreate], company_guid: uuid.UUID, session: AsyncSession) -> Dict[str, int]:
        # Convert company_guid to UUID if it's a string
        if isinstance(company_guid, str):
            company_guid = uuid.UUID(company_guid)
        
        # First, collect all project and component GUIDs referenced by the assemblies
        project_guids = set()
        component_guids = set()
        project_component_pairs = []  # To validate relationships
        
        for assembly in assemblies_data:
            if assembly.project_guid:
                project_guids.add(assembly.project_guid)
            if assembly.component_guid:
                component_guids.add(assembly.component_guid)
            if assembly.project_guid and assembly.component_guid:
                project_component_pairs.append((assembly.project_guid, assembly.component_guid))
        
        # Get all valid projects for this company
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
        
        # Get all valid components for this company and their project associations
        valid_component_guids = set()
        component_project_map = {}
        
        if component_guids:
            query = select(Component.guid, Component.project_guid).where(
                Component.guid.in_(component_guids),
                Component.company_guid == company_guid
            )
            result = await session.execute(query)
            rows = result.all()
            
            # Debug logging to see all returned rows
            logger.debug(f"Component query results: {rows}")
            
            # Process each component row
            for row in rows:
                component_guid_str = str(row[0]).lower()
                valid_component_guids.add(component_guid_str)
                
                # Only add to map if project_guid is not None
                if row[1] is not None:
                    component_project_map[component_guid_str] = str(row[1]).lower()
                else:
                    logger.warning(f"Component {component_guid_str} has NULL project_guid")
            
            logger.debug(f"Valid component GUIDs: {valid_component_guids}")
            logger.debug(f"Component->Project map: {component_project_map}")
        
        # Validate company isolation and references for all assemblies
        for i, assembly in enumerate(assemblies_data):
            # Validate company_guid matches authenticated user's company
            if assembly.company_guid is not None and assembly.company_guid != company_guid:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Assembly at index {i} has company_guid that doesn't match the authenticated user's company"
                )
            
            # Validate project_guid exists and belongs to this company
            if assembly.project_guid and str(assembly.project_guid).lower() not in valid_project_guids:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Assembly at index {i} references a project that doesn't exist or doesn't belong to your company"
                )
            
            # Validate component_guid exists and belongs to this company
            component_guid_str = str(assembly.component_guid).lower()
            if assembly.component_guid and component_guid_str not in valid_component_guids:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Assembly at index {i} references a component that doesn't exist or doesn't belong to your company"
                )
            
            # Validate component belongs to the specified project - using more robust checking
            if assembly.project_guid and assembly.component_guid:
                project_guid_str = str(assembly.project_guid).lower()
                
                # First check if the component exists in our map
                if component_guid_str not in component_project_map:
                    # Get the project_guid for this component directly from the database
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
                        # Component exists but has inconsistent data
                        logger.error(f"Assembly validation error: Component {component_guid_str} has project_guid={direct_project_guid} but wasn't in the component_project_map")
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Assembly at index {i} references a component with inconsistent project data. Please verify the component's project association."
                        )
                
                # Now check if the component's project matches the provided project
                component_project_guid = component_project_map[component_guid_str]
                if component_project_guid != project_guid_str:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Assembly at index {i} has mismatched project/component relationship. Component '{component_guid_str}' belongs to project '{component_project_guid}', not '{project_guid_str}'."
                    )
        
        # Check for duplicate GUIDs in the input data
        guid_set = set()
        for i, assembly in enumerate(assemblies_data):
            if assembly.guid:
                if assembly.guid in guid_set:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"Duplicate GUID found in input data: {assembly.guid}"
                    )
                guid_set.add(assembly.guid)
        
        # Check which GUIDs already exist in the database
        existing_guids = set()
        if guid_set:
            query = select(Assembly.guid).where(Assembly.guid.in_(guid_set))
            result = await session.execute(query)
            existing_guids = {row[0] for row in result.all()}
        
        # Convert AssemblyCreate objects to dicts
        insert_dicts = []
        update_dicts = []
        
        for a in assemblies_data:
            d = a.dict()
            d['company_guid'] = company_guid
            
            # If guid is provided, we need to determine if this is an insert or update
            if a.guid:
                if a.guid in existing_guids:
                    # This is an update
                    update_dicts.append(d)
                else:
                    # This is a new record with provided GUID
                    insert_dicts.append(d)
            else:
                # Auto-generate GUID for new records without GUID
                d['guid'] = uuid.uuid4()
                insert_dicts.append(d)
        
        # Handle inserts
        inserted_count = 0
        if insert_dicts:
            insert_stmt = insert(Assembly).values(insert_dicts)
            insert_result = await session.execute(insert_stmt)
            inserted_count = len(insert_dicts)
        
        # Handle updates
        updated_count = 0
        for update_dict in update_dicts:
            guid = update_dict.pop('guid')
            update_stmt = update(Assembly).where(Assembly.guid == guid).values(**update_dict)
            update_result = await session.execute(update_stmt)
            updated_count += update_result.rowcount
        
        await session.commit()
        return {"inserted": inserted_count, "updated": updated_count}
    
    @staticmethod
    async def sync_pieces(pieces_data: List[PieceCreate], company_guid: uuid.UUID, session: AsyncSession) -> Dict[str, int]:
        """Sync pieces for a company."""
        # Convert company_guid to UUID if it's a string
        if isinstance(company_guid, str):
            company_guid = uuid.UUID(company_guid)
        
        # Collect all referenced GUIDs for validation
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
        
        # Get valid project GUIDs
        valid_project_guids = set()
        if project_guids:
            query = select(Project.guid).where(
                Project.guid.in_(project_guids),
                Project.company_guid == company_guid
            )
            result = await session.execute(query)
            valid_project_guids = {str(row[0]).lower() for row in result.all()}
        
        # Get valid component GUIDs
        valid_component_guids = set()
        if component_guids:
            query = select(Component.guid).where(
                Component.guid.in_(component_guids),
                Component.company_guid == company_guid
            )
            result = await session.execute(query)
            valid_component_guids = {str(row[0]).lower() for row in result.all()}
        
        # Get valid assembly GUIDs
        valid_assembly_guids = set()
        if assembly_guids:
            query = select(Assembly.guid).where(
                Assembly.guid.in_(assembly_guids),
                Assembly.company_guid == company_guid
            )
            result = await session.execute(query)
            valid_assembly_guids = {str(row[0]).lower() for row in result.all()}
        
        # Validate all pieces
        for i, piece in enumerate(pieces_data):
            # Validate company_guid
            if piece.company_guid is not None and piece.company_guid != company_guid:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Piece at index {i} has company_guid that doesn't match the authenticated user's company"
                )
            
            # Validate project_guid
            if piece.project_guid and str(piece.project_guid).lower() not in valid_project_guids:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Piece at index {i} references a project that doesn't exist or doesn't belong to your company"
                )
            
            # Validate component_guid
            if piece.component_guid and str(piece.component_guid).lower() not in valid_component_guids:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Piece at index {i} references a component that doesn't exist or doesn't belong to your company"
                )
            
            # Validate assembly_guid if provided
            if piece.assembly_guid and str(piece.assembly_guid).lower() not in valid_assembly_guids:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Piece at index {i} references an assembly that doesn't exist or doesn't belong to your company"
                )
        
        # Check for duplicate GUIDs in the input data
        guid_set = set()
        for i, piece in enumerate(pieces_data):
            if piece.guid:
                if piece.guid in guid_set:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"Duplicate GUID found in input data: {piece.guid}"
                    )
                guid_set.add(piece.guid)
        
        # Check which GUIDs already exist in the database
        existing_guids = set()
        if guid_set:
            query = select(Piece.guid).where(Piece.guid.in_(guid_set))
            result = await session.execute(query)
            existing_guids = {row[0] for row in result.all()}
        
        # Convert PieceCreate objects to dicts
        insert_dicts = []
        update_dicts = []
        
        for p in pieces_data:
            d = p.dict()
            d['company_guid'] = company_guid
            
            # If guid is provided, we need to determine if this is an insert or update
            if p.guid:
                if p.guid in existing_guids:
                    # This is an update
                    update_dicts.append(d)
                else:
                    # This is a new record with provided GUID
                    insert_dicts.append(d)
            else:
                # Auto-generate GUID for new records without GUID
                d['guid'] = uuid.uuid4()
                insert_dicts.append(d)
        
        # Handle inserts
        inserted_count = 0
        if insert_dicts:
            insert_stmt = insert(Piece).values(insert_dicts)
            insert_result = await session.execute(insert_stmt)
            inserted_count = len(insert_dicts)
        
        # Handle updates
        updated_count = 0
        for update_dict in update_dicts:
            guid = update_dict.pop('guid')
            update_stmt = update(Piece).where(Piece.guid == guid).values(**update_dict)
            update_result = await session.execute(update_stmt)
            updated_count += update_result.rowcount
        
        await session.commit()
        return {"inserted": inserted_count, "updated": updated_count}
    
    @staticmethod
    async def sync_articles(articles_data: List[ArticleCreate], company_guid: uuid.UUID, session: AsyncSession) -> Dict[str, int]:
        """Sync articles for a company."""
        # Convert company_guid to UUID if it's a string
        if isinstance(company_guid, str):
            company_guid = uuid.UUID(company_guid)
        
        # First, collect all project and component GUIDs referenced by the articles
        project_guids = set()
        component_guids = set()
        
        for article in articles_data:
            if article.project_guid:
                project_guids.add(article.project_guid)
            if article.component_guid:
                component_guids.add(article.component_guid)
        
        # Get valid project GUIDs
        valid_project_guids = set()
        if project_guids:
            query = select(Project.guid).where(
                Project.guid.in_(project_guids),
                Project.company_guid == company_guid
            )
            result = await session.execute(query)
            valid_project_guids = {str(row[0]).lower() for row in result.all()}
        
        # Get valid component GUIDs
        valid_component_guids = set()
        if component_guids:
            query = select(Component.guid).where(
                Component.guid.in_(component_guids),
                Component.company_guid == company_guid
            )
            result = await session.execute(query)
            valid_component_guids = {str(row[0]).lower() for row in result.all()}
        
        # Validate all articles
        for i, article in enumerate(articles_data):
            # Validate company_guid
            if article.company_guid is not None and article.company_guid != company_guid:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Article at index {i} has company_guid that doesn't match the authenticated user's company"
                )
            
            # Validate project_guid
            if article.project_guid and str(article.project_guid).lower() not in valid_project_guids:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Article at index {i} references a project that doesn't exist or doesn't belong to your company"
                )
            
            # Validate component_guid
            if article.component_guid and str(article.component_guid).lower() not in valid_component_guids:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Article at index {i} references a component that doesn't exist or doesn't belong to your company"
                )
        
        # Check for duplicate GUIDs in the input data
        guid_set = set()
        for i, article in enumerate(articles_data):
            if article.guid:
                if article.guid in guid_set:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"Duplicate GUID found in input data: {article.guid}"
                    )
                guid_set.add(article.guid)
        
        # Check which GUIDs already exist in the database
        existing_guids = set()
        if guid_set:
            query = select(Article.guid).where(Article.guid.in_(guid_set))
            result = await session.execute(query)
            existing_guids = {row[0] for row in result.all()}
        
        # Convert ArticleCreate objects to dicts
        insert_dicts = []
        update_dicts = []
        
        for a in articles_data:
            d = a.dict()
            d['company_guid'] = company_guid
            
            # If guid is provided, we need to determine if this is an insert or update
            if a.guid:
                if a.guid in existing_guids:
                    # This is an update
                    update_dicts.append(d)
                else:
                    # This is a new record with provided GUID
                    insert_dicts.append(d)
            else:
                # Auto-generate GUID for new records without GUID
                d['guid'] = uuid.uuid4()
                insert_dicts.append(d)
        
        # Handle inserts
        inserted_count = 0
        if insert_dicts:
            insert_stmt = insert(Article).values(insert_dicts)
            insert_result = await session.execute(insert_stmt)
            inserted_count = len(insert_dicts)
        
        # Handle updates
        updated_count = 0
        for update_dict in update_dicts:
            guid = update_dict.pop('guid')
            update_stmt = update(Article).where(Article.guid == guid).values(**update_dict)
            update_result = await session.execute(update_stmt)
            updated_count += update_result.rowcount
        
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