---
title: List Projects
description: Details about the endpoint for listing projects.
---

# List Projects

Retrieves a list of projects, with optional filtering. By default, only active projects are returned.

## Endpoint

`GET /api/v1/projects`

## Query Parameters

| Parameter        | Type      | Optional | Default | Description                                                                  |
|------------------|-----------|----------|---------|------------------------------------------------------------------------------|
| `company_guid`   | UUID      | Yes      |         | Filter projects by company GUID. (Primarily for `SystemAdmin` role)            |
| `code`           | string    | Yes      |         | Filter projects by exact project code.                                       |
| `search`         | string    | Yes      |         | Search projects by a case-insensitive partial match on the project code.     |
| `include_inactive`| boolean  | Yes      | `false` | If `true`, includes soft-deleted projects in the results.                    |

## Responses

### Success: `200 OK`

Returns a JSON array of `ProjectResponse` objects.

**`ProjectResponse` Schema (Key Fields):**

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
  "deleted_at": "datetime" // Optional
}
```
(Refer to `src/ractory/backend/app/schemas/sync/projects.py` for full schema)

### Error Responses

Standard error responses apply (401, 403, 404, 422).

## Tenant Isolation

Standard tenant isolation applies. `SystemAdmin` can use `company_guid` for cross-tenant queries. 