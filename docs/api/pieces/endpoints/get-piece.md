---
title: Get Piece
description: Details about the endpoint for retrieving a specific piece.
---

# Get Piece

Retrieves detailed information for a specific piece by its GUID.

## Endpoint

`GET /api/v1/pieces/{piece_guid}`

## Path Parameters

| Parameter    | Type | Description                |
|--------------|------|----------------------------|
| `piece_guid` | UUID | The GUID of the piece.     |

## Query Parameters

| Parameter        | Type    | Optional | Default | Description                                          |
|------------------|---------|----------|---------|------------------------------------------------------|
| `include_inactive`| boolean | Yes      | `false` | If `true`, allows fetching a soft-deleted piece.   |

## Responses

### Success: `200 OK`

Returns a `PieceDetail` object.

**`PieceDetail` Schema:**

This schema includes all fields from `PieceResponse` plus additional details specific to a piece. Refer to `src/ractory/backend/app/schemas/sync/pieces.py` for the full list of fields, as it's extensive. Key fields include:

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
  // ... numerous other fields like orientation, trolley, cell, profile_code etc. ...
  "company_guid": "uuid",
  "created_at": "datetime",
  "updated_at": "datetime", // Optional
  "is_active": "boolean",
  "deleted_at": "datetime" // Optional, null if active
}
```

**Example Response:**

```json
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
  "orientation": "Horizontal",
  "profile_code": "PF001",
  // ... other fields ...
  "company_guid": "d1b2c3d4-e5f6-7890-1234-567890abcdef",
  "created_at": "2023-10-26T10:00:00Z",
  "updated_at": "2023-10-26T11:00:00Z",
  "is_active": true,
  "deleted_at": null
}
```

### Error: `403 Forbidden`

- If the user (not a `SystemAdmin`) attempts to access a piece belonging to a different company.

```json
{
  "detail": "Access to this piece is forbidden."
}
```

### Error: `404 Not Found`

- If the piece with the specified `piece_guid` does not exist.
- If the piece is soft-deleted and `include_inactive` is `false` (or not provided).

```json
{
  "detail": "Piece not found"
}
```

### Error: `500 Internal Server Error`

- If the retrieved piece data is missing required fields (indicates a data integrity issue).

```json
{
  "detail": "Piece missing required fields: ['field_name']"
}
```

## Tenant Isolation

- Access is restricted to pieces belonging to the user's tenant unless the user is a `SystemAdmin`.
- The `add_tenant_filter` is used as a defense-in-depth measure during retrieval. 