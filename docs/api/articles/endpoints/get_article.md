# Get Article

**Endpoint:** `GET /api/v1/articles/{article_guid}`

**Description:**
Retrieves a specific article by its GUID. By default, it only returns active articles. Use the `include_inactive` query parameter to fetch a soft-deleted article.

**Path Parameter:**

-   **`article_guid`** (UUID, required): The GUID of the article to retrieve.

**Query Parameters:**

-   **`include_inactive`** (boolean, optional, default: `false`): Set to `true` to retrieve the article even if it has been soft-deleted (`is_active = false`). If `false` (default) and the article is inactive, a `404 Not Found` error will be returned.

**Response (Success: 200 OK, `ArticleDetail` schema):**

```json
{
  "guid": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "code": "ART-001",
  "project_guid": "p1a2b3c4-e5f6-7890-1234-567890abcdef",
  "component_guid": "c1a2b3c4-e5f6-7890-1234-567890abcdef",
  "designation": "Main Support Beam",
  "company_guid": "co1a2b3c4-e5f6-7890-1234-567890abcdef",
  "created_at": "2023-10-26T10:00:00Z",
  "updated_at": "2023-10-26T14:30:00Z",
  "is_active": true,
  "deleted_at": null,
  "consume_group_designation": "Steel Profiles",
  "consume_group_priority": 1,
  "quantity": 10.5,
  "unit": "m",
  "category_designation": "Beams",
  "position": "P1.B3",
  "short_position": "B3",
  "code_no_color": "ART-001-NC",
  "component_code": "COMP-A",
  "is_extra": false,
  "length": 6000.0,
  "width": 120.0,
  "height": 80.0,
  "surface": 0.72,
  "angle1": 90.0,
  "angle2": 90.0,
  "unit_weight": 5.5,
  "bar_length": 6000.0
}
```

The response is an `ArticleDetail` object containing all available fields for the article, including dimensional data and other properties.

**Possible Errors:**

-   `401 Unauthorized`: If authentication fails.
-   `403 Forbidden`: If the user does not have permission to access this article (e.g., it belongs to a different company and the user is not a `SystemAdmin`).
-   `404 Not Found`: If the article with the specified `article_guid` does not exist, or if it is inactive and `include_inactive` is `false`.
-   `422 Unprocessable Entity`: If the `article_guid` path parameter is not a valid UUID.
-   `500 Internal Server Error`: If an unexpected error occurs (e.g., article data in DB is missing required fields). 