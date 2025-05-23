# Ra Factory API Usage Guide

This document provides a comprehensive guide to securely accessing and using the Ra Factory API endpoints.

## Quick Start Guide

1. **Authentication**:
   - Obtain an access token via `/api/v1/auth/login`
   - Include token in all subsequent requests: `Authorization: Bearer <access_token>`
   - Refresh token before expiration (900 seconds) using `/api/v1/auth/refresh`

2. **API Key Alternative**:
   - For system integration, use API keys instead of JWT tokens
   - Include via header: `X-API-Key: rfk_your_api_key`

3. **Content Type**:
   - All requests must include: `Content-Type: application/json`
   - Responses are always JSON formatted

## Security Best Practices

1. **Token Management**:
   - Never share or expose access tokens
   - Store tokens securely (e.g., secure HTTP-only cookies)
   - Refresh tokens before expiration
   - Implement proper token rotation

2. **API Key Security**:
   - Treat API keys as sensitive credentials
   - Use environment variables for storage
   - Rotate keys periodically
   - Use scoped keys with minimal required permissions

3. **Error Handling**:
   - Implement proper retry logic for 429 (Rate Limit) responses
   - Handle 401 (Unauthorized) by refreshing tokens
   - Never log sensitive data (tokens, keys, passwords)

## Authentication Methods

### 1. JWT Authentication (Recommended for Web Applications)

```bash
# 1. Login to obtain tokens
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "your_password"}'

# Response contains:
{
  "access_token": "eyJ...",  # Valid for 900 seconds
  "refresh_token": "eyJ...", # Use to obtain new access tokens
  "role": "UserRole",
  "expires_in": 900
}

# 2. Use access token for subsequent requests
curl -X GET http://localhost:8000/api/v1/protected-endpoint \
  -H "Authorization: Bearer eyJ..."

# 3. Refresh token before expiration
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "eyJ..."}'
```

### 2. API Key Authentication (Recommended for System Integration)

```bash
# Using X-API-Key header (recommended)
curl -X GET http://localhost:8000/api/v1/protected-endpoint \
  -H "X-API-Key: rfk_your_api_key"

# Alternative: Using Authorization header
curl -X GET http://localhost:8000/api/v1/protected-endpoint \
  -H "Authorization: ApiKey rfk_your_api_key"
```

### 3. QR Code Authentication (For Operator Workstations)

```bash
# Authenticate operator with QR code data
curl -X POST http://localhost:8000/api/v1/auth/qr \
  -H "Content-Type: application/json" \
  -d '{
    "user_guid": "uuid-from-qr",
    "workstation_guid": "workstation-uuid",
    "pin": "123456"
  }'
```

## Role-Based Access Control (RBAC)

The API implements a strict role hierarchy that determines access permissions:

1. **SystemAdmin**
   - Full system access across all companies
   - Can manage all user roles
   - Access to system configuration
   - Example endpoints: `/api/v1/auth/protected`

2. **CompanyAdmin**
   - Company-wide access
   - User management within company
   - Cannot access other companies' data
   - Example endpoints: `/api/v1/users`, `/api/v1/api-keys`

3. **ProjectManager**
   - Project data access
   - Logistics management
   - No user management permissions
   - Example endpoints: `/api/v1/projects`

4. **Operator**
   - Workstation-specific access
   - QR code authentication
   - Limited to assigned tasks
   - Example endpoints: `/api/v1/workstations/{guid}`

5. **Integration**
   - API key access
   - Scoped permissions
   - Data synchronization
   - Example endpoints: `/api/v1/sync/*`

## Multi-Tenant Security

The API enforces strict data isolation between companies:

1. **Company Isolation**:
   - Each request is scoped to the user's company
   - Cross-company access prevented by Row-Level Security
   - SystemAdmin role can bypass isolation

2. **Data Access**:
   - All entities linked to company_guid
   - Automatic filtering based on user's company
   - Proper error messages for cross-company attempts

## Error Handling

Common HTTP status codes and their meaning:

