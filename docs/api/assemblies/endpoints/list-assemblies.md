---
title: List Assemblies
description: Details about the endpoint for listing assemblies.
---

# List Assemblies

Retrieves a list of assemblies, with optional filtering. By default, only active (not soft-deleted) assemblies are returned.

## Endpoint

`GET /api/v1/assemblies`

## Query Parameters

| Parameter        | Type      | Optional | Default | Description                                                                  |
|------------------|-----------|----------|---------|------------------------------------------------------------------------------|
| `project_guid`   | UUID      | Yes      |         | Filter assemblies by the GUID of the project they belong to.                   |
| `component_guid` | UUID      | Yes      |         | Filter assemblies by the GUID of the component they belong to.               |
| `company_guid`   | UUID      | Yes      |         | Filter assemblies by company GUID. (Primarily for `SystemAdmin` role)          |
| `include_inactive`| boolean  | Yes      | `false` | If `true`, includes soft-deleted assemblies in the results.                  |

## Responses

### Success: `200 OK`

Returns a JSON array of `AssemblyResponse` objects.

**`AssemblyResponse` Schema (Key Fields):**

```json
{
  "guid": "uuid",
  "project_guid": "uuid",
  "component_guid": "uuid",
  "trolley_cell": "string", // Optional
  "trolley": "string", // Optional
  "cell_number": "integer", // Optional
  "company_guid": "uuid",
  "created_at": "datetime",
  "is_active": "boolean",
  "deleted_at": "datetime" // Optional, null if active
}
```
(Refer to `src/ractory/backend/app/schemas/sync/assemblies.py` for full schema)

**Example Response:**

```json
[
  {
    "guid": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "project_guid": "p1a2b3c4-d5e6-f789-0123-456789abcdef",
    "component_guid": "c1d2e3f4-g5h6-i7j8-k9l0-m1n2o3p4q5r6",
    "trolley_cell": "A1",
    "trolley": "T01",
    "cell_number": 1,
    "company_guid": "tenant-company-guid-123",
    "created_at": "2023-10-26T10:00:00Z",
    "is_active": true,
    "deleted_at": null
  }
]
```

### Error Responses

*   **`400 Bad Request`**: If `component_guid` is provided but does not belong to the specified `project_guid`.
*   **`403 Forbidden`**: If a non-`SystemAdmin` user tries to use `company_guid` for cross-tenant access.
*   **`404 Not Found`**: If `project_guid` or `component_guid` is not found or accessible.

## Tenant Isolation

Standard tenant isolation applies. `SystemAdmin` can use `company_guid` for cross-tenant queries. 