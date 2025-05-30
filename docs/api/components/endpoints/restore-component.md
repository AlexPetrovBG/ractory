---
title: Restore Component
description: Details about the endpoint for restoring a soft-deleted component.
---

# Restore Component

Restores a soft-deleted component by its GUID. Cascades to child entities.

## Endpoint

`POST /api/v1/components/{component_guid}/restore`

## Path Parameters

| Parameter      | Type | Description                               |
|----------------|------|-------------------------------------------|
| `component_guid`| UUID | The GUID of the component to restore.     |

## Responses

### Success: `204 No Content`

Indicates successful restoration.

### Error Responses

*   **`404 Not Found`**: Component not found or forbidden, or already active.

## Tenant Isolation

Standard tenant isolation applies.

## Cascading Behavior

Uses `SyncService.cascade_restore('component', ...)`. 