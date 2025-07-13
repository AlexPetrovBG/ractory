---
title: Soft-delete Project
description: Details about the endpoint for soft-deleting a project.
---

# Soft-delete Project

Soft-deletes a specific project by its GUID. Cascades to child entities.

## Endpoint

`DELETE /api/v1/projects/{project_guid}`

## Path Parameters

| Parameter      | Type | Description                             |
|----------------|------|-----------------------------------------|
| `project_guid` | UUID | The GUID of the project to soft-delete. |

## Responses

### Success: `204 No Content`

Indicates successful soft deletion.

### Error Responses

*   **`404 Not Found`**: Project not found or forbidden.

## Tenant Isolation

Standard tenant isolation applies.

## Cascading Behavior

Uses `SyncService.cascade_soft_delete('project', ...)`. 