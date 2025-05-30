---
title: Refresh Token
slug: /auth-api/refresh-token
---

## `POST /api/v1/auth/refresh`

Refreshes an access token using a valid refresh token. The refresh token can be provided either in the request body or as an `HttpOnly` cookie named `refresh_token`.

Upon successful validation, a new pair of access and refresh tokens is issued, along with role and expiry information. The new refresh token is also set as an `HttpOnly`, `Secure`, `SameSite=Strict` cookie.

### Request

**Method:** `POST`

**Path:** `/api/v1/auth/refresh`

**Body (application/json - `RefreshRequest` schema, optional):**

```json
{
  "refresh_token": "string_jwt_refresh_token"
}
```

*   `refresh_token` (string, optional): The JWT refresh token. Required if not sent as a cookie.

**Cookies:**

*   `refresh_token` (string, optional): The JWT refresh token can be sent as an `HttpOnly` cookie. If both body and cookie are present, the body might take precedence (verify specific implementation behavior if necessary, though typical use is one or the other).

### Response

**Status Code: 200 OK**

Returns a new JWT access token, a new refresh token, user role, and expiry time. The new refresh token is also set as an `HttpOnly` cookie.

**Body (application/json - `TokenResponse` schema):**

```json
{
  "access_token": "new_string_jwt_access_token",
  "refresh_token": "new_string_jwt_refresh_token",
  "role": "USER_ROLE_ENUM_VALUE",
  "expires_in": 900
}
```

*   `access_token` (string): The new JWT access token.
*   `refresh_token` (string): The new JWT refresh token (this is also set as an HttpOnly cookie in the response headers).
*   `role` (string, `UserRole` enum): The role of the user associated with the token.
*   `expires_in` (integer): The validity period of the new access token in seconds (e.g., 900 for 15 minutes).

**Response Headers:**

*   `Set-Cookie`: `refresh_token=new_string_jwt_refresh_token; Max-Age=604800; Path=/; HttpOnly; Secure; SameSite=Strict` (The actual path might vary based on API gateway/proxy configuration, but `HttpOnly`, `Secure`, and `SameSite=Strict` are set by the application).

**Status Code: 401 Unauthorized**

*   If the refresh token is missing (neither in body nor as a cookie).

    ```json
    {
      "detail": "Refresh token is required"
    }
    ```
*   If the provided refresh token is invalid, expired, or revoked.

    ```json
    {
      "detail": "Invalid or expired refresh token: <specific error message>",
      "headers": {"WWW-Authenticate": "Bearer"} // Note: headers in detail might be a documentation artifact, actual headers are HTTP response headers.
    }
    ```
    (The actual error message for an invalid token might vary.)

### Important Notes

*   This endpoint is crucial for maintaining an active session without requiring the user to log in repeatedly.
*   The new `refresh_token` received in the response body (and set as a cookie) should be securely stored by the client to be used for future refresh attempts.
*   The `HttpOnly` nature of the cookie helps mitigate XSS attacks by preventing client-side JavaScript from accessing the refresh token.
*   The `Secure` flag ensures the cookie is only sent over HTTPS.
*   The `SameSite=Strict` flag provides protection against CSRF attacks. 