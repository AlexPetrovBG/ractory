---
title: Sync Projects
description: Details about the endpoint for bulk inserting or updating projects.
---

# Sync Projects

Bulk inserts or updates project data. This endpoint is typically used for synchronizing project information from an external system like RaConnect.

## Endpoint

`POST /api/v1/sync/projects`

## Authorization

Requires an API key with the `sync:write` scope or one of the following user roles: `SystemAdmin`, `CompanyAdmin`, `Integration`.

## Request Body

The request body must be a JSON object containing a single key `projects`, which is an array of project objects to be created or updated.

**`ProjectBulkInsert` Schema:**

```json
{
  "projects": [
    // Array of ProjectCreate objects
  ]
}
```

**`ProjectCreate` Schema (for each object in the `projects` array):**

```json
{
  "guid": "uuid", // Optional. If provided and exists for the company, it will be updated. Otherwise, a new project is created (with this guid or an auto-generated one).
  "code": "string", // Required. Project code.
  "company_guid": "uuid", // Required. Must match the company of the authenticated user/API key, unless user is SystemAdmin.
  "due_date": "datetime", // Optional. Example: "2024-12-31T23:59:59Z"
  "in_production": "boolean", // Optional. Defaults to false.
  "company_name": "string", // Optional.
  "is_active": "boolean", // Optional. Defaults to true. Used for soft deletion tracking.
  "deleted_at": "datetime", // Optional. Timestamp of soft deletion.
  "updated_at": "datetime" // Optional. Timestamp of last update.
}
```

**Example Request:**

```json
{
  "projects": [
    {
      "guid": "123e4567-e89b-12d3-a456-426614174000",
      "code": "P2024-001",
      "company_guid": "abcdef12-3456-7890-abcd-ef1234567890",
      "due_date": "2024-12-31T00:00:00Z",
      "in_production": false,
      "company_name": "Client Alpha"
    },
    {
      "code": "P2024-002",
      "company_guid": "abcdef12-3456-7890-abcd-ef1234567890",
      "company_name": "Client Beta",
      "in_production": true
    }
  ]
}
```

## Responses

### Success: `200 OK`

Returns a `SyncResult` object indicating the number of projects inserted and updated.

**`SyncResult` Schema:**

```json
{
  "inserted": "integer", // Number of new projects created
  "updated": "integer"  // Number of existing projects updated
}
```

**Example Response:**

```json
{
  "inserted": 1,
  "updated": 1
}
```

### Error Responses

*   **`400 Bad Request`**: If the request payload is malformed.
*   **`401 Unauthorized`**: If authentication fails (e.g., invalid token or API key).
*   **`403 Forbidden`**: If the authenticated user/API key does not have the `sync:write` scope or required role, or if a `company_guid` in the payload does not match the user's company (and user is not `SystemAdmin`).
*   **`422 Unprocessable Entity`**: If the request payload fails validation (e.g., missing required fields like `code` or `company_guid`, incorrect data types).

## Important Notes

*   **Upsert Logic:** The `SyncService` determines whether to insert or update based on the provided `guid` and `company_guid`.
*   **Tenant Validation:** `company_guid` for each project in the list is validated against the authenticated entity's tenant. 