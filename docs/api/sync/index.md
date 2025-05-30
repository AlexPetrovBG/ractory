---
title: Synchronization API
description: Guide to the Synchronization API for bulk data operations.
---

# Synchronization API

The Synchronization API provides endpoints for bulk inserting or updating data for various entities. These endpoints are typically used for integrating with external systems like RaConnect to keep the database synchronized.

All operations require an API key with the `sync:write` scope or appropriate user roles (SystemAdmin, CompanyAdmin, Integration).

This guide covers the following topics:

- [Overview](./overview.md)
- [Endpoints](./endpoints/index.md)
  - [Sync Projects](./endpoints/sync-projects.md)
  - [Sync Components](./endpoints/sync-components.md)
  - [Sync Assemblies](./endpoints/sync-assemblies.md)
  - [Sync Pieces](./endpoints/sync-pieces.md)
  - [Sync Articles](./endpoints/sync-articles.md) 