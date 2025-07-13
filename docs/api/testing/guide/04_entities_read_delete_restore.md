## 8. Entity Read, Soft Delete & Restore Tests

These tests use entities created via Sync (e.g., `$PROJECT_S_GUID`, `$COMPONENT_S_GUID` from `03_sync.md`) or any other existing entity GUIDs available for the test company (e.g., `$COMPANY_A_GUID`). Use an appropriate auth header (`$AUTH_HEADER_SYNC` or another token like `$COMP_A_ADMIN_TOKEN` if appropriate for read operations).

### 8.1 Projects (`/api/v1/projects`)

#### 8.1.1 List Projects
```bash
# List all active projects for the current company
curl -s -G -H "$AUTH_HEADER_SYNC" "http://localhost:8000/api/v1/projects" | jq '.'

# List projects including inactive ones
curl -s -G -H "$AUTH_HEADER_SYNC" --data-urlencode "include_inactive=true" "http://localhost:8000/api/v1/projects" | jq '.'

# List projects with a specific code (ensure $PROJECT_CODE_S exists)
curl -s -G -H "$AUTH_HEADER_SYNC" --data-urlencode "code=$PROJECT_CODE_S" "http://localhost:8000/api/v1/projects" | jq '.'

# Search projects by code substring
curl -s -G -H "$AUTH_HEADER_SYNC" --data-urlencode "search=SYNC" "http://localhost:8000/api/v1/projects" | jq '.'

# For SystemAdmins: List projects for a specific company (replace $TARGET_COMPANY_GUID)
# curl -s -G -H "Authorization: Bearer $ADMIN_ACCESS_TOKEN" --data-urlencode "company_guid=$TARGET_COMPANY_GUID" "http://localhost:8000/api/v1/projects" | jq '.'
```
**Expected (200 OK):** List of projects matching filters.

#### 8.1.2 Get Project
```bash
# Use $PROJECT_S_GUID obtained from sync tests or another known Project GUID
cURL -s -G -H "$AUTH_HEADER_SYNC" "http://localhost:8000/api/v1/projects/$PROJECT_S_GUID" | jq '.' 
```
**Expected (200 OK):** Project details, `is_active: true` (if not yet deleted).

#### 8.1.3 Soft Delete Project
```bash
cURL -s -X DELETE -H "$AUTH_HEADER_SYNC" "http://localhost:8000/api/v1/projects/$PROJECT_S_GUID"
```
**Expected (204 No Content).**

#### 8.1.4 Get Soft-Deleted Project
```bash
# Verify it's not returned by default (expect 404)
cURL -s -G -H "$AUTH_HEADER_SYNC" "http://localhost:8000/api/v1/projects/$PROJECT_S_GUID"

# Verify it IS returned with include_inactive=true
cURL -s -G -H "$AUTH_HEADER_SYNC" --data-urlencode "include_inactive=true" "http://localhost:8000/api/v1/projects/$PROJECT_S_GUID" | jq '.'
```
**Expected (200 OK for second command):** Project details with `is_active: false` and `deleted_at` timestamp.

#### 8.1.5 Restore Project
```bash
cURL -s -X POST -H "$AUTH_HEADER_SYNC" "http://localhost:8000/api/v1/projects/$PROJECT_S_GUID/restore"
```
**Expected (204 No Content).**

#### 8.1.6 Verify Restored Project
```bash
cURL -s -G -H "$AUTH_HEADER_SYNC" "http://localhost:8000/api/v1/projects/$PROJECT_S_GUID" | jq '.'
```
**Expected (200 OK):** Project details with `is_active: true` and `deleted_at: null`.

### 8.2 Components (`/api/v1/components`)
Use `$COMPONENT_S_GUID` (obtained from sync tests). Repeat the Get, Soft Delete, Get (inactive), Restore, and Verify Restored flow as shown for Projects.
Test listing components of the project, including inactive: 
```bash
cURL -s -G -H "$AUTH_HEADER_SYNC" --data-urlencode "project_guid=$PROJECT_S_GUID" --data-urlencode "include_inactive=true" "http://localhost:8000/api/v1/components" | jq '.'
```

### 8.3 Assemblies (`/api/v1/assemblies`)
Use `$ASSEMBLY_S_GUID` (obtained from sync tests). Repeat the Get, Soft Delete, Get (inactive), Restore, and Verify Restored flow.

### 8.4 Pieces (`/api/v1/pieces`)
Use a known piece GUID (e.g., one created with `$PIECE_ID_S` during sync). Repeat the Get, Soft Delete, Get (inactive), Restore, and Verify Restored flow.
Test listing with pagination: `limit=10`, `offset=0`.

### 8.5 Articles (`/api/v1/articles`)
Use a known article GUID (e.g., one created with `$ARTICLE_CODE_S` during sync). Repeat the Get, Soft Delete, Get (inactive), Restore, and Verify Restored flow.
Test listing with pagination.

**General Cascade Behavior Testing:**
-   After soft-deleting `$PROJECT_S_GUID`, query its components (e.g., `$COMPONENT_S_GUID`) with `include_inactive=true`. Verify they are also soft-deleted and share the same `deleted_at` timestamp (or very close) as the project.
-   Restore `$PROJECT_S_GUID`. Verify that child entities (like `$COMPONENT_S_GUID`) that were part of the cascade delete are also restored.
-   If a child was deleted independently *before* the parent, it should *not* be restored when the parent is restored. 