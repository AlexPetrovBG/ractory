from pydantic import BaseModel, UUID4, Field, validator
from typing import List, Optional, Union
from datetime import datetime
import uuid

from app.models.enums import WorkflowActionType


class WorkflowBase(BaseModel):
    """Base schema for workflow entries."""
    action_type: WorkflowActionType
    action_value: Optional[str] = None
    workstation_guid: Optional[UUID4] = None
    user_guid: Optional[UUID4] = None
    api_key_guid: Optional[UUID4] = None


class WorkflowCreate(WorkflowBase):
    """Schema for creating a new workflow entry."""
    company_guid: Optional[UUID4] = None  # Optional as it can be derived from the authenticated user


class WorkflowResponse(WorkflowBase):
    """Schema for workflow entry response."""
    guid: UUID4
    company_guid: UUID4
    company_name: Optional[str] = None
    workstation_name: Optional[str] = None
    user_name: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class WorkflowList(BaseModel):
    """Schema for a list of workflow entries."""
    workflows: List[WorkflowResponse]


class WorkflowFilter(BaseModel):
    """Schema for filtering workflow entries."""
    action_type: Optional[WorkflowActionType] = None
    workstation_guid: Optional[UUID4] = None
    user_guid: Optional[UUID4] = None
    company_guid: Optional[UUID4] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: Optional[int] = Field(default=100, ge=1, le=1000)
    offset: Optional[int] = Field(default=0, ge=0)

    @validator('end_date')
    def end_date_must_be_after_start_date(cls, v, values):
        if v and 'start_date' in values and values['start_date'] is not None:
            if v < values['start_date']:
                raise ValueError("end_date must be after start_date")
        return v


class WorkflowStatistics(BaseModel):
    """Schema for workflow statistics."""
    total_count: int
    count_by_action_type: dict
    count_by_workstation: Optional[dict] = None
    count_by_user: Optional[dict] = None
    most_recent: Optional[datetime] = None 