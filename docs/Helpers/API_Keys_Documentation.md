# Ra Factory API Keys Guide

This document explains how to use API keys for integration with the Ra Factory API system. API keys provide a more secure and flexible authentication mechanism for machine-to-machine communication compared to regular user credentials.

## API Key Authentication vs. JWT Authentication

Ra Factory supports two authentication methods:

### 1. Regular JWT Authentication (User-based)

- Uses username/password credentials
- Returns short-lived JWT tokens (~15 minutes)
- Requires token refresh mechanism
- Tied to a specific user account
- Suitable for interactive sessions

### 2. API Key Authentication (Integration-based)

- Uses a single token that doesn't expire
- Doesn't require token refresh
- Can be scoped to specific operations
- Can be revoked without affecting user accounts
- Supports tracking of usage
- Ideal for machine-to-machine integration

## When to Use API Keys

Use API keys when:

- Building automated integrations with Ra Factory
- Setting up machine-to-machine communication
- Implementing CI/CD pipelines or workflows
- Creating long-running services that need API access
- You need to limit access to specific operations

## API Key Management

### Creating an API Key

Only users with `SystemAdmin` or `CompanyAdmin` roles can create API keys.

**Request:**
```bash
curl -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer <your_access_token>" \
     -d '{"description": "Integration with ERP system", "scopes": "sync:read,sync:write"}' \
     http://localhost:8000/api/v1/api-keys | cat
```

**Response:**
```json
{
  "guid": "550e8400-e29b-41d4-a716-446655440000",
  "key": "rfk_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
  "description": "Integration with ERP system",
  "scopes": "sync:read,sync:write",
  "created_at": "2023-04-01T12:00:00Z",
  "company_guid": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Important:** Store the returned `key` value securely. This is the only time it will be displayed, and it cannot be retrieved later. If lost, you will need to create a new API key.

### Listing API Keys

**Request:**
```bash
curl -X GET -H "Authorization: Bearer <your_access_token>" \
     http://localhost:8000/api/v1/api-keys | cat
```

**Response:**
```json
{
  "api_keys": [
    {
      "guid": "550e8400-e29b-41d4-a716-446655440000",
      "description": "Integration with ERP system",
      "scopes": "sync:read,sync:write",
      "created_at": "2023-04-01T12:00:00Z",
      "last_used_at": "2023-04-02T10:15:30Z",
      "is_active": true,
      "company_guid": "550e8400-e29b-41d4-a716-446655440000"
    },
    {
      "guid": "660e8400-e29b-41d4-a716-446655440000",
      "description": "Development environment",
      "scopes": "sync:read",
      "created_at": "2023-04-01T13:00:00Z",
      "last_used_at": null,
      "is_active": true,
      "company_guid": "550e8400-e29b-41d4-a716-446655440000"
    }
  ]
}
```

### Getting a Specific API Key

**Request:**
```bash
curl -X GET -H "Authorization: Bearer <your_access_token>" \
     http://localhost:8000/api/v1/api-keys/550e8400-e29b-41d4-a716-446655440000 | cat
```

**Response:**
```json
{
  "guid": "550e8400-e29b-41d4-a716-446655440000",
  "description": "Integration with ERP system",
  "scopes": "sync:read,sync:write",
  "created_at": "2023-04-01T12:00:00Z",
  "last_used_at": "2023-04-02T10:15:30Z",
  "is_active": true,
  "company_guid": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Updating an API Key

You can update an API key's description, scopes, or active status.

**Request:**
```bash
curl -X PUT -H "Content-Type: application/json" \
     -H "Authorization: Bearer <your_access_token>" \
     -d '{"description": "Updated description", "scopes": "sync:read", "is_active": true}' \
     http://localhost:8000/api/v1/api-keys/550e8400-e29b-41d4-a716-446655440000 | cat
```

**Response:**
```json
{
  "guid": "550e8400-e29b-41d4-a716-446655440000",
  "description": "Updated description",
  "scopes": "sync:read",
  "created_at": "2023-04-01T12:00:00Z",
  "last_used_at": "2023-04-02T10:15:30Z",
  "is_active": true,
  "company_guid": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Deleting an API Key

**Request:**
```bash
curl -X DELETE -H "Authorization: Bearer <your_access_token>" \
     http://localhost:8000/api/v1/api-keys/550e8400-e29b-41d4-a716-446655440000 | cat
```

**Response:**
```
204 No Content
```

## Using API Keys for Authentication

There are two ways to include your API key in requests:

### 1. Using the `X-API-Key` Header (Recommended)

```bash
curl -X GET -H "X-API-Key: rfk_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6" \
     http://localhost:8000/api/v1/sync/projects | cat
```

### 2. Using the `Authorization` Header

```bash
curl -X GET -H "Authorization: ApiKey rfk_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6" \
     http://localhost:8000/api/v1/sync/projects | cat
```

## Available Scopes

API keys can be restricted to specific operations using scopes. Multiple scopes are specified as a comma-separated string.

| Scope | Description |
|-------|-------------|
| `sync:read` | Permission to read synchronization data |
| `sync:write` | Permission to write synchronization data |
| `workstation:read` | Permission to read workstation data |
| `workstation:write` | Permission to manage workstations |
| `users:read` | Permission to read user data |

If no scope is specified, the API key won't have access to any protected endpoints. A SystemAdmin user bypasses scope checks.

## Best Practices for API Key Security

1. **Never expose API keys** in client-side code or version control
2. **Use environment variables** or a secure secrets manager to store keys
3. **Limit scopes** to only what each integration needs
4. **Create separate keys** for different integrations or environments
5. **Monitor usage** and rotate keys periodically
6. **Deactivate unused keys** promptly
7. **Apply rate limiting** in production environments
8. **Implement client-side retry logic** with exponential backoff

## Error Handling

When using API keys, be prepared to handle the following error responses:

- `401 Unauthorized`: Invalid or expired API key
- `403 Forbidden`: API key doesn't have the required scope
- `429 Too Many Requests`: Rate limit exceeded (if implemented)

Example error response:
```json
{
  "error": "Insufficient permissions",
  "detail": "API key missing required scopes. Need one of: sync:write"
}
```

## Integration with Sync Endpoints

API keys are particularly useful for the synchronization endpoints that import data from external systems:

```bash
# Sync projects example with API key
curl -X POST -H "Content-Type: application/json" \
     -H "X-API-Key: rfk_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6" \
     -d '{"projects": [{"code": "P001", "creation_date": "2023-01-01T00:00:00Z", "id": 1}]}' \
     http://localhost:8000/api/v1/sync/projects | cat
```

This requires an API key with the `sync:write` scope. 