---
title: Restore Component
slug: restore_component
---

This endpoint restores a soft-deleted component by its GUID.

## Endpoint

`POST /components/{component_guid}/restore`

## Access Control

- Access is tenant-based. Users can generally only restore components associated with their tenant (company).
- System Administrators can restore components across tenants.
- Tenant filtering is applied via `add_tenant_filter` to ensure the user has access to the component before restoration.

## Path Parameters

- `component_guid` (UUID, required): The unique identifier (GUID) of the component to restore.

## Request Body

No request body is required for this endpoint.

## Responses

### Success: 204 No Content

Indicates that the component was successfully restored. No content is returned in the response body.

### Error Responses:

- **404 Not Found**:
    - If the component with the specified `component_guid` does not exist, is not soft-deleted, or the user does not have access to it (due to tenant restrictions).
    ```json
    {
      "detail": "Component not found or forbidden"
    }
    ```

- **500 Internal Server Error**:
    - If an unexpected error occurs during the restoration process (e.g., issues with cascading the restore).

## Notes

- This operation restores a soft-deleted component:
    - The component's `is_active` field is set to `true`.
    - The component's `deleted_at` field is set to `NULL`.
- The `SyncService.cascade_restore` method is called. This service is responsible for restoring child entities (e.g., assemblies, pieces) that were soft-deleted at the same time as the parent component. It typically restores children whose `deleted_at` timestamp matches the parent component's `deleted_at` timestamp before restoration. 