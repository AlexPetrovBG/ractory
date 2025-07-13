## 3. Company Management Tests (`/api/v1/companies`)

Requires SystemAdmin token (`$ADMIN_ACCESS_TOKEN` from setup).

```bash
# Variables for test companies (ensure unique names/indices for each run)
COMPANY_A_NAME="TestCo A $(date +%N)"
COMPANY_A_CODE="TCA$(date +%N)"
COMPANY_A_INDEX=90 # Example, ensure unique

COMPANY_B_NAME="TestCo B $(date +%N)"
COMPANY_B_CODE="TCB$(date +%N)"
COMPANY_B_INDEX=91 # Example, ensure unique
```

### 3.1 Create Company
```bash
COMPANY_A_RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer $ADMIN_ACCESS_TOKEN" \
     -d "{\"name\": \"$COMPANY_A_NAME\", \"code\": \"$COMPANY_A_CODE\", \"company_index\": $COMPANY_A_INDEX}" \
     http://localhost:8000/api/v1/companies | jq '.')
COMPANY_A_GUID=$(echo $COMPANY_A_RESPONSE | jq -r '.guid')
echo "Company A ($COMPANY_A_NAME) GUID: $COMPANY_A_GUID"

COMPANY_B_RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer $ADMIN_ACCESS_TOKEN" \
     -d "{\"name\": \"$COMPANY_B_NAME\", \"code\": \"$COMPANY_B_CODE\", \"company_index\": $COMPANY_B_INDEX}" \
     http://localhost:8000/api/v1/companies | jq '.')
COMPANY_B_GUID=$(echo $COMPANY_B_RESPONSE | jq -r '.guid')
echo "Company B ($COMPANY_B_NAME) GUID: $COMPANY_B_GUID"
```
**Expected (201 Created):** Company details. Test error cases (duplicate name/index, invalid index).

### 3.2 List Companies
```bash
cURL -s -X GET -H "Authorization: Bearer $ADMIN_ACCESS_TOKEN" http://localhost:8000/api/v1/companies | jq '.'
```
### 3.3 Get Company
```bash
cURL -s -X GET -H "Authorization: Bearer $ADMIN_ACCESS_TOKEN" http://localhost:8000/api/v1/companies/$COMPANY_A_GUID | jq '.'
```
### 3.4 Update Company (PATCH)
```bash
cURL -s -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer $ADMIN_ACCESS_TOKEN" \
     -d "{\"name\": \"$COMPANY_A_NAME (Updated)\", \"is_active\": false}" \
     http://localhost:8000/api/v1/companies/$COMPANY_A_GUID | jq '.'
```
### 3.5 Delete Company
```bash
# curl -s -X DELETE -H "Authorization: Bearer $ADMIN_ACCESS_TOKEN" http://localhost:8000/api/v1/companies/$COMPANY_B_GUID # Uncomment to test
```

## 4. User Management Tests (`/api/v1/users`)

Use `$ADMIN_ACCESS_TOKEN` and Company GUIDs (`$COMPANY_A_GUID`).
```bash
USER_PASSWORD="securePassword123"
COMP_A_ADMIN_EMAIL="ca_a_$(date +%N)@example.com"
COMP_A_PM_EMAIL="pm_a_$(date +%N)@example.com"
```

### 4.1 Create User
```bash
# SystemAdmin creates CompanyAdmin for Company A
COMP_A_ADMIN_RESP=$(curl -s -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $ADMIN_ACCESS_TOKEN" \
     -d "{\"email\": \"$COMP_A_ADMIN_EMAIL\", \"password\": \"$USER_PASSWORD\", \"role\": \"CompanyAdmin\", \"company_guid\": \"$COMPANY_A_GUID\", \"name\": \"AdminA\"}" \
     http://localhost:8000/api/v1/users | jq '.')
COMP_A_ADMIN_GUID=$(echo $COMP_A_ADMIN_RESP | jq -r '.guid')
echo "Company A Admin GUID: $COMP_A_ADMIN_GUID"

# Login as CompanyAdmin A to get their token (for subsequent tests)
COMP_A_ADMIN_TOKEN=$(curl -s -X POST -H "Content-Type: application/json" \
     -d "{\"email\": \"$COMP_A_ADMIN_EMAIL\", \"password\": \"$USER_PASSWORD\"}" \
     http://localhost:8000/api/v1/auth/login | jq -r '.access_token')

# CompanyAdmin A creates ProjectManager for Company A
COMP_A_PM_RESP=$(curl -s -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $COMP_A_ADMIN_TOKEN" \
     -d "{\"email\": \"$COMP_A_PM_EMAIL\", \"password\": \"$USER_PASSWORD\", \"role\": \"ProjectManager\", \"company_guid\": \"$COMPANY_A_GUID\", \"name\": \"PMA\"}" \
     http://localhost:8000/api/v1/users | jq '.')
COMP_A_PM_GUID=$(echo $COMP_A_PM_RESP | jq -r '.guid')
echo "Company A PM GUID: $COMP_A_PM_GUID"
```
Test role hierarchy violations.

