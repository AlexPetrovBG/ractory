### Checklist Part 3: Data Operations (Sync, Entity R/W/D, Workflow)

**Tester:**
**Date:**

(Assumes setup from previous parts, including `$COMPANY_A_GUID`, tokens like `$COMP_A_ADMIN_TOKEN` or API key `$RAW_API_KEY_A` for Company A, and GUIDs for synced/created entities like `$PROJECT_S_GUID`, `$COMPONENT_S_GUID`, `$ASSEMBLY_S_GUID`, `$WORKFLOW_ENTRY_GUID`, etc.)

#### VIII. Data Synchronization Tests (`/api/v1/sync/*`) (Corresponds to Guide Section: 7) - COMPLETED ✅

-   [x] **SETUP:** Use `$AUTH_HEADER_SYNC` (API key for Co. A or Co. A Admin token). Define unique codes for sync items (e.g., `$PROJECT_CODE_S`).

1.  **Sync Projects (`POST /projects`)**
    -   [x] Sync new project to Co. A -> `200 OK`, `inserted: 1, updated: 0`. Store `$PROJECT_S_GUID` (retrieved via GET after sync).
    -   [x] Sync same project data again (with `$PROJECT_S_GUID` if schema supports it, or by unique code) -> `200 OK`, `inserted: 0, updated: 1` (or `updated: 0` if no change).
    -   [x] Attempt to sync project with `company_guid` for Co. B using Co. A API key/token -> `403 Forbidden`.
2.  **Sync Components (`POST /components`)** (Requires `$PROJECT_S_GUID`)
    -   [x] Sync new component to `$PROJECT_S_GUID` -> `200 OK`, `inserted: 1`. Store `$COMPONENT_S_GUID`.
    -   [x] Test update of this component.
    -   [x] Attempt with invalid `$PROJECT_S_GUID` -> Error (e.g., `400` or `422` due to FK violation).
3.  **Sync Assemblies (`POST /assemblies`)** (Requires `$PROJECT_S_GUID`, `$COMPONENT_S_GUID`)
    -   [x] Sync new assembly -> `200 OK`, `inserted: 1`. Store `$ASSEMBLY_S_GUID`.
    -   [x] Test update.
4.  **Sync Pieces (`POST /pieces`)** (Requires parent GUIDs)
    -   [x] Sync new piece -> `200 OK`, `inserted: 1`.
    -   [x] Test update.
    -   [x] Sync >1000 pieces -> `400 Bad Request`.
5.  **Sync Articles (`POST /articles`)** (Requires parent GUIDs)
    -   [x] Sync new article -> `200 OK`, `inserted: 1`.
    -   [x] Test update.

**VIII Summary - Done**: All sync operations working correctly with proper validation, authorization, and batch limits. API key: rfk_IJk7Mh7vXxz8y1RkmlaPdODdnQZCiXxo. Entity GUIDs: PROJECT_S_GUID=e707d120-28b3-4988-8411-727020c677b4, COMPONENT_S_GUID=09c52c5c-9e9b-43ff-acce-d42c6de3dc8c, ASSEMBLY_S_GUID=2e7a5961-9d4a-4d20-862b-ad7e048d69d9.

#### IX. Entity Read, Soft Delete & Restore Tests (Corresponds to Guide Section: 8) - COMPLETED ✅

(Use appropriate auth for Co. A, e.g., `$AUTH_HEADER_SYNC` or `$COMP_A_ADMIN_TOKEN`. Use entities like `$PROJECT_S_GUID`, `$COMPONENT_S_GUID` created via sync.)

