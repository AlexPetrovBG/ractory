"""Convert to GUIDs and make assembly optional

Revision ID: 20250428001
Revises: standardize_timestamps
Create Date: 2025-04-28 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '20250428001'
down_revision = 'standardize_timestamps'  # Updated to point to the last migration
branch_labels = None
depends_on = None

def upgrade():
    # First drop all data from related tables
    op.execute("TRUNCATE TABLE pieces, assemblies, components, articles, projects CASCADE;")
    
    # Drop existing foreign key constraints
    op.drop_constraint('pieces_id_assembly_fkey', 'pieces')
    op.drop_constraint('pieces_id_component_fkey', 'pieces')
    op.drop_constraint('pieces_id_project_fkey', 'pieces')
    op.drop_constraint('assemblies_id_component_fkey', 'assemblies')
    op.drop_constraint('assemblies_id_project_fkey', 'assemblies')
    op.drop_constraint('components_id_project_fkey', 'components')
    op.drop_constraint('articles_id_component_fkey', 'articles')
    op.drop_constraint('articles_id_project_fkey', 'articles')

    # Add GUID columns
    op.add_column('projects', sa.Column('guid', UUID(), nullable=True))
    op.add_column('components', sa.Column('guid', UUID(), nullable=True))
    op.add_column('assemblies', sa.Column('guid', UUID(), nullable=True))
    op.add_column('pieces', sa.Column('guid', UUID(), nullable=True))
    op.add_column('articles', sa.Column('guid', UUID(), nullable=True))

    # Add new foreign key reference columns
    op.add_column('components', sa.Column('project_guid', UUID(), nullable=True))
    op.add_column('assemblies', sa.Column('project_guid', UUID(), nullable=True))
    op.add_column('assemblies', sa.Column('component_guid', UUID(), nullable=True))
    op.add_column('pieces', sa.Column('project_guid', UUID(), nullable=True))
    op.add_column('pieces', sa.Column('component_guid', UUID(), nullable=True))
    op.add_column('pieces', sa.Column('assembly_guid', UUID(), nullable=True))
    op.add_column('articles', sa.Column('project_guid', UUID(), nullable=True))
    op.add_column('articles', sa.Column('component_guid', UUID(), nullable=True))

    # Make GUIDs not nullable
    op.alter_column('projects', 'guid', nullable=False)
    op.alter_column('components', 'guid', nullable=False)
    op.alter_column('assemblies', 'guid', nullable=False)
    op.alter_column('pieces', 'guid', nullable=False)
    op.alter_column('articles', 'guid', nullable=False)

    # Make foreign key references not nullable (except assembly_guid for pieces)
    op.alter_column('components', 'project_guid', nullable=False)
    op.alter_column('assemblies', 'project_guid', nullable=False)
    op.alter_column('assemblies', 'component_guid', nullable=False)
    op.alter_column('pieces', 'project_guid', nullable=False)
    op.alter_column('pieces', 'component_guid', nullable=False)
    op.alter_column('articles', 'project_guid', nullable=False)
    op.alter_column('articles', 'component_guid', nullable=False)

    # Create unique constraints first
    op.create_unique_constraint('uq_projects_guid', 'projects', ['guid'])
    op.create_unique_constraint('uq_components_guid', 'components', ['guid'])
    op.create_unique_constraint('uq_assemblies_guid', 'assemblies', ['guid'])
    op.create_unique_constraint('uq_pieces_guid', 'pieces', ['guid'])
    op.create_unique_constraint('uq_articles_guid', 'articles', ['guid'])

    # Add new foreign key constraints
    op.create_foreign_key('fk_components_project_guid', 'components', 'projects', ['project_guid'], ['guid'])
    op.create_foreign_key('fk_assemblies_project_guid', 'assemblies', 'projects', ['project_guid'], ['guid'])
    op.create_foreign_key('fk_assemblies_component_guid', 'assemblies', 'components', ['component_guid'], ['guid'])
    op.create_foreign_key('fk_pieces_project_guid', 'pieces', 'projects', ['project_guid'], ['guid'])
    op.create_foreign_key('fk_pieces_component_guid', 'pieces', 'components', ['component_guid'], ['guid'])
    op.create_foreign_key('fk_pieces_assembly_guid', 'pieces', 'assemblies', ['assembly_guid'], ['guid'])
    op.create_foreign_key('fk_articles_project_guid', 'articles', 'projects', ['project_guid'], ['guid'])
    op.create_foreign_key('fk_articles_component_guid', 'articles', 'components', ['component_guid'], ['guid'])

    # Drop old ID columns and sequences
    op.drop_column('projects', 'id')
    op.drop_column('components', 'id')
    op.drop_column('assemblies', 'id')
    op.drop_column('pieces', 'id')
    op.drop_column('articles', 'id')
    
    op.drop_column('components', 'id_project')
    op.drop_column('assemblies', 'id_project')
    op.drop_column('assemblies', 'id_component')
    op.drop_column('pieces', 'id_project')
    op.drop_column('pieces', 'id_component')
    op.drop_column('pieces', 'id_assembly')
    op.drop_column('articles', 'id_project')
    op.drop_column('articles', 'id_component')

    op.execute('DROP SEQUENCE IF EXISTS projects_id_seq;')
    op.execute('DROP SEQUENCE IF EXISTS components_id_seq;')
    op.execute('DROP SEQUENCE IF EXISTS assemblies_id_seq;')
    op.execute('DROP SEQUENCE IF EXISTS pieces_id_seq;')
    op.execute('DROP SEQUENCE IF EXISTS articles_id_seq;')

    # Add primary key constraints
    op.create_primary_key('pk_projects', 'projects', ['guid'])
    op.create_primary_key('pk_components', 'components', ['guid'])
    op.create_primary_key('pk_assemblies', 'assemblies', ['guid'])
    op.create_primary_key('pk_pieces', 'pieces', ['guid'])
    op.create_primary_key('pk_articles', 'articles', ['guid'])

def downgrade():
    # This is a breaking change, no downgrade path provided
    pass 