"""merge guid_conversion_and_updated_at_columns

Revision ID: a4c5f944fed8
Revises: 20250428001, add_missing_updated_at
Create Date: 2025-04-29 08:17:40.134630

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4c5f944fed8'
down_revision = ('20250428001', 'add_missing_updated_at')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass 