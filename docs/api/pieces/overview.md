---
title: Pieces API Overview
description: Overview of the Pieces API, its purpose, and general concepts.
---

# Pieces API Overview

The Pieces API is responsible for managing individual production pieces. These pieces are the most granular level of tracking in the system and are typically associated with an Assembly, which in turn belongs to a Component, and then a Project.

## Key Concepts

*   **Piece:** An individual item that is tracked through the manufacturing or assembly process. Each piece has a unique identifier and can store various attributes like dimensions, material, status, etc.
*   **Hierarchy:** Pieces exist within a hierarchy: `Project -> Component -> Assembly -> Piece`.
*   **Tenant Isolation:** Access to pieces is strictly controlled by tenant (company) GUID. Users can only access pieces belonging to their own tenant, with `SystemAdmin` users having broader access when a specific `company_guid` is provided in certain endpoints.
*   **Soft Deletion:** Pieces are not permanently deleted from the system. Instead, they are marked as inactive (`is_active = false`) and their `deleted_at` timestamp is set. This allows for data recovery and auditing.
*   **Cascading Operations:** Soft-deleting or restoring a parent entity (like an Assembly or Component) can cascade the operation to its child pieces. Similarly, direct soft-deletion or restoration of a piece can affect its related data if applicable (though pieces are generally the lowest level).
*   **Synchronization:** While this API provides direct management endpoints, the primary mechanism for creating and updating piece data in bulk is often through the [Synchronization Endpoints](../sync/index.md), which handle data ingestion from external systems.

## Authentication and Authorization

All endpoints require authentication. Authorization is based on user roles and tenant membership. See individual endpoint documentation for specific permission requirements.

## Base Path

All API endpoints for pieces are prefixed with `/api/v1/pieces`. 