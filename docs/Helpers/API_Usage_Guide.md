# Ra Factory API Usage Guide

This document provides a human-readable guide to the Ra Factory API endpoints, based on the `openapi_schema.json`.

**Base URL (Development):** `http://localhost:8000`

**General Notes:**

*   Most `POST` and `PUT` requests expect a JSON body with `Content-Type: application/json`.
*   Endpoints requiring authentication expect a Bearer token in the `Authorization` header: `Authorization: Bearer <your_access_token>`. Obtain this token from the `/api/v1/auth/login` endpoint.
*   For integration scenarios, API key authentication is also supported. See the [API Keys](#api-keys) section below.

---

## User Roles

The API uses the following roles for access control in a hierarchical structure. Roles are assigned to users and determine what actions they can perform.

*   **`SystemAdmin`**: Highest privileges, including cross-company access and system configuration. Can manage all roles.
*   **`CompanyAdmin`**: Full permissions (Create, Read, Update, Delete) for all data within their assigned company. Can manage roles below CompanyAdmin level.
*   **`ProjectManager`**: Can read project data and manage logistics-related information within their company. Cannot manage CompanyAdmin or SystemAdmin roles.
*   **`Operator`**: Limited permissions, typically restricted to actions at specific workstations on the shop floor (often authenticated via QR code). Cannot manage higher roles.
*   **`Integration`**: Used for machine-to-machine communication, granting specific permissions for automated tasks like data synchronization.

### Role Hierarchy and Management Restrictions

The system implements a strict role hierarchy that prevents users from creating or modifying users with roles equal to or higher than their own:

1. **SystemAdmin**
   - Can create/modify all roles
   - Full system access

2. **CompanyAdmin**
   - Cannot create/modify SystemAdmin roles
   - Cannot create peer CompanyAdmin roles
   - Can manage ProjectManager, Operator, and Integration roles
   - Access limited to own company

3. **ProjectManager**
   - Cannot create/modify SystemAdmin or CompanyAdmin roles
   - Limited to project-related operations
   - Access limited to own company

4. **Operator**
   - Cannot create/modify any roles
   - Limited to workstation operations
   - Access limited to assigned workstation

5. **Integration**
   - Special role for system integration
   - No user management capabilities
   - Access defined by API scopes

---

## Authentication System

The Ra Factory API uses bcrypt for password hashing and JWT (JSON Web Tokens) for session management. Authentication data is stored in the PostgreSQL database and follows a multi-tenant data architecture with Row-Level Security (RLS).

1. The application uses FastAPI with JWT tokens for authentication.
2. There's a role-based access control (RBAC) system with roles defined in the UserRole enum (SystemAdmin, CompanyAdmin, ProjectManager, Operator, Integration).
3. The auth.py file contains endpoints for login, refresh token, and QR code login.
4. JWT tokens include claims for user_id, tenant (company_guid), and role.
5. The system implements row-level security (RLS) at the database level using PostgreSQL session variables.
6. There are dependency functions for getting the current user from a JWT token and enforcing role requirements.
7. The application has multi-tenant support, with the tenant context set based on the user's company.
8. SystemAdmin users can bypass tenant restrictions, while other roles are limited to their own company's resources.

The authentication flow works through:
1. User sends credentials to /login or /qr-login
2. AuthService validates credentials and generates JWT tokens
3. The tokens are returned to the client and used for subsequent requests
4. For authenticated routes, the request passes through dependencies that validate the token and check permissions

### Password Management

Passwords in the system are:

- Hashed using bcrypt through Python's `passlib.CryptContext` library
- Stored in the `pwd_hash` column of the `users` table
- Never transmitted in plain text or recoverable form

When creating or updating passwords, it is critical to use the same hashing mechanism as the application to ensure compatibility:

```python
from passlib.context import CryptContext

# Use the same password hashing configuration as in security.py
PWD_CTX = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed_password = PWD_CTX.hash("your_password")
```

**Important Notes:**
- When updating passwords directly in the database, ensure the hash is stored correctly without corruption.
- The system is vulnerable to hash format corruption; always verify hashes are stored with the correct format, beginning with `$2b$12$`.
- If authentication issues occur, check the database for proper hash storage.

## API Keys

The Ra Factory API supports authentication using API keys for integration scenarios. API keys provide a more secure and flexible approach for machine-to-machine communication.

### Authentication Options

API keys can be included in requests in two ways:

1. Using the `X-API-Key` header (recommended):
   ```
   X-API-Key: rfk_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
   ```

2. Using the `Authorization` header:
   ```
   Authorization: ApiKey rfk_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
   ```

### API Key Features

- **Scoped Access**: API keys can be limited to specific operations (e.g., sync:read, sync:write)
- **Usage Tracking**: Last usage time is recorded for auditing
- **No Expiration**: Unlike JWT tokens, API keys don't expire until revoked
- **Company-Specific**: Each API key is tied to a specific company

### Creating and Managing API Keys

API keys can be managed through dedicated endpoints at `/api/v1/api-keys`. Only users with SystemAdmin or CompanyAdmin roles can create and manage API keys.

For detailed documentation on API key management and usage, see the [API Keys Documentation](./API_Keys_Documentation.md).

---

## Authentication Endpoints (`/api/v1/auth`)

These endpoints handle user login, token refresh, and identity management.

### 1. Login (`POST /api/v1/auth/login`)

**Description:** Authenticate a user with their email and password. Returns JWT access and refresh tokens upon successful authentication.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "your_password"
}
```

**Response (Success - 200 OK):**
```json
{
  "access_token": "...",
  "refresh_token": "...",
  "role": "UserRole",
  "expires_in": 900
}
```

**Example:**
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"email": "a.petrov@delice.bg", "password": "password"}' \
     http://localhost:8000/api/v1/auth/login | cat
```

