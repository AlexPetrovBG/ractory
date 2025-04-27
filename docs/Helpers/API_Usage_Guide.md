# Ra Factory API Usage Guide

This document provides a human-readable guide to the Ra Factory API endpoints, based on the `openapi_schema.json`.

**Base URL (Development):** `http://localhost:8000`

**General Notes:**

*   Most `POST` and `PUT` requests expect a JSON body with `Content-Type: application/json`.
*   Endpoints requiring authentication expect a Bearer token in the `Authorization` header: `Authorization: Bearer <your_access_token>`. Obtain this token from the `/api/v1/auth/login` endpoint.

---

## User Roles

The API uses the following roles for access control. Roles are assigned to users and determine what actions they can perform.

*   **`SystemAdmin`**: Highest privileges, including cross-company access and system configuration.
*   **`CompanyAdmin`**: Full permissions (Create, Read, Update, Delete) for all data within their assigned company.
*   **`ProjectManager`**: Can read project data and manage logistics-related information within their company.
*   **`Operator`**: Limited permissions, typically restricted to actions at specific workstations on the shop floor (often authenticated via QR code).
*   **`Integration`**: Used for machine-to-machine communication, granting specific permissions for automated tasks like data synchronization.

---

## Authentication System

The Ra Factory API uses bcrypt for password hashing and JWT (JSON Web Tokens) for session management. Authentication data is stored in the PostgreSQL database and follows a multi-tenant data architecture with Row-Level Security (RLS).

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
    { "code": "P001", "creation_date": "...", "id": 1, /* ... other project fields */ },
    { "code": "P002", "creation_date": "...", "id": 2, /* ... other project fields */ }
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