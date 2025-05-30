---
title: Sync Components
description: Details about the endpoint for bulk inserting or updating components.
---

# Sync Components

Bulk inserts or updates component data. This endpoint is typically used for synchronizing component information from an external system like RaConnect, linking them to existing projects.

## Endpoint

`POST /api/v1/sync/components`

## Authorization

Requires an API key with the `sync:write` scope or one of the following user roles: `SystemAdmin`, `CompanyAdmin`, `Integration`.

## Request Body

The request body must be a JSON object containing a single key `components`, which is an array of component objects to be created or updated.

**`ComponentBulkInsert` Schema:**

```json
{
  "components": [
    // Array of ComponentCreate objects
  ]
}
```

**`ComponentCreate` Schema (for each object in the `components` array):**

```json
{
  "guid": "uuid", // Optional. If provided and exists for the company, it will be updated. Otherwise, new component created.
  "code": "string", // Required. Component code.
  "designation": "string", // Optional.
  "project_guid": "uuid", // Required. GUID of the parent project. Project must exist and belong to the same company.
  "company_guid": "uuid", // Required. Must match the company of the authenticated user/API key.
  "quantity": "integer", // Optional. Defaults to 1.
  "picture": "bytes", // Optional. Binary data for component picture.
  "is_active": "boolean", // Optional. Defaults to true.
  "deleted_at": "datetime" // Optional. Timestamp of soft deletion.
}
```

**Example Request:**

```json
{
  "components": [
    {
      "guid": "223e4567-e89b-12d3-a456-426614174002",
      "code": "COMP-001A",
      "designation": "Main Frame Assembly",
      "project_guid": "123e4567-e89b-12d3-a456-426614174000",
      "company_guid": "abcdef12-3456-7890-abcd-ef1234567890",
      "quantity": 2
    },
    {
      "code": "COMP-001B",
      "designation": "Side Panel",
      "project_guid": "123e4567-e89b-12d3-a456-426614174000",
      "company_guid": "abcdef12-3456-7890-abcd-ef1234567890",
      "quantity": 4
    }
  ]
}
```

## Responses

### Success: `200 OK`

Returns a `SyncResult` object indicating the number of components inserted and updated.

**`SyncResult` Schema:**

```json
{
  "inserted": "integer",
  "updated": "integer"
}
```

### Error Responses

*   **`400 Bad Request`**: Malformed request.
*   **`401 Unauthorized`**: Authentication failure.
*   **`403 Forbidden`**: Authorization failure (scope, role, or company mismatch).
*   **`422 Unprocessable Entity`**: Validation error (e.g., missing `code`, `project_guid`, `company_guid`; `project_guid` not found or in wrong company).

## Important Notes

*   **Parent Project:** The `project_guid` must reference an existing project within the same `company_guid`.
*   **Upsert Logic:** Based on `guid` and `company_guid`.
*   **Tenant Validation:** `company_guid` for each component is validated. 