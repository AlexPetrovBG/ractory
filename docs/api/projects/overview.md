---
title: Projects API Overview
description: Overview of the Projects API, its purpose, and general concepts.
---

# Projects API Overview

The Projects API is responsible for managing project entities. Projects are the top-level organizational unit.

## Key Concepts

*   **Project:** The highest-level container for work, under which components, assemblies, and pieces are organized.
*   **Tenant Isolation:** Access is controlled by tenant (company) GUID.
*   **Soft Deletion:** Projects are soft-deleted.
*   **Data Creation and Updates:** While this API provides direct management endpoints for listing, retrieving, and soft-deleting projects, the primary mechanism for creating new projects or updating existing ones in bulk is through the [Synchronization API Endpoints](../sync/index.md#sync-projects). These endpoints are designed for data ingestion from external systems like RaConnect.

## Authentication and Authorization

All endpoints require authentication. Authorization is based on user roles and tenant membership.

## Base Path

All API endpoints for projects are prefixed with `/api/v1/projects`. 