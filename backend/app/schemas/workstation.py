from pydantic import BaseModel, validator
from typing import Optional
import uuid
from datetime import datetime


class WorkstationBase(BaseModel):
    location: str
    type: str
    is_active: Optional[bool] = True

    @validator('type')
    def validate_type(cls, v):
        valid_types = ['Machine', 'Assembly', 'Control', 'Logistics', 'Supply']
        if v not in valid_types:
            raise ValueError(f'Type must be one of: {", ".join(valid_types)}')
        return v


class WorkstationCreate(WorkstationBase):
    company_guid: Optional[uuid.UUID] = None  # Will be set from JWT token


class WorkstationUpdate(BaseModel):
    location: Optional[str] = None
    type: Optional[str] = None
    is_active: Optional[bool] = None

    @validator('type')
    def validate_type(cls, v):
        if v is not None:
            valid_types = ['Machine', 'Assembly', 'Control', 'Logistics', 'Supply']
            if v not in valid_types:
                raise ValueError(f'Type must be one of: {", ".join(valid_types)}')
        return v


class WorkstationInDB(WorkstationBase):
    guid: uuid.UUID
    company_guid: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class WorkstationResponse(WorkstationInDB):
    pass 