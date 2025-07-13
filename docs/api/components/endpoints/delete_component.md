---
title: Soft-delete Component
slug: delete_component
---

This endpoint soft-deletes a specific component by its GUID.

## Endpoint

`DELETE /components/{component_guid}`

## Access Control

- Access is tenant-based. Users can generally only soft-delete components associated with their tenant (company).
- System Administrators can soft-delete components across tenants.
- Tenant filtering is applied via `add_tenant_filter` to ensure the user has access to the component before deletion.

## Path Parameters

- `component_guid` (UUID, required): The unique identifier (GUID) of the component to soft-delete.

## Request Body

No request body is required for this endpoint.

## Responses

### Success: 204 No Content

Indicates that the component was successfully soft-deleted. No content is returned in the response body.

### Error Responses:

- **404 Not Found**:
    - If the component with the specified `component_guid` does not exist or the user does not have access to it (due to tenant restrictions).
    ```json
    {
      "detail": "Component not found or forbidden"
    }
    ```

- **500 Internal Server Error**:
    - If an unexpected error occurs during the soft-delete process (e.g., issues with cascading the soft delete).

## Notes

- This operation performs a "soft delete":
    - The component's `is_active` field is set to `false`.
    - The component's `deleted_at` field is set to the current timestamp.
- The `SyncService.cascade_soft_delete` method is called, indicating that this operation will also soft-delete associated child entities (e.g., assemblies, pieces, articles) that are currently active.
- The actual database record for the component is not removed. 