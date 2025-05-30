# Update API Key

**Endpoint:** `PUT /api/v1/api-keys/{guid}`

**Description:**
Updates an API key's description, scopes, or active status.
- `CompanyAdmin` can only update keys belonging to their own company.
- `SystemAdmin` can update any key by its GUID.

Partial updates are allowed; only include the fields you want to change in the request body.

**Path Parameter:**

-   **`guid`** (UUID, required): The GUID of the API key to update.

**Request Body (`ApiKeyUpdate` schema):**

```json
{
  "description": "Optional: Updated description for the key",
  "scopes": "Optional: sync:write",
  "is_active": false 
}
```

-   **`description`** (string, optional): The new description for the key. If omitted, the description is not changed.
-   **`scopes`** (string, optional): The new comma-separated list of scopes. If omitted, scopes are not changed. Valid scopes are `sync:read` and `sync:write`.
-   **`is_active`** (boolean, optional): The new active status for the key. If omitted, the status is not changed.

**Response (Success: 200 OK, `ApiKeyResponse` schema):**

The updated API key metadata.

```json
{
  "guid": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "description": "Updated description for the key",
  "scopes": "sync:write",
  "created_at": "2023-10-26T10:00:00Z",
  "last_used_at": "2023-10-27T08:15:00Z",
  "is_active": false,
  "company_guid": "z9y8x7w6-v5u4-t3s2-r1q0-p9o8n7m6l5k4"
}
```

**Possible Errors:**

-   `401 Unauthorized`: If authentication fails.
-   `403 Forbidden`:
    -   If the authenticated user does not have `CompanyAdmin` or `SystemAdmin` role.
    -   If a `CompanyAdmin` tries to update an API key not belonging to their company.
-   `404 Not Found`: If an API key with the specified `guid` does not exist.
-   `422 Unprocessable Entity`:
    -   If the `guid` path parameter is not a valid UUID.
    -   If `scopes` contains invalid scope values.
    -   Other validation errors for request body fields.
-   `500 Internal Server Error`: If an unexpected error occurs during the update. 