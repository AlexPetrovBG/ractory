"""allow_null_updated_at

Revision ID: 6739ad986e80
Revises: f89e50d73d47
Create Date: 2025-05-02 08:45:23.123456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6739ad986e80'
down_revision = 'f89e50d73d47'
branch_labels = None
depends_on = None


def upgrade():
    # Drop NOT NULL constraint from updated_at columns
    tables = [
        'companies', 'api_keys', 'articles', 'assemblies', 'components',
        'pieces', 'projects', 'ui_templates', 'users', 'workflow', 'workstations'
    ]
    
    for table in tables:
        op.alter_column(table, 'updated_at',
                       existing_type=sa.DateTime(timezone=True),
                       nullable=True)


def downgrade():
    # Restore NOT NULL constraint to updated_at columns
    tables = [
        'companies', 'api_keys', 'articles', 'assemblies', 'components',
        'pieces', 'projects', 'ui_templates', 'users', 'workflow', 'workstations'
    ]
    
    # First update any NULL values to created_at
    for table in tables:
        op.execute(f"UPDATE {table} SET updated_at = created_at WHERE updated_at IS NULL")
        op.alter_column(table, 'updated_at',
                       existing_type=sa.DateTime(timezone=True),
                       nullable=False) 