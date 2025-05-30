# Ra Factory API Testing Guide v3

## Environment Setup

### Development Environment Information

**Base URL:** `http://localhost:8000`
**Default Company GUID:** `28fbeed6-5e09-4b75-ad74-ab1cdc4dec71`

### Database Connection Details
```bash
Host: localhost
Port: 5434 (Development)
Database: rafactory_dev
User: rafactory_rw
Password: R4fDBP4ssw0rd9X
```

### Test Users
System admin user below have password: `password`

**SystemAdmin**
   - Email: `a.petrov@delice.bg`
   - GUID: `856d4637-cb16-4cf0-a535-efc02364096a`
   
### Initial Setup Steps

1. Start the development environment:
```bash
cd src/ractory
docker compose --profile dev up -d
```

2. Verify services are running:
```bash
docker compose ps
```

3. Get initial SystemAdmin token:
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"email": "a.petrov@delice.bg", "password": "password"}' \
     http://localhost:8000/api/v1/auth/login | jq '.'
```

## Test Sequence Overview

The tests should be executed in the following order to ensure proper dependency handling:

1. Health Check Tests
2. Authentication Tests
3. Company Management Tests
4. User Management Tests
5. Workstation Management Tests
6. API Key Management Tests
7. Data Synchronization Tests
8. Multi-Tenant Isolation Tests
9. Error Handling Tests
10. Soft Delete, Cascade, Restore, and Reactivation Tests

## 1. Health Check Tests

### 1.1 Root Health Check
```bash
# Test root health endpoint
curl http://localhost:8000/health | jq '.'

Expected response:
- Status code: 200
- Response contains status message and version
```

### 1.2 API v1 Health Check
```bash
# Test API v1 health endpoint
curl http://localhost:8000/api/v1/health | jq '.'

Expected response:
- Status code: 200
- Response contains status message and version
```

## 2. Authentication Tests

### 2.1 JWT Authentication

#### 2.1.1 Login Tests
```bash
# Test valid credentials (SystemAdmin)
curl -X POST -H "Content-Type: application/json" \
     -d '{"email": "a.petrov@delice.bg", "password": "password"}' \
     http://localhost:8000/api/v1/auth/login | jq '.'

Expected response:
- Status code: 200
- Contains: access_token, refresh_token, role, expires_in
- Role should be "SystemAdmin"

# Test invalid credentials
curl -X POST -H "Content-Type: application/json" \
     -d '{"email": "a.petrov@delice.bg", "password": "wrong_password"}' \
     http://localhost:8000/api/v1/auth/login | jq '.'

Expected response:
- Status code: 401
- Error message indicating authentication failure
```

#### 2.1.2 Token Refresh Tests
```bash
# First get valid tokens
TOKEN_RESPONSE=$(curl -X POST -H "Content-Type: application/json" \
     -d '{"email": "a.petrov@delice.bg", "password": "password"}' \
     http://localhost:8000/api/v1/auth/login | jq -r '.')

REFRESH_TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.refresh_token')

# Test refresh with valid token
curl -X POST -H "Content-Type: application/json" \
     -d "{\"refresh_token\": \"$REFRESH_TOKEN\"}" \
     http://localhost:8000/api/v1/auth/refresh | jq '.'

Expected response:
- Status code: 200
- New access_token and refresh_token
```

#### 2.1.3 Current User Info Tests
```bash
# Get current user info with valid token
ACCESS_TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.access_token')

curl -X GET -H "Authorization: Bearer $ACCESS_TOKEN" \
     http://localhost:8000/api/v1/auth/me | jq '.'

Expected response:
- Status code: 200
- Contains: guid, email, role, company_guid
```

### 2.2 QR Authentication Tests

#### 2.2.1 QR Login Tests
```bash
# Test valid QR login
curl -X POST -H "Content-Type: application/json" \
     -d '{
       "user_guid": "d92cd5b4-d760-43fd-a53e-cb0349d71d57",
       "workstation_guid": "<workstation_guid>",
       "pin": "123456"
     }' \
     http://localhost:8000/api/v1/auth/qr | jq '.'

