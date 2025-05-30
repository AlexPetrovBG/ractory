---
title: Get Company
slug: get_company
---

This endpoint allows System Administrators to retrieve a specific company by its GUID.

## Endpoint

`GET /companies/{company_guid}`

## Access Control

- Requires `SYSTEM_ADMIN` role.

## Path Parameters

- `company_guid` (UUID, required): The unique identifier (GUID) of the company to retrieve.

## Responses

### Success: 200 OK

Returns a JSON object representing the company, conforming to the `CompanyRead` schema.

```json
{
  "guid": "uuid",
  "name": "string",
  "short_name": "string | null",
  "logo_path": "string | null",
  "company_index": "integer | null",
  "is_active": "boolean",
  "created_at": "datetime_string",
  "updated_at": "datetime_string | null"
}
```

### Error Responses:

- **404 Not Found**:
    - If a company with the specified `company_guid` does not exist.
    ```json
    {
      "detail": "Company with GUID {company_guid} not found."
    }
    ```

- **500 Internal Server Error**:
    - If an unexpected error occurs on the server (though less common for GET by ID if the ID format is valid).

## Notes

- The `CompanyService.get_company` service method is used to fetch the company from the database. 