"""Standardize timestamp columns

Revision ID: standardize_timestamps
Revises: 5fe38ef5ec6e
Create Date: 2024-04-28 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'standardize_timestamps'
down_revision = '5fe38ef5ec6e'  # Previous migration
branch_labels = None
depends_on = None

def upgrade():
    # 1. Rename modified_date to updated_at in articles table
    op.alter_column('articles', 'modified_date',
                    new_column_name='updated_at',
                    existing_type=postgresql.TIMESTAMP(timezone=True),
                    nullable=True)
    
    # 2. Convert timestamp without time zone to timestamp with time zone
    # Companies table
    op.alter_column('companies', 'created_at',
                    type_=postgresql.TIMESTAMP(timezone=True),
                    existing_type=postgresql.TIMESTAMP(timezone=False),
                    postgresql_using='created_at AT TIME ZONE \'UTC\'')
    
    op.alter_column('companies', 'updated_at',
                    type_=postgresql.TIMESTAMP(timezone=True),
                    existing_type=postgresql.TIMESTAMP(timezone=False),
                    postgresql_using='updated_at AT TIME ZONE \'UTC\'')

def downgrade():
    # Convert timestamp with time zone back to timestamp without time zone
    op.alter_column('companies', 'created_at',
                    type_=postgresql.TIMESTAMP(timezone=False),
                    existing_type=postgresql.TIMESTAMP(timezone=True),
                    postgresql_using='created_at AT TIME ZONE \'UTC\'')
    
    op.alter_column('companies', 'updated_at',
                    type_=postgresql.TIMESTAMP(timezone=False),
                    existing_type=postgresql.TIMESTAMP(timezone=True),
                    postgresql_using='updated_at AT TIME ZONE \'UTC\'')
    
    # Rename updated_at back to modified_date in articles table
    op.alter_column('articles', 'updated_at',
                    new_column_name='modified_date',
                    existing_type=postgresql.TIMESTAMP(timezone=True),
                    nullable=True) 