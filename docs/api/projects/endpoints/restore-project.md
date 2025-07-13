---
title: Restore Project
description: Details about the endpoint for restoring a soft-deleted project.
---

# Restore Project

Restores a soft-deleted project by its GUID. Cascades to child entities.

## Endpoint

`POST /api/v1/projects/{project_guid}/restore`

## Path Parameters

| Parameter      | Type | Description                             |
|----------------|------|-----------------------------------------|
| `project_guid` | UUID | The GUID of the project to restore.     |

## Responses

### Success: `204 No Content`

Indicates successful restoration.

### Error Responses

*   **`404 Not Found`**: Project not found or forbidden, or already active.

## Tenant Isolation

Standard tenant isolation applies.

## Cascading Behavior

Uses `SyncService.cascade_restore('project', ...)`. 