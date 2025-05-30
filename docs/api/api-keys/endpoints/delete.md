# Delete API Key

**Endpoint:** `DELETE /api/v1/api-keys/{guid}`

**Description:**
Deletes an API key by its GUID.
- `CompanyAdmin` can only delete keys belonging to their own company.
- `SystemAdmin` can delete any key by its GUID.

Once deleted, the key can no longer be used for authentication.

**Path Parameter:**

-   **`guid`** (UUID, required): The GUID of the API key to delete.

**Request Body:**

None.

**Response (Success: 204 No Content):**

An empty response with HTTP status 204 indicates successful deletion.

**Possible Errors:**

-   `401 Unauthorized`: If authentication fails.
-   `403 Forbidden`:
    -   If the authenticated user does not have `CompanyAdmin` or `SystemAdmin` role.
    -   If a `CompanyAdmin` tries to delete an API key not belonging to their company.
-   `404 Not Found`: If an API key with the specified `guid` does not exist.
-   `422 Unprocessable Entity`: If the `guid` path parameter is not a valid UUID.
-   `500 Internal Server Error`: If an unexpected error occurs during deletion. 