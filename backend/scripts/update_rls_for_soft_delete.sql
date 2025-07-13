-- Update RLS policies to include is_active = TRUE for soft delete

-- Projects
DROP POLICY IF EXISTS tenant_isolation ON public.projects;
CREATE POLICY tenant_isolation ON public.projects
  USING ((company_guid = (current_setting('app.tenant'::text))::uuid AND is_active = TRUE)
         OR (current_setting('app.bypass_rls'::text, true) = 'true'));

-- Components
DROP POLICY IF EXISTS tenant_isolation ON public.components;
CREATE POLICY tenant_isolation ON public.components
  USING ((company_guid = (current_setting('app.tenant'::text))::uuid AND is_active = TRUE)
         OR (current_setting('app.bypass_rls'::text, true) = 'true'));

-- Assemblies
DROP POLICY IF EXISTS tenant_isolation ON public.assemblies;
CREATE POLICY tenant_isolation ON public.assemblies
  USING ((company_guid = (current_setting('app.tenant'::text))::uuid AND is_active = TRUE)
         OR (current_setting('app.bypass_rls'::text, true) = 'true'));

-- Pieces
DROP POLICY IF EXISTS tenant_isolation ON public.pieces;
CREATE POLICY tenant_isolation ON public.pieces
  USING ((company_guid = (current_setting('app.tenant'::text))::uuid AND is_active = TRUE)
         OR (current_setting('app.bypass_rls'::text, true) = 'true'));

-- Articles
DROP POLICY IF EXISTS tenant_isolation ON public.articles;
CREATE POLICY tenant_isolation ON public.articles
  USING ((company_guid = (current_setting('app.tenant'::text))::uuid AND is_active = TRUE)
         OR (current_setting('app.bypass_rls'::text, true) = 'true')); 