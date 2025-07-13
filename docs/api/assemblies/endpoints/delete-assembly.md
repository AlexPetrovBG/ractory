---
title: Soft-delete Assembly
description: Details about the endpoint for soft-deleting an assembly.
---

# Soft-delete Assembly

Soft-deletes a specific assembly by its GUID. This marks the assembly as inactive and sets `deleted_at`. It also cascades the soft delete to child entities (e.g., pieces).

## Endpoint

`DELETE /api/v1/assemblies/{assembly_guid}`

## Path Parameters

| Parameter      | Type | Description                             |
|----------------|------|-----------------------------------------|
| `assembly_guid`| UUID | The GUID of the assembly to soft-delete.|

## Responses

### Success: `204 No Content`

Indicates successful soft deletion.

### Error Responses

*   **`404 Not Found`**: Assembly not found or not accessible (forbidden).

## Tenant Isolation

Standard tenant isolation applies.

## Cascading Behavior

Uses `SyncService.cascade_soft_delete('assembly', ...)` to manage cascading to children. 