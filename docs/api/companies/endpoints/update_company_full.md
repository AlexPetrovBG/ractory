---
title: Update Company (Full)
slug: update_company_full
---

This endpoint allows System Administrators to fully update a specific company by its GUID. It functions as an alias to the `PATCH /companies/{company_guid}` endpoint.

## Endpoint

`PUT /companies/{company_guid}`

## Access Control

- Requires `SYSTEM_ADMIN` role.

## Path Parameters

- `company_guid` (UUID, required): The unique identifier (GUID) of the company to update.

## Request Body

The request body must be a JSON object conforming to the `CompanyUpdate` schema. For a `PUT` request, typically all fields are expected. Due to its alias nature to `PATCH`, it will behave as a partial update if some fields are omitted. However, to conform to `PUT` semantics, clients *should* provide all fields with their intended values.

```json
{
  "name": "string (1-100 chars)",
  "short_name": "string | null (max 50 chars)",
  "logo_path": "string | null (max 255 chars)",
  "company_index": "integer | null (0-99, must be unique if provided)",
  "is_active": "boolean"
}
```

### Fields:

- `name` (string): The name for the company. Min 1, Max 100 chars.
- `short_name` (string, optional): The short name for the company. Max 50 chars.
- `logo_path` (string, optional): The path to the company logo. Max 255 chars.
- `company_index` (integer, optional): The unique numerical index for the company (0-99). If provided, it must not be in use by another company (unless it's the current company's index).
- `is_active` (boolean): The active status for the company.

## Responses

Identical to the `PATCH /companies/{company_guid}` endpoint.

### Success: 200 OK

Returns a JSON object representing the updated company, conforming to the `CompanyRead` schema.

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

- **409 Conflict**:
    - If updating the `company_index` to a value that is already in use by another company.

- **422 Unprocessable Entity**:
    - If the request body fails validation (e.g. length constraints violated).

- **500 Internal Server Error**:
    - If an unexpected error occurs on the server.

(Refer to the [Update Company (Partial)](./update_company_partial.md) documentation for detailed error message examples.)

## Notes

- This endpoint directly calls the implementation of the `PATCH /companies/{company_guid}` endpoint.
- The primary reason for its existence is to solve potential `405 Method Not Allowed` errors if a client attempts a `PUT` request where only `PATCH` was initially defined.
- While it behaves like `PATCH` (allowing partial updates if fields are missing), clients using `PUT` should semantically aim to provide the complete resource representation. 