### 2. Refresh Token (`POST /api/v1/auth/refresh`)

**Description:** Obtain a new access token using a valid refresh token. The refresh token can be provided in the request body or as an `HttpOnly` cookie (if set by the server).

**Request Body (Option 1):**
```json
{
  "refresh_token": "<your_refresh_token>"
}
```

**Request (Option 2 - Cookie):** The request should include the `refresh_token` cookie sent by the browser or client.

**Response (Success - 200 OK):** Same format as the login response, with new tokens.

**Example (Using Request Body):**
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"refresh_token": "<your_refresh_token>"}' \
     http://localhost:8000/api/v1/auth/refresh | cat
```

### 3. QR Login (`POST /api/v1/auth/qr`)

**Description:** Authenticate an operator using their User GUID (from QR code), a Workstation GUID, and their PIN. Returns a short-lived, workstation-scoped JWT.

**Request Body:**
```json
{
  "user_guid": "uuid-of-user",
  "workstation_guid": "uuid-of-workstation",
  "pin": "123456"
}
```

**Response (Success - 200 OK):** Same format as the login response.

**Example:**
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"user_guid": "...", "workstation_guid": "...", "pin": "..."}' \
     http://localhost:8000/api/v1/auth/qr | cat
```

### 4. Get Current User Info (`GET /api/v1/auth/me`)

**Description:** Get information about the currently authenticated user based on the provided access token.

**Authentication:** Requires `Authorization: Bearer <token>` header.

**Response (Success - 200 OK):**
```json
{
  "guid": "user-guid",
  "email": "user@example.com",
  "role": "UserRole",
  "company_guid": "company-guid"
}
```

**Example:**
```bash
curl -X GET -H "Authorization: Bearer <your_access_token>" \
     http://localhost:8000/api/v1/auth/me | cat
```

### 5. Protected Test Route (`GET /api/v1/auth/protected`)

**Description:** A test endpoint specifically requiring the `SystemAdmin` role for access. Used for verifying role-based access control.

**Authentication:** Requires `Authorization: Bearer <token>` header (token must belong to a SystemAdmin).

**Response (Success - 200 OK):**
```json
{
  "message": "You have access to this protected route",
  "user_id": "user-guid",
  "role": "SystemAdmin",
  "tenant": "company-guid"
}
```

**Example:**
```bash
curl -X GET -H "Authorization: Bearer <system_admin_access_token>" \
     http://localhost:8000/api/v1/auth/protected | cat
```

---

## Synchronization Endpoints (`/api/v1/sync`)

These endpoints are used to bulk insert or update data, typically synchronized from an external source like RaConnect. They generally require authentication (Admin role or specific API key scope).

**Authentication:** Requires `Authorization: Bearer <token>` header.

**Response (Success - 200 OK) for all sync endpoints:**
```json
{
  "inserted": 10, // Number of records inserted
  "updated": 5    // Number of records updated
}
```

### 1. Sync Projects (`POST /api/v1/sync/projects`)

**Description:** Bulk insert/update project data.

**Request Body:**
```json
{
  "projects": [
    { "code": "P001", "creation_date": "...", "id": 1, "updated_at": "...", /* ... other project fields */ },
    { "code": "P002", "creation_date": "...", "id": 2, "updated_at": "...", /* ... other project fields */ }
    // ... more projects
  ]
}
```

