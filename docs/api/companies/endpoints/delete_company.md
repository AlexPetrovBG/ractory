---
title: Delete Company
slug: delete_company
---

This endpoint allows System Administrators to delete a specific company by its GUID.

## Endpoint

`DELETE /companies/{company_guid}`

## Access Control

- Requires `SYSTEM_ADMIN` role.

## Path Parameters

- `company_guid` (UUID, required): The unique identifier (GUID) of the company to delete.

## Request Body

No request body is required for this endpoint.

## Responses

### Success: 204 No Content

Indicates that the company was successfully deleted. No content is returned in the response body.

### Error Responses:

- **404 Not Found**:
    - If a company with the specified `company_guid` does not exist.
    ```json
    {
      "detail": "Company with GUID {company_guid} not found."
    }
    ```

- **500 Internal Server Error**:
    - If an unexpected error occurs on the server during the deletion process.
    ```json
    {
      "detail": "Could not delete company: {error_message}"
    }
    ```

## Notes

- The `CompanyService.delete_company` service method handles the deletion logic.
- It first verifies the existence of the company before attempting to delete it.
- Successful deletion results in a `204 No Content` status, which is standard for `DELETE` operations that don't return data. 