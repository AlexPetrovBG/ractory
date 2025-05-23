"""merge_heads

Revision ID: f89e50d73d47
Revises: 20250501_001, fix_api_keys_table
Create Date: 2025-05-02 08:41:51.980766

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f89e50d73d47'
down_revision = ('20250501_001', 'fix_api_keys_table')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass 