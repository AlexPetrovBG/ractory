# Multi-Tenant Security Implementation

## Overview

This document describes the multi-tenant security implementation in the Ra Factory API, focusing on data isolation between companies to ensure secure access.

## Security Model

The Ra Factory API employs a multi-layered security approach for tenant isolation:

1. **PostgreSQL Row-Level Security (RLS)**: Database-level security policies
2. **Application-level Filtering**: Additional tenant filter applied to all queries
3. **Request Validation**: Explicit validation of cross-tenant access attempts
4. **Middleware-based Monitoring**: Safety checks to ensure tenant context is properly set

## Implemented Fixes

The following fixes have been implemented to address potential security vulnerabilities:

### 1. Enhanced Tenant Context Management

Created a new utility module (`app/core/tenant_utils.py`) with robust tenant context management:

- `set_tenant_context()`: Properly sets PostgreSQL session variables for RLS
- `get_tenant_context()`: Retrieves current tenant context for diagnostics
- `verify_tenant_access()`: Validates company GUID matches for cross-tenant access attempts
- `add_tenant_filter()`: Adds explicit tenant filtering to all queries as a defense-in-depth measure

### 2. Middleware & Event Listeners

Added middleware and event listeners for monitoring and enforcing tenant isolation:

- `TenantIsolationMiddleware`: Request/response middleware for diagnostics
- `register_tenant_isolation_listeners()`: SQLAlchemy event listeners that intercept queries to ensure tenant context is set

### 3. Explicit Route Handler Enhancements

Updated all API route handlers with explicit company filtering:

- Added `add_tenant_filter()` to all query builders
- Added explicit tenant validation in sync endpoints
- Ensured proper error responses for unauthorized cross-tenant access

### 4. Test Scripts

Created comprehensive test scripts to verify tenant isolation:

- `app/tests/test_multi_tenant_isolation.py`: Comprehensive test suite for all endpoints
- `isolation_test.py`: Quick validation script for key endpoints

## Security Design Principles

Our multi-tenant security model follows these core principles:

1. **Defense in Depth**: Multiple layers of security ensuring no single point of failure
2. **Least Privilege**: Users can only access their own company's data
3. **Explicit Over Implicit**: All security checks are explicitly implemented, not implied
4. **Fail Secure**: Any failure in the security chain defaults to denying access
5. **Auditability**: Security-relevant operations are logged for auditing

## Row-Level Security Implementation

PostgreSQL Row-Level Security provides the foundation of our multi-tenant isolation:

```sql
CREATE POLICY tenant_isolation ON table_name
USING (company_guid = current_setting('app.tenant')::uuid OR 
       current_setting('app.bypass_rls', true) = 'true');
```

These policies are created for all tables during application startup.

## Session Variables

Two critical PostgreSQL session variables control tenant isolation:

1. `app.tenant`: Set to the authenticated user's company GUID
2. `app.bypass_rls`: Set to 'true' only for SystemAdmin role

The updated `get_tenant_session()` dependency correctly sets these variables for each request.

## Testing Tenant Isolation

### Running the Validation Script

```bash
cd /home/alex/src/ractory/backend
python isolation_test.py
```

This script:
1. Authenticates as both SystemAdmin and company admins
2. Tests JWT-based authentication isolation
3. Tests API key-based authentication isolation
4. Tests sync endpoint isolation

### Running the Comprehensive Test Suite

```bash
cd /home/alex/src/ractory/backend
python -m app.tests.test_multi_tenant_isolation
```

## Potential Future Enhancements

1. **Enhanced Logging**: Add detailed security event logging
2. **Automated Testing**: Add tenant isolation tests to CI/CD pipeline
3. **Metrics Tracking**: Add metrics for security-relevant operations
4. **Real-time Alerts**: Alert on suspicious cross-tenant access attempts 