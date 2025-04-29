"""Add missing updated_at columns and triggers

Revision ID: add_missing_updated_at
Revises: standardize_timestamps
Create Date: 2024-04-28 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_missing_updated_at'
down_revision = 'standardize_timestamps'
branch_labels = None
depends_on = None

def upgrade():
    # Add updated_at column to tables that don't have it
    tables = ['assemblies', 'components', 'pieces', 'users', 'workstations']
    
    # Create trigger function if it doesn't exist
    op.execute("""
    CREATE OR REPLACE FUNCTION update_updated_at_column()
    RETURNS TRIGGER AS $$
    BEGIN
       NEW.updated_at = NOW();
       RETURN NEW;
    END;
    $$ LANGUAGE 'plpgsql';
    """)
    
    for table in tables:
        # Check if column exists before adding it
        op.execute(f"""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 
                FROM information_schema.columns 
                WHERE table_name = '{table}' 
                AND column_name = 'updated_at'
            ) THEN
                ALTER TABLE {table} ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE;
            END IF;
        END $$;
        """)
        
        # Drop trigger if exists
        op.execute(f"DROP TRIGGER IF EXISTS update_{table}_updated_at ON {table};")
        
        # Create trigger
        op.execute(f"""
        CREATE TRIGGER update_{table}_updated_at
        BEFORE UPDATE ON {table}
        FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
        """)

def downgrade():
    # Drop triggers first
    tables = ['assemblies', 'components', 'pieces', 'users', 'workstations']
    
    for table in tables:
        op.execute(f"DROP TRIGGER IF EXISTS update_{table}_updated_at ON {table};")
    
    # Drop trigger function
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column();")
    
    # Drop updated_at columns
    for table in tables:
        op.drop_column(table, 'updated_at') 