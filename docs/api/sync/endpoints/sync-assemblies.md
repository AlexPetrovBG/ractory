---
title: Sync Assemblies
description: Details about the endpoint for bulk inserting or updating assemblies.
---

# Sync Assemblies

Bulk inserts or updates assembly data. This endpoint is typically used for synchronizing assembly information from an external system like RaConnect, linking them to existing projects and components.

## Endpoint

`POST /api/v1/sync/assemblies`

## Authorization

Requires an API key with the `sync:write` scope or one of the following user roles: `SystemAdmin`, `CompanyAdmin`, `Integration`.

## Request Body

The request body must be a JSON object containing a single key `assemblies`, which is an array of assembly objects to be created or updated.

**`AssemblyBulkInsert` Schema:**

```json
{
  "assemblies": [
    // Array of AssemblyCreate objects
  ]
}
```

**`AssemblyCreate` Schema (for each object in the `assemblies` array):**

```json
{
  "guid": "uuid", // Optional. If provided and exists, it will be updated. Otherwise, new assembly created.
  "project_guid": "uuid", // Required. GUID of the parent project.
  "component_guid": "uuid", // Required. GUID of the parent component.
  "company_guid": "uuid", // Required. Must match the company of the authenticated user/API key.
  "trolley_cell": "string", // Optional.
  "trolley": "string", // Optional.
  "cell_number": "integer", // Optional.
  "picture": "bytes", // Optional. Binary data for assembly picture.
  "is_active": "boolean", // Optional. Defaults to true.
  "deleted_at": "datetime" // Optional. Timestamp of soft deletion.
}
```

**Example Request:**

```json
{
  "assemblies": [
    {
      "guid": "323e4567-e89b-12d3-a456-426614174003",
      "project_guid": "123e4567-e89b-12d3-a456-426614174000",
      "component_guid": "223e4567-e89b-12d3-a456-426614174002",
      "company_guid": "abcdef12-3456-7890-abcd-ef1234567890",
      "trolley": "T01",
      "cell_number": 1
    },
    {
      "project_guid": "123e4567-e89b-12d3-a456-426614174000",
      "component_guid": "223e4567-e89b-12d3-a456-426614174002",
      "company_guid": "abcdef12-3456-7890-abcd-ef1234567890",
      "trolley_cell": "A2"
    }
  ]
}
```

## Responses

### Success: `200 OK`

Returns a `SyncResult` object indicating the number of assemblies inserted and updated.

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
*   **`403 Forbidden`**: Authorization failure (scope, role, or company/parent entity mismatch).
*   **`422 Unprocessable Entity`**: Validation error (e.g., missing `project_guid`, `component_guid`, `company_guid`; parent entities not found or in wrong company).

## Important Notes

*   **Parent Entities:** `project_guid` and `component_guid` must reference existing entities within the same `company_guid`.
*   **Upsert Logic:** Based on `guid` and `company_guid`.
*   **Tenant Validation:** `company_guid` for each assembly is validated. 