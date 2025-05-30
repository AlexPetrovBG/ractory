# API Key Management Overview

The Ra Factory API supports API key authentication for system-to-system integrations. API keys are long-lived credentials that can be scoped to specific permissions. They are associated with a specific company and can be managed by users with `CompanyAdmin` or `SystemAdmin` roles.

## Authentication

To authenticate with an API key, include it in your request headers. The API supports two header formats:

1.  **`X-API-Key: <your_api_key>`** (Recommended)
2.  **`Authorization: ApiKey <your_api_key>`**

If a valid, active API key is provided, the request will be authenticated, and the associated company and scopes will be used for authorization and data isolation.

## API Key Characteristics

-   **Prefix:** Generated API keys start with `rfk_`. Custom keys provided by users must also follow this prefix.
-   **Security:** The raw API key is only available at the time of creation. It is then hashed and stored securely. The system uses bcrypt for hashing, meaning the original key cannot be retrieved.
-   **Scopes:** API keys can be assigned scopes that limit their permissions. Currently, the available scopes are:
    -   `sync:read`: Allows reading data via synchronization endpoints.
    -   `sync:write`: Allows writing data via synchronization endpoints.
    Scopes are provided as a comma-separated string (e.g., "sync:read,sync:write").
-   **Uniqueness:** While `guid` is the primary identifier for an API key entry, the `key` itself (before hashing) must be unique across the system if a custom key is provided.
-   **Tracking:** The system tracks `created_at` and `last_used_at` timestamps for each key.

## Roles and Permissions

-   **`CompanyAdmin`**: Can manage API keys (create, read, update, delete) for their own company.
-   **`SystemAdmin`**: Can manage API keys for any company. When creating or managing keys for a specific company, the `company_guid` must be provided.

All API Key management endpoints are prefixed with `/api/v1/api-keys`. 