---
title: List Companies
slug: list_companies
---

This endpoint allows System Administrators to retrieve a list of all companies.

## Endpoint

`GET /companies`

## Access Control

- Requires `SYSTEM_ADMIN` role.

## Query Parameters

- `skip` (integer, optional, default: 0): Number of company records to skip for pagination.
- `limit` (integer, optional, default: 100): Maximum number of company records to return.

## Responses

### Success: 200 OK

Returns a JSON array of company objects, each conforming to the `CompanyRead` schema.

```json
[
  {
    "guid": "uuid",
    "name": "string",
    "short_name": "string | null",
    "logo_path": "string | null",
    "company_index": "integer | null",
    "is_active": "boolean",
    "created_at": "datetime_string",
    "updated_at": "datetime_string | null"
  },
  // ... more company objects
]
```

If no companies exist or match the pagination criteria, an empty array `[]` is returned.

### Error Responses:

- **500 Internal Server Error**:
    - If an unexpected error occurs on the server while retrieving the companies.
    ```json
    {
      "detail": "Could not retrieve companies."
    }
    ```

## Notes

- The `CompanyService.get_companies` service method handles the data retrieval.
- Pagination is supported via `skip` and `limit` query parameters. 