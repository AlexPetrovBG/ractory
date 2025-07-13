<!-- Intentional comment to force change -->
---
title: Components API Overview
description: Overview of the Components API, its purpose, and general concepts.
---

# Components API Overview

The Components API is responsible for managing component entities. Components exist within Projects and group Assemblies.

## Key Concepts

*   **Component:** A logical grouping of assemblies within a project.
*   **Hierarchy:** `Project -> Component -> Assembly -> Piece`.
*   **Tenant Isolation:** Access is controlled by tenant (company) GUID.
*   **Soft Deletion:** Components are soft-deleted.
*   **Data Creation and Updates:** While this API provides direct management endpoints for listing, retrieving, and soft-deleting components, the primary mechanism for creating new components or updating existing ones in bulk is through the [Synchronization API Endpoints](../sync/index.md#sync-components). These endpoints are designed for data ingestion from external systems like RaConnect.

## Authentication and Authorization

All endpoints require authentication. Authorization is based on user roles and tenant membership.

## Base Path

All API endpoints for components are prefixed with `/api/v1/components`. 