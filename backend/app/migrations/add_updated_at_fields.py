"""Add updated_at fields to all tables

Revision ID: add_updated_at_fields
Revises: <previous_revision>
Create Date: 2025-04-27

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_updated_at_fields'
down_revision = None  # Set this to the previous migration when running with Alembic
branch_labels = None
depends_on = None


def upgrade():
    # Execute the SQL script to add updated_at fields and create triggers
    op.execute("""
    -- Step 1: Add updated_at column to tables missing it
    ALTER TABLE public.companies 
    ADD COLUMN IF NOT EXISTS updated_at timestamp with time zone;
    
    ALTER TABLE public.users 
    ADD COLUMN IF NOT EXISTS updated_at timestamp with time zone;
    
    ALTER TABLE public.workstations 
    ADD COLUMN IF NOT EXISTS updated_at timestamp with time zone;
    
    ALTER TABLE public.assemblies 
    ADD COLUMN IF NOT EXISTS updated_at timestamp with time zone;
    
    ALTER TABLE public.components 
    ADD COLUMN IF NOT EXISTS updated_at timestamp with time zone;
    
    ALTER TABLE public.pieces 
    ADD COLUMN IF NOT EXISTS updated_at timestamp with time zone;
    
    ALTER TABLE public.api_keys 
    ADD COLUMN IF NOT EXISTS updated_at timestamp with time zone;
    
    -- Step 2: Rename modified_date to updated_at for consistency
    -- Check if the old column exists before attempting to rename
    DO $$
    BEGIN
        IF EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name = 'articles' AND column_name = 'modified_date') THEN
            ALTER TABLE public.articles RENAME COLUMN modified_date TO updated_at;
        END IF;
    END $$;
    
    DO $$
    BEGIN
        IF EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name = 'projects' AND column_name = 'modified_date') THEN
            ALTER TABLE public.projects RENAME COLUMN modified_date TO updated_at;
        END IF;
    END $$;
    
    -- Step 3: Set initial values for updated_at (same as created_at for existing records)
    UPDATE public.companies SET updated_at = created_at WHERE updated_at IS NULL;
    UPDATE public.users SET updated_at = created_at WHERE updated_at IS NULL;
    UPDATE public.workstations SET updated_at = created_at WHERE updated_at IS NULL;
    UPDATE public.assemblies SET updated_at = created_at WHERE updated_at IS NULL;
    UPDATE public.components SET updated_at = created_at WHERE updated_at IS NULL;
    UPDATE public.pieces SET updated_at = created_at WHERE updated_at IS NULL;
    UPDATE public.api_keys SET updated_at = created_at WHERE updated_at IS NULL;
    
    -- Step 4: Create function for automatic timestamp updates if it doesn't exist
    CREATE OR REPLACE FUNCTION update_updated_at_column()
    RETURNS TRIGGER AS $$
    BEGIN
       NEW.updated_at = NOW();
       RETURN NEW;
    END;
    $$ LANGUAGE 'plpgsql';
    
    -- Step 5: Create triggers for each table, dropping them first if they exist
    DROP TRIGGER IF EXISTS update_companies_updated_at ON public.companies;
    CREATE TRIGGER update_companies_updated_at
    BEFORE UPDATE ON public.companies
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    
    DROP TRIGGER IF EXISTS update_users_updated_at ON public.users;
    CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON public.users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    
    DROP TRIGGER IF EXISTS update_workstations_updated_at ON public.workstations;
    CREATE TRIGGER update_workstations_updated_at
    BEFORE UPDATE ON public.workstations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    
    DROP TRIGGER IF EXISTS update_assemblies_updated_at ON public.assemblies;
    CREATE TRIGGER update_assemblies_updated_at
    BEFORE UPDATE ON public.assemblies
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    
    DROP TRIGGER IF EXISTS update_components_updated_at ON public.components;
    CREATE TRIGGER update_components_updated_at
    BEFORE UPDATE ON public.components
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    
    DROP TRIGGER IF EXISTS update_pieces_updated_at ON public.pieces;
    CREATE TRIGGER update_pieces_updated_at
    BEFORE UPDATE ON public.pieces
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    
    DROP TRIGGER IF EXISTS update_api_keys_updated_at ON public.api_keys;
    CREATE TRIGGER update_api_keys_updated_at
    BEFORE UPDATE ON public.api_keys
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    
    DROP TRIGGER IF EXISTS update_articles_updated_at ON public.articles;
    CREATE TRIGGER update_articles_updated_at
    BEFORE UPDATE ON public.articles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    
    DROP TRIGGER IF EXISTS update_projects_updated_at ON public.projects;
    CREATE TRIGGER update_projects_updated_at
    BEFORE UPDATE ON public.projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    
    DROP TRIGGER IF EXISTS update_ui_templates_updated_at ON public.ui_templates;
    CREATE TRIGGER update_ui_templates_updated_at
    BEFORE UPDATE ON public.ui_templates
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    """)


def downgrade():
    # Execute SQL to revert the changes (remove triggers and updated_at columns)
    op.execute("""
    -- Remove triggers
    DROP TRIGGER IF EXISTS update_companies_updated_at ON public.companies;
    DROP TRIGGER IF EXISTS update_users_updated_at ON public.users;
    DROP TRIGGER IF EXISTS update_workstations_updated_at ON public.workstations;
    DROP TRIGGER IF EXISTS update_assemblies_updated_at ON public.assemblies;
    DROP TRIGGER IF EXISTS update_components_updated_at ON public.components;
    DROP TRIGGER IF EXISTS update_pieces_updated_at ON public.pieces;
    DROP TRIGGER IF EXISTS update_api_keys_updated_at ON public.api_keys;
    DROP TRIGGER IF EXISTS update_articles_updated_at ON public.articles;
    DROP TRIGGER IF EXISTS update_projects_updated_at ON public.projects;
    DROP TRIGGER IF EXISTS update_ui_templates_updated_at ON public.ui_templates;
    
    -- Remove function
    DROP FUNCTION IF EXISTS update_updated_at_column();
    
    -- Rename updated_at back to modified_date for specific tables
    ALTER TABLE public.articles RENAME COLUMN updated_at TO modified_date;
    ALTER TABLE public.projects RENAME COLUMN updated_at TO modified_date;
    
    -- Remove updated_at column from other tables
    ALTER TABLE public.companies DROP COLUMN IF EXISTS updated_at;
    ALTER TABLE public.users DROP COLUMN IF EXISTS updated_at;
    ALTER TABLE public.workstations DROP COLUMN IF EXISTS updated_at;
    ALTER TABLE public.assemblies DROP COLUMN IF EXISTS updated_at;
    ALTER TABLE public.components DROP COLUMN IF EXISTS updated_at;
    ALTER TABLE public.pieces DROP COLUMN IF EXISTS updated_at;
    ALTER TABLE public.api_keys DROP COLUMN IF EXISTS updated_at;
    """) 