# Ra Factory API Testing Plan

This document outlines a comprehensive testing plan for all Ra Factory API endpoints. Each endpoint will be tested to ensure correct functionality, proper error handling, and expected responses.

## Setup Requirements

1. [x] Development environment running via `docker compose --profile dev up -d`
2. [x] Test database accessible via `docker compose --profile test up -d db_test`
3. [x] Admin user created with credentials for testing
4. [x] Testing tools: curl, Postman, or similar HTTP client

> **Note:**
> - The test database (`db_test`) was started, connected successfully, and Alembic migrations were applied. The schema is initialized and ready for API/integration tests.

## Test Environment Information

- Base URL: `http://localhost:8000`
- Company GUID: `28fbeed6-5e09-4b75-ad74-ab1cdc4dec71`

### Test Users
All users below (except noted) have password: `password`

1. **SystemAdmin**
   - Email: `a.petrov@delice.bg`
   - GUID: `856d4637-cb16-4cf0-a535-efc02364096a`

2. **CompanyAdmin**
   - Email: `updated.admin@example.com`
   - GUID: `06a0c28e-1b6d-4aeb-a853-932c9d4e75a2`

3. **Operator**
   - Email: `operator.user@example.com`
   - GUID: `d92cd5b4-d760-43fd-a53e-cb0349d71d57`
   - PIN: `123456`

4. **ProjectManager**
   - Email: `project.manager@example.com`
   - GUID: `7a14ba5c-0289-4a9a-a402-ce5131cc2957`

5. **Integration**
   - Email: `integration.api@example.com`
   - GUID: `0295bd0f-d0e9-4aaf-a377-e8e310e23222`

### Database Access
- DB Credentials: `rafactory_rw` / `R4fDBP4ssw0rd9X`

## Testing Flow

The tests in this plan follow a logical dependency order:

1. Health checks to verify the API is running
2. Authentication with the SystemAdmin
3. Company management (creation and retrieval)
4. User management within those companies
5. Workstation management within those companies
6. Data synchronization (projects, components, etc.)

This approach follows the natural resource hierarchy in the system.

## 1. Health Check Endpoints

> **Test DB status:**
> - Test database is operational and schema is initialized. Ready for further API endpoint tests.

### 1.1 Root Health Check (`GET /health`)

- [x] **Test Steps:**
  1. Send GET request to `/health`
  2. Verify response status code is 200
  3. Verify response body is an empty JSON object or contains a status message

### 1.2 API v1 Health Check (`GET /api/v1/health`) 

- [x] **Test Steps:**
  1. Send GET request to `/api/v1/health`
  2. Verify response status code is 200
  3. Verify response body is an empty JSON object or contains a status message

## 2. Authentication Endpoints

### 2.1 Login (`POST /api/v1/auth/login`)

- [x] **Test with Valid Credentials:**
  1. Send POST request to `/api/v1/auth/login` with valid admin credentials
  2. Verify response contains `access_token`, `refresh_token`, `role`, and `expires_in`
  3. Store tokens for subsequent tests

- [x] **Test with Invalid Credentials:**
  1. Send POST request with incorrect password
  2. Verify response status code is 401
  3. Verify error message indicates authentication failure

### 2.2 Refresh Token (`POST /api/v1/auth/refresh`)

- [x] **Test with Valid Refresh Token:**
  1. Send POST request to `/api/v1/auth/refresh` with valid refresh token
  2. Verify response contains new `access_token`, `refresh_token`, `role`, and `expires_in`

- [x] **Test with Invalid Refresh Token:**
  1. Send POST request with invalid refresh token
  2. Verify response status code is 401
  3. Verify error message indicates invalid token

### 2.3 Get Current User Info (`GET /api/v1/auth/me`)

- [x] **Test with Valid Access Token:**
  1. Send GET request to `/api/v1/auth/me` with valid access token
  2. Verify response contains user GUID, email, role, and company GUID

