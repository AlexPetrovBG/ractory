# Create API Key

**Endpoint:** `POST /api/v1/api-keys`

**Description:**
Creates a new API key. 
- If you are a `CompanyAdmin`, the key is created for your company.
- If you are a `SystemAdmin`, you can optionally provide a `company_guid` to create a key for a specific company. If `company_guid` is not provided, the key is created for the `SystemAdmin`'s own company (if applicable, or this might be disallowed depending on system setup for admins without a direct company affiliation).

The raw API key value is returned **only once** in the response to this endpoint. You must store it securely at this point.

**Request Body (`ApiKeyCreate` schema):**

```json
{
  "description": "Optional: Integration key for ERP system",
  "scopes": "Optional: sync:read,sync:write",
  "key": "Optional: rfk_customKey123abc",
  "company_guid": "Optional: target-company-guid-for-systemadmin"
}
```

-   **`description`** (string, optional): A human-readable description for the key.
-   **`scopes`** (string, optional): A comma-separated list of permission scopes. Valid scopes are `sync:read` and `sync:write`.
-   **`key`** (string, optional): A user-defined API key. 
    -   If provided, it *must* start with `rfk_` and be at least 8 characters long.
    -   It also *must* be unique across the system. If a duplicate is provided, a `400 Bad Request` error will occur.
    -   If not provided, a secure, random key will be generated automatically.
-   **`company_guid`** (UUID, optional): The GUID of the company for which to create the key. This field is only considered if the authenticated user is a `SystemAdmin`.

**Response (Success: 201 Created, `ApiKeyCreated` schema):**

```json
{
  "guid": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "key": "rfk_xYz1aBcDeFgHiJkLmNoPqRsTuVwXyZ01",
  "description": "Integration key for ERP system",
  "scopes": "sync:read,sync:write",
  "created_at": "2023-10-27T10:30:00Z",
  "company_guid": "z9y8x7w6-v5u4-t3s2-r1q0-p9o8n7m6l5k4"
}
```

-   **`guid`** (UUID): The unique identifier for the API key object.
-   **`key`** (string): The generated or provided API key. **This is the only time the raw key is shown.**
-   **`description`** (string, optional): The description provided.
-   **`scopes`** (string, optional): The scopes assigned.
-   **`created_at`** (datetime): Timestamp of creation.
-   **`company_guid`** (UUID): The company GUID the key is associated with.

**Possible Errors:**

-   `400 Bad Request`: If a user-provided `key` already exists.
-   `401 Unauthorized`: If authentication fails (e.g., invalid token or user not found).
-   `403 Forbidden`: If the authenticated user does not have `CompanyAdmin` or `SystemAdmin` role.
-   `404 Not Found`: If `company_guid` is provided by a `SystemAdmin` but the company does not exist.
-   `422 Unprocessable Entity`:
    -   If `scopes` contains invalid scope values.
    -   If a user-provided `key` does not start with `rfk_` or is too short.
    -   Other validation errors for request body fields.
-   `500 Internal Server Error`: If an unexpected error occurs during key creation. 