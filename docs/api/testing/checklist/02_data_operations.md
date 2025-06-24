### Checklist Part 3: Data Operations (Sync, Entity R/W/D, Workflow)

**Tester:**
**Date:**

(Assumes setup from previous parts, including `$COMPANY_A_GUID`, tokens like `$COMP_A_ADMIN_TOKEN` or API key `$RAW_API_KEY_A` for Company A, and GUIDs for synced/created entities like `$PROJECT_S_GUID`, `$COMPONENT_S_GUID`, `$ASSEMBLY_S_GUID`, `$WORKFLOW_ENTRY_GUID`, etc.)

#### VIII. Data Synchronization Tests (`/api/v1/sync/*`) (Corresponds to Guide Section: 7)

-   [ ] **SETUP:** Use `$AUTH_HEADER_SYNC` (API key for Co. A or Co. A Admin token). Define unique codes for sync items (e.g., `$PROJECT_CODE_S`).

1.  **Sync Projects (`POST /projects`)**
    -   [ ] Sync new project to Co. A -> `200 OK`, `inserted: 1, updated: 0`. Store `$PROJECT_S_GUID` (retrieved via GET after sync).
    -   [ ] Sync same project data again (with `$PROJECT_S_GUID` if schema supports it, or by unique code) -> `200 OK`, `inserted: 0, updated: 1` (or `updated: 0` if no change).
    -   [ ] Attempt to sync project with `company_guid` for Co. B using Co. A API key/token -> `403 Forbidden`.
2.  **Sync Components (`POST /components`)** (Requires `$PROJECT_S_GUID`)
    -   [ ] Sync new component to `$PROJECT_S_GUID` -> `200 OK`, `inserted: 1`. Store `$COMPONENT_S_GUID`.
    -   [ ] Test update of this component.
    -   [ ] Attempt with invalid `$PROJECT_S_GUID` -> Error (e.g., `400` or `422` due to FK violation).
3.  **Sync Assemblies (`POST /assemblies`)** (Requires `$PROJECT_S_GUID`, `$COMPONENT_S_GUID`)
    -   [ ] Sync new assembly -> `200 OK`, `inserted: 1`. Store `$ASSEMBLY_S_GUID`.
    -   [ ] Test update.
4.  **Sync Pieces (`POST /pieces`)** (Requires parent GUIDs)
    -   [ ] Sync new piece -> `200 OK`, `inserted: 1`.
    -   [ ] Test update.
    -   [ ] Sync >1000 pieces -> `400 Bad Request`.
5.  **Sync Articles (`POST /articles`)** (Requires parent GUIDs)
    -   [ ] Sync new article -> `200 OK`, `inserted: 1`.
    -   [ ] Test update.

#### IX. Entity Read, Soft Delete & Restore Tests (Corresponds to Guide Section: 8)

(Use appropriate auth for Co. A, e.g., `$AUTH_HEADER_SYNC` or `$COMP_A_ADMIN_TOKEN`. Use entities like `$PROJECT_S_GUID`, `$COMPONENT_S_GUID` created via sync.)

**A. Projects (`/api/v1/projects`)**
-   [ ] List projects (`GET /`) for Co. A. Test `code`, `search`, `include_inactive` filters.
-   [ ] Get `$PROJECT_S_GUID` (`GET /{guid}`) -> `200 OK`, `is_active: true` (initially).
-   [ ] Soft Delete `$PROJECT_S_GUID` (`DELETE /{guid}`) -> `204 No Content`.
-   [ ] Get `$PROJECT_S_GUID` (no inactive flag) -> `404 Not Found`.
-   [ ] Get `$PROJECT_S_GUID` (`include_inactive=true`) -> `200 OK`, `is_active: false`, `deleted_at` set.
-   [ ] Restore `$PROJECT_S_GUID` (`POST /{guid}/restore`) -> `204 No Content`.
-   [ ] Get `$PROJECT_S_GUID` -> `200 OK`, `is_active: true`, `deleted_at: null`.

**B. Components (`/api/v1/components`)** (Use `$COMPONENT_S_GUID`)
-   [ ] Repeat Get, List (with filters like `project_guid`, `include_inactive`), Soft Delete, Get (inactive), Restore, Get (active) flow.

**C. Assemblies (`/api/v1/assemblies`)** (Use `$ASSEMBLY_S_GUID`)
-   [ ] Repeat Get, List (with filters), Soft Delete, Get (inactive), Restore, Get (active) flow.

**D. Pieces (`/api/v1/pieces`)** (Use a known piece GUID from sync)
-   [ ] Repeat Get, List (with filters, pagination), Soft Delete, Get (inactive), Restore, Get (active) flow.

**E. Articles (`/api/v1/articles`)** (Use a known article GUID from sync)
-   [ ] Repeat Get, List (with filters, pagination), Soft Delete, Get (inactive), Restore, Get (active) flow.

**F. Cascade Behavior**
-   [ ] Soft Delete `$PROJECT_S_GUID`. Verify `$COMPONENT_S_GUID` (child of project) is also soft-deleted (check with `include_inactive=true`, `deleted_at` timestamp).
-   [ ] Restore `$PROJECT_S_GUID`. Verify `$COMPONENT_S_GUID` is also restored.
-   [ ] Manually soft-delete a child (e.g. an Assembly). Then soft-delete its parent Component. Then restore the Component. Verify the Assembly (deleted prior) remains deleted.

#### X. Workflow Management Tests (`/api/v1/workflow`) (Corresponds to Guide Section: 9)

(Requires ProjectManager token, e.g., `$COMP_A_PM_TOKEN`. Use `$COMPANY_A_GUID`, `$WS_A_GUID`.)

1.  **Create Workflow Entry (`POST /`)**
    -   [ ] Create entry (valid `action_type`, e.g., `barcode_scan`, provide `company_guid`, `workstation_guid`, `action_value`) -> `201 Created`. Store `$WORKFLOW_ENTRY_GUID`.
    -   [ ] Verify response: `company_name`, `workstation_name`, `user_name` populated.
    -   [ ] Create entry with invalid `action_type` -> `422 Unprocessable Entity` (error lists valid types).
    -   [ ] Create entry omitting `user_guid` (should default to token user) -> `201 Created`.
2.  **List Workflow Entries (`GET /`)**
    -   [ ] List entries (use filters: `action_type`, `workstation_guid`, `limit=5`) -> `200 OK`. Entries match filters.
    -   [ ] Test `start_date` / `end_date` filters.
    -   [ ] Test pagination (`offset`, `limit`).
3.  **Get Workflow Entry (`GET /{guid}`)**
    -   [ ] Get `$WORKFLOW_ENTRY_GUID` -> `200 OK`.
4.  **Get Workflow Statistics (`GET /statistics`)**
    -   [ ] Get stats (optionally with date filters) -> `200 OK`. Response matches `WorkflowStatistics` schema. 