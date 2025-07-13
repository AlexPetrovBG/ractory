# List Articles

**Endpoint:** `GET /api/v1/articles`

**Description:**
Retrieves a list of articles. Supports filtering by project, component, and company, as well as pagination. By default, only active (not soft-deleted) articles are returned.

**Query Parameters:**

-   **`project_guid`** (UUID, optional): Filter articles belonging to a specific project.
-   **`component_guid`** (UUID, optional): Filter articles belonging to a specific component.
    -   If `project_guid` is also provided, the component must belong to that project.
-   **`company_guid`** (UUID, optional): 
    -   For `SystemAdmin` users, this filters articles by the specified company. 
    -   For other users, if provided, it must match their own company; otherwise, an error might occur or it will be ignored (behavior depends on `validate_company_access`). Access is primarily controlled by the user's token.
-   **`include_inactive`** (boolean, optional, default: `false`): Set to `true` to include soft-deleted articles in the results. When `true`, articles with `is_active = false` will be returned.
-   **`limit`** (integer, optional, default: `100`): Maximum number of articles to return. Minimum `1`, maximum `1000`.
-   **`offset`** (integer, optional, default: `0`): Number of articles to skip for pagination. Minimum `0`.

**Response (Success: 200 OK, List of `ArticleResponse` schema):**

```json
[
  {
    "guid": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "code": "ART-001",
    "project_guid": "p1a2b3c4-e5f6-7890-1234-567890abcdef",
    "component_guid": "c1a2b3c4-e5f6-7890-1234-567890abcdef",
    "designation": "Main Support Beam",
    "company_guid": "co1a2b3c4-e5f6-7890-1234-567890abcdef",
    "created_at": "2023-10-26T10:00:00Z",
    "is_active": true,
    "deleted_at": null
  },
  {
    "guid": "b2c3d4e5-f6a7-8901-2345-678901bcdef0",
    "code": "ART-002",
    "project_guid": "p1a2b3c4-e5f6-7890-1234-567890abcdef",
    "component_guid": "c1a2b3c4-e5f6-7890-1234-567890abcdef",
    "designation": "Side Panel",
    "company_guid": "co1a2b3c4-e5f6-7890-1234-567890abcdef",
    "created_at": "2023-10-27T11:00:00Z",
    "is_active": true,
    "deleted_at": null
  }
  // ... more articles
]
```

Each object in the list is an `ArticleResponse` containing:
-   `guid` (UUID)
-   `code` (string)
-   `project_guid` (UUID)
-   `component_guid` (UUID)
-   `designation` (string, optional)
-   `company_guid` (UUID)
-   `created_at` (datetime)
-   `is_active` (boolean)
-   `deleted_at` (datetime, optional)

**Possible Errors:**

-   `400 Bad Request`: If `component_guid` is provided but does not belong to the specified `project_guid`.
-   `401 Unauthorized`: If authentication fails.
-   `403 Forbidden`: If a non-SystemAdmin user tries to access data for a `company_guid` other than their own.
-   `404 Not Found`:
    -   If `project_guid` is provided and the project is not found or not accessible.
    -   If `component_guid` is provided and the component is not found or not accessible.
-   `422 Unprocessable Entity`: If query parameters are invalid (e.g., `limit` out of range).
-   `500 Internal Server Error`: If an unexpected error occurs. 