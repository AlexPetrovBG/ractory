# API Key Management

This section describes how to manage and use API keys for the Ra Factory API.

## Table of Contents

-   [Overview](./overview.md)
    -   Authentication Methods
    -   API Key Characteristics
    -   Roles and Permissions
-   Endpoints
    -   [Create API Key](./endpoints/create.md)
    -   [List API Keys](./endpoints/list.md)
    -   [Get API Key](./endpoints/get.md)
    -   [Update API Key](./endpoints/update.md)
    -   [Delete API Key](./endpoints/delete.md)

## Introduction

API keys provide a way to authenticate system-to-system integrations or automated scripts with the Ra Factory API. They are long-lived credentials that can be scoped with specific permissions to control access to resources.

Refer to the [Overview](./overview.md) for details on how API keys work, including authentication methods, key characteristics (prefix, security, scopes), and the roles required to manage them.

The following sections detail the available API endpoints for managing API keys. All management endpoints are prefixed with `/api/v1/api-keys` and require at least `CompanyAdmin` role for access.

-   **[Create API Key](./endpoints/create.md)**: `POST /api/v1/api-keys`
-   **[List API Keys](./endpoints/list.md)**: `GET /api/v1/api-keys`
-   **[Get API Key](./endpoints/get.md)**: `GET /api/v1/api-keys/{guid}`
-   **[Update API Key](./endpoints/update.md)**: `PUT /api/v1/api-keys/{guid}`
-   **[Delete API Key](./endpoints/delete.md)**: `DELETE /api/v1/api-keys/{guid}`

Make sure to handle the API key value securely, especially the raw key returned upon creation, as it will not be shown again. 