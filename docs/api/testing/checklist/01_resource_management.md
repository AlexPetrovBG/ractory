### Checklist Part 2: Resource Management (Users, API Keys, Workstations)

**Tester:**
**Date:**

(Assumes `$ADMIN_ACCESS_TOKEN`, `$COMPANY_A_GUID`, `$COMPANY_B_GUID` are available from previous setup)

#### V. User Management Tests (`/api/v1/users`) (Corresponds to Guide Section: 4)

-   [ ] **SETUP:** Define unique user emails (e.g., `$COMP_A_ADMIN_EMAIL`, `$COMP_A_PM_EMAIL`), password (`$USER_PASSWORD`).

1.  **Create User (`POST /`)**
    -   [ ] SystemAdmin creates CompanyAdmin for Co. A (`$COMP_A_ADMIN_EMAIL`, role `CompanyAdmin`, company `$COMPANY_A_GUID`) -> `201 Created`. Store `$COMP_A_ADMIN_GUID`.
    -   [ ] **LOGIN:** Obtain `$COMP_A_ADMIN_TOKEN` by logging in as `$COMP_A_ADMIN_EMAIL`.
    -   [ ] CompanyAdmin for Co. A (`$COMP_A_ADMIN_TOKEN`) creates ProjectManager (`$COMP_A_PM_EMAIL`, role `ProjectManager`, company `$COMPANY_A_GUID`) -> `201 Created`. Store `$COMP_A_PM_GUID`.
    -   [ ] SystemAdmin tries to create user with existing email -> `400 Bad Request`.
    -   [ ] CompanyAdmin tries to create SystemAdmin role -> `403 Forbidden`.
    -   [ ] CompanyAdmin for Co. A tries to create user in Co. B -> `403 Forbidden`.
2.  **List Users (`GET /`)**
    -   [ ] SystemAdmin lists users for `$COMPANY_A_GUID` (query param `company_guid`) -> `200 OK`. Includes created users.
    -   [ ] CompanyAdmin for Co. A (`$COMP_A_ADMIN_TOKEN`) lists users (no query param) -> `200 OK`. Shows only Co. A users.
    -   [ ] CompanyAdmin for Co. A tries to list for `$COMPANY_B_GUID` -> `403 Forbidden`.
    -   [ ] Test `role` and `active` query filters.
3.  **Get User (`GET /{guid}`)**
    -   [ ] SystemAdmin gets `$COMP_A_PM_GUID` -> `200 OK`.
    -   [ ] CompanyAdmin for Co. A (`$COMP_A_ADMIN_TOKEN`) gets `$COMP_A_PM_GUID` -> `200 OK`.
    -   [ ] CompanyAdmin for Co. A tries to get a user from Co. B (if one exists and GUID known) -> `403 Forbidden`.
4.  **Update User (`PUT /{guid}`)**
    -   [ ] CompanyAdmin for Co. A (`$COMP_A_ADMIN_TOKEN`) updates `$COMP_A_PM_GUID` (e.g., `name`, `pin`) -> `200 OK`.
    -   [ ] CompanyAdmin for Co. A tries to update `$COMP_A_PM_GUID` to `CompanyAdmin` role -> `403 Forbidden`.
    -   [ ] User tries to update their own role (get token for `$COMP_A_PM_EMAIL`) -> `403 Forbidden`.
    -   [ ] SystemAdmin updates any user's role (respecting hierarchy if applicable by design, or full power).
    -   [ ] Update with email already registered to another user -> `400 Bad Request`.
5.  **Delete User (Soft Delete) (`DELETE /{guid}`)**
    -   [ ] CompanyAdmin for Co. A (`$COMP_A_ADMIN_TOKEN`) deactivates `$COMP_A_PM_GUID` -> `200 OK` (message and GUID).
    -   [ ] Verify: Get `$COMP_A_PM_GUID` (with Co. A admin) shows `is_active: false`.
    -   [ ] SystemAdmin deactivates `$COMP_A_ADMIN_GUID` (created by SystemAdmin) -> `200 OK`.
    -   [ ] Attempt to delete own account -> `400 Bad Request`.
    -   [ ] CompanyAdmin attempts to delete SystemAdmin -> `403 Forbidden`.

#### VI. API Key Management Tests (`/api/v1/api-keys`) (Corresponds to Guide Section: 5)

