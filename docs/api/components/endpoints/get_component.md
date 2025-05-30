---
title: Get Component
slug: get_component
---

This endpoint retrieves a specific component by its GUID.

## Endpoint

`GET /components/{component_guid}`

## Access Control

- Access is tenant-based. Users can generally only retrieve components associated with their tenant (company).
- System Administrators have access to components across tenants.
- The endpoint explicitly checks if `current_user.role != UserRole.SYSTEM_ADMIN and str(component.company_guid) != str(current_user.tenant)` and raises a 403 Forbidden error if access is denied.
- Tenant filtering is also applied via `add_tenant_filter` during the initial query.

## Path Parameters

- `component_guid` (UUID, required): The unique identifier (GUID) of the component to retrieve.

## Query Parameters

- `include_inactive` (boolean, optional, default: `false`): If `true`, allows retrieval of a component that has been soft-deleted (i.e., `is_active` is `false`). If `false` (default) and the component is inactive, it will result in a 404 Not Found.

## Responses

### Success: 200 OK

Returns a JSON object representing the component, conforming to the `ComponentDetail` schema.

```json
{
  "guid": "uuid",
  "code": "string",
  "designation": "string | null",
  "project_guid": "uuid",
  "quantity": "integer",
  "company_guid": "uuid",
  "is_active": "boolean",
  "deleted_at": "datetime_string | null",
  "created_at": "datetime_string",
  "updated_at": "datetime_string | null",
  "assembly_count": "integer", // Placeholder, actual calculation logic might be elsewhere
  "piece_count": "integer"    // Placeholder, actual calculation logic might be elsewhere
  // Other fields from ComponentDetail schema as defined
}
```

### Error Responses:

- **404 Not Found**:
    - If the component with the specified `component_guid` does not exist.
    - If `include_inactive` is `false` (or not provided) and the component is soft-deleted.
    ```json
    {
      "detail": "Component not found"
    }
    ```

- **403 Forbidden**:
    - If the user (not a System Admin) tries to access a component belonging to a different tenant.
    ```json
    {
      "detail": "Access to this component is forbidden."
    }
    ```

- **500 Internal Server Error**:
    - If the retrieved component data is missing required fields (e.g., due to data integrity issues).
    ```json
    {
      "detail": "Component missing required fields: ['field_name']"
    }
    ```
    - If an unexpected server error occurs.

## Notes

- The endpoint constructs the `ComponentDetail` response manually in the code, including placeholder values for `assembly_count` and `piece_count`. The actual calculation for these counts might be implemented elsewhere or intended for future development.
- A specific check is made for required fields in the component data before returning the response to prevent server errors due to incomplete data. 