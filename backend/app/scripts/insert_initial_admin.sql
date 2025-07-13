-- Insert initial company
INSERT INTO companies (guid, name, is_active, created_at, updated_at, company_index, short_name, logo_path)
VALUES ('28fbeed6-5e09-4b75-ad74-ab1cdc4dec71', 'Delice Automatics Ltd.', TRUE, NOW(), NOW(), 1, NULL, NULL)
ON CONFLICT (guid) DO NOTHING;

-- Insert test Company A for multi-tenant isolation testing
INSERT INTO companies (guid, name, is_active, created_at, updated_at, company_index, short_name, logo_path)
VALUES ('11111111-1111-1111-1111-111111111111', 'Company A', TRUE, NOW(), NOW(), 2, 'COMP_A', NULL)
ON CONFLICT (guid) DO NOTHING;

-- Insert test Company B for multi-tenant isolation testing
INSERT INTO companies (guid, name, is_active, created_at, updated_at, company_index, short_name, logo_path)
VALUES ('22222222-2222-2222-2222-222222222222', 'Company B', TRUE, NOW(), NOW(), 3, 'COMP_B', NULL)
ON CONFLICT (guid) DO NOTHING;

-- Insert initial admin user
INSERT INTO users (guid, company_guid, email, pwd_hash, role, is_active, created_at, updated_at, name, surname, picture_path, pin)
VALUES (
  '856d4637-cb16-4cf0-a535-efc02364096a',
  '28fbeed6-5e09-4b75-ad74-ab1cdc4dec71',
  'a.petrov@delice.bg',
  '$2b$12$ErSpwYoypZAdkDIQZCTKPOi/Y6XOqTwGcXwEs.3hrSvyv22ym7SiK', -- bcrypt for 'SecureAdminPassword123'
  'SystemAdmin',
  TRUE,
  NOW(),
  NOW(),
  NULL,
  NULL,
  NULL,
  NULL
)
ON CONFLICT (guid) DO UPDATE SET 
  pwd_hash = EXCLUDED.pwd_hash;

-- Insert Company A admin user
INSERT INTO users (guid, company_guid, email, pwd_hash, role, is_active, created_at, updated_at, name, surname, picture_path, pin)
VALUES (
  '33333333-3333-3333-3333-333333333333',
  '11111111-1111-1111-1111-111111111111',
  'admin1.a@example.com',
  '$2b$12$gOE4AUzzCGEI30WT.BYslODPPnF6WHni3GKxDFV7DRCpM72Ot0p5u', -- bcrypt for 'password'
  'CompanyAdmin',
  TRUE,
  NOW(),
  NOW(),
  'Admin',
  'Company A',
  NULL,
  NULL
)
ON CONFLICT (guid) DO NOTHING;

-- Insert Company B admin user
INSERT INTO users (guid, company_guid, email, pwd_hash, role, is_active, created_at, updated_at, name, surname, picture_path, pin)
VALUES (
  '44444444-4444-4444-4444-444444444444',
  '22222222-2222-2222-2222-222222222222',
  'admin1.b@example.com',
  '$2b$12$gOE4AUzzCGEI30WT.BYslODPPnF6WHni3GKxDFV7DRCpM72Ot0p5u', -- bcrypt for 'password'
  'CompanyAdmin',
  TRUE,
  NOW(),
  NOW(),
  'Admin',
  'Company B',
  NULL,
  NULL
)
ON CONFLICT (guid) DO NOTHING; 