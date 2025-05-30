## 7. Data Synchronization Tests (`/api/v1/sync/*`)

These tests require an API key with `sync:write` scope for the target company (e.g., use `$RAW_API_KEY_A` for `$COMPANY_A_GUID` from previous core resource tests) or an admin token for that company.

**Important:**
-   Verify `inserted` and `updated` counts in the response for each sync operation.
-   Test upsert logic: Providing an existing GUID should update; omitting or providing a new GUID should create.
-   Ensure all synced data correctly reflects the `company_guid` of the authenticated entity (API key/user token).

```bash
# Use $RAW_API_KEY_A (ensure it has sync:write and belongs to COMPANY_A_GUID)
# Or use $COMP_A_ADMIN_TOKEN (token for a CompanyAdmin of Company A)
AUTH_HEADER_SYNC="X-API-Key: $RAW_API_KEY_A" # Or "Authorization: Bearer $COMP_A_ADMIN_TOKEN"

# Variables for synced entities (use unique codes for each test run)
PROJECT_CODE_S="PSYNC_$(date +%N)"
COMPONENT_CODE_S="CSYNC_$(date +%N)"
ASSEMBLY_TROLLEY_S="TSYNC_$(date +%N)"
PIECE_ID_S="PISYNC_$(date +%N)"
ARTICLE_CODE_S="ASYNC_$(date +%N)"
```

### 7.1 Sync Projects
```bash
SYNC_PROJECT_RESP=$(curl -s -X POST -H "Content-Type: application/json" -H "$AUTH_HEADER_SYNC" \
     -d "{\"projects\": [{\"code\": \"$PROJECT_CODE_S\", \"company_guid\": \"$COMPANY_A_GUID\", \"due_date\": \"2025-10-10T10:00:00Z\"}]}" \
     http://localhost:8000/api/v1/sync/projects | jq '.')
echo $SYNC_PROJECT_RESP

# After sync, retrieve the project to get its GUID for subsequent tests
# Use admin/appropriate token for COMPANY_A_GUID to list projects
PROJECT_S_GUID=$(curl -s -G -H "Authorization: Bearer $COMP_A_ADMIN_TOKEN" \
     --data-urlencode "code=$PROJECT_CODE_S" \
     "http://localhost:8000/api/v1/projects" | jq -r '.[0].guid') # Assumes unique code and gets first match
echo "Synced Project GUID (PROJECT_S_GUID): $PROJECT_S_GUID"
```
**Expected (200 OK):** `{"inserted": 1, "updated": 0}` (or vice-versa if testing updates).

### 7.2 Sync Components
(Requires `$PROJECT_S_GUID` and `$COMPANY_A_GUID`)
```bash
SYNC_COMP_RESP=$(curl -s -X POST -H "Content-Type: application/json" -H "$AUTH_HEADER_SYNC" \
     -d "{\"components\": [{\"code\": \"$COMPONENT_CODE_S\", \"project_guid\": \"$PROJECT_S_GUID\", \"company_guid\": \"$COMPANY_A_GUID\", \"quantity\": 10}]}" \
     http://localhost:8000/api/v1/sync/components | jq '.')
echo $SYNC_COMP_RESP

COMPONENT_S_GUID=$(curl -s -G -H "Authorization: Bearer $COMP_A_ADMIN_TOKEN" \
     --data-urlencode "project_guid=$PROJECT_S_GUID" \
     "http://localhost:8000/api/v1/components" | jq -r --arg code "$COMPONENT_CODE_S" '.[] | select(.code == $code) | .guid')
echo "Synced Component GUID (COMPONENT_S_GUID): $COMPONENT_S_GUID"
```

### 7.3 Sync Assemblies
(Requires `$PROJECT_S_GUID`, `$COMPONENT_S_GUID`, `$COMPANY_A_GUID`)
```bash
SYNC_ASSY_RESP=$(curl -s -X POST -H "Content-Type: application/json" -H "$AUTH_HEADER_SYNC" \
     -d "{\"assemblies\": [{\"project_guid\": \"$PROJECT_S_GUID\", \"component_guid\": \"$COMPONENT_S_GUID\", \"company_guid\": \"$COMPANY_A_GUID\", \"trolley\": \"$ASSEMBLY_TROLLEY_S\"}]}" \
     http://localhost:8000/api/v1/sync/assemblies | jq '.')
echo $SYNC_ASSY_RESP

ASSEMBLY_S_GUID=$(curl -s -G -H "Authorization: Bearer $COMP_A_ADMIN_TOKEN" \
     --data-urlencode "component_guid=$COMPONENT_S_GUID" \
     "http://localhost:8000/api/v1/assemblies" | jq -r --arg trolley "$ASSEMBLY_TROLLEY_S" '.[] | select(.trolley == $trolley) | .guid')
echo "Synced Assembly GUID (ASSEMBLY_S_GUID): $ASSEMBLY_S_GUID"
```

### 7.4 Sync Pieces
(Requires parent GUIDs; Max 1000 pieces)
```bash
curl -s -X POST -H "Content-Type: application/json" -H "$AUTH_HEADER_SYNC" \
     -d "{\"pieces\": [{\"piece_id\": \"$PIECE_ID_S\", \"project_guid\": \"$PROJECT_S_GUID\", \"component_guid\": \"$COMPONENT_S_GUID\", \"assembly_guid\": \"$ASSEMBLY_S_GUID\", \"company_guid\": \"$COMPANY_A_GUID\", \"outer_length\": 123.45}]}" \
     http://localhost:8000/api/v1/sync/pieces | jq '.'
# Test batch limit (>1000 pieces) separately, expect 400 Bad Request.
```

### 7.5 Sync Articles
(Requires parent GUIDs)
```bash
curl -s -X POST -H "Content-Type: application/json" -H "$AUTH_HEADER_SYNC" \
     -d "{\"articles\": [{\"code\": \"$ARTICLE_CODE_S\", \"project_guid\": \"$PROJECT_S_GUID\", \"component_guid\": \"$COMPONENT_S_GUID\", \"company_guid\": \"$COMPANY_A_GUID\", \"quantity\": 50, \"unit\": \"pcs\"}]}" \
     http://localhost:8000/api/v1/sync/articles | jq '.'
``` 