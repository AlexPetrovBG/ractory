---
title: Soft-delete Piece
description: Details about the endpoint for soft-deleting a piece.
---

# Soft-delete Piece

Soft-deletes a specific piece by its GUID. This operation marks the piece as inactive and sets its `deleted_at` timestamp. The actual data is not removed from the database.

This operation will cascade and soft-delete any active children entities if applicable (though pieces are usually the most granular level).

## Endpoint

`DELETE /api/v1/pieces/{piece_guid}`

## Path Parameters

| Parameter    | Type | Description                       |
|--------------|------|-----------------------------------|
| `piece_guid` | UUID | The GUID of the piece to soft-delete. |

## Responses

### Success: `204 No Content`

Indicates that the piece was successfully soft-deleted. The response body is empty.

### Error: `404 Not Found`

- If the piece with the specified `piece_guid` does not exist or is not accessible to the user (e.g., belongs to another tenant and the user is not a `SystemAdmin`).

```json
{
  "detail": "Piece not found or forbidden"
}
```

## Tenant Isolation

- Users can only soft-delete pieces belonging to their own tenant.
- `SystemAdmin` users can soft-delete pieces belonging to any tenant, provided they can access the piece initially based on the `piece_guid` and their permissions.
- The `add_tenant_filter` is used to ensure the piece belongs to the current user's tenant before attempting deletion (unless the user is a `SystemAdmin`).

## Cascading Behavior

The `SyncService.cascade_soft_delete('piece', piece_guid, session)` method is called, which handles the logic for cascading the soft delete to any dependent child entities. For pieces themselves, this might be less relevant as they are often leaf nodes, but the framework is in place. 