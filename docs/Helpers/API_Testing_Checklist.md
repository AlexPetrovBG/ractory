## Detailed Test Execution Checklist

### 1. Environment Setup Tests
[X] Development environment started successfully
[X] Database connection verified
[X] Initial SystemAdmin token obtained

### 2. Health Check Tests
[X] Root health endpoint returns 200
[X] Root health endpoint contains status message
[X] Root health endpoint contains version
[X] API v1 health endpoint returns 200
[X] API v1 health endpoint contains status message
[X] API v1 health endpoint contains version

### 3. Authentication Tests
#### 3.1 JWT Authentication - Login
[X] Valid SystemAdmin credentials return 200
[X] Valid SystemAdmin response contains access_token
[X] Valid SystemAdmin response contains refresh_token
[X] Valid SystemAdmin response contains correct role
[X] Invalid credentials return 401
[X] Invalid credentials contain proper error message
[X] Non-existent user returns 401
[X] Empty credentials return 422

#### 3.2 JWT Authentication - Token Refresh
[X] Valid refresh token returns 200
[X] Valid refresh provides new access_token
[X] Valid refresh provides new refresh_token
[X] Invalid refresh token format returns 401
[X] Empty refresh token returns 422

#### 3.3 Current User Info
[X] Valid token returns user info
[X] User info contains correct GUID
[X] User info contains correct email
[X] User info contains correct role
[X] User info contains correct company_guid
[X] Invalid token returns 401

### 4. Company Management Tests
#### 4.1 Company Creation
[X] Create Company A with SystemAdmin
[X] Create Company B with SystemAdmin
[X] Verify Company A GUID stored
[X] Verify Company B GUID stored


#### 4.2 Company Index Tests
[X] Set valid company index (0-99)
[X] Verify index uniqueness across companies
[X] Attempt to set invalid index (negative) returns 422
[X] Attempt to set invalid index (>99) returns 422
[X] Attempt to set duplicate index returns 409 (Fixed: Now returns proper 409 status code)
[X] Update existing index successfully
[X] Verify index constraints in multi-company operations

### 5. User Management Tests

#### 5.1 Company A User Creation
[X] Create CompanyAdmin 1
[X] Create CompanyAdmin 2
[X] Create ProjectManager 1
[X] Create ProjectManager 2
[X] Create Operator 1
[X] Create Operator 2
[X] Verify all users created successfully

#### 5.2 Company B User Creation
[X] Create CompanyAdmin 1
[X] Create CompanyAdmin 2
[X] Create ProjectManager 1
[X] Create ProjectManager 2
[X] Create Operator 1
[X] Create Operator 2
[X] Verify all users created successfully

#### 5.3 User Management Permissions
[X] CompanyAdmin can't create SystemAdmin
[X] CompanyAdmin can't create peer CompanyAdmin
[X] ProjectManager can't create any users
[X] Operator can't create any users
[X] CompanyAdmin can view own company users
[X] CompanyAdmin can't view other company users

#### 5.4 Extended User Fields Tests
[X] Create user with name and surname
[X] Create user with picture_path
[X] Update user name
[X] Update user surname
[X] Update user picture_path
[X] Verify extended fields in user info response
[X] Test empty/null field handling
[X] Test field validation rules
[X] Test field length limits
[X] Test picture_path format validation

#### 5.5 User Listing
[X] SystemAdmin can view all users
[X] SystemAdmin can filter users by company
[X] CompanyAdmin can view own company users
[X] CompanyAdmin cannot view other company users
[X] Cross-company access returns 403
[X] Role filtering works correctly
[X] Active status filtering works correctly

### 6. Workstation Management Tests
[X] Create Assembly workstation
[X] Create Logistics workstation
[X] Invalid workstation type returns 422
[X] Invalid company GUID returns 404
[X] Verify workstation GUIDs stored (Note: Individual workstation access works, but listing endpoint returns empty array - potential API issue)

