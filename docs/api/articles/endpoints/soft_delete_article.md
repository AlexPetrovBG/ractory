# Soft Delete Article

**Endpoint:** `DELETE /api/v1/articles/{article_guid}`

**Description:**
Soft deletes an article by its GUID. This operation marks the article as inactive (`is_active = false`) and sets its `deleted_at` timestamp to the current time. 

This action will trigger a cascade soft delete of related entities managed by the `SyncService`.

**Path Parameter:**

-   **`article_guid`** (UUID, required): The GUID of the article to soft delete.

**Request Body:**

None.

**Response (Success: 204 No Content):**

An empty response with HTTP status 204 indicates successful soft deletion.

**Possible Errors:**

-   `401 Unauthorized`: If authentication fails.
-   `403 Forbidden`: If the user does not have permission to delete this article (e.g., it belongs to a different company and the user is not a `SystemAdmin`, or insufficient role).
-   `404 Not Found`: If the article with the specified `article_guid` does not exist or is not accessible to the user.
-   `422 Unprocessable Entity`: If the `article_guid` path parameter is not a valid UUID.
-   `500 Internal Server Error`: If an unexpected error occurs during the soft deletion process. 