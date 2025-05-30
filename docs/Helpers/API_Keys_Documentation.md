# Ra Factory API Keys Guide

## Overview

Ra Factory uses API keys for secure machine-to-machine authentication, primarily for data synchronization operations. Each API key is associated with a specific company and can have defined scopes that limit its access.

## API Key Format

API keys follow this format:
- Prefix: `rfk_` (Ra Factory Key)
- Random string: 32 characters of alphanumeric content
- Example: `rfk_7PebwYeCHIOyoCtDOPp7Avgwx0ulutuw`

## Security Features

- API keys are securely hashed before storage using the same mechanism as passwords
- Each key has a unique hash stored in the database
- Keys are validated using constant-time comparison to prevent timing attacks
- API keys are company-scoped for tenant isolation
- Active/inactive status can be toggled for immediate revocation
- Last used timestamp is tracked for auditing

## Database Schema

The API keys are stored in the `api_keys` table with the following structure:

```sql
CREATE TABLE api_keys (
    guid UUID PRIMARY KEY,
    company_guid UUID NOT NULL REFERENCES companies(guid),
    key_hash VARCHAR NOT NULL UNIQUE,
    description VARCHAR,
    scopes VARCHAR,
    is_active BOOLEAN NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now(),
    last_used_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ
);
```

## API Endpoints

### Create API Key
```http
POST /api/v1/api-keys
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
    "description": "Test Integration",
    "scopes": "sync:read,sync:write"
}
```

Response:
```json
{
    "guid": "uuid-string",
    "key": "rfk_<random-string>",
    "description": "Test Integration",
    "scopes": "sync:read,sync:write",
    "created_at": "2024-05-02T10:00:00Z",
    "company_guid": "company-uuid"
}
```

### List API Keys
```http
GET /api/v1/api-keys
Authorization: Bearer <jwt_token>
```

Response:
```json
{
    "api_keys": [
        {
            "guid": "uuid-string",
            "description": "Test Integration",
            "scopes": "sync:read,sync:write",
            "created_at": "2024-05-02T10:00:00Z",
            "last_used_at": "2024-05-02T11:00:00Z",
            "is_active": true,
            "company_guid": "company-uuid"
        }
    ]
}
```

### Update API Key
```http
PUT /api/v1/api-keys/{guid}
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
    "description": "Updated Description",
    "scopes": "sync:read",
    "is_active": true
}
```

### Delete API Key
```http
DELETE /api/v1/api-keys/{guid}
Authorization: Bearer <jwt_token>
```

## Using API Keys

API keys can be provided in HTTP requests in two ways:

1. Using the `X-API-Key` header:
```http
GET /api/v1/sync/projects
X-API-Key: rfk_your_api_key_here
```

2. Using the Authorization header with ApiKey scheme:
```http
GET /api/v1/sync/projects
Authorization: ApiKey rfk_your_api_key_here
```

## Available Scopes

API keys can be assigned one or more of the following scopes (comma-separated):

- `sync:read` - Read access to synchronization endpoints
- `sync:write` - Write access to synchronization endpoints

Example: `"sync:read,sync:write"`

## Authentication Flow

1. Client creates an API key through the management API using JWT authentication
2. The API returns the key only once - it must be stored securely by the client
3. The key hash is stored in the database
4. Client uses the API key for subsequent requests
5. Server validates the key by:
   - Checking if the key exists and is active
   - Verifying the key hash matches
   - Confirming the associated company has access to the requested resource
   - Validating the requested operation against the key's scopes

## Best Practices

1. **Key Storage**
   - Store API keys securely
   - Never commit API keys to version control
   - Use environment variables or secure vaults
   - Rotate keys periodically

2. **Scope Usage**
   - Follow the principle of least privilege
   - Only grant required scopes
   - Regularly audit key permissions

3. **Key Management**
   - Document the purpose of each key
   - Use descriptive names in the description field
   - Monitor key usage through last_used_at
   - Deactivate unused keys
   - Delete keys that are no longer needed

4. **Security**
   - Use HTTPS for all API requests
   - Don't share keys between applications
   - Rotate keys if compromised
   - Monitor for unusual activity

## Error Handling

Common error responses when using API keys:

- `401 Unauthorized`: Invalid or expired API key
- `403 Forbidden`: Valid key but insufficient scope
- `404 Not Found`: API key doesn't exist
- `422 Unprocessable Entity`: Invalid scope format

## Rate Limiting

API key authentication is subject to rate limiting:
- Limits are per API key
- Exceeded limits return 429 Too Many Requests
- Headers indicate remaining quota

## Monitoring and Auditing

The following data is tracked for each API key:
- Creation timestamp
- Last used timestamp
- Updates to key configuration
- Active/inactive status changes

## Implementation Details

The API key service (`ApiKeyService`) provides the following functionality:

1. **Key Generation**
   - Uses cryptographically secure random generation
   - Ensures key uniqueness
   - Applies consistent formatting

2. **Key Validation**
   - Constant-time comparison
   - Automatic last_used_at updates
   - Scope validation

3. **Key Management**
   - CRUD operations
   - Scope management
   - Status toggling

## Troubleshooting

Common issues and solutions:

1. **Invalid Key Format**
   - Ensure key includes `rfk_` prefix
   - Verify key length (36 characters total)
   - Check for proper character set (alphanumeric)

2. **Authentication Failures**
   - Verify key is active
   - Check company_guid matches
   - Confirm required scopes
   - Ensure proper header format

3. **Rate Limiting**
   - Monitor usage patterns
   - Check rate limit headers
   - Implement backoff strategy

## Migration Notes

The API key system was updated with the following changes:
- Added GUID as primary key
- Improved scope handling
- Added description field
- Enhanced timestamp tracking
- Added unique constraint on key_hash

## Future Enhancements

Planned improvements to the API key system:

1. **Enhanced Scoping**
   - Resource-level permissions
   - Time-based restrictions
   - IP-based restrictions

2. **Monitoring**
   - Usage analytics
   - Anomaly detection
   - Automated key rotation

3. **Management**
   - Bulk operations
   - Key expiration
   - Automated cleanup

## Soft Delete & Restore Permissions

### Roles Allowed
- **SystemAdmin**: Can soft delete and restore any entity in any company
- **CompanyAdmin**: Can soft delete and restore entities within their own company
- **ProjectManager, Operator, Integration**: Cannot soft delete or restore entities

### API Key Scopes
- API keys **cannot** be used for soft delete or restore endpoints. These operations require JWT authentication with the appropriate role (SystemAdmin or CompanyAdmin).

### Endpoints Requiring Permissions
- `DELETE /api/v1/{entity}/{guid}` (soft delete)
- `POST /api/v1/{entity}/{guid}/restore` (restore)

**Note:** Attempting to access these endpoints without the required role or with an API key will result in a 403 Forbidden error.