Expected response:
- Status code: 200
- Contains: access_token, refresh_token, role
- Role should be "Operator"
```

## 3. Company Management Tests

### 3.1 Create Test Companies

First, we'll create two test companies to use throughout our testing:

```bash
# Login as SystemAdmin
ADMIN_TOKEN=$(curl -X POST -H "Content-Type: application/json" \
     -d '{"email": "a.petrov@delice.bg", "password": "password"}' \
     http://localhost:8000/api/v1/auth/login | jq -r '.access_token')

# Create Company A
curl -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer $ADMIN_TOKEN" \
     -d '{
       "name": "Company A",
       "code": "COMP_A"
     }' \
     http://localhost:8000/api/v1/companies | jq '.'

# Store Company A GUID
COMPANY_A_GUID=$(curl -H "Authorization: Bearer $ADMIN_TOKEN" \
     http://localhost:8000/api/v1/companies | jq -r '.companies[0].guid')

# Create Company B
curl -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer $ADMIN_TOKEN" \
     -d '{
       "name": "Company B",
       "code": "COMP_B"
     }' \
     http://localhost:8000/api/v1/companies | jq '.'

# Store Company B GUID
COMPANY_B_GUID=$(curl -H "Authorization: Bearer $ADMIN_TOKEN" \
     http://localhost:8000/api/v1/companies | jq -r '.companies[1].guid')
```

## 4. User Management Tests

### 4.1 Create Test Users

Create a full set of test users for both companies:

```bash
# Function to create user
create_user() {
    local company_guid=$1
    local role=$2
    local email=$3
    
    curl -X POST -H "Content-Type: application/json" \
         -H "Authorization: Bearer $ADMIN_TOKEN" \
         -d "{
           \"email\": \"$email\",
           \"password\": \"password\",
           \"role\": \"$role\",
           \"company_guid\": \"$company_guid\"
         }" \
         http://localhost:8000/api/v1/users | cat
}

# Create Company A users
create_user $COMPANY_A_GUID "CompanyAdmin" "admin1.a@example.com"
create_user $COMPANY_A_GUID "CompanyAdmin" "admin2.a@example.com"
create_user $COMPANY_A_GUID "ProjectManager" "pm1.a@example.com"
create_user $COMPANY_A_GUID "ProjectManager" "pm2.a@example.com"
create_user $COMPANY_A_GUID "Operator" "op1.a@example.com"
create_user $COMPANY_A_GUID "Operator" "op2.a@example.com"

# Create Company B users
create_user $COMPANY_B_GUID "CompanyAdmin" "admin1.b@example.com"
create_user $COMPANY_B_GUID "CompanyAdmin" "admin2.b@example.com"
create_user $COMPANY_B_GUID "ProjectManager" "pm1.b@example.com"
create_user $COMPANY_B_GUID "ProjectManager" "pm2.b@example.com"
create_user $COMPANY_B_GUID "Operator" "op1.b@example.com"
create_user $COMPANY_B_GUID "Operator" "op2.b@example.com"
```

### 4.2 User Management Tests

```bash
# Get Company A admin token
COMPANY_A_TOKEN=$(curl -X POST -H "Content-Type: application/json" \
     -d '{"email": "admin1.a@example.com", "password": "password"}' \
     http://localhost:8000/api/v1/auth/login | jq -r .access_token)

# Test user listing within company
curl -H "Authorization: Bearer $COMPANY_A_TOKEN" \
     http://localhost:8000/api/v1/users | cat

# Test cross-company access (should fail)
curl -H "Authorization: Bearer $COMPANY_A_TOKEN" \
     http://localhost:8000/api/v1/users?company_guid=$COMPANY_B_GUID | cat

Expected response:
- Status code: 403
- Error message about insufficient permissions
```

## 5. Workstation Management Tests

### 5.1 Create Test Workstations

```bash
# Create workstations for Company A
curl -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer $COMPANY_A_TOKEN" \
     -d '{
       "location": "Assembly Line 1",
       "type": "Assembly",
       "is_active": true
     }' \
     http://localhost:8000/api/v1/workstations | cat

# Store workstation GUID
WORKSTATION_A_GUID=$(curl -H "Authorization: Bearer $COMPANY_A_TOKEN" \
     http://localhost:8000/api/v1/workstations | jq -r '.workstations[0].guid')

# Create workstations for Company B
curl -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer $COMPANY_B_TOKEN" \
     -d '{
       "location": "Assembly Line 1",
       "type": "Assembly",
       "is_active": true
     }' \
     http://localhost:8000/api/v1/workstations | cat