- 200: Success
- 201: Resource created
- 400: Invalid request data
- 401: Authentication required/failed
- 403: Insufficient permissions
- 404: Resource not found
- 429: Too many requests
- 500: Server error

Example error response:
```json
{
  "error": "Detailed error message",
  "status_code": 401,
  "suggestion": "Action to resolve the error"
}
```

## Rate Limiting

- Implement exponential backoff for retries
- Handle 429 responses appropriately
- Default limits: [Add your rate limits here]

## API Versioning

Current version: v1
Base URL: `http://localhost:8000/api/v1`

Future versions will be available at `/api/v2`, etc.

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

These endpoints are used to bulk insert or update data, typically synchronized from an external source like RaConnect. They require authentication (Admin role or specific API key scope).

**Important GUID Notes:**
- All entities (projects, components, assemblies, pieces, articles) use UUIDs (GUIDs) as primary keys
- GUIDs are automatically generated if not provided
- Foreign key relationships use GUIDs instead of integer IDs
- Company isolation is enforced through company_guid
- All GUIDs must be valid UUID v4 format

**Authentication:** Requires `Authorization: Bearer <token>` header.

**Response (Success - 200 OK) for all sync endpoints:**
```json
{
  "inserted": 10, // Number of records inserted
  "updated": 5    // Number of records updated
}
```

### Data Modification Guide

#### Update Operations

Unlike traditional RESTful APIs, Ra Factory does not implement PUT/PATCH endpoints for entity updates. Instead, all data modifications (create, update, delete) are performed through the sync endpoints:

- `/api/v1/sync/projects` - For project updates
- `/api/v1/sync/components` - For component updates
- `/api/v1/sync/assemblies` - For assembly updates
- `/api/v1/sync/pieces` - For piece updates
- `/api/v1/sync/articles` - For article updates

#### How to Update Entities

To update an existing entity, include its GUID in the request body along with the updated fields:

```bash
# Example: Updating a project
curl -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer <token>" \
     -d '{
       "projects": [
         {
           "guid": "existing-project-guid",  # GUID identifies this as an update operation
           "code": "UPDATED_CODE",
           "company_guid": "your-company-guid"
         }
       ]
     }' \
     http://localhost:8000/api/v1/sync/projects
```

The API will:
1. Recognize this as an update operation because the GUID exists
2. Update only the fields you provide, leaving other fields unchanged
3. Return counts of inserted and updated records

#### Implementation Notes

- If the GUID exists, the record is updated
- If the GUID doesn't exist, a new record is created
- Only include fields you want to update
- Always include required fields (e.g., company_guid)
- For successful updates, "updated" count will be incremented in the response

### 1. Sync Projects (`POST /api/v1/sync/projects`)

**Description:** Bulk insert/update project data.

**Request Body:**
```json
{
  "projects": [
    {
      "code": "P001",
      "guid": "550e8400-e29b-41d4-a716-446655440000",  // Optional, will be generated if not provided
      "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71",
      "due_date": "2024-12-31T23:59:59Z",
      "in_production": false,
      "company_name": "Example Corp"
    }
    // ... more projects
  ]
}
```

### 2. Sync Components (`POST /api/v1/sync/components`)

**Description:** Bulk insert/update component data.

**Request Body:**
```json
{
  "components": [
    {
      "code": "C001",
      "guid": "550e8400-e29b-41d4-a716-446655440001",  // Optional, will be generated if not provided
      "project_guid": "550e8400-e29b-41d4-a716-446655440000",  // Required, must reference existing project
      "designation": "Main Component",
      "quantity": 1,
      "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71"
    }
    // ... more components
  ]
}
```

### 3. Sync Assemblies (`POST /api/v1/sync/assemblies`)

**Description:** Bulk insert/update assembly data.

