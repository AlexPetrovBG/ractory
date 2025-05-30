---
title: User Management API
slug: /users
---

# User Management

Endpoints for managing users. Access is governed by a role hierarchy.

All endpoints are prefixed with `/api/v1/users`.

### Role Hierarchy and Permissions

-   **`SystemAdmin`**: Can manage all users and all roles across all companies.
-   **`CompanyAdmin`**: Can manage users within their own company. Can create/update users with roles `ProjectManager` and `Operator`. Cannot manage `SystemAdmin` or other `CompanyAdmin` roles.
-   **`ProjectManager`**, **`Operator`**: Cannot manage users.

## Endpoints

- **[Create User](./endpoints/create_user.md)**: `POST /` - Creates a new user.
- **[List Users](./endpoints/list_users.md)**: `GET /` - Retrieves a list of users.
- **[Get User](./endpoints/get_user.md)**: `GET /{guid}` - Retrieves a specific user by their GUID.
- **[Update User](./endpoints/update_user.md)**: `PUT /{guid}` - Updates a user's information.
- **[Delete User](./endpoints/delete_user.md)**: `DELETE /{guid}` - Soft-deletes a user. 