```

## 6. API Key Management Tests

### 6.1 Create and Test API Keys

```bash
# Create API key for Company A
curl -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer $COMPANY_A_TOKEN" \
     -d '{
       "description": "Test Integration",
       "scopes": "sync:read,sync:write"
     }' \
     http://localhost:8000/api/v1/api-keys | jq '.'

# Store API key
API_KEY_A=$(curl -H "Authorization: Bearer $COMPANY_A_TOKEN" \
     http://localhost:8000/api/v1/api-keys | jq -r '.api_keys[0].key')

# Test API key authentication
curl -H "X-API-Key: $API_KEY_A" \
     http://localhost:8000/api/v1/sync/projects | jq '.'
```

## 7. Data Synchronization Tests

### 7.1 Project Sync Tests

```bash
# Test 1: Sync project without providing GUID (auto-generated)
curl -X POST -H "Content-Type: application/json" \
     -H "X-API-Key: $API_KEY_A" \
     -d '{
       "projects": [
         {
           "code": "PROJ_A1",
           "company_guid": "'$COMPANY_A_GUID'",
           "due_date": "2024-12-31T23:59:59Z"
         }
       ]
     }' \
     http://localhost:8000/api/v1/sync/projects | jq '.'

Expected response:
- Status code: 200
- Contains: inserted count
- Verify GUID was auto-generated

# Store the auto-generated project GUID
PROJECT_A1_GUID=$(curl -H "X-API-Key: $API_KEY_A" \
     http://localhost:8000/api/v1/projects | jq -r '.projects[0].guid')

# Test 2: Sync project with provided GUID
curl -X POST -H "Content-Type: application/json" \
     -H "X-API-Key: $API_KEY_A" \
     -d '{
       "projects": [
         {
           "guid": "550e8400-e29b-41d4-a716-446655440000",
           "code": "PROJ_A2",
           "company_guid": "'$COMPANY_A_GUID'",
           "due_date": "2024-12-31T23:59:59Z"
         }
       ]
     }' \
     http://localhost:8000/api/v1/sync/projects | jq '.'

# Store the provided project GUID
PROJECT_A2_GUID="550e8400-e29b-41d4-a716-446655440000"

# Test 3: Try to sync project with invalid GUID format
curl -X POST -H "Content-Type: application/json" \
     -H "X-API-Key: $API_KEY_A" \
     -d '{
       "projects": [
         {
           "guid": "invalid-guid-format",
           "code": "PROJ_A3",
           "company_guid": "'$COMPANY_A_GUID'",
           "due_date": "2024-12-31T23:59:59Z"
         }
       ]
     }' \
     http://localhost:8000/api/v1/sync/projects | cat

Expected response:
- Status code: 422
- Error about invalid UUID format

# Test 4: Try to sync project with wrong company_guid (should fail)
curl -X POST -H "Content-Type: application/json" \
     -H "X-API-Key: $API_KEY_A" \
     -d '{
       "projects": [
         {
           "code": "PROJ_B1",
           "company_guid": "'$COMPANY_B_GUID'",
           "due_date": "2024-12-31T23:59:59Z"
         }
       ]
     }' \
     http://localhost:8000/api/v1/sync/projects | cat

Expected response:
- Status code: 403
- Error about company mismatch

# Test 5: Bulk project sync with mixed GUIDs
curl -X POST -H "Content-Type: application/json" \
     -H "X-API-Key: $API_KEY_A" \
     -d '{
       "projects": [
         {
           "code": "PROJ_A4",
           "company_guid": "'$COMPANY_A_GUID'",
           "due_date": "2024-12-31T23:59:59Z"
         },
         {
           "guid": "550e8400-e29b-41d4-a716-446655440001",
           "code": "PROJ_A5",
           "company_guid": "'$COMPANY_A_GUID'",
           "due_date": "2024-12-31T23:59:59Z"
         }
       ]
     }' \
     http://localhost:8000/api/v1/sync/projects | cat
```

### 7.2 Component Sync Tests

```bash
# Test 1: Sync component with auto-generated GUID
curl -X POST -H "Content-Type: application/json" \
     -H "X-API-Key: $API_KEY_A" \
     -d '{
       "components": [
         {
           "code": "COMP_A1",
           "project_guid": "'$PROJECT_A1_GUID'",
           "company_guid": "'$COMPANY_A_GUID'",
           "quantity": 1
         }
       ]
     }' \
     http://localhost:8000/api/v1/sync/components | cat

