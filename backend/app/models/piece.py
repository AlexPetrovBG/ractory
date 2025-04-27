from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, LargeBinary, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .base import Base

class Piece(Base):
    __tablename__ = "pieces"
    
    id = Column(Integer, primary_key=True) # From RaConnect
    piece_id = Column(String, nullable=False)
    outer_length = Column(Integer, nullable=True)
    angle_left = Column(Integer, nullable=True)
    angle_right = Column(Integer, nullable=True)
    orientation = Column(String, nullable=True)
    barcode = Column(String, nullable=True)
    assembly_width = Column(Integer, nullable=True)
    assembly_height = Column(Integer, nullable=True)
    trolley = Column(String, nullable=True)
    cell = Column(String, nullable=True)
    trolley_cell = Column(String, nullable=True)
    operations = Column(String, nullable=True)
    component_code = Column(String, nullable=True)
    component_description = Column(String, nullable=True)
    info2 = Column(String, nullable=True)
    info3 = Column(String, nullable=True)
    client = Column(String, nullable=True)
    dealer = Column(String, nullable=True)
    project_description = Column(String, nullable=True)
    inner_length = Column(Integer, nullable=True)
    reinforcement_code = Column(String, nullable=True)
    reinforcement_length = Column(Integer, nullable=True)
    hardware_info = Column(String, nullable=True)
    glass_info = Column(String, nullable=True)
    other_length = Column(Integer, nullable=True)
    project_number = Column(String, nullable=True)
    component_number = Column(String, nullable=True)
    water_handle = Column(String, nullable=True)
    segment_order = Column(String, nullable=True)
    cutting_pattern = Column(String, nullable=True)
    fixing_mode = Column(String, nullable=True)
    material_type = Column(String, nullable=True)
    project_code_parent = Column(String, nullable=True)
    bar_id = Column(String, nullable=True)
    bar_rest = Column(Integer, nullable=True)
    bar_length = Column(Integer, nullable=True)
    bar_cutting_tolerance = Column(Integer, nullable=True)
    profile_code = Column(String, nullable=True)
    profile_name = Column(String, nullable=True)
    lamination = Column(String, nullable=True)
    gasket = Column(String, nullable=True)
    profile_width = Column(Integer, nullable=True)
    profile_height = Column(Integer, nullable=True)
    welding_tolerance = Column(Integer, nullable=True)
    profile_color = Column(String, nullable=True)
    profile_type_ra = Column(String, nullable=True)
    profile_type = Column(String, nullable=True)
    trolley_size = Column(String, nullable=True)
    profile_code_with_color = Column(String, nullable=True)
    id_project = Column(Integer, ForeignKey("projects.id"), nullable=False)
    id_component = Column(Integer, ForeignKey("components.id"), nullable=False)
    id_assembly = Column(Integer, ForeignKey("assemblies.id"), nullable=False)
    created_date = Column(DateTime(timezone=True), nullable=False)
    parent_assembly_trolley_cell = Column(String, nullable=True)
    mullion_trolley_cell = Column(String, nullable=True)
    glazing_bead_trolley_cell = Column(String, nullable=True)
    picture = Column(LargeBinary, nullable=True)
    project_phase = Column(String, nullable=True)
    company_guid = Column(UUID(as_uuid=True), ForeignKey("companies.guid"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    project = relationship("Project") # Direct relation needed?
    component = relationship("Component") # Direct relation needed?
    assembly = relationship("Assembly", back_populates="pieces")
    
    def __repr__(self):
        return f"<Piece id={self.id}, piece_id={self.piece_id}>" 