- [x] **Test with Invalid Access Token:**
  1. Send GET request with invalid access token
  2. Verify response status code is 401

### 2.4 Protected Test Route (`GET /api/v1/auth/protected`)

- [x] **Test with SystemAdmin Role:**
  1. Login as a SystemAdmin user
  2. Send GET request to `/api/v1/auth/protected` with valid access token
  3. Verify response indicates access is granted

- [x] **Test with Non-SystemAdmin Role:**
  1. Login as a non-SystemAdmin user (e.g., CompanyAdmin)
  2. Send GET request to the protected endpoint
  3. Verify response indicates access is denied

## 3. Company Management Endpoints

- [x] **Test Create Company:**
  1. Login as SystemAdmin
  2. Send POST request to create a new company
  3. Verify response contains company details
  4. Verify company is added to the database

- [x] **Test Get Companies:**
  1. Login as SystemAdmin
  2. Send GET request to retrieve companies
  3. Verify response contains list of companies

- [x] **Test Update Company:**
  1. Login as SystemAdmin
  2. Send PUT request to update company details
  3. Verify response contains updated information
  4. Verify changes are reflected in the database

## 4. User Management Endpoints

### 4.1 Create User (`POST /api/v1/users`)

- [x] **Test with SystemAdmin Role:**
  1. Login as SystemAdmin
  2. Send POST request to `/api/v1/users` with valid user data
  3. Verify response contains user GUID and success message
  4. Verify the user exists in the database

- [x] **Test with Non-SystemAdmin Role:**
  1. Login as a non-SystemAdmin user
  2. Send POST request to create a user
  3. Verify access is denied with appropriate error message

### 4.2 Get Users (`GET /api/v1/users`)

- [x] **Test with SystemAdmin Role:**
  1. Login as SystemAdmin
  2. Send GET request to `/api/v1/users`
  3. Verify response contains list of users for the company

- [x] **Test with CompanyAdmin Role:**
  1. Login as CompanyAdmin
  2. Send GET request to `/api/v1/users`
  3. Verify response contains only users from the same company

### 4.3 Get User by GUID (`GET /api/v1/users/{guid}`)

- [x] **Test with Valid GUID and Proper Authorization:**
  1. Login as appropriate role
  2. Send GET request to `/api/v1/users/{guid}` with valid user GUID
  3. Verify response contains user details

- [x] **Test with Invalid GUID:**
  1. Send GET request with non-existent user GUID
  2. Verify appropriate 404 error response

### 4.4 Update User (`PUT /api/v1/users/{guid}`)

- [x] **Test Valid User Update:**
  1. Login as SystemAdmin
  2. Send PUT request to update user details
  3. Verify response indicates successful update
  4. Verify changes are reflected in the database

- [x] **Test User Role Update Restrictions:**
  1. Login as CompanyAdmin
  2. Attempt to update a user role to SystemAdmin
  3. Verify appropriate error response (forbidden as expected, tested 2025-04-28)

### 4.5 Delete User (`DELETE /api/v1/users/{guid}`)

- [x] **Test with SystemAdmin Role:**
  1. Login as SystemAdmin
  2. Send DELETE request to remove a user
  3. Verify success response
  4. Verify user is marked as inactive in the database (tested 2025-04-28)

- [x] **Test with Non-SystemAdmin Role:**
  1. Login as a regular user (CompanyAdmin)
  2. Attempt to delete a user
  3. Verify access is denied (CompanyAdmin cannot delete Integration users, bug fixed 2025-04-28)

## 5. Workstation Management Endpoints

### 5.1 Create Workstation (`POST /api/v1/workstations`)

- [x] **Test with Valid Workstation Data:**
  - Done – tested 2025-04-28, record created and verified in dev DB.
  1. Login as SystemAdmin or CompanyAdmin
  2. Send POST request with valid workstation data (types: Machine, Assembly, Control, Logistics, Supply)
  3. Verify response contains workstation GUID
  4. Verify workstation is added to the database