**Request Body:**
```json
{
  "assemblies": [
    {
      "guid": "550e8400-e29b-41d4-a716-446655440002",  // Optional, will be generated if not provided
      "project_guid": "550e8400-e29b-41d4-a716-446655440000",  // Required
      "component_guid": "550e8400-e29b-41d4-a716-446655440001",  // Required
      "trolley_cell": "A1",
      "trolley": "T1",
      "cell_number": 1,
      "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71"
    }
    // ... more assemblies
  ]
}
```

### 4. Sync Pieces (`POST /api/v1/sync/pieces`)

**Description:** Bulk insert/update piece data (e.g., profiles). Maximum 1000 pieces per request.

**Request Body:**
```json
{
  "pieces": [
    {
      "guid": "550e8400-e29b-41d4-a716-446655440003",  // Optional, will be generated if not provided
      "piece_id": "PIECE001",  // Required
      "project_guid": "550e8400-e29b-41d4-a716-446655440000",  // Required
      "component_guid": "550e8400-e29b-41d4-a716-446655440001",  // Required
      "assembly_guid": "550e8400-e29b-41d4-a716-446655440002",  // Optional
      "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71",
      // ... other optional fields
      "outer_length": 100,
      "angle_left": 45,
      "angle_right": 45,
      "barcode": "BAR123",
      "profile_code": "PRF001"
    }
    // ... more pieces (up to 1000)
  ]
}
```

### 5. Sync Articles (`POST /api/v1/sync/articles`)

**Description:** Bulk insert/update article data (e.g., hardware, accessories).

**Request Body:**
```json
{
  "articles": [
    {
      "guid": "550e8400-e29b-41d4-a716-446655440004",  // Optional, will be generated if not provided
      "code": "A001",  // Required
      "project_guid": "550e8400-e29b-41d4-a716-446655440000",  // Required
      "component_guid": "550e8400-e29b-41d4-a716-446655440001",  // Required
      "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71",
      "designation": "Hardware Item",
      "quantity": 1.0,
      "unit": "pcs",
      // ... other optional fields
    }
    // ... more articles
  ]
}
```

**Important Notes on Data Relationships:**

1. **Hierarchical Dependencies:**
   - Projects are top-level entities
   - Components must reference a valid project_guid
   - Assemblies must reference valid project_guid and component_guid
   - Pieces must reference valid project_guid and component_guid, with optional assembly_guid
   - Articles must reference valid project_guid and component_guid

2. **Company Isolation:**
   - All entities must belong to a company (company_guid)
   - Users can only access/modify entities within their company
   - SystemAdmin role can access all companies

3. **GUID Generation:**
   - If not provided, GUIDs are automatically generated using UUID v4
   - If provided, GUIDs must be valid UUID v4 format
   - GUIDs must be unique across all instances of an entity type

4. **Validation:**
   - Foreign key relationships are strictly enforced
   - Referenced GUIDs must exist in the database
   - Company_guid must match the authenticated user's company
   - Bulk operations are atomic - all succeed or all fail

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
  "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71",  // Required - the company GUID this user belongs to
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
  "company_guid": "company-guid",
  "is_active": true,
  "created_at": "2023-01-01T12:00:00Z"
}
```

**Example:**
```bash
curl -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer <your_access_token>" \
     -d '{
       "email": "new.user@example.com",
       "password": "secure_password",
       "role": "CompanyAdmin",
       "company_guid": "your-company-guid"
     }' \
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

**Description:** Soft-delete a user by setting their `is_active`

## Endpoint Categories

### Authentication Endpoints

1. **Login** - `POST /api/v1/auth/login`
   - Required Role: None
   - Rate Limit: 5 requests per minute
   - Use for: Web application user login
   ```json
   {
     "email": "user@example.com",
     "password": "your_password"
   }
   ```

2. **Refresh Token** - `POST /api/v1/auth/refresh`
   - Required Role: None
   - Rate Limit: 10 requests per minute
   - Use for: Obtaining new access tokens
   ```json
   {
     "refresh_token": "your_refresh_token"
   }
   ```

