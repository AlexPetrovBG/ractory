---
title: Restore Piece
description: Details about the endpoint for restoring a soft-deleted piece.
---

# Restore Piece

Restores a soft-deleted piece by its GUID. This operation marks the piece as active (`is_active = true`) and sets its `deleted_at` timestamp to `NULL`.

This operation will cascade and restore children entities that were soft-deleted at the same time as the parent piece (if applicable).

## Endpoint

`POST /api/v1/pieces/{piece_guid}/restore`

## Path Parameters

| Parameter    | Type | Description                          |
|--------------|------|--------------------------------------|
| `piece_guid` | UUID | The GUID of the piece to restore.    |

## Responses

### Success: `204 No Content`

Indicates that the piece was successfully restored. The response body is empty.

### Error: `404 Not Found`

- If the piece with the specified `piece_guid` does not exist or is not accessible to the user (e.g., belongs to another tenant and the user is not a `SystemAdmin`).
- If the piece is not currently soft-deleted (i.e., it's already active).

```json
{
  "detail": "Piece not found or forbidden"
}
```

## Tenant Isolation

- Users can only restore pieces belonging to their own tenant.
- `SystemAdmin` users can restore pieces belonging to any tenant, provided they can access the piece initially.
- The `add_tenant_filter` ensures the piece belongs to the current user's tenant before attempting restoration (unless the user is a `SystemAdmin`).

## Cascading Behavior

The `SyncService.cascade_restore('piece', piece_guid, session)` method is called. This service handles the logic for:
1.  Restoring the specified piece.
2.  Cascading the restore operation to children entities that were soft-deleted *at the same time* as this piece. This prevents accidental restoration of children that were independently soft-deleted. 