(Requires `$COMP_A_ADMIN_TOKEN` for Co. A operations. `$ADMIN_ACCESS_TOKEN` for SystemAdmin specific cases.)
-   [ ] **SETUP:** Define `$API_KEY_DESC`, `$API_KEY_SCOPES` (e.g., "sync:read sync:write").

1.  **Create API Key (`POST /`)**
    -   [ ] Co. A Admin (`$COMP_A_ADMIN_TOKEN`) creates key (desc, scopes) -> `201 Created`. Key metadata + raw `key` returned. Store `$RAW_API_KEY_A` and `$API_KEY_A_GUID`.
    -   [ ] SystemAdmin creates key for Co. B (specify `company_guid: $COMPANY_B_GUID`) -> `201 Created`.
    -   [ ] Attempt to create key with non-existent `company_guid` (as SystemAdmin) -> `404 Not Found`.
    -   [ ] Attempt to provide an existing key value during creation -> Error (e.g., `409 Conflict` or `500` depending on handling, should be graceful).
    -   [ ] Attempt to create key with invalid scopes -> `422 Unprocessable Entity`.
2.  **List API Keys (`GET /`)**
    -   [ ] Co. A Admin (`$COMP_A_ADMIN_TOKEN`) lists keys -> `200 OK`. Shows key `$API_KEY_A_GUID` (no raw key). Only Co. A keys.
3.  **Get API Key (`GET /{guid}`)**
    -   [ ] Co. A Admin (`$COMP_A_ADMIN_TOKEN`) gets `$API_KEY_A_GUID` -> `200 OK`. Metadata, no raw key.
    -   [ ] Co. A Admin tries to get API key from Co. B -> `403 Forbidden` or `404 Not Found`.
4.  **Update API Key (`PUT /{guid}`)**
    -   [ ] Co. A Admin (`$COMP_A_ADMIN_TOKEN`) updates `$API_KEY_A_GUID` (description, scopes, `is_active: false`) -> `200 OK`.
    -   [ ] Verify Get `$API_KEY_A_GUID` shows changes.
5.  **Delete API Key (`DELETE /{guid}`)**
    -   [ ] Co. A Admin (`$COMP_A_ADMIN_TOKEN`) deletes `$API_KEY_A_GUID` -> `204 No Content`.
    -   [ ] Verify Get `$API_KEY_A_GUID` -> `404 Not Found`.

#### VII. Workstation Management Tests (`/api/v1/workstations`) (Corresponds to Guide Section: 6)

(Requires `$COMP_A_ADMIN_TOKEN` for Co. A. `$ADMIN_ACCESS_TOKEN` can manage any if `company_guid` is specified).
-   [ ] **SETUP:** Define `$WS_LOCATION` (e.g., "Assembly WS1 $(date +%N)"), `$WS_TYPE` ("Assembly").

1.  **Create Workstation (`POST /`)**
    -   [ ] Co. A Admin (`$COMP_A_ADMIN_TOKEN`) creates workstation (`location`, `type`) for Co. A (implicit company) -> `201 Created`. Store `$WS_A_GUID`.
    -   [ ] SystemAdmin creates workstation for Co. B (explicit `company_guid: $COMPANY_B_GUID`) -> `201 Created`.
    -   [ ] Co. A Admin tries to create for Co. B (explicit `company_guid`) -> `403 Forbidden`.
    -   [ ] Invalid `type` enum -> `422 Unprocessable Entity`.
2.  **List Workstations (`GET /`)**
    -   [ ] Co. A Admin lists (no query param) -> `200 OK`. Only Co. A workstations. Includes `$WS_A_GUID`.
    -   [ ] SystemAdmin lists for Co. A (query `company_guid=$COMPANY_A_GUID`) -> `200 OK`.
    -   [ ] Test filters: `type`, `active`, `location` (substring match).
3.  **Get Workstation (`GET /{guid}`)**
    -   [ ] Co. A Admin gets `$WS_A_GUID` -> `200 OK`.
4.  **Update Workstation (`PUT /{guid}`)**
    -   [ ] Co. A Admin updates `$WS_A_GUID` (new `location`, `is_active: false`) -> `200 OK`.
5.  **Delete Workstation (Soft Delete) (`DELETE /{guid}`)**
    -   [ ] Co. A Admin deactivates `$WS_A_GUID` -> `200 OK` (message and GUID).
    -   [ ] Verify: Get `$WS_A_GUID` shows `is_active: false`. 