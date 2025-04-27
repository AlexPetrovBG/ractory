-- Migration script to add updated_at fields and triggers
-- This script adds updated_at column to tables missing it, 
-- standardizes naming by renaming modified_date to updated_at, 
-- and adds triggers to automatically update the timestamps

-- Step 1: Add updated_at column to tables missing it
ALTER TABLE public.companies 
ADD COLUMN updated_at timestamp with time zone;

ALTER TABLE public.users 
ADD COLUMN updated_at timestamp with time zone;

ALTER TABLE public.workstations 
ADD COLUMN updated_at timestamp with time zone;

ALTER TABLE public.assemblies 
ADD COLUMN updated_at timestamp with time zone;

ALTER TABLE public.components 
ADD COLUMN updated_at timestamp with time zone;

ALTER TABLE public.pieces 
ADD COLUMN updated_at timestamp with time zone;

ALTER TABLE public.api_keys 
ADD COLUMN updated_at timestamp with time zone;

-- Step 2: Rename modified_date to updated_at for consistency
ALTER TABLE public.articles 
RENAME COLUMN modified_date TO updated_at;

ALTER TABLE public.projects 
RENAME COLUMN modified_date TO updated_at;

-- Step 3: Set initial values for updated_at (same as created_at for existing records)
UPDATE public.companies SET updated_at = created_at;
UPDATE public.users SET updated_at = created_at;
UPDATE public.workstations SET updated_at = created_at;
UPDATE public.assemblies SET updated_at = created_at;
UPDATE public.components SET updated_at = created_at;
UPDATE public.pieces SET updated_at = created_at;
UPDATE public.api_keys SET updated_at = created_at;

-- Step 4: Create function for automatic timestamp updates
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = NOW();
   RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

-- Step 5: Create triggers for each table
CREATE TRIGGER update_companies_updated_at
BEFORE UPDATE ON public.companies
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at
BEFORE UPDATE ON public.users
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_workstations_updated_at
BEFORE UPDATE ON public.workstations
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_assemblies_updated_at
BEFORE UPDATE ON public.assemblies
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_components_updated_at
BEFORE UPDATE ON public.components
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_pieces_updated_at
BEFORE UPDATE ON public.pieces
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_api_keys_updated_at
BEFORE UPDATE ON public.api_keys
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_articles_updated_at
BEFORE UPDATE ON public.articles
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_projects_updated_at
BEFORE UPDATE ON public.projects
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ui_templates_updated_at
BEFORE UPDATE ON public.ui_templates
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Note: We're not modifying alembic_version as it's a special table for migration tracking 