---
title: Companies API
slug: /companies
---

This section provides a detailed overview of the Companies API endpoints.

The Companies API allows System Administrators to manage company records within the platform. This includes creating, retrieving, updating, and deleting company information.

All endpoints in this API are restricted to users with the `SYSTEM_ADMIN` role.

## Endpoints

The following endpoints are available under the `/companies` path:

- **[Create Company](./endpoints/create_company.md)**: `POST /` - Create a new company.
- **[List Companies](./endpoints/list_companies.md)**: `GET /` - List all companies.
- **[Get Company](./endpoints/get_company.md)**: `GET /{company_guid}` - Retrieve a specific company by its GUID.
- **[Update Company (Partial)](./endpoints/update_company_partial.md)**: `PATCH /{company_guid}` - Partially update an existing company.
- **[Update Company (Full)](./endpoints/update_company_full.md)**: `PUT /{company_guid}` - Fully update an existing company.
- **[Delete Company](./endpoints/delete_company.md)**: `DELETE /{company_guid}` - Delete a specific company.

Each endpoint is documented in detail on its respective page, including request parameters, response schemas, and potential error codes. 