## Environment Setup

### Development Environment Information

**Base URL:** `http://localhost:8000` (or your configured development URL)
**Default Test Company GUID:** (Obtain after creating a test company or use one from your seed data)

### Database Connection Details (Example for Development)
```bash
Host: localhost
Port: 5434 # Or your dev DB port
Database: rafactory_dev
User: rafactory_rw
Password: R4fDBP4ssw0rd9X
```

### Test Users
Ensure you have test users with different roles. The password for seeded users is typically `password`.

**Example SystemAdmin:**
-   Email: `a.petrov@delice.bg`
-   GUID: (Refer to your database or seed data)

### Initial Setup Steps

1.  **Start the development environment:**
    ```bash
    cd src/ractory # Or your project root
    docker compose --profile dev up -d # Or your specific startup command
    ```

2.  **Verify services are running:**
    ```bash
    docker compose ps
    ```

3.  **Obtain an initial SystemAdmin token:** This token will be used for administrative setup tasks during testing.
    ```bash
    # Replace with your SystemAdmin credentials
    ADMIN_EMAIL="a.petrov@delice.bg"
    ADMIN_PASSWORD="password"
    
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