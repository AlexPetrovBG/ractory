---
title: Synchronization API Overview
description: Overview of the Synchronization API, its purpose, and general concepts.
---

# Synchronization API Overview

The Synchronization API is designed for bulk data import and update operations, primarily to facilitate integration with external systems, such as RaConnect. It allows for efficient management of large datasets for Projects, Components, Assemblies, Pieces, and Articles.

## Key Concepts

*   **Bulk Operations:** The API supports sending arrays of objects to create or update multiple records in a single request.
*   **Upsert Logic:** The `SyncService` handles the underlying logic. If an entity with a provided GUID exists for the user's company, it's updated; otherwise, a new entity is created. If no GUID is provided for an item, a new one is generated.
*   **Tenant Isolation & Validation:** All operations are strictly scoped to the authenticated user's tenant (company). Each item in a bulk request undergoes `company_guid` validation against the current user's tenant. `SystemAdmin` users might have broader capabilities depending on the specific implementation of `validate_company_access`.
*   **Required Scopes/Roles:** Access to these endpoints is protected and requires an API key with the `sync:write` scope or specific user roles (SystemAdmin, CompanyAdmin, Integration).
*   **Response Format:** All sync endpoints return a `SyncResult` object, which indicates the number of records successfully inserted and updated.
    ```json
    {
      "inserted": 10, // Number of new records created
      "updated": 5    // Number of existing records updated
    }
    ```
*   **Error Handling:**
    *   `400 Bad Request`: For issues like exceeding batch limits (e.g., for pieces).
    *   `401 Unauthorized`: If authentication fails (e.g., invalid token).
    *   `403 Forbidden`: If the user/API key lacks the required scope/role, or if there's a company access violation.
    *   `422 Unprocessable Entity`: For validation errors in the request payload (e.g., missing required fields, incorrect data types).

## Base Path

All API endpoints for synchronization are prefixed with `/api/v1/sync`.

## Entity-Specific Notes

*   **Pieces:** The `/sync/pieces` endpoint has a maximum batch size of 1000 pieces per request.

This API is the primary mechanism for populating and updating core manufacturing and project data within the system, ensuring consistency with external sources of truth. 