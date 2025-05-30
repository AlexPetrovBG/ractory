# Get API Key

**Endpoint:** `GET /api/v1/api-keys/{guid}`

**Description:**
Retrieves metadata for a specific API key by its GUID. 
- `CompanyAdmin` can only retrieve keys belonging to their own company.
- `SystemAdmin` can retrieve any key by its GUID.

The actual API key value (`key`) is **not** returned, only its metadata.

**Path Parameter:**

-   **`guid`** (UUID, required): The GUID of the API key to retrieve.

**Response (Success: 200 OK, `ApiKeyResponse` schema):**

```json
{
  "guid": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "description": "Main integration key",
  "scopes": "sync:read,sync:write",
  "created_at": "2023-10-26T10:00:00Z",
  "last_used_at": "2023-10-27T08:15:00Z",
  "is_active": true,
  "company_guid": "z9y8x7w6-v5u4-t3s2-r1q0-p9o8n7m6l5k4"
}
```

-   **`guid`** (UUID): The unique identifier for the API key object.
-   **`description`** (string, optional): The description.
-   **`scopes`** (string, optional): Assigned scopes.
-   **`created_at`** (datetime): Timestamp of creation.
-   **`last_used_at`** (datetime, optional): Timestamp of the last time the key was used. `null` if never used.
-   **`is_active`** (boolean): Whether the key is currently active.
-   **`company_guid`** (UUID): The company GUID the key is associated with.

**Possible Errors:**

-   `401 Unauthorized`: If authentication fails.
-   `403 Forbidden`:
    -   If the authenticated user does not have `CompanyAdmin` or `SystemAdmin` role.
    -   If a `CompanyAdmin` tries to access an API key not belonging to their company.
-   `404 Not Found`: If an API key with the specified `guid` does not exist.
-   `422 Unprocessable Entity`: If the `guid` path parameter is not a valid UUID.
-   `500 Internal Server Error`: If an unexpected error occurs. 