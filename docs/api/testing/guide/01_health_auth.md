## 1. Health Check Tests

### 1.1 Root Health Check (`GET /health`)
```bash
cURL http://localhost:8000/health | jq '.'
```
**Expected (200 OK):**
```json
{
  "status": "healthy",
  "version": "x.y.z",
  "api_version": "v1"
}
```

### 1.2 API v1 Health Check (`GET /api/v1/health`)
```bash
cURL http://localhost:8000/api/v1/health | jq '.'
```
**Expected (200 OK):**
```json
{
  "status": "healthy",
  "version": "x.y.z",
  "api_version": "v1",
  "environment": "development", // Or your current environment
  "database": "connected"
}
```

## 2. Authentication Tests (`/auth`)

### 2.1 JWT Authentication

#### 2.1.1 Login (`POST /api/v1/auth/login`)
```bash
# Test valid credentials (SystemAdmin example, use $ADMIN_EMAIL, $ADMIN_PASSWORD from setup)
curl -X POST -H "Content-Type: application/json" \
     -d "{\"email\": \"$ADMIN_EMAIL\", \"password\": \"$ADMIN_PASSWORD\"}" \
     http://localhost:8000/api/v1/auth/login | jq '.'
```
**Expected (200 OK):**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "role": "SystemAdmin",
  "expires_in": 900
}
```

```bash
# Test invalid credentials
curl -X POST -H "Content-Type: application/json" \
     -d '{"email": "a.petrov@delice.bg", "password": "wrong_password"}' \
     http://localhost:8000/api/v1/auth/login | jq '.'
```
**Expected (401 Unauthorized):** Error message indicating invalid credentials.

#### 2.1.2 Token Refresh (`POST /api/v1/auth/refresh`)
Using `$ADMIN_REFRESH_TOKEN` obtained during setup.
```bash
curl -X POST -H "Content-Type: application/json" \
     -d "{\"refresh_token\": \"$ADMIN_REFRESH_TOKEN\"}" \
     http://localhost:8000/api/v1/auth/refresh | jq '.'
```
**Expected (200 OK):** New `access_token`, `refresh_token`, `role`, `expires_in`.

#### 2.1.3 Current User Info (`GET /api/v1/auth/me`)
Requires a valid access token (e.g., `$ADMIN_ACCESS_TOKEN` or another user's token).
```bash
# Example with Admin token
curl -X GET -H "Authorization: Bearer $ADMIN_ACCESS_TOKEN" \
     http://localhost:8000/api/v1/auth/me | jq '.'
```
**Expected (200 OK for JWT):**
```json
{
  "guid": "user-guid",
  "email": "user@example.com",
  "role": "UserRole",
  "company_guid": "user-company-guid",
  "auth_type": "jwt"
}
```
**For API Key Auth (if testing `/me` with an API Key):**
```json
{
  "guid": "api-key-guid-as-user-id",
  "email": null,
  "role": "Integration", // Or role derived from scopes
  "company_guid": "key-company-guid",
  "auth_type": "api_key",
  "scopes": "scope1 scope2"
}
```

### 2.2 QR Authentication (`POST /api/v1/auth/qr`)
Requires a valid Operator `user_guid`, `workstation_guid`, and `pin`.
```bash
# Setup: Ensure an Operator user and a Workstation are created. 
# Define: OPERATOR_USER_GUID, WORKSTATION_GUID, OPERATOR_PIN

cURL -X POST -H "Content-Type: application/json" \
     -d "{
       \"user_guid\": \"$OPERATOR_USER_GUID\",
       \"workstation_guid\": \"$WORKSTATION_GUID\",
       \"pin\": \"$OPERATOR_PIN\"
     }" \
     http://localhost:8000/api/v1/auth/qr | jq '.'
```
**Expected (200 OK):** TokenResponse with Operator role.
*   `400 Bad Request`: If workstation not found.
*   `401 Unauthorized`: If invalid credentials.

### 2.3 Protected Test Route (`GET /api/v1/auth/protected`)
Requires SystemAdmin token (`$ADMIN_ACCESS_TOKEN`).
```bash
cURL -X GET -H "Authorization: Bearer $ADMIN_ACCESS_TOKEN" \
     http://localhost:8000/api/v1/auth/protected | jq '.'
```
**Expected (200 OK):** Details confirming SystemAdmin access.

### 2.4 Mock Authentication (`POST /api/v1/mock-auth`)
```bash
cURL -X POST -H "Content-Type: application/json" \
     -d '{"email": "a.petrov@delice.bg", "password": "password"}' \
     http://localhost:8000/api/v1/mock-auth | jq '.'
```
**Expected (200 OK):** Mock TokenResponse (e.g., role `CompanyAdmin`). 