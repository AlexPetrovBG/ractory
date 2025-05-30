---
title: Get Current User Info (/me)
slug: /auth-api/get-me
---

## `GET /api/v1/auth/me`

Retrieves information about the currently authenticated user or API key.

This endpoint can be used to verify authentication status and obtain basic details of the authenticated principal (user or API key).

### Request

**Method:** `GET`

**Path:** `/api/v1/auth/me`

**Headers:**

*   `Authorization`: `Bearer <access_token>` (string, required for JWT-based auth)
    OR
*   `X-API-Key`: `<your-api-key>` (string, required for API key-based auth)

### Response

**Status Code: 200 OK**

Returns a JSON object containing information about the authenticated user or API key.
The structure of the response varies slightly based on the authentication method (JWT vs. API Key).

**Body (application/json - if authenticated via JWT):**

```json
{
  "guid": "user-guid-12345",
  "email": "user@example.com",
  "role": "COMPANY_ADMIN", // Example role
  "company_guid": "tenant-company-guid-abcde",
  "auth_type": "jwt"
}
```

*   `guid` (UUID, string): The unique identifier of the user.
*   `email` (string, nullable): The email address of the user. Can be `null` if the user record is somehow missing an email (though unlikely for JWT auth).
*   `role` (string, `UserRole` enum): The role of the user (e.g., `SYSTEM_ADMIN`, `COMPANY_ADMIN`, `OPERATOR`).
*   `company_guid` (UUID, string): The GUID of the company/tenant the user belongs to.
*   `auth_type` (string): Always "jwt" for this case.

**Body (application/json - if authenticated via API Key):**

```json
{
  "guid": "api-key-guid-or-associated-user-guid", // This is current_user.user_id, which for API keys might be the key's ID or a service user ID
  "email": null,
  "role": "API_KEY_ROLE", // Example role derived from API key
  "company_guid": "tenant-company-guid-abcde",
  "auth_type": "api_key",
  "scopes": "read:articles write:pieces"
}
```

*   `guid` (UUID, string): The identifier associated with the API key (could be the API key's own GUID or a linked service user's GUID).
*   `email` (null): API keys do not have an associated email address, so this is `null`.
*   `role` (string): The role assigned to or derived from the API key.
*   `company_guid` (UUID, string): The GUID of the company/tenant the API key is associated with.
*   `auth_type` (string): Always "api_key" for this case.
*   `scopes` (string): A space-separated string of scopes granted to the API key (e.g., "read:assemblies write:components").

**Status Code: 401 Unauthorized**

*   If no valid `Authorization` header (for JWT) or `X-API-Key` header is provided, or if the token/key is invalid or expired.

    ```json
    {
      "detail": "Not authenticated"
      // or other specific authentication error messages
    }
    ```

### Important Notes

*   This endpoint is useful for client applications to confirm who is logged in and to get basic profile information.
*   The distinction in response based on `auth_type` allows clients to handle user sessions and API key interactions appropriately. 