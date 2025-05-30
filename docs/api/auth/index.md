---
title: Authentication API
slug: /auth-api
---

This guide provides a comprehensive overview of the Authentication (Auth) API endpoints, enabling user and system authentication within the Ra Factory platform.

The Auth API allows for:

*   **Standard Login:** Authenticate users via email and password.
*   **Token Refresh:** Obtain new access tokens using a refresh token.
*   **QR Code Login:** Authenticate operators at workstations using a QR code (User GUID) and PIN.
*   **User Information:** Retrieve details about the currently authenticated user or API key.

## API Base Path

All Auth API endpoints are relative to the following base path:

`/api/v1/auth`

## Token Types

*   **Access Token:** A short-lived JWT used to authenticate API requests. Included in the `Authorization: Bearer <token>` header.
*   **Refresh Token:** A longer-lived token used to obtain a new access token. Can be provided in request body or as an `HttpOnly` cookie.
*   **Workstation Token:** A JWT specifically scoped to a workstation, typically with a shorter expiry (e.g., 1 hour), issued via QR login.

Explore the following sections for detailed information on each endpoint:

*   [Login (Email/Password)](./endpoints/login.md)
*   [Refresh Token](./endpoints/refresh-token.md)
*   [QR Code Login](./endpoints/qr-login.md)
*   [Get Current User Info (`/me`)](./endpoints/get-me.md)
*   [Protected Route (Test)](./endpoints/protected-route.md)

# Authentication

The Ra Factory API supports multiple authentication methods to cater to different use cases, primarily JWT-based authentication for users and API Key based authentication for system integrations.

## Endpoints

### 1. Login (`POST /api/v1/auth/login`)

**Description:** Authenticates a user with their email and password. Returns JWT access and refresh tokens upon successful authentication.

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
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "role": "UserRole",
  "expires_in": 900
}
```

### 2. Refresh Token (`POST /api/v1/auth/refresh`)

**Description:** Obtains a new access token using a valid refresh token. The refresh token can be provided in the request body or as an `HttpOnly` cookie.

**Request Body (Option 1):**
```json
{
  "refresh_token": "<your_refresh_token>"
}
```
**Request (Option 2 - Cookie):** The request should include the `refresh_token` cookie.

**Response (Success - 200 OK):** Same as login response.

### 3. QR Login (`POST /api/v1/auth/qr`)

**Description:** Authenticates an operator using their User GUID (from QR code), a Workstation GUID, and their PIN. Returns a short-lived, workstation-scoped JWT.

**Request Body:**
```json
{
  "user_guid": "uuid-of-user",
  "workstation_guid": "uuid-of-workstation",
  "pin": "123456"
}
```
**Response (Success - 200 OK):** Same as login response.

### 4. Get Current User Info (`GET /api/v1/auth/me`)

**Description:** Gets information about the currently authenticated user based on the provided access token or API key.

**Authentication:** Requires `Authorization: Bearer <token>` or `X-API-Key: <key>` header.

**Response (Success - 200 OK for JWT):**
```json
{
  "guid": "user-guid",
  "email": "user@example.com",
  "role": "UserRole",
  "company_guid": "company-guid",
  "auth_type": "jwt"
}
```

**Response (Success - 200 OK for API Key):**
```json
{
  "guid": "api-key-guid-as-user-id",
  "email": null,
  "role": "Integration", // Or role associated with key scopes
  "company_guid": "company-guid",
  "auth_type": "api_key",
  "scopes": "sync:read sync:write"
}
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

### Mock Authentication

#### `POST /api/v1/mock-auth`
**Description:** A mock authentication endpoint for development/testing without a database. Bypasses actual credential validation.

**Request Body:** Same as `/api/v1/auth/login`.
**Response (Success - 200 OK):** Same format as login response, with mock tokens. 