---
title: List Components
slug: list_components
---

This endpoint allows users to retrieve a list of components, with optional filtering.

## Endpoint

`GET /components`

## Access Control

- Access is tenant-based. Users can generally only list components associated with their tenant (company).
- System Administrators may have broader access if `company_guid` is specified and validated.
- Tenant filtering is applied via `add_tenant_filter` using `current_user.tenant` or a validated `company_guid` for System Admins.

## Query Parameters

- `project_guid` (UUID, optional): If provided, filters components belonging to the specified project. The project must be accessible to the user.
- `company_guid` (UUID, optional): If provided by a System Administrator, filters components belonging to the specified company. For other users, this parameter might be ignored or validated against their own tenant.
- `include_inactive` (boolean, optional, default: `false`): If `true`, includes components that have been soft-deleted (i.e., `is_active` is `false`). By default, only active components are returned.

## Responses

### Success: 200 OK

Returns a JSON array of component objects, each conforming to the `ComponentResponse` schema.

```json
[
  {
    "guid": "uuid",
    "code": "string",
    "designation": "string | null",
    "project_guid": "uuid",
    "quantity": "integer",
    "company_guid": "uuid",
    "is_active": "boolean",
    "deleted_at": "datetime_string | null",
    "created_at": "datetime_string"
    // Other fields from ComponentResponse schema as defined
  }
  // ... more component objects
]
```

If no components match the criteria, an empty array `[]` is returned.

### Error Responses:

- **404 Not Found**:
    - If `project_guid` is provided but the project is not found or not accessible to the user.
    ```json
    {
      "detail": "Project with GUID {project_guid} not found or not accessible."
    }
    ```
- **403 Forbidden** (Implicit):
    - If `company_guid` is provided and access validation fails (e.g., a non-System Admin tries to access another company's components).
- **500 Internal Server Error**:
    - If an unexpected error occurs on the server.

## Notes

- The endpoint uses `add_tenant_filter` for ensuring data isolation.
- If `project_guid` is used, the accessibility of the project itself is first verified.
- Soft-deleted components have `is_active: false` and `deleted_at` set to a timestamp. 