**Example:**
```bash
curl -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer <your_access_token>" \
     -d '{"projects": [ { /* project data */ } ]}' \
     http://localhost:8000/api/v1/sync/projects | cat
```

### 2. Sync Components (`POST /api/v1/sync/components`)

**Description:** Bulk insert/update component data.

**Request Body:**
```json
{
  "components": [
    { "code": "C001", "id_project": 1, "id": 10, "created_date": "...", /* ... */ },
    { "code": "C002", "id_project": 1, "id": 11, "created_date": "...", /* ... */ }
    // ... more components
  ]
}
```

**Example:**
```bash
curl -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer <your_access_token>" \
     -d '{"components": [ { /* component data */ } ]}' \
     http://localhost:8000/api/v1/sync/components | cat
```

### 3. Sync Assemblies (`POST /api/v1/sync/assemblies`)

**Description:** Bulk insert/update assembly data.

**Request Body:**
```json
{
  "assemblies": [
    { "id_project": 1, "id_component": 10, "id": 100, /* ... */ },
    { "id_project": 1, "id_component": 11, "id": 101, /* ... */ }
    // ... more assemblies
  ]
}
```

**Example:**
```bash
curl -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer <your_access_token>" \
     -d '{"assemblies": [ { /* assembly data */ } ]}' \
     http://localhost:8000/api/v1/sync/assemblies | cat
```

### 4. Sync Pieces (`POST /api/v1/sync/pieces`)

**Description:** Bulk insert/update piece data (e.g., profiles). Maximum 1000 pieces per request.

**Request Body:**
```json
{
  "pieces": [
    { "piece_id": "...", "id_project": 1, "id_component": 10, "id_assembly": 100, "id": 1000, "created_date": "...", /* ... */ },
    { "piece_id": "...", "id_project": 1, "id_component": 10, "id_assembly": 100, "id": 1001, "created_date": "...", /* ... */ }
    // ... more pieces (up to 1000)
  ]
}
```

**Example:**
```bash
curl -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer <your_access_token>" \
     -d '{"pieces": [ { /* piece data */ } ]}' \
     http://localhost:8000/api/v1/sync/pieces | cat
```

### 5. Sync Articles (`POST /api/v1/sync/articles`)

**Description:** Bulk insert/update article data (e.g., hardware, accessories).

**Request Body:**
```json
{
  "articles": [
    { "code": "A001", "id_project": 1, "id_component": 10, "id": 500, "created_date": "...", /* ... */ },
    { "code": "A002", "id_project": 1, "id_component": 11, "id": 501, "created_date": "...", /* ... */ }
    // ... more articles
  ]
}
```

**Example:**
```bash
curl -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer <your_access_token>" \
     -d '{"articles": [ { /* article data */ } ]}' \
     http://localhost:8000/api/v1/sync/articles | cat
```

---

## Mocking Endpoints (`/api/v1/mock-auth`)

### 1. Mock Auth (`POST /api/v1/mock-auth`)

**Description:** A mock authentication endpoint intended **only for development/testing purposes** when a database connection might not be available or desired. It likely bypasses actual credential validation.

**Request Body:** Same as `/api/v1/auth/login`.
```json
{
  "email": "test@example.com",
  "password": "password"
}
```

**Response (Success - 200 OK):** Same format as the login response, but the tokens might be mock tokens.

**Example:**
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "password"}' \
     http://localhost:8000/api/v1/mock-auth | cat
