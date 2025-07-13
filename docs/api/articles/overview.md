# Articles API Overview

Articles represent individual items or materials within a project and component. They store detailed information about each piece, such as its code, designation, dimensions, and other manufacturing-specific attributes.

The Articles API provides endpoints to retrieve and manage article data. Articles are company-specific and are subject to tenant isolation rules. `SystemAdmin` users have broader access capabilities.

## Key Concepts

-   **Soft Deletion:** Articles are typically soft-deleted. This means they are marked as inactive (`is_active = false`) and their `deleted_at` timestamp is set, rather than being permanently removed from the database. This allows for data recovery and historical tracking.
-   **Cascading Operations:** Soft deleting or restoring an article can have cascading effects on related entities, handled by the `SyncService`.
-   **Filtering:** The list endpoint provides robust filtering capabilities based on project, component, and company.
-   **Tenant Isolation:** Access to articles is restricted based on the authenticated user's company. `SystemAdmin` users can access articles across different companies if they provide the `company_guid`.
-   **Data Creation and Updates:** While this API provides endpoints for listing, retrieving, and deleting articles, the primary mechanism for creating new articles or updating existing ones in bulk is through the [Synchronization API Endpoints](../sync/index.md#sync-articles). These endpoints are designed for data ingestion from external systems like RaConnect.

## Associated Entities

-   **Projects:** Articles belong to a `Project` (via `project_guid`).
-   **Components:** Articles also belong to a `Component` (via `component_guid`), which in turn belongs to a project.

All Articles API endpoints are prefixed with `/api/v1/articles`. 