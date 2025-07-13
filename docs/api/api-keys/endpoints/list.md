# List API Keys

**Endpoint:** `GET /api/v1/api-keys`

**Description:**
Retrieves a list of all API keys for the authenticated user's company. 
- If you are a `CompanyAdmin`, this returns keys for your company.
- If you are a `SystemAdmin`, this endpoint (as currently implemented in the router `app.api.v1.api_keys.router`) will also return keys associated with your `current_user.tenant` (i.e., your own company, if applicable). To list keys for *any* company as a SystemAdmin, a different endpoint or a query parameter would typically be required (e.g., `GET /api/v1/system/companies/{company_guid}/api-keys` or `GET /api/v1/api-keys?company_guid=xxx`). *This guide reflects the current specific endpoint behavior.*

The actual API key values (`key`) are **not** returned, only their metadata.

**Request Parameters:**

None.

**Response (Success: 200 OK, `ApiKeyList` schema):**

```json
{
  "api_keys": [
    {
      "guid": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
      "description": "Main integration key",
      "scopes": "sync:read,sync:write",
      "created_at": "2023-10-26T10:00:00Z",
      "last_used_at": "2023-10-27T08:15:00Z",
      "is_active": true,
      "company_guid": "z9y8x7w6-v5u4-t3s2-r1q0-p9o8n7m6l5k4"
    },
    {
      "guid": "b2c3d4e5-f6a7-8901-2345-678901bcdef0",
      "description": "Read-only sync key",
      "scopes": "sync:read",
      "created_at": "2023-09-15T14:30:00Z",
      "last_used_at": null,
      "is_active": true,
      "company_guid": "z9y8x7w6-v5u4-t3s2-r1q0-p9o8n7m6l5k4"
    }
    // ... more keys
  ]
}
```

-   Each object in the `api_keys` list follows the `ApiKeyResponse` schema:
    -   **`guid`** (UUID): The unique identifier for the API key object.
    -   **`description`** (string, optional): The description.
    -   **`scopes`** (string, optional): Assigned scopes.
    -   **`created_at`** (datetime): Timestamp of creation.
    -   **`last_used_at`** (datetime, optional): Timestamp of the last time the key was used for authentication. `null` if never used.
    -   **`is_active`** (boolean): Whether the key is currently active.
    -   **`company_guid`** (UUID): The company GUID the key is associated with.

**Possible Errors:**

-   `401 Unauthorized`: If authentication fails.
-   `403 Forbidden`: If the authenticated user does not have `CompanyAdmin` or `SystemAdmin` role.
-   `500 Internal Server Error`: If an unexpected error occurs. 