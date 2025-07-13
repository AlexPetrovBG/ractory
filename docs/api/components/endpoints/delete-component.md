---
title: Soft-delete Component
description: Details about the endpoint for soft-deleting a component.
---

# Soft-delete Component

Soft-deletes a specific component by its GUID. Cascades to child entities.

## Endpoint

`DELETE /api/v1/components/{component_guid}`

## Path Parameters

| Parameter      | Type | Description                               |
|----------------|------|-------------------------------------------|
| `component_guid`| UUID | The GUID of the component to soft-delete. |

## Responses

### Success: `204 No Content`

Indicates successful soft deletion.

### Error Responses

*   **`404 Not Found`**: Component not found or forbidden.

## Tenant Isolation

Standard tenant isolation applies.

## Cascading Behavior

Uses `SyncService.cascade_soft_delete('component', ...)`. 