# Store the auto-generated component GUID
COMPONENT_A1_GUID=$(curl -H "X-API-Key: $API_KEY_A" \
     http://localhost:8000/api/v1/components | jq -r '.components[0].guid')

# Test 2: Sync component with provided GUID
curl -X POST -H "Content-Type: application/json" \
     -H "X-API-Key: $API_KEY_A" \
     -d '{
       "components": [
         {
           "guid": "550e8400-e29b-41d4-a716-446655440002",
           "code": "COMP_A2",
           "project_guid": "'$PROJECT_A1_GUID'",
           "company_guid": "'$COMPANY_A_GUID'",
           "quantity": 1
         }
       ]
     }' \
     http://localhost:8000/api/v1/sync/components | cat

# Store the provided component GUID
COMPONENT_A2_GUID="550e8400-e29b-41d4-a716-446655440002"

# Test 3: Try to sync component with non-existent project_guid
curl -X POST -H "Content-Type: application/json" \
     -H "X-API-Key: $API_KEY_A" \
     -d '{
       "components": [
         {
           "code": "COMP_A3",
           "project_guid": "550e8400-e29b-41d4-a716-446655440999",
           "company_guid": "'$COMPANY_A_GUID'",
           "quantity": 1
         }
       ]
     }' \
     http://localhost:8000/api/v1/sync/components | cat

Expected response:
- Status code: 400
- Error about invalid project reference
```

### 7.3 Assembly Sync Tests

```bash
# Test 1: Sync assembly with auto-generated GUID
curl -X POST -H "Content-Type: application/json" \
     -H "X-API-Key: $API_KEY_A" \
     -d '{
       "assemblies": [
         {
           "project_guid": "'$PROJECT_A1_GUID'",
           "component_guid": "'$COMPONENT_A1_GUID'",
           "company_guid": "'$COMPANY_A_GUID'",
           "trolley": "T1",
           "cell_number": 1
         }
       ]
     }' \
     http://localhost:8000/api/v1/sync/assemblies | cat

# Store the auto-generated assembly GUID
ASSEMBLY_A1_GUID=$(curl -H "X-API-Key: $API_KEY_A" \
     http://localhost:8000/api/v1/assemblies | jq -r '.assemblies[0].guid')

# Test 2: Sync assembly with provided GUID
curl -X POST -H "Content-Type: application/json" \
     -H "X-API-Key: $API_KEY_A" \
     -d '{
       "assemblies": [
         {
           "guid": "550e8400-e29b-41d4-a716-446655440003",
           "project_guid": "'$PROJECT_A1_GUID'",
           "component_guid": "'$COMPONENT_A1_GUID'",
           "company_guid": "'$COMPANY_A_GUID'",
           "trolley": "T2",
           "cell_number": 2
         }
       ]
     }' \
     http://localhost:8000/api/v1/sync/assemblies | cat

# Store the provided assembly GUID
ASSEMBLY_A2_GUID="550e8400-e29b-41d4-a716-446655440003"

# Test 3: Try to sync assembly with mismatched project/component relationship
curl -X POST -H "Content-Type: application/json" \
     -H "X-API-Key: $API_KEY_A" \
     -d '{
       "assemblies": [
         {
           "project_guid": "'$PROJECT_A2_GUID'",  # Different project
           "component_guid": "'$COMPONENT_A1_GUID'",
           "company_guid": "'$COMPANY_A_GUID'",
           "trolley": "T3",
           "cell_number": 3
         }
       ]
     }' \
     http://localhost:8000/api/v1/sync/assemblies | cat

Expected response:
- Status code: 400
- Error about invalid component/project relationship
```

### 7.4 Piece Sync Tests

```bash
# Test 1: Sync piece with auto-generated GUID and optional assembly
curl -X POST -H "Content-Type: application/json" \
     -H "X-API-Key: $API_KEY_A" \
     -d '{
       "pieces": [
         {
           "piece_id": "PIECE001",
           "project_guid": "'$PROJECT_A1_GUID'",
           "component_guid": "'$COMPONENT_A1_GUID'",
           "assembly_guid": "'$ASSEMBLY_A1_GUID'",
           "company_guid": "'$COMPANY_A_GUID'",
           "outer_length": 100,
           "angle_left": 45,
           "angle_right": 45
         }
       ]
     }' \
     http://localhost:8000/api/v1/sync/pieces | cat

