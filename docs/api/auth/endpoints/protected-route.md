---
title: Protected Route (Test)
slug: /auth-api/protected-route
---

## `GET /api/v1/auth/protected`

This is a test endpoint designed to demonstrate role-based access control. Access to this route is restricted to users with the `SYSTEM_ADMIN` role.

### Request

**Method:** `GET`

**Path:** `/api/v1/auth/protected`

**Headers:**

*   `Authorization`: `Bearer <access_token>` (string, required)
    (The access token must belong to a user with the `SYSTEM_ADMIN` role.)

### Response

**Status Code: 200 OK**

Returned if the authenticated user is a `SYSTEM_ADMIN`.

**Body (application/json):**

```json
{
  "message": "You have access to this protected route",
  "user_id": "system-admin-user-guid",
  "role": "SYSTEM_ADMIN",
  "tenant": "system-admin-tenant-guid-or-null"
}
```

*   `message` (string): A success message indicating access is granted.
*   `user_id` (UUID, string): The GUID of the authenticated System Admin user.
*   `role` (string): The role of the user, which will be `SYSTEM_ADMIN`.
*   `tenant` (UUID, string, nullable): The tenant GUID associated with the System Admin's token. This might be a specific tenant or `null` depending on the context of the System Admin's session.

**Status Code: 403 Forbidden**

*   If the authenticated user does not have the `SYSTEM_ADMIN` role.

    ```json
    {
      "detail": "User does not have the required role: SYSTEM_ADMIN"
      // Or a more generic "Forbidden" message depending on RBAC middleware
    }
    ```

**Status Code: 401 Unauthorized**

*   If no valid `Authorization` header is provided, or if the token is invalid or expired.

    ```json
    {
      "detail": "Not authenticated"
      // Or other specific authentication error messages
    }
    ```

### Important Notes

*   This endpoint primarily serves as an example or test case for verifying `SYSTEM_ADMIN` role enforcement.
*   The `require_system_admin` dependency in the route definition handles the role check. 