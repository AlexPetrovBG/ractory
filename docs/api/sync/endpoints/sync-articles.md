---
title: Sync Articles
description: Details about the endpoint for bulk inserting or updating articles.
---

# Sync Articles

Bulk inserts or updates article data (e.g., hardware, accessories, raw materials). This endpoint is typically used for synchronizing article information from an external system like RaConnect, linking them to existing projects and components.

## Endpoint

`POST /api/v1/sync/articles`

## Authorization

Requires an API key with the `sync:write` scope or one of the following user roles: `SystemAdmin`, `CompanyAdmin`, `Integration`.

## Request Body

The request body must be a JSON object containing a single key `articles`, which is an array of article objects to be created or updated.

**`ArticleBulkInsert` Schema:**

```json
{
  "articles": [
    // Array of ArticleCreate objects
  ]
}
```

**`ArticleCreate` Schema (for each object in the `articles` array):**

Key required fields include:

*   `code`: "string" (Article code)
*   `project_guid`: "uuid"
*   `component_guid`: "uuid"
*   `company_guid`: "uuid"

Optional fields include `guid` (for updates), `designation`, `quantity`, `unit`, and other article-specific attributes like `length`, `width`, `category_designation`, etc.

Refer to `src/ractory/backend/app/schemas/sync/articles.py` for the complete `ArticleCreate` schema definition.

**Example Request (Simplified):**

```json
{
  "articles": [
    {
      "guid": "523e4567-e89b-12d3-a456-426614174005", // For update
      "code": "HW-BOLT-M8",
      "project_guid": "123e4567-e89b-12d3-a456-426614174000",
      "component_guid": "223e4567-e89b-12d3-a456-426614174002",
      "company_guid": "abcdef12-3456-7890-abcd-ef1234567890",
      "designation": "M8 Bolt, Steel",
      "quantity": 100,
      "unit": "pcs"
    },
    {
      "code": "ACC-HANDLE-01", // For new insert
      "project_guid": "123e4567-e89b-12d3-a456-426614174000",
      "component_guid": "223e4567-e89b-12d3-a456-426614174002",
      "company_guid": "abcdef12-3456-7890-abcd-ef1234567890",
      "designation": "Door Handle, Aluminium",
      "quantity": 10,
      "unit": "pcs"
    }
  ]
}
```

## Responses

### Success: `200 OK`

Returns a `SyncResult` object indicating the number of articles inserted and updated.

**`SyncResult` Schema:**

```json
{
  "inserted": "integer",
  "updated": "integer"
}
```

### Error Responses

*   **`400 Bad Request`**: Malformed request.
*   **`401 Unauthorized`**: Authentication failure.
*   **`403 Forbidden`**: Authorization failure.
*   **`422 Unprocessable Entity`**: Validation error (e.g., missing required fields; parent entities not found or in wrong company).

## Important Notes

*   **Parent Entities:** `project_guid` and `component_guid` must reference existing entities within the same `company_guid`.
*   **Upsert Logic:** Based on `guid` (if provided) and `company_guid`.
*   **Tenant Validation:** `company_guid` for each article is validated. 