3. **QR Login** - `POST /api/v1/auth/qr`
   - Required Role: None
   - Rate Limit: 5 requests per minute
   - Use for: Operator workstation authentication
   ```json
   {
     "user_guid": "uuid-from-qr",
     "workstation_guid": "workstation-uuid",
     "pin": "123456"
   }
   ```

### User Management Endpoints

1. **Create User** - `POST /api/v1/users`
   - Required Role: SystemAdmin or CompanyAdmin
   - Company Isolation: Yes
   - Use for: Creating new users within company
   ```json
   {
     "email": "new.user@example.com",
     "password": "secure_password",
     "role": "ProjectManager",
     "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71",  // Required - the company GUID this user belongs to
     "pin": "123456",  // Optional, typically for Operator role
     "is_active": true  // Optional, defaults to true
   }
   ```

2. **List Users** - `GET /api/v1/users`
   - Required Role: SystemAdmin or CompanyAdmin
   - Company Isolation: Yes
   - Query Parameters:
     - `role`: Filter by role
     - `active`: Filter by active status

### Workstation Management Endpoints

1. **Create Workstation** - `POST /api/v1/workstations`
   - Required Role: SystemAdmin or CompanyAdmin
   - Company Isolation: Yes
   - Use for: Setting up new workstations
   ```json
   {
     "location": "Assembly Line 1",
     "type": "Assembly",
     "is_active": true
   }
   ```

2. **List Workstations** - `GET /api/v1/workstations`
   - Required Role: Any authenticated user
   - Company Isolation: Yes
   - Query Parameters:
     - `type`: Filter by workstation type
     - `active`: Filter by active status

### Data Synchronization Endpoints

1. **Sync Projects** - `POST /api/v1/sync/projects`
   - Required Role: Integration or SystemAdmin
   - Rate Limit: 100 requests per minute
   - Batch Size: Maximum 1000 projects
   - Company Isolation: Yes
   ```json
   {
     "projects": [
       {
         "code": "PRJ001",
         "company_guid": "your-company-guid",
         "due_date": "2024-12-31T23:59:59Z"
       }
     ]
   }
   ```

2. **Sync Components** - `POST /api/v1/sync/components`
   - Required Role: Integration or SystemAdmin
   - Rate Limit: 100 requests per minute
   - Batch Size: Maximum 1000 components
   - Company Isolation: Yes

## Common Integration Patterns

### 1. Web Application Integration

```javascript
// Example of proper token management
class ApiClient {
  constructor(baseUrl) {
    this.baseUrl = baseUrl;
    this.accessToken = null;
    this.refreshToken = null;
    this.tokenExpiry = null;
  }

  async login(email, password) {
    const response = await fetch(`${this.baseUrl}/api/v1/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    
    const data = await response.json();
    this.accessToken = data.access_token;
    this.refreshToken = data.refresh_token;
    this.tokenExpiry = Date.now() + (data.expires_in * 1000);
  }

  async ensureValidToken() {
    if (Date.now() >= this.tokenExpiry - 60000) { // Refresh 1 minute before expiry
      await this.refreshAccessToken();
    }
  }

  async makeRequest(endpoint, options = {}) {
    await this.ensureValidToken();
    return fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers: {
        ...options.headers,
        'Authorization': `Bearer ${this.accessToken}`
      }
    });
  }
}
```

### 2. System Integration

```python
# Example of proper API key usage
import os
import requests

class RaFactoryClient:
    def __init__(self):
        self.api_key = os.environ.get('RA_FACTORY_API_KEY')
        self.base_url = 'http://localhost:8000/api/v1'
        
    def make_request(self, endpoint, method='GET', data=None):
        response = requests.request(
            method,
            f'{self.base_url}{endpoint}',
            headers={'X-API-Key': self.api_key},
            json=data
        )
        response.raise_for_status()
        return response.json()
        
    def sync_projects(self, projects):
        return self.make_request(
            '/sync/projects',
            method='POST',
            data={'projects': projects}
        )
