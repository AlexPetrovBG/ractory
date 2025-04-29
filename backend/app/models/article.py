from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base

class Article(Base):
    __tablename__ = "articles"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False)
    designation = Column(String, nullable=True)
    consume_group_designation = Column(String, nullable=True)
    consume_group_priority = Column(Integer, nullable=True)
    quantity = Column(Float, nullable=True)
    unit = Column(String, nullable=True)
    category_designation = Column(String, nullable=True)
    position = Column(String, nullable=True)
    short_position = Column(String, nullable=True)
    code_no_color = Column(String, nullable=True)
    component_code = Column(String, nullable=True)
    is_extra = Column(Boolean, nullable=True)
    length = Column(Float, nullable=True)
    width = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    surface = Column(Float, nullable=True)
    angle1 = Column(Float, nullable=True)
    angle2 = Column(Float, nullable=True)
    unit_weight = Column(Float, nullable=True)
    bar_length = Column(Float, nullable=True)
    id_project = Column(Integer, ForeignKey('projects.id'), nullable=False)
    id_component = Column(Integer, ForeignKey('components.id'), nullable=False)
    company_guid = Column(UUID(as_uuid=True), ForeignKey('companies.guid'), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=True)

    # Define relationships
    project = relationship("Project", back_populates="articles")
    component = relationship("Component", back_populates="articles")
    company = relationship("Company", back_populates="articles")

    def __repr__(self):
        return f"<Article(id={self.id}, code='{self.code}')>" 