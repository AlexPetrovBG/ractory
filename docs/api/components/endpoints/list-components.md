---
title: List Components
description: Details about the endpoint for listing components.
---

# List Components

Retrieves a list of components, with optional filtering. By default, only active components are returned.

## Endpoint

`GET /api/v1/components`

## Query Parameters

| Parameter        | Type      | Optional | Default | Description                                                                  |
|------------------|-----------|----------|---------|------------------------------------------------------------------------------|
| `project_guid`   | UUID      | Yes      |         | Filter components by the GUID of the project they belong to.                 |
| `company_guid`   | UUID      | Yes      |         | Filter components by company GUID. (Primarily for `SystemAdmin` role)        |
| `include_inactive`| boolean  | Yes      | `false` | If `true`, includes soft-deleted components in the results.                  |

## Responses

### Success: `200 OK`

Returns a JSON array of `ComponentResponse` objects.

**`ComponentResponse` Schema (Key Fields):**

```json
{
  "guid": "uuid",
  "code": "string",
  "designation": "string", // Optional
  "project_guid": "uuid",
  "quantity": "integer",
  "company_guid": "uuid",
  "created_at": "datetime",
  "is_active": "boolean",
  "deleted_at": "datetime" // Optional
}
```
(Refer to `src/ractory/backend/app/schemas/sync/components.py` for full schema)

### Error Responses

*   **`404 Not Found`**: If `project_guid` is provided and the project is not found/accessible.

## Tenant Isolation

Standard tenant isolation applies. 