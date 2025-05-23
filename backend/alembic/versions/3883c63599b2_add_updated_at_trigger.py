"""add_updated_at_trigger

Revision ID: 3883c63599b2
Revises: f570b9d188e5
Create Date: 2025-05-02 09:12:34.567890

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3883c63599b2'
down_revision = 'f570b9d188e5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create the trigger function
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ language 'plpgsql';
    """)
    
    # Add the trigger to all tables with updated_at column
    tables = [
        'users', 'companies', 'projects', 'assemblies', 'pieces', 
        'components', 'articles', 'api_keys', 'ui_templates', 'workstations'
    ]
    
    for table in tables:
        # Drop existing trigger if it exists
        op.execute(f"DROP TRIGGER IF EXISTS update_updated_at_timestamp ON {table};")
        
        # Create new trigger
        op.execute(f"""
            CREATE TRIGGER update_updated_at_timestamp
            BEFORE UPDATE ON {table}
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
        """)


def downgrade() -> None:
    # Remove triggers from all tables
    tables = [
        'users', 'companies', 'projects', 'assemblies', 'pieces', 
        'components', 'articles', 'api_keys', 'ui_templates', 'workstations'
    ]
    
    for table in tables:
        op.execute(f"DROP TRIGGER IF EXISTS update_updated_at_timestamp ON {table};")
    
    # Drop the trigger function
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column();") 