- [x] **Test with Invalid Workstation Data:**
  - Done – tested 2025-04-28, validation error returned as expected.
  1. Send POST request with missing required fields
  2. Verify appropriate validation error response

### 5.2 Get Workstations (`GET /api/v1/workstations`)

- [x] **Test Retrieval of Company Workstations:**
  1. Login as CompanyAdmin
  2. Send GET request to list workstations
  3. Verify response contains list of workstations for the company

- [x] **Test Filtering by Workstation Type:**
  1. Send GET request with type filter parameter (e.g., Machine, Assembly, Control)
  2. Verify response contains only workstations of specified type

### 5.3 Get Workstation by GUID (`GET /api/v1/workstations/{guid}`)

- [x] **Test with Valid GUID:**
  - Done – tested 2025-04-28, correct workstation returned.
  1. Send GET request with valid workstation GUID
  2. Verify response contains workstation details

- [x] **Test with Invalid GUID:**
  1. Send GET request with non-existent workstation GUID
  2. Verify appropriate 404 error response

### 5.4 Update Workstation (`PUT /api/v1/workstations/{guid}`)

- [✓] **Test Workstation Update:**
  1. Login as appropriate role
  2. Send PUT request to update workstation details
  3. Verify response indicates successful update
  4. Verify changes are reflected in the database

### 5.5 Delete Workstation (`DELETE /api/v1/workstations/{guid}`)

- [✓] **Test Workstation Deactivation:**
  1. Login as appropriate role
  2. Send DELETE request for a workstation
  3. Verify success response
  4. Verify workstation is marked as inactive in the database

## 6. Synchronization Endpoints

### 6.1 Sync Projects (`POST /api/v1/sync/projects`)

- [ ] **Test with Valid Project Data:**
  1. Prepare sample project data according to schema
  2. Send POST request to `/api/v1/sync/projects` with valid access token
  3. Verify response indicates successful insertion/update
  4. Verify data is correctly stored in the database

- [ ] **Test with Invalid Project Data:**
  1. Send POST request with malformed project data
  2. Verify appropriate error response

### 6.2 Sync Components (`POST /api/v1/sync/components`)

- [ ] **Test with Valid Component Data:**
  1. Prepare sample component data referencing existing projects
  2. Send POST request to `/api/v1/sync/components` with valid access token
  3. Verify response indicates successful insertion/update
  4. Verify data is correctly stored in the database

- [ ] **Test with Invalid Component Data:**
  1. Send POST request with malformed component data
  2. Verify appropriate error response

### 6.3 Sync Assemblies (`POST /api/v1/sync/assemblies`)

- [ ] **Test with Valid Assembly Data:**
  1. Prepare sample assembly data referencing existing projects and components
  2. Send POST request to `/api/v1/sync/assemblies` with valid access token
  3. Verify response indicates successful insertion/update
  4. Verify data is correctly stored in the database

- [ ] **Test with Invalid Assembly Data:**
  1. Send POST request with malformed assembly data
  2. Verify appropriate error response

### 6.4 Sync Pieces (`POST /api/v1/sync/pieces`)

- [ ] **Test with Valid Piece Data:**
  1. Prepare sample piece data referencing existing projects, components, and assemblies
  2. Send POST request to `/api/v1/sync/pieces` with valid access token
  3. Verify response indicates successful insertion/update
  4. Verify data is correctly stored in the database

- [ ] **Test Large Piece Batch:**
  1. Prepare a batch of 1000 pieces (maximum allowed)
  2. Verify system handles the large batch correctly

- [ ] **Test with Invalid Piece Data:**
  1. Send POST request with malformed piece data
  2. Verify appropriate error response

### 6.5 Sync Articles (`POST /api/v1/sync/articles`)