```

---

## Health Check Endpoints

These endpoints are used to verify that the service is running and accessible.

### 1. Root Health Check (`GET /health`)

**Description:** Basic service health check.

**Response (Success - 200 OK):** An empty JSON object `{}` or a simple status message.

**Example:**
```bash
curl http://localhost:8000/health | cat
```

### 2. API v1 Health Check (`GET /api/v1/health`)

**Description:** Specific health check for the v1 API routes.

**Response (Success - 200 OK):** An empty JSON object `{}` or a simple status message.

**Example:**
```bash
curl http://localhost:8000/api/v1/health | cat
```

---

## Root Endpoint (`/`)

### 1. Root (`GET /`)

**Description:** Accessing the root URL typically redirects to the interactive API documentation (Swagger UI or ReDoc).

**Response:** Usually a 30x Redirect response, or the HTML content of the documentation page.

**Example (Follow Redirects):**
```bash
curl -L http://localhost:8000/
```

---

## User Management Endpoints (`/api/v1/users`)

These endpoints handle user creation, retrieval, updating, and deactivation. Most operations require SystemAdmin or CompanyAdmin privileges.

### 1. Create User (`POST /api/v1/users`)

**Description:** Create a new user within the authenticated user's company. SystemAdmin role can create users with any role, while CompanyAdmin can only create users with roles below SystemAdmin.

**Authentication:** Requires `Authorization: Bearer <token>` header with SystemAdmin or CompanyAdmin role.

**Request Body:**
```json
{
  "email": "new.user@example.com",
  "password": "secure_password",
  "role": "CompanyAdmin",
  "pin": "123456",  // Optional, typically for Operator role
  "is_active": true  // Optional, defaults to true
}
```

**Response (Success - 201 Created):**
```json
{
  "guid": "user-guid",
  "email": "new.user@example.com",
  "role": "CompanyAdmin",
  "is_active": true,
  "created_at": "2023-01-01T12:00:00Z"
}
```

**Example:**
```bash
curl -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer <your_access_token>" \
     -d '{"email": "new.user@example.com", "password": "secure_password", "role": "CompanyAdmin"}' \
     http://localhost:8000/api/v1/users | cat
```

### 2. Get Users (`GET /api/v1/users`)

**Description:** Retrieve a list of users belonging to the authenticated user's company. Results are filtered based on the user's role.

**Authentication:** Requires `Authorization: Bearer <token>` header.

**Query Parameters:**
- `role` (optional): Filter users by role
- `active` (optional): Filter by active status (`true` or `false`)

**Response (Success - 200 OK):**
```json
{
  "users": [
    {
      "guid": "user-guid-1",
      "email": "user1@example.com",
      "role": "CompanyAdmin",
      "is_active": true,
      "created_at": "2023-01-01T12:00:00Z"
    },
    {
      "guid": "user-guid-2",
      "email": "user2@example.com",
      "role": "ProjectManager",
      "is_active": true,
      "created_at": "2023-01-02T12:00:00Z"
    }
  ]
}
```

**Example:**
```bash
curl -X GET -H "Authorization: Bearer <your_access_token>" \
     http://localhost:8000/api/v1/users | cat
```

### 3. Get User by GUID (`GET /api/v1/users/{guid}`)

**Description:** Retrieve details for a specific user by their GUID.

**Authentication:** Requires `Authorization: Bearer <token>` header.

**Response (Success - 200 OK):**
```json
{
  "guid": "user-guid",
  "email": "user@example.com",
  "role": "CompanyAdmin",
  "is_active": true,
  "created_at": "2023-01-01T12:00:00Z",
  "updated_at": "2023-01-02T12:00:00Z"
}
```

**Example:**
```bash
curl -X GET -H "Authorization: Bearer <your_access_token>" \
     http://localhost:8000/api/v1/users/550e8400-e29b-41d4-a716-446655440000 | cat
```

### 4. Update User (`PUT /api/v1/users/{guid}`)

**Description:** Update user details including email, password, role, and active status.

**Authentication:** Requires `Authorization: Bearer <token>` header with appropriate permissions.

**Request Body:**
```json
{
  "email": "updated.email@example.com",  // Optional
  "password": "new_password",            // Optional
  "role": "ProjectManager",              // Optional
  "is_active": false                     // Optional
}
```

**Response (Success - 200 OK):**
```json
{
  "guid": "user-guid",
  "email": "updated.email@example.com",
  "role": "ProjectManager",
  "is_active": false,
  "updated_at": "2023-01-03T12:00:00Z"
}
```

**Example:**
```bash
curl -X PUT -H "Content-Type: application/json" \
     -H "Authorization: Bearer <your_access_token>" \
     -d '{"role": "ProjectManager"}' \
     http://localhost:8000/api/v1/users/550e8400-e29b-41d4-a716-446655440000 | cat
```

### 5. Delete User (`DELETE /api/v1/users/{guid}`)

**Description:** Soft-delete a user by setting their `is_active` status to `false`. The user remains in the database but can no longer access the system.

**Authentication:** Requires `Authorization: Bearer <token>` header with SystemAdmin or CompanyAdmin role.

**Response (Success - 200 OK):**
```json
{
  "message": "User deactivated successfully",
  "guid": "user-guid"
}
```

**Example:**
```bash
curl -X DELETE -H "Authorization: Bearer <your_access_token>" \
     http://localhost:8000/api/v1/users/550e8400-e29b-41d4-a716-446655440000 | cat
