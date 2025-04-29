"""remove_created_date_columns

Revision ID: 5fe38ef5ec6e
Revises: 1e0c0be8ce63
Create Date: 2024-04-28 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5fe38ef5ec6e'
down_revision = '1e0c0be8ce63'  # Previous head revision
branch_labels = None
depends_on = None


def upgrade():
    # Remove created_date column from articles table
    op.drop_column('articles', 'created_date')
    
    # Remove created_date column from components table
    op.drop_column('components', 'created_date')
    
    # Remove created_date column from pieces table
    op.drop_column('pieces', 'created_date')


def downgrade():
    # Add created_date column back to articles table
    op.add_column('articles',
        sa.Column('created_date', sa.DateTime(timezone=True), nullable=False)
    )
    
    # Add created_date column back to components table
    op.add_column('components',
        sa.Column('created_date', sa.DateTime(timezone=True), nullable=False)
    )
    
    # Add created_date column back to pieces table
    op.add_column('pieces',
        sa.Column('created_date', sa.DateTime(timezone=True), nullable=False)
    ) 