**A. Projects (`/api/v1/projects`)**
-   [x] List projects (`GET /`) for Co. A. Test `code`, `search`, `include_inactive` filters.
-   [x] Get `$PROJECT_S_GUID` (`GET /{guid}`) -> `200 OK`, `is_active: true` (initially).
-   [x] Soft Delete `$PROJECT_S_GUID` (`DELETE /{guid}`) -> `204 No Content`.
-   [x] Get `$PROJECT_S_GUID` (no inactive flag) -> `404 Not Found`.
-   [x] Get `$PROJECT_S_GUID` (`include_inactive=true`) -> `200 OK`, `is_active: false`, `deleted_at` set.
-   [x] Restore `$PROJECT_S_GUID` (`POST /{guid}/restore`) -> `204 No Content`.
-   [x] Get `$PROJECT_S_GUID` -> `200 OK`, `is_active: true`, `deleted_at: null`.

**B. Components (`/api/v1/components`)** (Use `$COMPONENT_S_GUID`)
-   [x] Repeat Get, List (with filters like `project_guid`, `include_inactive`), Soft Delete, Get (inactive), Restore, Get (active) flow.

**C. Assemblies (`/api/v1/assemblies`)** (Use `$ASSEMBLY_S_GUID`)
-   [x] Repeat Get, List (with filters), Soft Delete, Get (inactive), Restore, Get (active) flow.

**D. Pieces (`/api/v1/pieces`)** (Use a known piece GUID from sync)
-   [x] Repeat Get, List (with filters, pagination), Soft Delete, Get (inactive), Restore, Get (active) flow.

**E. Articles (`/api/v1/articles`)** (Use a known article GUID from sync)
-   [x] Repeat Get, List (with filters, pagination), Soft Delete, Get (inactive), Restore, Get (active) flow.

**F. Cascade Behavior**
-   [x] Soft Delete `$PROJECT_S_GUID`. Verify `$COMPONENT_S_GUID` (child of project) is also soft-deleted (check with `include_inactive=true`, `deleted_at` timestamp).
-   [x] Restore `$PROJECT_S_GUID`. Verify `$COMPONENT_S_GUID` is also restored.
-   [x] Manually soft-delete a child (e.g. an Assembly). Then soft-delete its parent Component. Then restore the Component. Verify the Assembly (deleted prior) remains deleted.

**IX Summary - Done**: Entity CRUD operations working perfectly. Cascade delete/restore working with matching timestamps. All entity types (Projects, Components, Assemblies, Pieces, Articles) follow consistent soft delete patterns. Multi-tenant isolation maintained throughout.

#### X. Workflow Management Tests (`/api/v1/workflow`) (Corresponds to Guide Section: 9) - COMPLETED ✅

(Requires ProjectManager token, e.g., `$COMP_A_PM_TOKEN`. Use `$COMPANY_A_GUID`, `$WS_A_GUID`.)

1.  **Create Workflow Entry (`POST /`)**
    -   [x] Create entry (valid `action_type`, e.g., `barcode_scan`, provide `company_guid`, `workstation_guid`, `action_value`) -> `201 Created`. Store `$WORKFLOW_ENTRY_GUID`.
    -   [x] Verify response: `company_name`, `workstation_name`, `user_name` populated.
    -   [x] Create entry with invalid `action_type` -> `422 Unprocessable Entity` (error lists valid types).
    -   [x] Create entry omitting `user_guid` (should default to token user) -> `201 Created`.
2.  **List Workflow Entries (`GET /`)**
    -   [x] List entries (use filters: `action_type`, `workstation_guid`, `limit=5`) -> `200 OK`. Entries match filters.
    -   [x] Test `start_date` / `end_date` filters.
    -   [x] Test pagination (`offset`, `limit`).
3.  **Get Workflow Entry (`GET /{guid}`)**
    -   [x] Get `$WORKFLOW_ENTRY_GUID` -> `200 OK`.
4.  **Get Workflow Statistics (`GET /statistics`)**
    -   [x] Get stats (optionally with date filters) -> `200 OK`. Response matches `WorkflowStatistics` schema.

**X Summary - Done**: Workflow management fully functional. All action types validated correctly. Auto-population working. Filtering, pagination, and statistics all working with proper schema compliance. Multi-tenant isolation maintained. WORKFLOW_ENTRY_GUID=0ec7ce9c-a9fd-416d-97c4-452e3d3bc166. 