```

### 3. Operator Workstation Integration

```python
# Example of QR code authentication
class WorkstationClient:
    def __init__(self, workstation_guid):
        self.workstation_guid = workstation_guid
        self.base_url = 'http://localhost:8000/api/v1'
        self.access_token = None
        
    async def authenticate_operator(self, user_guid, pin):
        response = await self.post('/auth/qr', {
            'user_guid': user_guid,
            'workstation_guid': self.workstation_guid,
            'pin': pin
        })
        self.access_token = response['access_token']
```

## Security Considerations

### 1. Token Storage
- Never store tokens in localStorage (vulnerable to XSS)
- Use secure HTTP-only cookies for web applications
- Store API keys in environment variables
- Implement proper token rotation

### 2. Error Handling
- Implement retry logic with exponential backoff
- Handle token expiration gracefully
- Log errors without exposing sensitive data
- Validate all input data

### 3. Rate Limiting
- Implement client-side rate limiting
- Use token bucket algorithm
- Handle 429 responses properly
- Add jitter to retry attempts

### 4. Data Validation
- Validate all input data
- Use proper data types
- Handle special characters
- Implement request size limits

## Troubleshooting Guide

### Common Issues

1. **Authentication Failures**
   - Check token expiration
   - Verify correct credentials
   - Ensure proper header format
   - Check company_guid matches

2. **Permission Denied**
   - Verify user role
   - Check company isolation
   - Validate API key scope
   - Review access logs

3. **Rate Limiting**
   - Implement backoff strategy
   - Batch requests when possible
   - Monitor usage patterns
   - Optimize request frequency

### Support Contacts

For technical support:
- Email: support@rafactory.com
- Documentation: https://docs.rafactory.com
- Status Page: https://status.rafactory.com

## Company Fields

Companies now include a new field:
- `company_index`: Integer between 0-99, unique across all companies

## User Fields

Users now include additional fields:
- `name`: User's first name
- `surname`: User's last name
- `picture_path`: Path to user's profile picture

## Workflow System

The workflow system tracks all interactions within the system. Each workflow entry contains:

- `guid`: Unique identifier
- `company_guid`: Associated company
- `company_name`: Company name (for quick reference)
- `workstation_guid`: Associated workstation (optional)
- `workstation_name`: Workstation name (optional)
- `api_key_guid`: Associated API key (optional)
- `user_guid`: Associated user (optional)
- `user_name`: User name (optional)
- `action_type`: Type of action (see below)
- `action_value`: Additional data for the action (optional)
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last update

### Workflow Action Types

The following action types are supported:

1. `barcode_scan`: Scanning of barcodes/QR codes
2. `piece_cut`: Piece cutting operation
3. `assembly_weld`: Assembly welding operation
4. `quality_check`: Quality control check
5. `packaging`: Packaging operation
6. `shipping`: Shipping operation
7. `material_request`: Request for materials
8. `material_received`: Material receipt confirmation
9. `workstation_login`: User login at workstation
10. `workstation_logout`: User logout at workstation
11. `error_report`: Error reporting
12. `maintenance_request`: Maintenance request
13. `system_event`: System-level event

### Example Workflow Entry

```json
{
  "guid": "550e8400-e29b-41d4-a716-446655440000",
  "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71",
  "company_name": "Example Corp",
  "workstation_guid": "550e8400-e29b-41d4-a716-446655440001",
  "workstation_name": "Assembly Line 1",
  "user_guid": "550e8400-e29b-41d4-a716-446655440002",
  "user_name": "John Doe",
  "action_type": "piece_cut",
  "action_value": "Length: 100mm, Angle: 45°",
  "created_at": "2025-05-01T14:30:00Z",
  "updated_at": "2025-05-01T14:30:00Z"
}
```

### Invalid Action Type Handling

When an invalid action type is provided, the API will return a 422 Unprocessable Entity response with a list of valid action types:

```json
{
  "error": "Invalid action_type provided",
  "valid_types": [
    "barcode_scan",
    "piece_cut",
    "assembly_weld",
    // ... other valid types ...
  ]
}
```