---
title: Update Company (Partial)
slug: update_company_partial
---

This endpoint allows System Administrators to partially update a specific company by its GUID. Only the fields provided in the request body will be updated.

## Endpoint

`PATCH /companies/{company_guid}`

## Access Control

- Requires `SYSTEM_ADMIN` role.

## Path Parameters

- `company_guid` (UUID, required): The unique identifier (GUID) of the company to update.

## Request Body

The request body must be a JSON object conforming to the `CompanyUpdate` schema. All fields are optional.

```json
{
  "name": "string (optional, 1-100 chars)",
  "short_name": "string (optional, max 50 chars)",
  "logo_path": "string (optional, max 255 chars)",
  "company_index": "integer (optional, 0-99, must be unique if provided)",
  "is_active": "boolean (optional)"
}
```

### Fields:

- `name` (string, optional): The new name for the company. If provided, it must be unique. Min 1, Max 100 chars.
- `short_name` (string, optional): The new short name for the company. Max 50 chars.
- `logo_path` (string, optional): The new path to the company logo. Max 255 chars.
- `company_index` (integer, optional): The new unique numerical index for the company (0-99). If provided, it must not be in use by another company (unless it's the current company's index).
- `is_active` (boolean, optional): The new active status for the company.

If the request body is empty or contains no updatable fields (e.g., `{}`), the endpoint will return the existing company data without making any changes.

## Responses

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
    ```json
    {
      "detail": "Company with GUID {company_guid} not found."
    }
    ```

- **409 Conflict**:
    - If updating the `company_index` to a value that is already in use by another company.
    ```json
    {
      "detail": "Company index {company_index} is already in use."
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
    - If an unexpected error occurs on the server during the update process.
    ```json
    {
      "detail": "Could not update company: {error_message}"
    }
    ```

## Notes

- The `CompanyService.update_company` service method handles the update logic.
- It first verifies the existence of the company.
- If `company_index` is part of the update, its uniqueness (excluding the current company) is checked.
- Only fields present in the `company_update` Pydantic model and set (not `None` or `exclude_unset=True`) are passed to the service for updating. 