- [ ] **Test with Valid Article Data:**
  1. Prepare sample article data referencing existing projects and components
  2. Send POST request to `/api/v1/sync/articles` with valid access token
  3. Verify response indicates successful insertion/update
  4. Verify data is correctly stored in the database

- [ ] **Test with Invalid Article Data:**
  1. Send POST request with malformed article data
  2. Verify appropriate error response

## 7. QR Authentication

### 7.1 QR Login (`POST /api/v1/auth/qr`)

- [ ] **Test with Valid QR Credentials:**
  1. Retrieve a valid user GUID, workstation GUID, and PIN
  2. Send POST request to `/api/v1/auth/qr` with these credentials
  3. Verify response contains tokens and role information

- [ ] **Test with Invalid QR Credentials:**
  1. Send POST request with invalid user GUID
  2. Verify response status code indicates authentication failure

## 8. API Key Management

### 8.1 Create API Key (`POST /api/v1/api-keys`)

- [ ] **Test with CompanyAdmin Role:**
  1. Login as CompanyAdmin
  2. Send POST request to create a new API key
  3. Verify response contains API key details including the actual key
  4. Note that the key is only shown once

- [ ] **Test with Insufficient Permissions:**
  1. Login as a non-admin user
  2. Attempt to create an API key
  3. Verify access is denied

### 8.2 List API Keys (`GET /api/v1/api-keys`)

- [ ] **Test Retrieval of Company API Keys:**
  1. Login as CompanyAdmin
  2. Send GET request to list API keys
  3. Verify response contains list of API keys for the company

### 8.3 Get API Key by GUID (`GET /api/v1/api-keys/{guid}`)

- [ ] **Test with Valid GUID:**
  1. Send GET request with valid API key GUID
  2. Verify response contains API key details

- [ ] **Test with Invalid GUID:**
  1. Send GET request with non-existent API key GUID
  2. Verify appropriate 404 error response

### 8.4 Update API Key (`PUT /api/v1/api-keys/{guid}`)

- [ ] **Test API Key Update:**
  1. Login as CompanyAdmin
  2. Send PUT request to update API key details
  3. Verify response reflects changes
  4. Verify changes are stored in the database

### 8.5 Delete API Key (`DELETE /api/v1/api-keys/{guid}`)

- [ ] **Test API Key Deletion:**
  1. Login as CompanyAdmin
  2. Send DELETE request for an API key
  3. Verify success response (204 No Content)
  4. Verify API key is removed from the database

### 8.6 API Key Authentication

- [ ] **Test with X-API-Key Header:**
  1. Create an API key with appropriate scopes
  2. Send a request to a protected endpoint with the X-API-Key header
  3. Verify successful authentication

- [ ] **Test with Authorization: ApiKey Header:**
  1. Create an API key with appropriate scopes
  2. Send a request to a protected endpoint with the Authorization header
  3. Verify successful authentication

- [ ] **Test with Invalid API Key:**
  1. Send a request with an invalid API key
  2. Verify authentication fails with 401 status code

### 8.7 API Key Scope Validation

- [ ] **Test with Missing Required Scope:**
  1. Create an API key with limited scopes
  2. Attempt to access an endpoint requiring a scope not granted to this key
  3. Verify response indicates insufficient permissions (403 Forbidden)

- [ ] **Test with Valid Scope:**
  1. Create an API key with specific scopes
  2. Access an endpoint requiring one of those scopes
  3. Verify successful access

## 9. Mock Endpoints

### 9.1 Mock Auth (`POST /api/v1/mock-auth`)

- [ ] **Test Mock Authentication:**
  1. Send POST request to `/api/v1/mock-auth` with test credentials
  2. Verify response contains mock tokens
  3. Verify these tokens cannot be used for actual authenticated endpoints

## 10. Role-Based Access Control Tests

### 10.1 Role Hierarchy Tests

