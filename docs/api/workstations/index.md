---
title: Workstation API
slug: /workstations
---

# Workstation Management

Endpoints for managing workstations.

All endpoints are prefixed with `/api/v1/workstations`.

### Permissions

-   **`SystemAdmin`**: Can manage workstations in any company.
-   **`CompanyAdmin`**: Can manage workstations only within their own company.
-   Other roles typically have read-only access to workstations within their company, if any.

## Endpoints

- **[Create Workstation](./endpoints/create_workstation.md)**: `POST /` - Creates a new workstation.
- **[List Workstations](./endpoints/list_workstations.md)**: `GET /` - Retrieves a list of workstations.
- **[Get Workstation](./endpoints/get_workstation.md)**: `GET /{guid}` - Retrieves a specific workstation.
- **[Update Workstation](./endpoints/update_workstation.md)**: `PUT /{guid}` - Updates a workstation.
- **[Delete Workstation](./endpoints/delete_workstation.md)**: `DELETE /{guid}` - Deactivates a workstation.

### 1. Create Workstation (`POST /`)

**Description:** Creates a new workstation.

**Permissions:** `