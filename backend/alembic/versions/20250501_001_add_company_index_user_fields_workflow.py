"""Add company index, user fields, and workflow table

Revision ID: 20250501_001
Revises: a4c5f944fed8
Create Date: 2025-05-01 14:31:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20250501_001'
down_revision = 'a4c5f944fed8'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Add company_index to companies table
    op.add_column('companies', sa.Column('company_index', sa.Integer(), nullable=True))
    op.create_check_constraint('company_index_range', 'companies', 'company_index >= 0 AND company_index <= 99')
    op.create_unique_constraint('uq_company_index', 'companies', ['company_index'])

    # Add new columns to users table
    op.add_column('users', sa.Column('name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('surname', sa.String(), nullable=True))
    op.add_column('users', sa.Column('picture_path', sa.String(), nullable=True))

    # Create workflow table
    op.create_table('workflow',
        sa.Column('guid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('company_guid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('company_name', sa.String(), nullable=True),
        sa.Column('workstation_guid', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('workstation_name', sa.String(), nullable=True),
        sa.Column('api_key_guid', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('user_guid', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('user_name', sa.String(), nullable=True),
        sa.Column('action_type', sa.String(), nullable=False),  # Using String instead of Enum
        sa.Column('action_value', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['company_guid'], ['companies.guid'], ),
        sa.ForeignKeyConstraint(['workstation_guid'], ['workstations.guid'], ),
        sa.ForeignKeyConstraint(['user_guid'], ['users.guid'], ),
        sa.PrimaryKeyConstraint('guid')
    )

    # Create indexes for better query performance
    op.create_index('ix_workflow_company_guid', 'workflow', ['company_guid'])
    op.create_index('ix_workflow_workstation_guid', 'workflow', ['workstation_guid'])
    op.create_index('ix_workflow_user_guid', 'workflow', ['user_guid'])
    op.create_index('ix_workflow_action_type', 'workflow', ['action_type'])
    op.create_index('ix_workflow_created_at', 'workflow', ['created_at'])

def downgrade() -> None:
    # Drop workflow table and its indexes
    op.drop_table('workflow')

    # Remove user columns
    op.drop_column('users', 'picture_path')
    op.drop_column('users', 'surname')
    op.drop_column('users', 'name')

    # Remove company_index
    op.drop_constraint('uq_company_index', 'companies')
    op.drop_constraint('company_index_range', 'companies')
    op.drop_column('companies', 'company_index') 