- [ ] **Test Role Creation Restrictions:**
  1. Login as CompanyAdmin
  2. Attempt to create a SystemAdmin user, verify it is denied
  3. Attempt to create another CompanyAdmin user, verify it is denied
  4. Successfully create a ProjectManager user
  5. Successfully create an Operator user

- [ ] **Test Role Modification Restrictions:**
  1. Login as ProjectManager
  2. Attempt to modify a CompanyAdmin user, verify it is denied
  3. Attempt to modify another ProjectManager user, verify it is denied
  4. Successfully view (but not modify) peer ProjectManager details

- [ ] **Test Role Elevation Prevention:**
  1. Login as CompanyAdmin
  2. Attempt to elevate a ProjectManager to CompanyAdmin, verify it is denied
  3. Login as ProjectManager
  4. Attempt to elevate an Operator to ProjectManager, verify it is denied

### 10.2 SystemAdmin Role Tests

- [ ] **Test Access to All Endpoints:**
  1. Login as SystemAdmin
  2. Verify access to all endpoints is granted
  3. Successfully create users of all role types
  4. Successfully modify users of all role types

### 10.3 CompanyAdmin Role Tests

- [x] **Test Company-Specific Access:**
  1. Login as CompanyAdmin
  2. Verify access is limited to company-specific data
  3. Attempt to access data from another company, verify access is denied
  4. Successfully manage ProjectManager and Operator users
  5. Verify inability to create/modify SystemAdmin or peer CompanyAdmin users
  6. Verify inability to delete Integration users (security confirmed, tested 2025-04-28)

### 10.4 ProjectManager Role Tests

- [ ] **Test Project Management Access:**
  1. Login as ProjectManager
  2. Verify appropriate read/write permissions for project data
  3. Attempt administrative actions, verify they are denied
  4. Verify inability to create/modify any user roles
  5. Verify read-only access to peer ProjectManager information

### 10.5 Operator Role Tests

- [ ] **Test Operator-Specific Access:**
  1. Login as Operator using QR authentication
  2. Verify access is limited to workstation-specific operations
  3. Attempt administrative actions, verify they are denied
  4. Verify inability to access user management endpoints
  5. Verify inability to access project management endpoints

### 10.6 Integration Role Tests

- [ ] **Test Integration API Access:**
  1. Use Integration role credentials
  2. Verify appropriate access for automated tasks
  3. Verify limitations on other system operations
  4. Verify inability to access user management endpoints
  5. Verify data synchronization capabilities

## 11. Database Validation Tests

- [ ] **Verify Row-Level Security:**
  1. Create test users for different companies
  2. Verify users can only access their company's data

- [ ] **Verify Foreign Key Constraints:**
  1. Attempt to sync data with invalid foreign key references
  2. Verify appropriate error handling

- [ ] **Verify Data Integrity:**
  1. After sync operations, query the database directly
  2. Verify all data relationships are maintained correctly

## 12. Error Handling Tests

- [ ] **Test Invalid JSON Payloads:**
  1. Send malformed JSON to various endpoints
  2. Verify appropriate error responses

- [ ] **Test Rate Limiting:**
  1. Send multiple rapid requests to authentication endpoints
  2. Verify rate limiting behavior if implemented

- [ ] **Test Invalid Token Handling:**
  1. Send expired, malformed, or tampered tokens to authenticated endpoints
  2. Verify appropriate security responses

## 13. Documentation Validation

- [ ] **Validate API Documentation:**
  1. Access the root endpoint (`/`)
  2. Verify it redirects to OpenAPI documentation
  3. Verify all endpoints are properly documented

## 14. Security Testing

### 14.1 Authentication Security

- [ ] **JWT Token Security:**
  1. Extract and inspect JWT token structure
  2. Verify token expiration is enforced
  3. Test token refresh behavior when approaching expiration

- [ ] **Password Security:**
  1. Test password change functionality if available
  2. Verify password hashing is implemented correctly
  3. Attempt login with old passwords after change

