-- Insert initial company
INSERT INTO companies (guid, name, is_active, created_at, updated_at, company_index, short_name, logo_path)
VALUES ('28fbeed6-5e09-4b75-ad74-ab1cdc4dec71', 'Delice Automatics Ltd.', TRUE, NOW(), NOW(), 1, NULL, NULL)
ON CONFLICT (guid) DO NOTHING;

-- Insert initial admin user
INSERT INTO users (guid, company_guid, email, pwd_hash, role, is_active, created_at, updated_at, name, surname, picture_path, pin)
VALUES (
  '856d4637-cb16-4cf0-a535-efc02364096a',
  '28fbeed6-5e09-4b75-ad74-ab1cdc4dec71',
  'a.petrov@delice.bg',
  '$2b$12$gOE4AUzzCGEI30WT.BYslODPPnF6WHni3GKxDFV7DRCpM72Ot0p5u', -- bcrypt for 'password'
  'SystemAdmin',
  TRUE,
  NOW(),
  NOW(),
  NULL,
  NULL,
  NULL,
  NULL
)
ON CONFLICT (guid) DO NOTHING; 