# Restore Article

**Endpoint:** `POST /api/v1/articles/{article_guid}/restore`

**Description:**
Restores a previously soft-deleted article by its GUID. This operation sets the article's `is_active` status to `true` and clears its `deleted_at` timestamp (sets to `NULL`).

This action will trigger a cascade restore of related entities managed by the `SyncService`. The cascade restore logic might have specific conditions, such as only restoring children whose `deleted_at` timestamp matches the parent's original `deleted_at` (if such a mechanism is in place).

**Path Parameter:**

-   **`article_guid`** (UUID, required): The GUID of the article to restore.

**Request Body:**

None.

**Response (Success: 204 No Content):**

An empty response with HTTP status 204 indicates successful restoration.

**Possible Errors:**

-   `401 Unauthorized`: If authentication fails.
-   `403 Forbidden`: If the user does not have permission to restore this article (e.g., it belongs to a different company and the user is not a `SystemAdmin`, or insufficient role).
-   `404 Not Found`: If the article with the specified `article_guid` does not exist, is not accessible, or was not previously soft-deleted.
-   `422 Unprocessable Entity`: If the `article_guid` path parameter is not a valid UUID.
-   `500 Internal Server Error`: If an unexpected error occurs during the restoration process. 