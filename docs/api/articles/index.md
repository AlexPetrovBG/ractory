# Articles API

This section describes the API endpoints available for managing and retrieving Articles within the Ra Factory system.

## Table of Contents

-   [Overview](./overview.md)
    -   Key Concepts
    -   Associated Entities
-   Endpoints
    -   [List Articles](./endpoints/list_articles.md)
    -   [Get Article](./endpoints/get_article.md)
    -   [Soft Delete Article](./endpoints/soft_delete_article.md)
    -   [Restore Article](./endpoints/restore_article.md)

## Introduction

Articles are fundamental data entities representing specific items or materials used in projects and components. The API allows for querying article information and managing their lifecycle (e.g., soft deletion and restoration).

Refer to the [Overview](./overview.md) for more details on article characteristics and general API behavior.

The following sections detail the available API endpoints. All endpoints are prefixed with `/api/v1/articles`.

-   **[List Articles](./endpoints/list_articles.md)**: `GET /api/v1/articles`
-   **[Get Article](./endpoints/get_article.md)**: `GET /api/v1/articles/{article_guid}`
-   **[Soft Delete Article](./endpoints/soft_delete_article.md)**: `DELETE /api/v1/articles/{article_guid}`
-   **[Restore Article](./endpoints/restore_article.md)**: `POST /api/v1/articles/{article_guid}/restore`

Note: Currently, there are no direct API endpoints for creating or updating individual articles through this router. Article creation and updates are likely handled by other mechanisms, such as a synchronization process or different API modules (e.g., related to project or component data import).

# Article Management

Endpoints for managing articles (e.g., hardware, accessories). Data creation and updates are typically handled via [Synchronization Endpoints](./../sync/index.md).

All endpoints are prefixed with `/api/v1/articles`.

## Soft Deletion and Restoration

Articles support soft deletion, which can be cascaded from parent entities or initiated directly. Restoring an article also follows cascading rules.

### 1. List Articles (`GET /`)

**Description:** Retrieves a list of articles, scoped by the authenticated user's company.

**Query Parameters:**
*   `project_guid` (UUID, optional): Filter by project.
*   `component_guid` (UUID, optional): Filter by component.
*   `company_guid` (UUID, optional): Filter by company (`SystemAdmin` only).
*   `include_inactive` (bool, optional, default: `false`): Include soft-deleted articles.
*   `limit` (int, optional, default: 100, max: 1000): Pagination limit.
*   `offset` (int, optional, default: 0): Pagination offset.

**Response (Success - 200 OK, List of `ArticleResponse` schema):**
```json
[
  {
    "guid": "article-guid",
    "code": "HW-001",
    "designation": "Screw M5x20",
    "project_guid": "project-guid",
    "component_guid": "component-guid",
    "company_guid": "company-guid",
    "quantity": 100.0,
    "unit": "pcs",
    // ... other article-specific fields ...
    "is_active": true,
    "deleted_at": null,
    "created_at": "timestamp",
    "updated_at": "timestamp"
  }
]
```
*   `404 Not Found`: If a specified parent entity (project, component) is not found/accessible.
*   `400 Bad Request`: For inconsistent parent entity GUIDs (e.g., component not belonging to project).

### 2. Get Article (`GET /{article_guid}`)

**Description:** Retrieves a specific article by its GUID.

**Path Parameter:**
*   `article_guid`: The GUID of the article.

**Query Parameters:**
*   `include_inactive` (bool, optional, default: `false`): Include if soft-deleted.

**Response (Success - 200 OK, `ArticleDetail` schema):** Contains all fields from `ArticleResponse` plus any additional details.
*   `404 Not Found`: If article does not exist or is not accessible.
*   `403 Forbidden`: If user attempts to access an article from another company (and is not `SystemAdmin`).

### 3. Soft Delete Article (`DELETE /{article_guid}`)

**Description:** Soft-deletes an article.

**Path Parameter:**
*   `article_guid`: The GUID of the article to soft-delete.

**Response (Success - 204 No Content).**
*   `404 Not Found`: If article does not exist or is not accessible.

### 4. Restore Article (`POST /{article_guid}/restore`)

**Description:** Restores a soft-deleted article.

**Path Parameter:**
*   `article_guid`: The GUID of the article to restore.

**Response (Success - 204 No Content).**
*   `404 Not Found`: If article does not exist or is not accessible. 