### 14.2 Authorization Boundaries

- [ ] **Cross-Company Access Prevention:**
  1. Login as user from Company A
  2. Attempt to access/modify resources from Company B
  3. Verify proper isolation between companies

- [ ] **Vertical Privilege Escalation:**
  1. Login as lower-privilege user
  2. Modify request headers or payloads to attempt accessing admin functions
  3. Verify proper role enforcement

### 14.3 Input Validation and Sanitization

- [ ] **SQL Injection Prevention:**
  1. Test endpoints with SQL injection patterns in inputs
  2. Verify proper parameterization and error handling

- [ ] **XSS Prevention:**
  1. Input script tags and other XSS vectors in string fields
  2. Verify proper encoding/escaping of outputs

## 15. Performance Testing

- [ ] **Response Time Baseline:**
  1. Measure response times for key endpoints under normal load
  2. Document baseline for future comparison

- [ ] **Bulk Data Handling:**
  1. Test sync endpoints with increasingly large payloads
  2. Identify maximum practical payload size before performance degradation

- [ ] **Concurrent Request Handling:**
  1. Simulate multiple users accessing the API simultaneously
  2. Verify system stability and response times under load

## 16. Test Automation Framework

### 16.1 Setting Up Automated Tests

- [ ] **Create Test Structure:**
  1. Set up test directory structure in `src/ractory/backend/tests/api`
  2. Organize tests by endpoint categories

- [ ] **Environment Configuration:**
  1. Create test environment configuration
  2. Set up test database fixture creation and teardown

### 16.2 Implementation with pytest

```python
# Example test structure for authentication endpoints
def test_login_valid_credentials(client):
    response = client.post("/api/v1/auth/login", json={
        "email": "test@example.com", 
        "password": "password"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

def test_login_invalid_credentials(client):
    response = client.post("/api/v1/auth/login", json={
        "email": "test@example.com", 
        "password": "wrong_password"
    })
    assert response.status_code == 401
```

## 17. Testing Environment Management

### 17.1 Database State Management

- [ ] **Setup Test Data:**
  1. Create script to populate test database with minimal test data
  2. Include sample users with different role types
  3. Include sample projects, components, assemblies, and pieces

- [ ] **Database Reset:**
  1. Create procedure to reset database to known state between tests
  2. Ensure isolation between test runs

### 17.2 Testing Across Environments

- [ ] **Development Testing:**
  1. Run tests against development database (port 5434)
  2. Focus on feature validation and integration

- [ ] **Production-Like Testing:**
  1. Configure tests to run against production-like environment
  2. Test with production database schema but isolated data

## 18. Test Progress Tracking

### 18.1 Endpoint Coverage Checklist

| Endpoint | Basic Functionality | Error Handling | Auth/Roles | Notes |
|----------|---------------------|----------------|------------|-------|
| GET /health | ✓ | □ | N/A | |
| GET /api/v1/health | ✓ | □ | N/A | |
| POST /api/v1/auth/login | ✓ | □ | N/A | |
| POST /api/v1/auth/refresh | ✓ | □ | N/A | |
| POST /api/v1/auth/qr | □ | □ | N/A | |
| GET /api/v1/auth/me | ✓ | □ | ✓ | |
| GET /api/v1/auth/protected | ✓ | □ | ✓ | |
| POST /api/v1/sync/projects | □ | □ | □ | Internal Server Error |
| POST /api/v1/sync/components | □ | □ | □ | |
| POST /api/v1/sync/assemblies | □ | □ | □ | |
| POST /api/v1/sync/pieces | □ | □ | □ | |
| POST /api/v1/sync/articles | □ | □ | □ | |
| POST /api/v1/mock-auth | □ | □ | N/A | |
| POST /api/v1/users | □ | □ | □ | New endpoint |
| GET /api/v1/users | □ | □ | □ | New endpoint |
| GET /api/v1/users/{guid} | □ | □ | □ | New endpoint |
| PUT /api/v1/users/{guid} | □ | □ | □ | New endpoint |
| DELETE /api/v1/users/{guid} | □ | □ | □ | New endpoint |
| POST /api/v1/workstations | □ | □ | □ | New endpoint |
| GET /api/v1/workstations | □ | □ | □ | New endpoint |
| GET /api/v1/workstations/{guid} | ✓ | □ | □ | New endpoint |
| PUT /api/v1/workstations/{guid} | ✓ | □ | □ | New endpoint |
| DELETE /api/v1/workstations/{guid} | ✓ | □ | □ | New endpoint |
| POST /api/v1/api-keys | □ | □ | □ | New endpoint |
| GET /api/v1/api-keys | □ | □ | □ | New endpoint |
| GET /api/v1/api-keys/{guid} | □ | □ | □ | New endpoint |
| PUT /api/v1/api-keys/{guid} | □ | □ | □ | New endpoint |
| DELETE /api/v1/api-keys/{guid} | □ | □ | □ | New endpoint |

