---
title: Create Company
slug: create_company
---

This endpoint allows System Administrators to create a new company.

## Endpoint

`POST /companies`

## Access Control

- Requires `SYSTEM_ADMIN` role.

## Request Body

The request body must be a JSON object conforming to the `CompanyCreate` schema.

```json
{
  "name": "string (required, 1-100 chars)",
  "short_name": "string (optional, max 50 chars)",
  "logo_path": "string (optional, max 255 chars)",
  "company_index": "integer (optional, 0-99, must be unique)",
  "is_active": "boolean (optional, defaults to true)"
}
```

### Fields:

- `name` (string, required): The name of the company. Min 1, Max 100 characters.
- `short_name` (string, optional): An optional short name for the company. Max 50 characters.
- `logo_path` (string, optional): An optional path to the company logo. Max 255 characters.
- `company_index` (integer, optional): An optional unique numerical index for the company (0-99). If provided, it must not be in use by another company.
- `is_active` (boolean, optional): Whether the company is active. Defaults to `true` if not provided.

## Responses

### Success: 201 Created

Returns a JSON object representing the newly created company, conforming to the `CompanyRead` schema.

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

- **409 Conflict**:
    - If a company with the provided `name` already exists.
    - If a `company_index` is provided and it's already in use by another company.
    ```json
    {
      "detail": "Company with name 'Example Corp' already exists."
    }
    ```
    ```json
    {
      "detail": "Company index 12 is already in use."
    }
    ```

- **422 Unprocessable Entity**:
    - If the request body fails validation (e.g., `company_index` out of range, invalid data types, length constraints violated).
    ```json
    {
      "detail": "Validation error message from Pydantic."
    }
    ```

- **500 Internal Server Error**:
    - If an unexpected error occurs on the server.
    ```json
    {
      "detail": "Could not create company."
    }
    ```

## Notes

- The `CompanyService.create_company` service method handles the actual creation logic.
- It first checks for existing companies by name and, if provided, by `company_index` to ensure uniqueness. 