---
title: Get Project
description: Details about the endpoint for retrieving a specific project.
---

# Get Project

Retrieves detailed information for a specific project by its GUID.

## Endpoint

`GET /api/v1/projects/{project_guid}`

## Path Parameters

| Parameter    | Type | Description                |
|--------------|------|----------------------------|
| `project_guid`| UUID | The GUID of the project.   |

## Query Parameters

| Parameter        | Type    | Optional | Default | Description                                          |
|------------------|---------|----------|---------|------------------------------------------------------|
| `include_inactive`| boolean | Yes      | `false` | If `true`, allows fetching a soft-deleted project.   |

## Responses

### Success: `200 OK`

Returns a `ProjectDetail` object.

**`ProjectDetail` Schema (Key Fields):**

```json
{
  "guid": "uuid",
  "code": "string",
  "company_guid": "uuid",
  "due_date": "datetime", // Optional
  "in_production": "boolean",
  "company_name": "string", // Optional
  "created_at": "datetime",
  "updated_at": "datetime", // Optional
  "is_active": "boolean",
  "deleted_at": "datetime", // Optional
  "component_count": "integer",
  "piece_count": "integer"
}
```
(Refer to `src/ractory/backend/app/schemas/sync/projects.py` for full schema)

### Error Responses

*   **`403 Forbidden`**: Access to project is forbidden.
*   **`404 Not Found`**: Project not found or not accessible.

## Tenant Isolation

Standard tenant isolation applies. 