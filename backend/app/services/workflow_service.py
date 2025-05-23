from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, and_, between
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime

from app.models.workflow import Workflow
from app.models.company import Company
from app.models.workstation import Workstation
from app.models.user import User
from app.models.enums import WorkflowActionType


class WorkflowService:
    """Service for handling workflow entries."""

    @staticmethod
    async def create_workflow_entry(
        action_type: WorkflowActionType,
        company_guid: uuid.UUID,
        workstation_guid: Optional[uuid.UUID] = None,
        user_guid: Optional[uuid.UUID] = None,
        api_key_guid: Optional[uuid.UUID] = None,
        action_value: Optional[str] = None,
        session: AsyncSession = None
    ) -> Workflow:
        """
        Create a new workflow entry.
        
        Args:
            action_type: Type of action (must be a valid WorkflowActionType)
            company_guid: UUID of the company
            workstation_guid: Optional UUID of the workstation
            user_guid: Optional UUID of the user
            api_key_guid: Optional UUID of the API key
            action_value: Optional additional data for the action
            session: SQLAlchemy AsyncSession
            
        Returns:
            The created workflow entry
        """
        # Create a new workflow entry
        workflow_entry = Workflow(
            action_type=action_type,
            company_guid=company_guid,
            workstation_guid=workstation_guid,
            user_guid=user_guid,
            api_key_guid=api_key_guid,
            action_value=action_value
        )
        
        # Populate related names if the related entities exist
        if company_guid:
            company_stmt = select(Company).where(Company.guid == company_guid)
            company = (await session.execute(company_stmt)).scalar_one_or_none()
            if company:
                workflow_entry.company_name = company.name
        
        if workstation_guid:
            workstation_stmt = select(Workstation).where(Workstation.guid == workstation_guid)
            workstation = (await session.execute(workstation_stmt)).scalar_one_or_none()
            if workstation:
                workflow_entry.workstation_name = workstation.location
        
        if user_guid:
            user_stmt = select(User).where(User.guid == user_guid)
            user = (await session.execute(user_stmt)).scalar_one_or_none()
            if user:
                user_name = ""
                if user.name:
                    user_name += user.name
                if user.surname:
                    if user_name:
                        user_name += " "
                    user_name += user.surname
                if not user_name:
                    user_name = user.email
                workflow_entry.user_name = user_name
        
        # Add to session and flush
        session.add(workflow_entry)
        await session.flush()
        
        return workflow_entry

    @staticmethod
    async def get_workflow_entries(
        company_guid: uuid.UUID,
        action_type: Optional[WorkflowActionType] = None,
        workstation_guid: Optional[uuid.UUID] = None,
        user_guid: Optional[uuid.UUID] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0,
        session: AsyncSession = None
    ) -> List[Workflow]:
        """
        Get workflow entries with optional filtering.
        
        Args:
            company_guid: UUID of the company
            action_type: Optional filter by action type
            workstation_guid: Optional filter by workstation
            user_guid: Optional filter by user
            start_date: Optional filter by start date
            end_date: Optional filter by end date
            limit: Maximum number of entries to return
            offset: Offset for pagination
            session: SQLAlchemy AsyncSession
            
        Returns:
            List of workflow entries
        """
        # Build query with filters
        query = select(Workflow).where(Workflow.company_guid == company_guid)
        
        if action_type:
            query = query.where(Workflow.action_type == action_type)
        
        if workstation_guid:
            query = query.where(Workflow.workstation_guid == workstation_guid)
        
        if user_guid:
            query = query.where(Workflow.user_guid == user_guid)
        
        if start_date and end_date:
            query = query.where(between(Workflow.created_at, start_date, end_date))
        elif start_date:
            query = query.where(Workflow.created_at >= start_date)
        elif end_date:
            query = query.where(Workflow.created_at <= end_date)
        
        # Order by created_at descending (newest first)
        query = query.order_by(Workflow.created_at.desc())
        
        # Apply pagination
        query = query.limit(limit).offset(offset)
        
        # Execute query
        result = await session.execute(query)
        workflow_entries = result.scalars().all()
        
        return list(workflow_entries)

    @staticmethod
    async def get_workflow_by_guid(
        guid: uuid.UUID,
        session: AsyncSession
    ) -> Optional[Workflow]:
        """
        Get a workflow entry by GUID.
        
        Args:
            guid: UUID of the workflow entry
            session: SQLAlchemy AsyncSession
            
        Returns:
            The workflow entry or None if not found
        """
        query = select(Workflow).where(Workflow.guid == guid)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_workflow_statistics(
        company_guid: uuid.UUID,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        session: AsyncSession = None
    ) -> Dict[str, Any]:
        """
        Get statistics about workflow entries.
        
        Args:
            company_guid: UUID of the company
            start_date: Optional filter by start date
            end_date: Optional filter by end date
            session: SQLAlchemy AsyncSession
            
        Returns:
            Dictionary with statistics
        """
        # Build base query with filters
        base_query = select(Workflow).where(Workflow.company_guid == company_guid)
        
        if start_date and end_date:
            base_query = base_query.where(between(Workflow.created_at, start_date, end_date))
        elif start_date:
            base_query = base_query.where(Workflow.created_at >= start_date)
        elif end_date:
            base_query = base_query.where(Workflow.created_at <= end_date)
        
        # Get total count
        count_query = select(func.count()).select_from(base_query.subquery())
        total_count = (await session.execute(count_query)).scalar() or 0
        
        # Get count by action type
        action_type_query = select(
            Workflow.action_type,
            func.count().label('count')
        ).where(
            Workflow.company_guid == company_guid
        )
        
        if start_date and end_date:
            action_type_query = action_type_query.where(between(Workflow.created_at, start_date, end_date))
        elif start_date:
            action_type_query = action_type_query.where(Workflow.created_at >= start_date)
        elif end_date:
            action_type_query = action_type_query.where(Workflow.created_at <= end_date)
            
        action_type_query = action_type_query.group_by(Workflow.action_type)
        
        action_type_result = await session.execute(action_type_query)
        count_by_action_type = {str(row[0]): row[1] for row in action_type_result}
        
        # Get count by workstation
        workstation_query = select(
            Workflow.workstation_guid,
            Workflow.workstation_name,
            func.count().label('count')
        ).where(
            and_(
                Workflow.company_guid == company_guid,
                Workflow.workstation_guid.isnot(None)
            )
        )
        
        if start_date and end_date:
            workstation_query = workstation_query.where(between(Workflow.created_at, start_date, end_date))
        elif start_date:
            workstation_query = workstation_query.where(Workflow.created_at >= start_date)
        elif end_date:
            workstation_query = workstation_query.where(Workflow.created_at <= end_date)
            
        workstation_query = workstation_query.group_by(Workflow.workstation_guid, Workflow.workstation_name)
        
        workstation_result = await session.execute(workstation_query)
        count_by_workstation = {str(row[1] or row[0]): row[2] for row in workstation_result}
        
        # Get count by user
        user_query = select(
            Workflow.user_guid,
            Workflow.user_name,
            func.count().label('count')
        ).where(
            and_(
                Workflow.company_guid == company_guid,
                Workflow.user_guid.isnot(None)
            )
        )
        
        if start_date and end_date:
            user_query = user_query.where(between(Workflow.created_at, start_date, end_date))
        elif start_date:
            user_query = user_query.where(Workflow.created_at >= start_date)
        elif end_date:
            user_query = user_query.where(Workflow.created_at <= end_date)
            
        user_query = user_query.group_by(Workflow.user_guid, Workflow.user_name)
        
        user_result = await session.execute(user_query)
        count_by_user = {str(row[1] or row[0]): row[2] for row in user_result}
        
        # Get most recent entry date
        most_recent_query = select(func.max(Workflow.created_at)).where(Workflow.company_guid == company_guid)
        most_recent = (await session.execute(most_recent_query)).scalar()
        
        return {
            "total_count": total_count,
            "count_by_action_type": count_by_action_type,
            "count_by_workstation": count_by_workstation,
            "count_by_user": count_by_user,
            "most_recent": most_recent
        } 