"""Fix API keys table schema

Revision ID: fix_api_keys_table
Revises: a4c5f944fed8
Create Date: 2025-05-02 05:13:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fix_api_keys_table'
down_revision = 'a4c5f944fed8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop old API keys table
    op.drop_table('api_keys')
    
    # Create new API keys table with correct schema
    op.create_table('api_keys',
        sa.Column('guid', sa.UUID(), nullable=False),
        sa.Column('company_guid', sa.UUID(), nullable=False),
        sa.Column('key_hash', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('scopes', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('last_used_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['company_guid'], ['companies.guid'], ),
        sa.PrimaryKeyConstraint('guid'),
        sa.UniqueConstraint('key_hash')
    )
    
    # Create trigger for updated_at
    op.execute("""
        CREATE TRIGGER api_keys_updated_at_trigger
        BEFORE UPDATE ON api_keys
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();
    """)


def downgrade() -> None:
    # Drop trigger
    op.execute("DROP TRIGGER IF EXISTS api_keys_updated_at_trigger ON api_keys;")
    
    # Drop new API keys table
    op.drop_table('api_keys')
    
    # Recreate old API keys table
    op.create_table('api_keys',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('company_guid', sa.UUID(), nullable=False),
        sa.Column('key_hash', sa.String(length=64), nullable=False),
        sa.Column('scope', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('last_used', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['company_guid'], ['companies.guid'], ),
        sa.PrimaryKeyConstraint('id')
    ) 