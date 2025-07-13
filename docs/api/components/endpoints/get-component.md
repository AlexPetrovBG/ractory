---
title: Get Component
description: Details about the endpoint for retrieving a specific component.
---

# Get Component

Retrieves detailed information for a specific component by its GUID.

## Endpoint

`GET /api/v1/components/{component_guid}`

## Path Parameters

| Parameter      | Type | Description                  |
|----------------|------|------------------------------|
| `component_guid`| UUID | The GUID of the component.   |

## Query Parameters

| Parameter        | Type    | Optional | Default | Description                                            |
|------------------|---------|----------|---------|--------------------------------------------------------|
| `include_inactive`| boolean | Yes      | `false` | If `true`, allows fetching a soft-deleted component.   |

## Responses

### Success: `200 OK`

Returns a `ComponentDetail` object.

**`ComponentDetail` Schema (Key Fields):**

```json
{
  "guid": "uuid",
  "code": "string",
  "designation": "string", // Optional
  "project_guid": "uuid",
  "quantity": "integer",
  "company_guid": "uuid",
  "created_at": "datetime",
  "updated_at": "datetime", // Optional
  "is_active": "boolean",
  "deleted_at": "datetime", // Optional
  "assembly_count": "integer",
  "piece_count": "integer"
}
```
(Refer to `src/ractory/backend/app/schemas/sync/components.py` for full schema)

### Error Responses

*   **`403 Forbidden`**: Access to component is forbidden.
*   **`404 Not Found`**: Component not found or not accessible.
*   **`500 Internal Server Error`**: If component data is missing required fields.

## Tenant Isolation

Standard tenant isolation applies. 