---
title: Soft Delete Assembly
slug: /assemblies-api/soft-delete-assembly
---

## `DELETE /api/v1/assemblies/{assembly_guid}`

Soft deletes an assembly by its GUID. This operation marks the assembly as inactive (`is_active: false`) and records the deletion timestamp (`deleted_at`).

This action also triggers a cascade soft delete for all active child entities (e.g., pieces, articles) associated with this assembly.

### Request

**Method:** `DELETE`

**Path:** `/api/v1/assemblies/{assembly_guid}`

**Headers:**

*   `X-API-Key`: Your API Key (string, required)

**Path Parameters:**

*   `assembly_guid` (UUID, required): The unique identifier of the assembly to soft delete.

### Response

**Status Code: 204 No Content**

*   Indicates successful soft deletion of the assembly and its active children.

**Status Code: 403 Forbidden**

*   If the user attempts to soft delete an assembly belonging to a different tenant (and is not a System Admin with appropriate cross-tenant privileges if such a feature were explicitly supported for deletion, which it currently isn't for this direct delete endpoint).

    ```json
    {
      "detail": "Assembly not found or forbidden"
      // Note: The error message might be generic "not found" if tenant check happens before existence check.
    }
    ```

**Status Code: 404 Not Found**

*   If no active assembly with the specified `assembly_guid` is found within the user's tenant.

    ```json
    {
      "detail": "Assembly not found or forbidden"
    }
    ```

### Authorization

*   **Users with appropriate permissions (e.g., Admin, Editor roles):** Can soft delete assemblies within their own tenant.
*   **System Admins:** Can soft delete assemblies within their own tenant (or potentially any tenant, though the current router code focuses tenant filtering on `current_user.tenant`).

### Important Notes

*   **Cascading Soft Delete:** Soft deleting an assembly will also soft delete its dependent active children (pieces, articles) via the `SyncService.cascade_soft_delete` mechanism. This ensures data integrity and consistency.
*   **Idempotency:** Attempting to soft delete an already soft-deleted or non-existent assembly will likely result in a 404 Not Found error, as the initial query targets active assemblies within the tenant.
*   This operation does not permanently remove data from the database. The assembly can be restored using the [Restore Assembly](./restore-assembly.md) endpoint. 