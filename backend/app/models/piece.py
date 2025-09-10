import uuid
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, ForeignKey, UniqueConstraint, LargeBinary, func
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy as sa

from app.core.database import Base
from .base import TimestampMixin

class Piece(Base, TimestampMixin):
    """Piece model representing data synced from RaWorkshop."""
    __tablename__ = "pieces"

    # Using original ID from RaWorkshop + company_guid as composite PK might be better,
    # but for simplicity, using a separate UUID PK for now.
    guid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_id = Column(Integer, nullable=False, index=True) # RaWorkshop ID
    company_guid = Column(UUID(as_uuid=True), ForeignKey("companies.guid"), nullable=False, index=True)
    
    # Identification
    piece_id = Column(String, comment="Unique identifier for the piece")
    barcode = Column(String, index=True, comment="Barcode identifier for tracking")
    
    # Dimensions
    outer_length = Column(Integer, comment="Outer length dimension")
    inner_length = Column(Integer, comment="Inner length dimension")
    angle_left = Column(Integer, comment="Left angle measurement")
    angle_right = Column(Integer, comment="Right angle measurement")
    orientation = Column(String, comment="Orientation of the piece")
    assembly_width = Column(Integer, comment="Width when assembled")
    assembly_height = Column(Integer, comment="Height when assembled")
    
    # Trolley information
    trolley = Column(String, comment="Trolley identifier")
    cell = Column(String, comment="Cell identifier")
    trolley_cell = Column(String, comment="Combined trolley and cell reference")
    trolley_size = Column(String, comment="Size of the trolley")
    parent_assembly_trolley_cell = Column(String, comment="Trolley cell of parent assembly")
    mullion_trolley_cell = Column(String, comment="Trolley cell for mullion")
    glazing_bead_trolley_cell = Column(String, comment="Trolley cell for glazing bead")
    
    # Manufacturing details
    operations = Column(String, comment="Operations to perform on the piece")
    component_code = Column(String, comment="Code of the component this piece belongs to")
    component_description = Column(String, comment="Description of the component")
    info2 = Column(String, comment="Additional information field 2")
    info3 = Column(String, comment="Additional information field 3")
    client = Column(String, comment="Client information")
    dealer = Column(String, comment="Dealer information")
    project_description = Column(String, comment="Description of the associated project")
    project_phase = Column(String, comment="Current phase of the project")
    
    # Material details
    reinforcement_code = Column(String, comment="Code for reinforcement material")
    reinforcement_length = Column(Integer, comment="Length of reinforcement")
    hardware_info = Column(String, comment="Information about hardware components")
    glass_info = Column(String, comment="Information about glass components")
    other_length = Column(Integer, comment="Additional length measurement")
    project_number = Column(String, comment="Project number reference")
    component_number = Column(String, comment="Component number reference")
    water_handle = Column(String, comment="Water handle information")
    segment_order = Column(String, comment="Order of segments")
    cutting_pattern = Column(String, comment="Pattern used for cutting")
    fixing_mode = Column(String, comment="Method of fixing/mounting")
    material_type = Column(String, comment="Type of material")
    project_code_parrent = Column(String, comment="Parent project code")
    
    # Bar information
    bar_id = Column(String, comment="Bar identifier")
    bar_rest = Column(Integer, comment="Remaining bar material")
    bar_length = Column(Integer, comment="Length of bar")
    bar_cutting_tolerance = Column(Integer, comment="Tolerance for cutting bars")
    
    # Profile information
    profile_code = Column(String, comment="Code for the profile")
    profile_name = Column(String, comment="Name of the profile")
    lamination = Column(String, comment="Lamination information")
    gasket = Column(String, comment="Gasket information")
    profile_width = Column(Integer, comment="Width of the profile")
    profile_height = Column(Integer, comment="Height of the profile")
    welding_tolerance = Column(Integer, comment="Tolerance for welding")
    profile_color = Column(String, comment="Color of the profile")
    profile_type_ra = Column(String, comment="Type of profile (Ra specific)")
    profile_type = Column(String, comment="General type of profile")
    profile_code_with_color = Column(String, comment="Profile code including color information")
    
    # Relationships
    id_project = Column(Integer, ForeignKey("projects.original_id"), index=True, comment="Foreign key to Projects.Id")
    id_component = Column(Integer, ForeignKey("components.original_id"), index=True, comment="Foreign key to Components.Id")
    id_assembly = Column(Integer, ForeignKey("assemblies.original_id"), index=True, comment="Foreign key to Assemblies.Id")
    
    # Metadata
    created_date = Column(DateTime(timezone=True), comment="When the piece was created")
    synced_at = Column(DateTime(timezone=True), server_default=func.now(), comment="When the piece was last synced")
    picture = Column(LargeBinary, comment="Visual representation of the piece")
    
    # Add unique constraint on original_id and company_guid
    __table_args__ = (sa.UniqueConstraint('original_id', 'company_guid', name='uq_piece_original_id_company'),)

    def __repr__(self):
        return f"<Piece {self.barcode or self.piece_id or self.original_id} (Company: {self.company_guid})>" 