### 7. QR Authentication Tests
[X] Valid QR code data returns 200
[X] Valid QR response contains tokens
[X] Valid QR response contains Operator role
[X] Invalid workstation GUID returns 400
[X] Invalid user GUID returns 401
[X] Invalid PIN returns 401
[X] Non-operator user returns 401

### 8. API Key Management Tests
#### 8.1 Company A API Keys
[X] Create API key with sync scopes
[X] Store API key securely
[X] Verify API key works for sync endpoints
[X] Invalid scope returns 422
[X] Duplicate key returns 400

#### 8.2 Company B API Keys
[X] Create API key with sync scopes
[X] Store API key securely
[X] Verify API key works for sync endpoints
[X] Cross-company access returns 403 (Note: API correctly returns 403 Forbidden with proper error message)

### 9. Data Synchronization Tests
#### 9.1 Project Sync Tests
[X] Auto-generated GUID project creation for Company A
[X] Provided GUID project creation for Company A
[X] Create at least 3 projects for Company A (name them Project_A1, Project_A2, Project_A3)
[X] Auto-generated GUID project creation for Company B
[X] Provided GUID project creation for Company B
[X] Create at least 3 projects for Company B (name them Project_B1, Project_B2, Project_B3)
[X] Verify all projects are correctly stored with appropriate GUIDs
[X] Invalid GUID format returns 422
[X] Cross-company GUID returns 403
[X] Bulk project sync with mixed GUIDs
[X] Store all Project GUIDs for use in subsequent tests

#### 9.2 Component Sync Tests
[X] Auto-generated GUID component creation for Company A Project_A1
[X] Create at least 2 components for each Company A project
[X] Provided GUID component creation for Company A Project_A2
[X] Auto-generated GUID component creation for Company B Project_B1
[X] Create at least 2 components for each Company B project
[X] Provided GUID component creation for Company B Project_B2
[X] Test component creation with all types of references
[X] Invalid project reference returns 400
[X] Component GUIDs stored correctly
[X] Cross-company project reference returns 403
[X] Invalid component data returns 422
[X] Store all Component GUIDs for use in subsequent tests

#### 9.3 Assembly Sync Tests
[X] Auto-generated GUID assembly creation for Company A components
[X] Create at least 1 assembly for each Company A component
[X] Provided GUID assembly creation for Company A components 
[X] Auto-generated GUID assembly creation for Company B components
[X] Create at least 1 assembly for each Company B component
[X] Provided GUID assembly creation for Company B components
[X] Mismatched project/component returns 400
[X] Assembly GUIDs stored correctly
[X] Invalid assembly data returns 422
[X] Cross-company references return 403
[X] Store all Assembly GUIDs for use in subsequent tests

#### 9.4 Piece Sync Tests
[X] Auto-generated GUID piece with assembly for Company A
[X] Create at least 3 pieces with assembly for Company A
[X] Auto-generated GUID piece without assembly for Company A
[X] Create at least 3 pieces without assembly for Company A
[X] Provided GUID piece with assembly for Company A
[X] Provided GUID piece without assembly for Company A
[X] Auto-generated GUID piece with assembly for Company B
[X] Create at least 3 pieces with assembly for Company B
[X] Auto-generated GUID piece without assembly for Company B
[X] Create at least 3 pieces without assembly for Company B
[X] Provided GUID piece with assembly for Company B
[X] Provided GUID piece without assembly for Company B
[X] Bulk sync within 1000 limit
[X] Bulk sync exceeding 1000 returns 400
[X] Invalid piece data returns 422
[X] Cross-company references return 403
[X] Store all Piece GUIDs for use in subsequent tests


#### 9.5 Article Sync Tests
[X] Auto-generated GUID article creation for Company A
[X] Create at least a few articles per Company A project
[X] Provided GUID article creation for Company A
[X] Auto-generated GUID article creation for Company B
[X] Create at least a few articles per Company B project
[X] Provided GUID article creation for Company B
[X] Invalid article data returns 422
[X] Article GUIDs stored correctly
[X] Cross-company references return 403
[X] Store all Article GUIDs for use in subsequent tests

