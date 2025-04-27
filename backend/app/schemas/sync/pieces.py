from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

class PieceBase(BaseModel):
    """Base schema for Piece fields."""
    piece_id: str
    id_project: int
    id_component: int
    id_assembly: int
    barcode: Optional[str] = None
    outer_length: Optional[int] = None
    angle_left: Optional[int] = None
    angle_right: Optional[int] = None
    
class PieceCreate(PieceBase):
    """Schema for creating a Piece."""
    id: int
    created_date: datetime
    # Including all optional fields
    orientation: Optional[str] = None
    assembly_width: Optional[int] = None
    assembly_height: Optional[int] = None
    trolley: Optional[str] = None
    cell: Optional[str] = None
    trolley_cell: Optional[str] = None
    operations: Optional[str] = None
    component_code: Optional[str] = None
    component_description: Optional[str] = None
    info2: Optional[str] = None
    info3: Optional[str] = None
    client: Optional[str] = None
    dealer: Optional[str] = None
    project_description: Optional[str] = None
    inner_length: Optional[int] = None
    reinforcement_code: Optional[str] = None
    reinforcement_length: Optional[int] = None
    hardware_info: Optional[str] = None
    glass_info: Optional[str] = None
    other_length: Optional[int] = None
    project_number: Optional[str] = None
    component_number: Optional[str] = None
    water_handle: Optional[str] = None
    segment_order: Optional[str] = None
    cutting_pattern: Optional[str] = None
    fixing_mode: Optional[str] = None
    material_type: Optional[str] = None
    project_code_parent: Optional[str] = None
    bar_id: Optional[str] = None
    bar_rest: Optional[int] = None
    bar_length: Optional[int] = None
    bar_cutting_tolerance: Optional[int] = None
    profile_code: Optional[str] = None
    profile_name: Optional[str] = None
    lamination: Optional[str] = None
    gasket: Optional[str] = None
    profile_width: Optional[int] = None
    profile_height: Optional[int] = None
    welding_tolerance: Optional[int] = None
    profile_color: Optional[str] = None
    profile_type_ra: Optional[str] = None
    profile_type: Optional[str] = None
    trolley_size: Optional[str] = None
    profile_code_with_color: Optional[str] = None
    parent_assembly_trolley_cell: Optional[str] = None
    mullion_trolley_cell: Optional[str] = None
    glazing_bead_trolley_cell: Optional[str] = None
    picture: Optional[bytes] = None
    project_phase: Optional[str] = None
    company_guid: Optional[str] = None  # Will be set from token if not provided

class PieceBulkInsert(BaseModel):
    """Schema for bulk inserting Pieces."""
    pieces: List[PieceCreate]

class PieceResponse(PieceBase):
    """Schema for Piece responses."""
    id: int
    company_guid: str
    created_at: datetime

    class Config:
        orm_mode = True 