```

---

## Workstation Management Endpoints (`/api/v1/workstations`)

These endpoints handle workstation creation, retrieval, updating, and deactivation.

### 1. Create Workstation (`POST /api/v1/workstations`)

**Description:** Create a new workstation within the authenticated user's company.

**Authentication:** Requires `Authorization: Bearer <token>` header with SystemAdmin or CompanyAdmin role.

**Request Body:**
```json
{
  "location": "Production Floor A",
  "type": "Assembly",  // Should match one of: Machine, Assembly, Control, Logistics, Supply
  "is_active": true    // Optional, defaults to true
}
```

**Response (Success - 201 Created):**
```json
{
  "guid": "workstation-guid",
  "location": "Production Floor A",
  "type": "Assembly",
  "is_active": true,
  "created_at": "2023-01-01T12:00:00Z"
}
```

**Example:**
```bash
curl -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer <your_access_token>" \
     -d '{"location": "Production Floor A", "type": "Assembly"}' \
     http://localhost:8000/api/v1/workstations | cat
```

### 2. Get Workstations (`GET /api/v1/workstations`)

**Description:** Retrieve a list of workstations belonging to the authenticated user's company.

**Authentication:** Requires `Authorization: Bearer <token>` header.

**Query Parameters:**
- `type` (optional): Filter by workstation type
- `active` (optional): Filter by active status (`true` or `false`)
- `location` (optional): Filter by location (substring match)

**Response (Success - 200 OK):**
```json
{
  "workstations": [
    {
      "guid": "workstation-guid-1",
      "location": "Production Floor A",
      "type": "Assembly",
      "is_active": true,
      "created_at": "2023-01-01T12:00:00Z"
    },
    {
      "guid": "workstation-guid-2",
      "location": "Production Floor B",
      "type": "Machine",
      "is_active": true,
      "created_at": "2023-01-02T12:00:00Z"
    }
  ]
}
```

**Example:**
```bash
curl -X GET -H "Authorization: Bearer <your_access_token>" \
     "http://localhost:8000/api/v1/workstations?type=Assembly" | cat
```

### 3. Get Workstation by GUID (`GET /api/v1/workstations/{guid}`)

**Description:** Retrieve details for a specific workstation by its GUID.

**Authentication:** Requires `Authorization: Bearer <token>` header.

**Response (Success - 200 OK):**
```json
{
  "guid": "workstation-guid",
  "location": "Production Floor A",
  "type": "Assembly",
  "is_active": true,
  "created_at": "2023-01-01T12:00:00Z",
  "updated_at": "2023-01-02T12:00:00Z"
}
```

**Example:**
```bash
curl -X GET -H "Authorization: Bearer <your_access_token>" \
     http://localhost:8000/api/v1/workstations/550e8400-e29b-41d4-a716-446655440000 | cat
```

### 4. Update Workstation (`PUT /api/v1/workstations/{guid}`)

**Description:** Update workstation details including location, type, and active status.

**Authentication:** Requires `Authorization: Bearer <token>` header with SystemAdmin or CompanyAdmin role.

**Request Body:**
```json
{
  "location": "Updated Floor Location",  // Optional
  "type": "Control",                     // Optional, must be one of: Machine, Assembly, Control, Logistics, Supply
  "is_active": false                     // Optional
}
```

**Response (Success - 200 OK):**
```json
{
  "guid": "workstation-guid",
  "location": "Updated Floor Location",
  "type": "Control",
  "is_active": false,
  "updated_at": "2023-01-03T12:00:00Z"
}
```

**Example:**
```bash
curl -X PUT -H "Content-Type: application/json" \
     -H "Authorization: Bearer <your_access_token>" \
     -d '{"location": "Updated Floor Location"}' \
     http://localhost:8000/api/v1/workstations/550e8400-e29b-41d4-a716-446655440000 | cat
```

### 5. Delete Workstation (`DELETE /api/v1/workstations/{guid}`)

**Description:** Soft-delete a workstation by setting its `is_active` status to `false`.

**Authentication:** Requires `Authorization: Bearer <token>` header with SystemAdmin or CompanyAdmin role.

**Response (Success - 200 OK):**
```json
{
  "message": "Workstation deactivated successfully",
  "guid": "workstation-guid"
}
```

**Example:**
```bash
curl -X DELETE -H "Authorization: Bearer <your_access_token>" \
     http://localhost:8000/api/v1/workstations/550e8400-e29b-41d4-a716-446655440000 | cat
``` 