### 4.2 List Users
```bash
# SystemAdmin lists users in Company A
cURL -s -X GET -H "Authorization: Bearer $ADMIN_ACCESS_TOKEN" "http://localhost:8000/api/v1/users?company_guid=$COMPANY_A_GUID" | jq '.'
# CompanyAdmin A lists users in Company A
cURL -s -X GET -H "Authorization: Bearer $COMP_A_ADMIN_TOKEN" "http://localhost:8000/api/v1/users" | jq '.'
```
### 4.3 Get User
```bash
cURL -s -X GET -H "Authorization: Bearer $ADMIN_ACCESS_TOKEN" http://localhost:8000/api/v1/users/$COMP_A_PM_GUID | jq '.'
```
### 4.4 Update User
```bash
cURL -s -X PUT -H "Content-Type: application/json" -H "Authorization: Bearer $COMP_A_ADMIN_TOKEN" \
     -d '{"name": "ProjectManagerA Updated", "pin": "9876"}' \
     http://localhost:8000/api/v1/users/$COMP_A_PM_GUID | jq '.'
```
### 4.5 Delete User (Soft Delete)
```bash
# curl -s -X DELETE -H "Authorization: Bearer $COMP_A_ADMIN_TOKEN" http://localhost:8000/api/v1/users/$USER_TO_DELETE_GUID | jq '.' # Uncomment to test
```

## 5. API Key Management Tests (`/api/v1/api-keys`)

Use `$COMP_A_ADMIN_TOKEN` for Company A.

### 5.1 Create API Key
```bash
API_KEY_RESP=$(curl -s -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $COMP_A_ADMIN_TOKEN" \
     -d '{"description": "Sync Key for CompA", "scopes": "sync:read sync:write"}' \
     http://localhost:8000/api/v1/api-keys | jq '.')
RAW_API_KEY_A=$(echo $API_KEY_RESP | jq -r '.key')
API_KEY_A_GUID=$(echo $API_KEY_RESP | jq -r '.guid')
echo "Company A API Key GUID: $API_KEY_A_GUID - Raw Key: $RAW_API_KEY_A"
```
### 5.2 List API Keys (for Company A)
```bash
cURL -s -X GET -H "Authorization: Bearer $COMP_A_ADMIN_TOKEN" http://localhost:8000/api/v1/api-keys | jq '.'
```
### 5.3 Get API Key
```bash
cURL -s -X GET -H "Authorization: Bearer $COMP_A_ADMIN_TOKEN" http://localhost:8000/api/v1/api-keys/$API_KEY_A_GUID | jq '.'
```
### 5.4 Update API Key
```bash
cURL -s -X PUT -H "Content-Type: application/json" -H "Authorization: Bearer $COMP_A_ADMIN_TOKEN" \
     -d '{"description": "Updated Sync Key", "is_active": false}' \
     http://localhost:8000/api/v1/api-keys/$API_KEY_A_GUID | jq '.'
```
### 5.5 Delete API Key
```bash
# curl -s -X DELETE -H "Authorization: Bearer $COMP_A_ADMIN_TOKEN" http://localhost:8000/api/v1/api-keys/$API_KEY_A_GUID # Uncomment to test
```

## 6. Workstation Management Tests (`/api/v1/workstations`)

Use `$COMP_A_ADMIN_TOKEN`.

### 6.1 Create Workstation
```bash
WS_A_RESP=$(curl -s -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $COMP_A_ADMIN_TOKEN" \
     -d '{"location": "Main Assy Line WS1", "type": "Assembly"}' \
     http://localhost:8000/api/v1/workstations | jq '.')
WS_A_GUID=$(echo $WS_A_RESP | jq -r '.guid')
echo "Company A Workstation GUID: $WS_A_GUID"
```
### 6.2 List Workstations (for Company A)
```bash
cURL -s -X GET -H "Authorization: Bearer $COMP_A_ADMIN_TOKEN" http://localhost:8000/api/v1/workstations | jq '.'
```
### 6.3 Get Workstation
```bash
cURL -s -X GET -H "Authorization: Bearer $COMP_A_ADMIN_TOKEN" http://localhost:8000/api/v1/workstations/$WS_A_GUID | jq '.'
```
### 6.4 Update Workstation
```bash
cURL -s -X PUT -H "Content-Type: application/json" -H "Authorization: Bearer $COMP_A_ADMIN_TOKEN" \
     -d '{"location": "Main Assy Line WS1 (Updated)", "is_active": false}' \
     http://localhost:8000/api/v1/workstations/$WS_A_GUID | jq '.'
```
### 6.5 Delete Workstation (Soft Delete)
```bash
# curl -s -X DELETE -H "Authorization: Bearer $COMP_A_ADMIN_TOKEN" http://localhost:8000/api/v1/workstations/$WS_A_GUID | jq '.' # Uncomment to test
``` 