### 17.2 Issue Tracking

| Issue ID | Endpoint | Description | Status | Resolution |
|----------|----------|-------------|--------|------------|
| 1 | POST /api/v1/sync/projects | Internal Server Error when sending valid project data | Open | |

## 19. API Client Configuration

### 19.1 Postman Collection

- [ ] **Create Postman Collection:**
  1. Set up environment variables for base URL and tokens
  2. Create request templates for all endpoints
  3. Include test scripts for automated validation

### 19.2 Curl Command Reference

- [ ] **Create Curl Command Document:**
  1. Document curl commands for all API operations
  2. Include examples with different roles and scenarios

## 20. Regression Testing Plan

- [ ] **Identify Critical Paths:**
  1. Document the most critical API workflows
  2. Create automated tests that cover these paths

- [ ] **Periodic Testing Schedule:**
  1. Establish schedule for running regression tests
  2. Define triggers for mandatory regression testing (e.g., database schema changes)

## 21. Test Results and Reporting

- [ ] **Create Test Report Template:**
  1. Include coverage statistics
  2. Document any discovered issues
  3. Track performance metrics

- [ ] **Automated Test Reports:**
  1. Configure pytest to generate HTML or XML reports
  2. Set up notification system for test failures

## Test Execution Command Templates

```bash
# Health check
curl http://localhost:8000/health | cat

# Login
curl -X POST -H "Content-Type: application/json" \
     -d '{"email": "a.petrov@delice.bg", "password": "password"}' \
     http://localhost:8000/api/v1/auth/login | cat

# Use token in subsequent requests
curl -X GET -H "Authorization: Bearer <token>" \
     http://localhost:8000/api/v1/auth/me | cat

# Sync projects example
curl -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer <token>" \
     -d '{"projects": [{"code": "P001", "creation_date": "2023-01-01T00:00:00Z", "id": 1}]}' \
     http://localhost:8000/api/v1/sync/projects | cat
```

## Database Verification Queries

```sql
-- Verify projects were synced
SELECT * FROM projects ORDER BY created_at DESC LIMIT 5;

-- Verify components were synced with correct project references
SELECT c.*, p.code as project_code 
FROM components c 
JOIN projects p ON c.id_project = p.id 
ORDER BY c.created_at DESC LIMIT 5;

-- Verify user authentication
SELECT guid, email, role FROM users WHERE email = 'a.petrov@delice.bg';
```

## Conclusion

This comprehensive testing plan provides a structured approach to validating the Ra Factory API. As tests are executed, mark them as completed in this document and record any issues encountered. Regular testing using this plan will help maintain API reliability and prevent regressions during development.

Remember to update the test plan when new endpoints are added or existing ones are modified. The goal is to maintain 100% test coverage of all API functionality.

<!-- Traceability: Last updated after RBAC bug fix for Integration user deletion, 2025-04-28 --> 