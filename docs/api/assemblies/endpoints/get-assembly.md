---
title: Get Assembly
description: Details about the endpoint for retrieving a specific assembly.
---

# Get Assembly

Retrieves detailed information for a specific assembly by its GUID.

## Endpoint

`GET /api/v1/assemblies/{assembly_guid}`

## Path Parameters

| Parameter      | Type | Description                  |
|----------------|------|------------------------------|
| `assembly_guid`| UUID | The GUID of the assembly.    |

## Query Parameters

| Parameter        | Type    | Optional | Default | Description                                            |
|------------------|---------|----------|---------|--------------------------------------------------------|
| `include_inactive`| boolean | Yes      | `false` | If `true`, allows fetching a soft-deleted assembly.    |

## Responses

### Success: `200 OK`

Returns an `AssemblyDetail` object.

**`AssemblyDetail` Schema (Key Fields):**

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
  "updated_at": "datetime", // Optional
  "is_active": "boolean",
  "deleted_at": "datetime", // Optional
  "piece_count": "integer" // Count of associated pieces
}
```
(Refer to `src/ractory/backend/app/schemas/sync/assemblies.py` for full schema)

**Example Response:**

```json
{
  "guid": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "project_guid": "p1a2b3c4-d5e6-f789-0123-456789abcdef",
  "component_guid": "c1d2e3f4-g5h6-i7j8-k9l0-m1n2o3p4q5r6",
  "trolley_cell": "A1",
  "company_guid": "tenant-company-guid-123",
  "created_at": "2023-10-26T10:00:00Z",
  "is_active": true,
  "deleted_at": null,
  "piece_count": 0
}
```

### Error Responses

*   **`403 Forbidden`**: Access to assembly is forbidden (e.g., wrong tenant).
*   **`404 Not Found`**: Assembly not found or not accessible (respects `include_inactive`).
*   **`500 Internal Server Error`**: If assembly data is missing required fields.

## Tenant Isolation

Standard tenant isolation applies. 