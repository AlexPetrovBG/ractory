## Environment Setup

### Development Environment Information

**Base URL:** `http://localhost:8000` (or your configured development URL)
**Default Test Company GUID:** (Obtain after creating a test company or use one from your seed data)

### Database Connection Details

You can connect to the PostgreSQL database using any compatible GUI tool (like DBeaver, DataGrip, etc.). The key is understanding Docker's port mapping. The `docker-compose.yml` files map a port on the host machine (e.g., `5434`) to the PostgreSQL container's internal port (`5432`).

#### Scenario A: Direct Connection (Docker is on your local machine)

If you are running the Docker environment on your local computer, you can connect directly using the settings below.

- **Host**: `localhost` or `127.0.0.1`
- **Port**: `5434` (for `dev`), `5432` (for `prod`)
- **Database**: `rafactory_dev`, `rafactory`
- **User**: `rafactory_rw`
- **Password**: The value of `DB_PASSWORD` in the corresponding `.env` file.

#### Scenario B: Remote Connection (Docker is on a server)

If you are connecting from your local machine to a Docker environment running on a remote server (e.g., `87.246.26.4`), you **must** use an SSH Tunnel.

**DBeaver SSH Tunnel Setup:**
1. In DBeaver's connection settings, go to the **SSH** tab.
2. Check **Use SSH Tunnel**.
3. **Host/IP**: Enter your remote server's IP (e.g., `87.246.26.4`).
4. **User Name**: Your SSH username for the server (e.g., `alex`).
5. **Authentication Method**: Choose Password or Public Key.

**DBeaver Main Connection Settings (with SSH Tunnel active):**
- **Host**: `localhost` (This is crucial - it refers to `localhost` *on the remote server*).
- **Port**: The port as defined in the `docker-compose.yml` file on the server.
  - **Dev DB Port**: `5434`
  - **Prod DB Port**: `5432`
- **Database**: The name of the database (`rafactory_dev`, `rafactory`).
- **User**: `rafactory_rw`
- **Password**: The value of `DB_PASSWORD` from the corresponding `.env` file *on the server*.

**Important Note on Port Conflicts:**
You cannot run multiple environments at the same time if they are configured to use the same host port. If you have connection issues, ensure only the environment you are trying to connect to is running, or assign them unique ports in their `docker-compose.yml` files.

### Test Users


**Obtain an initial SystemAdmin token:** This token will be used for administrative setup tasks during testing.
    ```bash
    # Use the credentials from your admin_config.env file
    ADMIN_EMAIL="a.petrov@delice.bg"  # From admin_config.env
    ADMIN_PASSWORD="SecureAdminPassword123!"  # From admin_config.env
    
    ADMIN_TOKEN_RESPONSE=$(curl -X POST -H "Content-Type: application/json" \
         -d "{\"email\": \"$ADMIN_EMAIL\", \"password\": \"$ADMIN_PASSWORD\"}" \
         http://localhost:8000/api/v1/auth/login | jq '.')
    
    ADMIN_ACCESS_TOKEN=$(echo $ADMIN_TOKEN_RESPONSE | jq -r '.access_token')
    ADMIN_REFRESH_TOKEN=$(echo $ADMIN_TOKEN_RESPONSE | jq -r '.refresh_token')
    
    echo "Admin Access Token: $ADMIN_ACCESS_TOKEN"
    ```

## Test Sequence Overview

Execute tests in a logical order to ensure dependencies are met:

1.  Health Check Tests
2.  Authentication Tests (`/auth`)
3.  Company Management Tests (`/companies`)
4.  User Management Tests (`/users`)
5.  API Key Management Tests (`/api-keys`)
6.  Workstation Management Tests (`/workstations`)
7.  Data Synchronization Tests (`/sync/*`)
    *   Sync Projects
    *   Sync Components
    *   Sync Assemblies
    *   Sync Pieces
    *   Sync Articles
8.  Entity Read, Soft Delete & Restore Tests
    *   Projects (`/projects`)
    *   Components (`/components`)
    *   Assemblies (`/assemblies`)
    *   Pieces (`/pieces`)
    *   Articles (`/articles`)
9.  Workflow Management Tests (`/workflow`)
10. Multi-Tenant Isolation Tests
11. Error Handling & Edge Case Tests 

## IMPORTANT: Database Migration & Setup Order (Quick Start)

**Before running any admin/user management scripts or API tests, you must ensure the database schema is initialized.**

### 1. Build and Start Database Container
```bash
cd /home/alex/apps/ractory/dev
# Build the database service with no cache to ensure a clean environment
# (Use the correct service name 'db' as defined in docker-compose.yml)
docker compose build --no-cache db
# Start only the database service
docker compose up -d db
```

### 2. Run Database Migrations (REQUIRED)
If your API does not run Alembic migrations automatically on startup, you must run them manually:
```bash
# From the project root
docker compose run --rm api alembic upgrade head
# Or, if running locally:
alembic upgrade head
```

### 3. Start/Restart the API Service
```bash
cd apps/ractory/dev
docker compose up -d --force-recreate
```

## Common Pitfalls & Troubleshooting

- **Error: `relation "companies" does not exist`**
  - Cause: Database migrations have not been run. Run Alembic migrations before any scripts or API startup.
- **Error: `admin_config.env not found`**
  - Cause: Script must be run from the project root where this file exists.
- **Error: `Invalid email or password` when testing admin login**
  - Cause: Admin user was not created/updated. (This step is now managed outside this guide.)
- **Docker Compose KeyError: 'ContainerConfig'**
  - Cause: Outdated Docker Compose. Upgrade to v2+ and clean up old containers/images.

## Recommended Order for Initial Testing
1. Build and start the database container.
2. Run database migrations.
3. Start/restart the API container.
4. Obtain SystemAdmin token and proceed with API tests. 