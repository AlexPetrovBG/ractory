---
title: Restore Assembly
description: Details about the endpoint for restoring a soft-deleted assembly.
---

# Restore Assembly

Restores a soft-deleted assembly by its GUID. This marks the assembly as active and clears `deleted_at`. It also cascades the restore to child entities.

## Endpoint

`POST /api/v1/assemblies/{assembly_guid}/restore`

## Path Parameters

| Parameter      | Type | Description                             |
|----------------|------|-----------------------------------------|
| `assembly_guid`| UUID | The GUID of the assembly to restore.    |

## Responses

### Success: `204 No Content`

Indicates successful restoration.

### Error Responses

*   **`404 Not Found`**: Assembly not found or not accessible (forbidden), or already active.

## Tenant Isolation

Standard tenant isolation applies.

## Cascading Behavior

Uses `SyncService.cascade_restore('assembly', ...)` to manage cascading to children. 