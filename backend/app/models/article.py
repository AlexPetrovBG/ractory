import uuid
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy as sa

from app.core.database import Base

class Article(Base):
    """Article model representing data synced from RaWorkshop."""
    __tablename__ = "articles"

    guid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_id = Column(Integer, nullable=False, index=True, comment="RaWorkshop ID")
    company_guid = Column(UUID(as_uuid=True), ForeignKey("companies.guid"), nullable=False, index=True)
    
    code = Column(String, index=True, comment="Article code identifier")
    designation = Column(String, comment="Name or description of the article")
    consume_group_designation = Column(String, comment="Designation of the consumption group")
    consume_group_priority = Column(Integer, comment="Priority within the consumption group")
    quantity = Column(Float, comment="Quantity of articles")
    unit = Column(String, comment="Unit of measurement")
    category_designation = Column(String, comment="Category of the article")
    position = Column(String, comment="Position information")
    short_position = Column(String, comment="Abbreviated position information")
    code_no_color = Column(String, comment="Code without color information")
    component_code = Column(String, comment="Code of the related component")
    is_extra = Column(Boolean, comment="Flag indicating if this is an extra article")
    
    # Measurements
    length = Column(Float, comment="Length measurement")
    width = Column(Float, comment="Width measurement")
    height = Column(Float, comment="Height measurement")
    surface = Column(Float, comment="Surface area")
    angle1 = Column(Float, comment="First angle measurement")
    angle2 = Column(Float, comment="Second angle measurement")
    unit_weight = Column(Float, comment="Weight per unit")
    bar_length = Column(Float, comment="Length of bar")
    
    # Relationships
    id_project = Column(Integer, ForeignKey("projects.original_id"), index=True, nullable=True, comment="Foreign key to Projects.Id")
    id_component = Column(Integer, ForeignKey("components.original_id"), index=True, nullable=True, comment="Foreign key to Components.Id")
    
    # Metadata
    created_date = Column(DateTime(timezone=True), comment="When the article was created")
    modified_date = Column(DateTime(timezone=True), comment="When the article was last modified")
    synced_at = Column(DateTime(timezone=True), server_default=func.now(), comment="When the article was last synced")
    
    # Add unique constraint on original_id and company_guid
    __table_args__ = (sa.UniqueConstraint('original_id', 'company_guid', name='uq_article_original_id_company'),)

    def __repr__(self):
        return f"<Article {self.code or self.original_id} (Project: {self.id_project}, Company: {self.company_guid})>" 