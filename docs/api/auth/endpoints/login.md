---
title: Login (Email/Password)
slug: /auth-api/login
---

## `POST /api/v1/auth/login`

Authenticates a user with their email address and password.

On successful authentication, it returns a JWT access token, a refresh token, the user's role, and token expiry information.

### Request

**Method:** `POST`

**Path:** `/api/v1/auth/login`

**Body (application/json - `LoginRequest` schema):**

```json
{
  "email": "user@example.com",
  "password": "string"
}
```

*   `email` (string, required): The user's email address.
*   `password` (string, required): The user's password.

### Response

**Status Code: 200 OK**

Returns JWT access and refresh tokens, user role, and expiry time.

**Body (application/json - `TokenResponse` schema):**

```json
{
  "access_token": "string_jwt_access_token",
  "refresh_token": "string_jwt_refresh_token",
  "role": "USER_ROLE_ENUM_VALUE",
  "expires_in": 900
}
```

*   `access_token` (string): The JWT access token.
*   `refresh_token` (string): The JWT refresh token.
*   `role` (string, `UserRole` enum): The role of the authenticated user (e.g., `SYSTEM_ADMIN`, `COMPANY_ADMIN`, `OPERATOR`).
*   `expires_in` (integer): The validity period of the access token in seconds (e.g., 900 for 15 minutes).

**Status Code: 401 Unauthorized**

*   If the provided email or password is invalid.

    ```json
    {
      "detail": "Invalid email or password"
    }
    ```

### Important Notes

*   The `access_token` should be sent in the `Authorization` header as a Bearer token for subsequent authenticated requests (e.g., `Authorization: Bearer <access_token>`).
*   The `refresh_token` is used to obtain a new `access_token` via the [Refresh Token](./refresh-token.md) endpoint when the current access token expires. 