# Test 2: Sync piece with provided GUID and no assembly
curl -X POST -H "Content-Type: application/json" \
     -H "X-API-Key: $API_KEY_A" \
     -d '{
       "pieces": [
         {
           "guid": "550e8400-e29b-41d4-a716-446655440004",
           "piece_id": "PIECE002",
           "project_guid": "'$PROJECT_A1_GUID'",
           "component_guid": "'$COMPONENT_A1_GUID'",
           "company_guid": "'$COMPANY_A_GUID'",
           "outer_length": 200,
           "angle_left": 90,
           "angle_right": 90
         }
       ]
     }' \
     http://localhost:8000/api/v1/sync/pieces | cat

# Test 3: Bulk piece sync (test limit of 1000)
curl -X POST -H "Content-Type: application/json" \
     -H "X-API-Key: $API_KEY_A" \
     -d '{
       "pieces": [
         {
           "piece_id": "PIECE003",
           "project_guid": "'$PROJECT_A1_GUID'",
           "component_guid": "'$COMPONENT_A1_GUID'",
           "company_guid": "'$COMPANY_A_GUID'"
         },
         {
           "guid": "550e8400-e29b-41d4-a716-446655440005",
           "piece_id": "PIECE004",
           "project_guid": "'$PROJECT_A1_GUID'",
           "component_guid": "'$COMPONENT_A1_GUID'",
           "company_guid": "'$COMPANY_A_GUID'"
         }
         // ... add more pieces up to 1000
       ]
     }' \
     http://localhost:8000/api/v1/sync/pieces | cat

# Test 4: Try to sync more than 1000 pieces (should fail)
# Create an array of 1001 pieces and test the limit
```

### 7.5 Article Sync Tests

```bash
# Test 1: Sync article with auto-generated GUID
curl -X POST -H "Content-Type: application/json" \
     -H "X-API-Key: $API_KEY_A" \
     -d '{
       "articles": [
         {
           "code": "ART001",
           "project_guid": "'$PROJECT_A1_GUID'",
           "component_guid": "'$COMPONENT_A1_GUID'",
           "company_guid": "'$COMPANY_A_GUID'",
           "designation": "Test Article",
           "quantity": 1.0,
           "unit": "pcs"
         }
       ]
     }' \
     http://localhost:8000/api/v1/sync/articles | cat

# Test 2: Sync article with provided GUID
curl -X POST -H "Content-Type: application/json" \
     -H "X-API-Key: $API_KEY_A" \
     -d '{
       "articles": [
         {
           "guid": "550e8400-e29b-41d4-a716-446655440006",
           "code": "ART002",
           "project_guid": "'$PROJECT_A1_GUID'",
           "component_guid": "'$COMPONENT_A1_GUID'",
           "company_guid": "'$COMPANY_A_GUID'",
           "designation": "Test Article 2",
           "quantity": 2.0,
           "unit": "pcs"
         }
       ]
     }' \
     http://localhost:8000/api/v1/sync/articles | cat