#### 9.6 Cross-Entity Validation Tests
[X] Circular reference detection
[X] Cross-company reference prevention
[X] Duplicate GUID prevention
[X] Non-existent entity updates return 404
[X] Missing required references return 400


### 10. Cross-Tenant Isolation Tests
#### 10.1 Data Access Tests
[X] Company A users can list all Company A projects
[X] Company A users can list all Company A components
[X] Company A users can list all Company A assemblies
[X] Company A users can list all Company A pieces
[X] Company A users can list all Company A articles
[X] Company A users can search/filter Company A projects
[X] Company A users can search/filter Company A components
[X] Company A users can search/filter Company A pieces

[X] Company A can't read Company B projects
[X] Company A can't read Company B components
[X] Company A can't read Company B assemblies
[X] Company A can't read Company B pieces
[X] Company A can't read Company B articles
[X] Company A can't read Company B workstations
[X] Company A can't read Company B users

[X] Company B users can list all Company B projects
[X] Company B users can list all Company B components
[X] Company B users can list all Company B assemblies
[X] Company B users can list all Company B pieces
[X] Company B users can list all Company B articles
[X] Company B users can search/filter Company B projects 
[X] Company B users can search/filter Company B components
[X] Company B users can search/filter Company B pieces

[X] Company B can't read Company A projects
[X] Company B can't read Company A components
[X] Company B can't read Company A assemblies
[X] Company B can't read Company A pieces
[X] Company B can't read Company A articles
[X] Company B can't read Company A workstations
[X] Company B can't read Company A users

#### 10.2 Data Modification Tests
[X] Company A can update Company A projects
[X] Company A can update Company A components
[X] Company A can update Company A assemblies
[X] Company A can update Company A pieces
[X] Company A can update Company A articles

[X] Company A can't modify Company B projects
[X] Company A can't modify Company B components
[X] Company A can't modify Company B assemblies
[X] Company A can't modify Company B pieces
[X] Company A can't modify Company B articles
[X] Company A can't modify Company B workstations
[X] Company A can't modify Company B users

[X] Company B can update Company B projects
[X] Company B can update Company B components
[X] X Company B can update Company B assemblies
[X] Company B can update Company B pieces
[X] Company B can update Company B articles

[X] Company B can't modify Company A projects
[X] Company B can't modify Company A components
[X] Company B can't modify Company A assemblies
[X] Company B can't modify Company A pieces
[X] Company B can't modify Company A articles
[X] Company B can't modify Company A workstations
[X] Company B can't modify Company A users

[ ] Non-SystemAdmin company creation returns 403
[ ] Invalid company data returns 422

#### 10.3 Data Deletion Tests
[ ] Company A can delete Company A projects
[ ] Company A can delete Company A components
[ ] Company A can delete Company A assemblies
[ ] Company A can delete Company A pieces
[ ] Company A can delete Company A articles

[ ] Company A can't delete Company B projects
[ ] Company A can't delete Company B components
[ ] Company A can't delete Company B assemblies
[ ] Company A can't delete Company B pieces
[ ] Company A can't delete Company B articles
[ ] Company A can't delete Company B workstations
[ ] Company A can't delete Company B users

[ ] Company B can delete Company B projects
[ ] Company B can delete Company B components
[ ] Company B can delete Company B assemblies
[ ] Company B can delete Company B pieces
[ ] Company B can delete Company B articles

[ ] Company B can't delete Company A projects
[ ] Company B can't delete Company A components
[ ] Company B can't delete Company A assemblies
[ ] Company B can't delete Company A pieces
[ ] Company B can't delete Company A articles
[ ] Company B can't delete Company A workstations
[ ] Company B can't delete Company A users

