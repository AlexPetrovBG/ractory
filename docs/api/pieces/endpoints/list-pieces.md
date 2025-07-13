---
title: List Pieces
description: Details about the endpoint for listing pieces.
---

# List Pieces

Retrieves a list of pieces, with optional filtering and pagination. By default, only active (not soft-deleted) pieces are returned.

## Endpoint

`GET /api/v1/pieces`

## Query Parameters

| Parameter        | Type      | Optional | Default | Description                                                                 |
|------------------|-----------|----------|---------|-----------------------------------------------------------------------------|
| `project_guid`   | UUID      | Yes      |         | Filter pieces by the GUID of the project they belong to.                      |
| `component_guid` | UUID      | Yes      |         | Filter pieces by the GUID of the component they belong to.                  |
| `assembly_guid`  | UUID      | Yes      |         | Filter pieces by the GUID of the assembly they belong to.                   |
| `company_guid`   | UUID      | Yes      |         | Filter pieces by company GUID. (Primarily for `SystemAdmin` role)             |
| `include_inactive`| boolean  | Yes      | `false` | If `true`, includes soft-deleted pieces in the results.                     |
| `limit`          | integer   | Yes      | `100`   | Maximum number of pieces to return. (Min: 1, Max: 1000)                     |
| `offset`         | integer   | Yes      | `0`     | Number of pieces to skip before starting to collect the result set.         |

## Responses

### Success: `200 OK`

Returns a JSON array of `PieceResponse` objects.

**`PieceResponse` Schema:**

```json
{
  "guid": "uuid",
  "piece_id": "string",
  "project_guid": "uuid",
  "component_guid": "uuid",
  "assembly_guid": "uuid", // Optional
  "barcode": "string", // Optional
  "outer_length": "integer", // Optional
  "angle_left": "integer", // Optional
  "angle_right": "integer", // Optional
  "is_active": "boolean",
  "deleted_at": "datetime", // Optional, null if active
  "company_guid": "uuid",
  "created_at": "datetime"
}
```

**Example Response:**

```json
[
  {
    "guid": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "piece_id": "PCE-001",
    "project_guid": "p1b2c3d4-e5f6-7890-1234-567890abcdef",
    "component_guid": "c1b2c3d4-e5f6-7890-1234-567890abcdef",
    "assembly_guid": "s1b2c3d4-e5f6-7890-1234-567890abcdef",
    "barcode": "1234567890123",
    "outer_length": 1500,
    "angle_left": 90,
    "angle_right": 90,
    "is_active": true,
    "deleted_at": null,
    "company_guid": "d1b2c3d4-e5f6-7890-1234-567890abcdef",
    "created_at": "2023-10-26T10:00:00Z"
  },
  // ... more pieces
]
```

### Error: `400 Bad Request`

- If `component_guid` is provided but does not belong to the specified `project_guid`.
- If `assembly_guid` is provided but does not belong to the specified `component_guid` or `project_guid`.

```json
{
  "detail": "Component {component_guid} does not belong to project {project_guid}."
}
```

### Error: `403 Forbidden`

- If a non-`SystemAdmin` user tries to use `company_guid` to access data outside their tenant (this is usually caught by `validate_company_access` before the main query).

```json
{
  "detail": "User does not have access to the specified company."
}
```

### Error: `404 Not Found`

- If `project_guid`, `component_guid`, or `assembly_guid` is provided but the corresponding entity is not found or not accessible to the user.

```json
{
  "detail": "Project with GUID {project_guid} not found or not accessible."
}
```

## Tenant Isolation

- For regular users, results are automatically filtered to their tenant.
- `SystemAdmin` users can query across tenants if `company_guid` is provided; otherwise, it defaults to their primary tenant context if applicable or might require `company_guid`.
- Access to parent entities (Project, Component, Assembly) is also validated against the user's tenant and role. 