```

### 7.6 Cross-Entity Validation Tests

```bash
# Test 1: Try to create circular references
# Test 2: Try to reference entities across companies
# Test 3: Try to use duplicate GUIDs across different entity types
# Test 4: Try to update non-existent entities
# Test 5: Try to create entities with missing required references
```

### Important Testing Notes for Synchronization

1. **GUID Handling:**
   - GUIDs are optional in request payloads
   - If not provided, UUIDv4 is auto-generated
   - If provided, must be valid UUIDv4 format
   - GUIDs must be unique within each entity type

2. **Required References:**
   - company_guid is always required
   - Components require valid project_guid
   - Assemblies require valid project_guid and component_guid
   - Pieces require valid project_guid and component_guid (assembly_guid optional)
   - Articles require valid project_guid and component_guid

3. **Validation Rules:**
   - All GUIDs must be valid UUID v4 format
   - Foreign key relationships are strictly enforced
   - Company isolation is enforced through company_guid
   - Bulk operations are atomic (all succeed or all fail)

4. **Error Cases to Test:**
   - Invalid UUID format
   - Duplicate GUIDs
   - Non-existent reference GUIDs
   - Cross-company reference attempts
   - Missing required references
   - Invalid data types or formats
   - Batch size limits

5. **Performance Considerations:**
   - Test with maximum batch sizes
   - Monitor response times
   - Check database performance
   - Verify memory usage

## 8. Multi-Tenant Isolation Tests

This section focuses on verifying that proper tenant isolation is implemented between companies, preventing any data leakage or unauthorized cross-company access.

### 8.1 Test Preparation

To thoroughly test multi-tenant isolation, we need:
1. Two or more companies with their respective users
2. API keys for each company
3. Data belonging to each company

```bash
# Ensure we have tokens for both Company A and Company B
COMPANY_A_ADMIN_TOKEN=$(curl -X POST -H "Content-Type: application/json" \
     -d '{"email": "admin1.a@example.com", "password": "password"}' \
     http://localhost:8000/api/v1/auth/login | jq -r '.access_token')

COMPANY_B_ADMIN_TOKEN=$(curl -X POST -H "Content-Type: application/json" \
     -d '{"email": "admin1.b@example.com", "password": "password"}' \
     http://localhost:8000/api/v1/auth/login | jq -r '.access_token')

# Create API keys for both companies if needed
COMPANY_A_API_KEY=$(curl -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer $COMPANY_A_ADMIN_TOKEN" \
     -d '{"description": "Isolation Test Key", "scopes": "sync:read,sync:write"}' \
     http://localhost:8000/api/v1/api-keys | jq -r '.key')

COMPANY_B_API_KEY=$(curl -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer $COMPANY_B_ADMIN_TOKEN" \
     -d '{"description": "Isolation Test Key", "scopes": "sync:read,sync:write"}' \
     http://localhost:8000/api/v1/api-keys | jq -r '.key')

# Get company GUIDs
COMPANY_A_GUID=$(curl -H "Authorization: Bearer $COMPANY_A_ADMIN_TOKEN" \
     http://localhost:8000/api/v1/auth/me | jq -r '.company_guid')

COMPANY_B_GUID=$(curl -H "Authorization: Bearer $COMPANY_B_ADMIN_TOKEN" \
     http://localhost:8000/api/v1/auth/me | jq -r '.company_guid')
```

### 8.2 Manual JWT Isolation Tests

```bash
# Test 1: Company A user accessing Company A projects (should succeed)
curl -H "Authorization: Bearer $COMPANY_A_ADMIN_TOKEN" \
     http://localhost:8000/api/v1/projects | cat

# Test 2: Company A user trying to access Company B projects (should fail)
curl -H "Authorization: Bearer $COMPANY_A_ADMIN_TOKEN" \
     "http://localhost:8000/api/v1/projects?company_guid=$COMPANY_B_GUID" | cat

Expected response:
- Status code: 403
- Error message about insufficient permissions

# Test 3: Company B user trying to access Company A projects (should fail)
curl -H "Authorization: Bearer $COMPANY_B_ADMIN_TOKEN" \
     "http://localhost:8000/api/v1/projects?company_guid=$COMPANY_A_GUID" | cat

Expected response:
- Status code: 403
- Error message about insufficient permissions
```

### 8.3 Manual API Key Isolation Tests

```bash
# Test 1: Company A API key accessing Company A projects (should succeed)
curl -H "X-API-Key: $COMPANY_A_API_KEY" \
     http://localhost:8000/api/v1/projects | cat

# Test 2: Company A API key trying to access Company B projects (should fail)
curl -H "X-API-Key: $COMPANY_A_API_KEY" \
     "http://localhost:8000/api/v1/projects?company_guid=$COMPANY_B_GUID" | cat

Expected response:
- Status code: 403
- Error message about insufficient permissions

# Test 3: Company A API key trying to sync Company B data (should fail)
curl -X POST -H "Content-Type: application/json" \
     -H "X-API-Key: $COMPANY_A_API_KEY" \
     -d '{
       "projects": [
         {
           "code": "TEST_PROJECT",
           "company_guid": "'$COMPANY_B_GUID'",
           "due_date": "2024-12-31T23:59:59Z"
         }
       ]
     }' \
     http://localhost:8000/api/v1/sync/projects | cat

Expected response:
- Status code: 403
- Error message about company mismatch
```

### 8.4 Automated Isolation Tests

To run the automated isolation tests, follow these steps:

#### 8.4.1 Prerequisites

Before running the isolation tests, ensure you have:

1. Created test companies A and B
2. Created users with different roles in both companies
3. Created API keys for both companies
4. Created test data (projects, components, etc.) for both companies
5. Installed required Python dependencies

```bash
# Install required dependencies (make sure virtual environment is activated)
cd /home/alex/src/ractory
source venv/bin/activate
pip install aiohttp
```

#### 8.4.2 Quick Isolation Test

The `isolation_test.py` script provides a quick verification of the most critical isolation points:

```bash
# Run the quick isolation test
cd /home/alex/src/ractory/backend
python isolation_test.py
```

This script tests:
- JWT authentication isolation
- API key authentication isolation
- Sync endpoint isolation

Expected output will show passed/failed tests with specific endpoints and responses.

#### 8.4.3 Comprehensive Isolation Test

For a more thorough test across all entity types:

```bash
# Run the comprehensive isolation test
cd /home/alex/src/ractory/backend
python -m app.tests.test_multi_tenant_isolation
```

This comprehensive test covers:
- All entity endpoints (projects, components, assemblies, pieces, articles, workstations, users)
- Both JWT and API key authentication
- All sync endpoints
- Both GET and POST operations

#### 8.4.4 Troubleshooting Test Failures

If the isolation tests fail:

1. **Missing Endpoints (404 errors)**: This may indicate the endpoint isn't implemented yet. Check if the endpoint exists before considering it a security issue.

2. **Validation Errors (422)**: For sync endpoints, ensure the test is sending proper payloads with required fields. The test may be failing at validation before reaching the isolation check.

3. **Successful Cross-Company Access (200)**: This indicates a true isolation failure that needs to be fixed in the API implementation.

4. **Cross-Company Modification (200 for PUT/POST/DELETE)**: These are critical security issues that should be addressed immediately.

#### 8.4.5 Documenting Automated Test Results

When documenting automated test results, include:

```
## Automated Isolation Tests
Date: [YYYY-MM-DD]
Tester: [Name]

### Quick Isolation Test (isolation_test.py):
- Tests Passed: X of Y
- Main Issues Found: [List key issues]

### Comprehensive Test (test_multi_tenant_isolation.py):
- JWT Tests Passed: X of Y
- API Key Tests Passed: X of Y
- Sync Endpoint Tests Passed: X of Y
- Main Issues Found: [List key issues]

### Priority Issues:
1. [High] Cross-company read access possible for [endpoints]
2. [Critical] Cross-company write access possible for [endpoints]
3. [Medium] Validation occurs before authorization check for [endpoints]
```

## 9. Error Handling Tests

### 9.1 Invalid Input Tests

```bash
# Test invalid JSON
curl -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer $ADMIN_TOKEN" \
     -d '{invalid json}' \
     http://localhost:8000/api/v1/users | cat

Expected response:
- Status code: 400
- Error about invalid JSON format

# Test missing required fields
curl -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer $ADMIN_TOKEN" \
     -d '{}' \
     http://localhost:8000/api/v1/users | cat

Expected response:
- Status code: 422
- Error about missing required fields
```

### 9.2 Authentication Error Tests

```bash
# Test expired token
curl -H "Authorization: Bearer expired.token.here" \
     http://localhost:8000/api/v1/users | cat

Expected response:
- Status code: 401
- Error about expired token

# Test invalid token format
curl -H "Authorization: Bearer invalid-token" \
     http://localhost:8000/api/v1/users | cat

Expected response:
- Status code: 401
- Error about invalid token format
```

## Test Results Documentation

For each test section, document the results in the following format:

```markdown
## Test Section: [Name]
Date: [YYYY-MM-DD]
Tester: [Name]

### Test Cases:
1. [Test Case Name]
   - Status: [Pass/Fail]
   - Response Code: [XXX]
   - Notes: [Any relevant observations]

### Issues Found:
1. [Issue Description]
   - Severity: [High/Medium/Low]
   - Steps to Reproduce: [Steps]
   - Expected vs Actual: [Description]
```

## Important Testing Notes

1. **Order of Testing:**
   - Always start with health checks
   - Complete authentication tests before proceeding
   - Test CRUD operations in order: Create, Read, Update, Delete
   - Test multi-tenant isolation last

2. **Security Considerations:**
   - Never share or commit access tokens
   - Rotate test passwords regularly
   - Monitor rate limiting responses
   - Test all endpoints with various roles

3. **Data Cleanup:**
   - Clean up test data after testing sessions
   - Use separate test databases for different testing phases
   - Document any persistent test data created

4. **Error Handling:**
   - Test both success and failure cases
   - Verify error message format and content
   - Test rate limiting behavior
   - Test timeout scenarios

5. **Cross-Tenant Testing:**
   - Always verify data isolation between companies
   - Test with multiple company combinations
   - Verify SystemAdmin override capabilities
   - Test API key scope restrictions 

## Bug Fix Report

### Fixed Issues (2025-05-02)

#### 1. User Extended Fields Bug
- **Issue**: Name and surname fields were not being included in user responses and were not being properly stored in the database.
- **Root Cause**: The UserResponse schema did not explicitly include these fields.
- **Fix**: Updated the UserResponse schema to explicitly include all user fields including name, surname, and picture_path.
- **Validation**: Successfully created and updated users with name and surname fields.

#### 2. Updated_at Timestamp Bug
- **Issue**: The updated_at field was not being automatically updated when records were modified.
- **Root Cause**: Missing database trigger to handle the timestamp updates.
- **Fix**: 
  - Updated the TimestampMixin in base.py to properly handle the updated_at field
  - Created a database trigger function (update_updated_at_column)
  - Applied this trigger to all tables with updated_at columns
- **Validation**: Verified that updated_at timestamps are correctly set when updating records.

### Testing Summary
All extended user field tests have been completed successfully:
- Creating users with name/surname fields
- Updating user name/surname fields
- Verifying fields in API responses
- Confirming updated_at timestamp functionality

Additional improvements could be made to test field validation rules, length limits, and format validation.

## 10. Soft Delete, Cascade, Restore, and Reactivation Tests

### 10.1 Soft Delete via REST Endpoint

#### Example: Soft delete a project
```bash
curl -X DELETE -H "Authorization: Bearer $TOKEN" \
     http://localhost:8000/api/v1/projects/{project_guid}
```
- **Expected:** 204 No Content. Project and all children are soft deleted (is_active: false, deleted_at set).

#### Example: Soft delete a component
```bash
curl -X DELETE -H "Authorization: Bearer $TOKEN" \
     http://localhost:8000/api/v1/components/{component_guid}
```
- **Expected:** 204 No Content. Component and all children are soft deleted.

### 10.2 Soft Delete via Sync Endpoint

#### Example: Sync omitting a child (should soft delete missing children)
```bash
curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
     -d '{"components": [{"guid": "...", "code": "...", ...}]}' \
     http://localhost:8000/api/v1/sync/components
```
- **Expected:** Children not present in payload are soft deleted (is_active: false, deleted_at set).

### 10.3 Cascade Soft Delete
- Soft deleting a parent (project/component/assembly) cascades to all active children recursively.
- All cascaded entities have the same deleted_at timestamp.

### 10.4 Selective Restore

#### Example: Restore a project
```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
     http://localhost:8000/api/v1/projects/{project_guid}/restore
```
- **Expected:** Project and only children with matching deleted_at are restored (is_active: true, deleted_at: null).

### 10.5 Reactivation via Sync

#### Example: Reactivate a soft-deleted component via sync
```bash
curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
     -d '{"components": [{"guid": "...", "code": "UPDATED", ...}]}' \
     http://localhost:8000/api/v1/sync/components
```
- **Expected:** Soft-deleted component is reactivated and updated (is_active: true, deleted_at: null).

### 10.6 GET with/without Inactive

#### Example: Get only active components (default)
```bash
curl -H "Authorization: Bearer $TOKEN" \
     http://localhost:8000/api/v1/components
```
- **Expected:** Only active components returned.

#### Example: Get all components including soft-deleted
```bash
curl -H "Authorization: Bearer $TOKEN" \
     http://localhost:8000/api/v1/components?include_inactive=true
```
- **Expected:** Both active and soft-deleted components returned.

### 10.7 Edge Cases
- Multiple generations of soft-deleted children (deep cascade)
- Partial soft delete and selective restoration
- Sync reactivation edge cases

**See `src/ractory/backend/test_edge_cases.py` for automated test coverage of all above scenarios.**