#### 10.4 Cascading Operations Tests
[ ] Deletion of Company A project cascades to its components
[ ] Deletion of Company A component cascades to its assemblies, pieces, and articles
[ ] Deletion of Company A assembly cascades to associated pieces
[ ] Verify cascade operations don't affect Company B data
[ ] Verify cascade operations don't cross company boundaries

#### 10.5 System Admin Override Tests
[ ] SystemAdmin can read all companies' data
[ ] SystemAdmin can modify all companies' data
[ ] SystemAdmin can delete data from all companies
[ ] Verify proper audit trail when SystemAdmin performs cross-company operations

### 11. Multi-Tenant Isolation Security Tests
#### 11.1 JWT Authentication Isolation
[X] Company A user can access own projects
[X] Company A user cannot access Company B projects (returns 403)
[X] Company B user can access own projects
[X] Company B user cannot access Company A projects (returns 403)
[X] Company A user cannot list other company entities with explicit company_guid query parameter
[X] Verify isolation for all entity types (projects, components, assemblies, pieces, articles, workstations, users)

#### 11.2 API Key Authentication Isolation
[X] Company A API key can access own data
[X] Company A API key cannot access Company B data (returns 403)
[X] Company B API key can access own data
[X] Company B API key cannot access Company A data (returns 403)
[X] Verify API key isolation for all entity types

#### 11.3 Sync Endpoint Isolation
[X] Company A API key cannot sync Company B projects (returns 403)
[X] Company B API key cannot sync Company A projects (returns 403)
[X] Explicit company_guid validation works correctly
[X] Verify isolation for all sync endpoints (projects, components, assemblies, pieces, articles)

#### 11.4 Automated Isolation Tests
[X] Install required dependencies (aiohttp)
[X] Run isolation_test.py script with proper virtual environment activation
[X] Run test_multi_tenant_isolation.py comprehensive test
[X] Document test results including pass/fail statistics
[X] Identify and categorize isolation issues by severity
[X] Distinguish between missing endpoints (404) and true isolation failures (200)
[X] Create report using standard format from testing guide

### 12. Error Handling Tests
#### 12.1 Input Validation
[X] Invalid JSON returns 400
[X] Missing required fields returns 422
[X] Invalid data types returns 422
[X] Empty request body returns 422

#### 12.2 Authentication Errors
[X] Expired token returns 401
[X] Invalid token format returns 401
[X] Missing token returns 401
[X] Invalid API key returns 401

#### 12.3 Authorization Errors
[X] Insufficient permissions returns 403
[X] Cross-company access returns 403
[X] Invalid scope returns 403

### 13. Workflow Tests
#### 13.1 Workflow Entry Creation
[ ] Create workflow entry with all fields (Implemented and working)
[ ] Create entry with minimum required fields (Implemented and working)
[ ] Verify automatic timestamp creation (Implemented and working - created_at is auto-populated)
[ ] Test all valid action types (Implemented and working)
[ ] Invalid action type returns 422 with valid types list (Implemented and working)
[ ] Verify company name population (Implemented and working - company name is auto-populated)
[ ] Verify user name population (Implemented and working - user name is derived from email or name/surname fields)
[ ] Verify workstation name population (Implemented and working)

