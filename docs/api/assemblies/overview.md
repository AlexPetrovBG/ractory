---
title: Assemblies API Overview
description: Overview of the Assemblies API, its purpose, and general concepts.
---

# Assemblies API Overview

The Assemblies API is responsible for managing assembly entities. Assemblies group together multiple Pieces and are associated with a Component, which in turn belongs to a Project.

## Key Concepts

*   **Assembly:** A collection of pieces forming a larger unit within a component.
*   **Hierarchy:** Assemblies fit into the hierarchy: `Project -> Component -> Assembly -> Piece`.
*   **Tenant Isolation:** Access is controlled by tenant (company) GUID. Users primarily access assemblies within their own tenant. `SystemAdmin` users may have broader access.
*   **Soft Deletion:** Assemblies are soft-deleted (marked inactive) rather than permanently removed, allowing for recovery and auditing.
*   **Cascading Operations:** Soft-deleting or restoring an assembly cascades to its child pieces, managed by `SyncService`.
*   **Data Creation and Updates:** While this API provides direct management endpoints for listing, retrieving, and soft-deleting assemblies, the primary mechanism for creating new assemblies or updating existing ones in bulk is through the [Synchronization API Endpoints](../sync/index.md#sync-assemblies). These endpoints are designed for data ingestion from external systems like RaConnect.

## Authentication and Authorization

All endpoints require authentication. Authorization is based on user roles and tenant membership. See individual endpoint documentation for specific permission requirements.

## Base Path

All API endpoints for assemblies are prefixed with `/api/v1/assemblies`. 