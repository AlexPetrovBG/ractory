---
title: QR Code Login
slug: /auth-api/qr-login
---

## `POST /api/v1/auth/qr`

Authenticates an operator (typically a user with an Operator role) for a specific workstation using their User GUID (often embedded in a QR code) and a PIN.

On successful authentication, it returns a workstation-scoped JWT access token, a refresh token, the user's role, and token expiry information.

### Request

**Method:** `POST`

**Path:** `/api/v1/auth/qr`

**Body (application/json - `QrLoginRequest` schema):**

```json
{
  "user_guid": "user-guid-from-qr",
  "workstation_guid": "workstation-guid-where-login-occurs",
  "pin": "1234"
}
```

*   `user_guid` (UUID, string, required): The User GUID, usually obtained from scanning a QR code.
*   `workstation_guid` (UUID, string, required): The GUID of the workstation where the login is occurring.
*   `pin` (string, required): The user's PIN for QR login.

### Response

**Status Code: 200 OK**

Returns a workstation-scoped JWT access token, a refresh token, user role, and expiry time.

**Body (application/json - `TokenResponse` schema):**

```json
{
  "access_token": "string_workstation_scoped_jwt_access_token",
  "refresh_token": "string_workstation_scoped_jwt_refresh_token",
  "role": "OPERATOR_ROLE_ENUM_VALUE",
  "expires_in": 3600 
}
```

*   `access_token` (string): The workstation-scoped JWT access token. This token may have a specific expiry time (e.g., 1 hour / 3600 seconds as suggested by the original router docstring, though `create_tokens` currently uses 15 mins / 900s by default for all tokens unless overridden).
*   `refresh_token` (string): The workstation-scoped JWT refresh token.
*   `role` (string, `UserRole` enum): The role of the authenticated operator (e.g., `OPERATOR`).
*   `expires_in` (integer): The validity period of the access token in seconds. For QR login, this might be 3600 (1 hour) or 900 (15 minutes) depending on `create_tokens` implementation details for workstation-scoped tokens.

**Status Code: 400 Bad Request**

*   If the specified `workstation_guid` does not correspond to an existing workstation.

    ```json
    {
      "detail": "Workstation not found"
    }
    ```

**Status Code: 401 Unauthorized**

*   If the `user_guid`, `workstation_guid`, and `pin` combination is invalid or the user is not authorized for QR login at that workstation.

    ```json
    {
      "detail": "Invalid QR login credentials"
    }
    ```

### Important Notes

*   This login method is designed for operator-level users at specific workstations.
*   The returned `access_token` is specifically for use at that workstation and may have a shorter lifespan than standard user tokens.
*   The `AuthService.validate_qr_login` handles the core logic of validating the credentials against the database, including PIN verification and user-workstation association (if applicable). 