---
title: Sync Pieces
description: Details about the endpoint for bulk inserting or updating pieces.
---

# Sync Pieces

Bulk inserts or updates piece data (e.g., profiles, cuts). This endpoint is typically used for synchronizing detailed piece information from an external system like RaConnect.

**Batch Limit:** A maximum of 1000 pieces can be processed per request.

## Endpoint

`POST /api/v1/sync/pieces`

## Authorization

Requires an API key with the `sync:write` scope or one of the following user roles: `SystemAdmin`, `CompanyAdmin`, `Integration`.

## Request Body

The request body must be a JSON object containing a single key `pieces`, which is an array of piece objects to be created or updated.

**`PieceBulkInsert` Schema:**

```json
{
  "pieces": [
    // Array of PieceCreate objects (max 1000)
  ]
}
```

**`PieceCreate` Schema (for each object in the `pieces` array):**

This schema is extensive. Key required fields include:

*   `piece_id`: "string" (Unique identifier for the piece)
*   `project_guid`: "uuid"
*   `component_guid`: "uuid"
*   `company_guid`: "uuid"

Optional fields include `guid` (for updates), `assembly_guid`, `barcode`, `outer_length`, `angle_left`, `angle_right`, and numerous other manufacturing-specific attributes (e.g., `profile_code`, `orientation`, `trolley_cell`, etc.).

Refer to `src/ractory/backend/app/schemas/sync/pieces.py` for the complete `PieceCreate` schema definition.

**Example Request (Simplified):**

```json
{
  "pieces": [
    {
      "guid": "423e4567-e89b-12d3-a456-426614174004", // For update
      "piece_id": "PCE-001-001",
      "project_guid": "123e4567-e89b-12d3-a456-426614174000",
      "component_guid": "223e4567-e89b-12d3-a456-426614174002",
      "assembly_guid": "323e4567-e89b-12d3-a456-426614174003",
      "company_guid": "abcdef12-3456-7890-abcd-ef1234567890",
      "barcode": "BARCODE001",
      "outer_length": 1200,
      "profile_code": "XPS-01"
    },
    {
      "piece_id": "PCE-001-002", // For new insert
      "project_guid": "123e4567-e89b-12d3-a456-426614174000",
      "component_guid": "223e4567-e89b-12d3-a456-426614174002",
      "company_guid": "abcdef12-3456-7890-abcd-ef1234567890",
      "barcode": "BARCODE002",
      "outer_length": 1250,
      "profile_code": "XPS-01"
    }
    // ... up to 1000 pieces
  ]
}
```

## Responses

### Success: `200 OK`

Returns a `SyncResult` object indicating the number of pieces inserted and updated.

**`SyncResult` Schema:**

```json
{
  "inserted": "integer",
  "updated": "integer"
}
```

### Error Responses

*   **`400 Bad Request`**: Malformed request, or if `len(data.pieces) > 1000`.
*   **`401 Unauthorized`**: Authentication failure.
*   **`403 Forbidden`**: Authorization failure.
*   **`422 Unprocessable Entity`**: Validation error (e.g., missing required fields; parent entities not found or in wrong company).

## Important Notes

*   **Parent Entities:** `project_guid`, `component_guid`, and optional `assembly_guid` must reference existing entities within the same `company_guid`.
*   **Upsert Logic:** Based on `guid` (if provided) and `company_guid`.
*   **Tenant Validation:** `company_guid` for each piece is validated. 