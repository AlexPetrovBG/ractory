from pydantic import BaseModel, validator, Field
from typing import Optional, Literal
import uuid
from datetime import datetime
from enum import Enum

from ..models.enums import WorkstationType


class WorkstationBase(BaseModel):
    location: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Physical location of the workstation in the factory"
    )
    type: WorkstationType = Field(
        ...,
        description="Type of workstation that determines its role in the production process"
    )
    is_active: Optional[bool] = Field(
        True,
        description="Whether the workstation is currently active and available for use"
    )

    @validator('type')
    def validate_type(cls, v):
        valid_types = ['Machine', 'Assembly', 'Control', 'Logistics', 'Supply']
        if v not in valid_types:
            raise ValueError(f'Type must be one of: {", ".join(valid_types)}')
        return v


class WorkstationCreate(WorkstationBase):
    """
    Schema for creating a new workstation.
    If company_guid is not provided, it will be set from the authenticated user's company.
    """
    company_guid: Optional[uuid.UUID] = Field(
        None,
        description="Company GUID. If not provided, will be set from authenticated user's company"
    )


class WorkstationUpdate(BaseModel):
    """
    Schema for updating an existing workstation.
    Only provided fields will be updated.
    """
    location: Optional[str] = Field(
        None,
        min_length=3,
        max_length=100,
        description="New physical location of the workstation"
    )
    type: Optional[WorkstationType] = Field(
        None,
        description="New type of the workstation"
    )
    is_active: Optional[bool] = Field(
        None,
        description="Whether to activate or deactivate the workstation"
    )

    @validator('type')
    def validate_type(cls, v):
        if v is not None:
            valid_types = ['Machine', 'Assembly', 'Control', 'Logistics', 'Supply']
            if v not in valid_types:
                raise ValueError(f'Type must be one of: {", ".join(valid_types)}')
        return v


class WorkstationInDB(WorkstationBase):
    """
    Internal schema representing a workstation as stored in the database.
    Includes all system fields.
    """
    guid: uuid.UUID = Field(..., description="Unique identifier of the workstation")
    company_guid: uuid.UUID = Field(..., description="Company that owns this workstation")
    created_at: datetime = Field(..., description="When the workstation was created")
    updated_at: Optional[datetime] = Field(None, description="When the workstation was last updated")

    class Config:
        orm_mode = True


class WorkstationResponse(WorkstationInDB):
    """
    Schema for workstation responses in the API.
    Includes all fields that are safe to expose to clients.
    """
    pass 