#### 13.2 Workflow Querying
[ ] Filter by action type (Implemented and working)
[ ] Filter by date range (Implemented and working)
[ ] Filter by company (Implemented and working - company filtering is automatic based on user's token)
[ ] Filter by workstation (Implemented and working)
[ ] Filter by user (Implemented and working)
[ ] Verify proper ordering (Implemented and working - order by created_at desc)
[ ] Test pagination (Implemented and working - with limit and offset parameters)
[ ] Test result limits (Implemented and working - default limit is 100, max is 1000)

#### 13.3 Workflow Security
[ ] Verify company isolation (Implemented and working - enforced by RLS and double-checked in API)
[ ] Test user association validation (Implemented and working)
[ ] Test workstation association validation (Implemented and working)
[ ] Test API key association validation (Implemented and working)
[ ] Verify proper error responses (Implemented and working)
[ ] Test permission requirements (Implemented and working - minimum role is ProjectManager)

### 14. Performance Tests
[ ] Bulk sync response time within limits
[ ] Database performance acceptable
[ ] Memory usage within limits
[ ] Rate limiting functioning correctly

### Test Results Documentation
[ ] All test results documented
[ ] Issues categorized by severity
[ ] Steps to reproduce documented
[ ] Expected vs actual results documented
[ ] Performance metrics recorded

### Post-Testing Tasks
[ ] Test data cleaned up
[ ] Test users deactivated
[ ] Test API keys revoked
[ ] Test results reported
[ ] Issues logged in tracking system


## Entity Hierarchy Summary for Testing

For comprehensive testing, the following entity hierarchy should be created for each company:

1. **Company**
   - Company A
   - Company B

2. **Projects** (at least 3 per company)
   - Company A: Project_A1, Project_A2, Project_A3
   - Company B: Project_B1, Project_B2, Project_B3

3. **Components** (at least 2 per project)
   - Company A: At least 6 components (2+ per project)
   - Company B: At least 6 components (2+ per project)

4. **Assemblies** (at least 1 per component)
   - Company A: At least 6 assemblies (1+ per component)
   - Company B: At least 6 assemblies (1+ per component)

5. **Pieces** (with and without assembly references)
   - Company A: At least 12 pieces (some with assembly, some without)
   - Company B: At least 12 pieces (some with assembly, some without)

6. **Articles** (several per project)
   - Company A: At least 6 articles (2+ per project)
   - Company B: At least 6 articles (2+ per project)

This structure ensures comprehensive testing of all entity types, their relationships, and cross-company isolation. 

**Note:** All update operations in the Ra Factory API are performed through the sync endpoints (`/api/v1/sync/*`), not through traditional PUT/PATCH endpoints. To update an entity, send a POST request to the appropriate sync endpoint with the entity GUID included. 

[X] Company A can't modify Company B pieces
[X] Company A can't modify Company B articles
[X] Company A can't modify Company B workstations
[X] Company A can't modify Company B users
[X] Company B can't modify Company A assemblies

### 11. Soft Delete, Cascade, Restore, and Reactivation Tests

#### 11.1 Soft Delete via REST Endpoint
[X] DELETE /api/v1/projects/{guid} soft deletes project and cascades to children
[X] DELETE /api/v1/components/{guid} soft deletes component and cascades to children
[X] DELETE /api/v1/assemblies/{guid} soft deletes assembly and cascades to children
[X] DELETE /api/v1/pieces/{guid} soft deletes piece
[X] DELETE /api/v1/articles/{guid} soft deletes article

#### 11.2 Soft Delete via Sync Endpoint
[X] Sync endpoint soft deletes children not present in payload (with new deleted_at)
[X] Sync endpoint reactivates soft-deleted entity if provided in payload

#### 11.3 Cascade Soft Delete
[X] Soft deleting a parent cascades to all active children recursively (same deleted_at)
[X] All cascaded entities have the same deleted_at timestamp

#### 11.4 Selective Restore
[X] POST /api/v1/{entity}/{guid}/restore restores entity and only children with matching deleted_at
[X] Restored entities have is_active = TRUE and deleted_at = NULL
[X] Other soft-deleted children remain inactive

#### 11.5 Reactivation via Sync
[X] Syncing a soft-deleted entity with updated data reactivates and updates it
[X] Reactivated entity has is_active = TRUE and deleted_at = NULL

#### 11.6 GET with/without Inactive
[X] GET endpoints return only active entities by default
[X] GET endpoints return soft-deleted entities when ?include_inactive=true is used

#### 11.7 Edge Cases
[X] Multiple generations of soft-deleted children (deep cascade)
[X] Partial soft delete and selective restoration
[X] Sync reactivation edge cases

> All above tested and verified in `src/ractory/backend/test_edge_cases.py` and related integration/unit tests. 