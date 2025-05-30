### Checklist Part 2: Resource Management (Users, API Keys, Workstations)

**Tester:**
**Date:**

(Assumes `$ADMIN_ACCESS_TOKEN`, `$COMPANY_A_GUID`, `$COMPANY_B_GUID` are available from previous setup)

#### V. User Management Tests (`/api/v1/users`) (Corresponds to Guide Section: 4)

-   [X] **SETUP:** Define unique user emails (e.g., `$COMP_A_ADMIN_EMAIL`, `$COMP_A_PM_EMAIL`), password (`$USER_PASSWORD`).

1.  **Create User (`POST /`)**
    -   [X] SystemAdmin creates CompanyAdmin for Co. A (`$COMP_A_ADMIN_EMAIL`, role `CompanyAdmin`, company `$COMPANY_A_GUID`) -> `201 Created`. Store `$COMP_A_ADMIN_GUID`.
    -   [X] **LOGIN:** Obtain `$COMP_A_ADMIN_TOKEN` by logging in as `$COMP_A_ADMIN_EMAIL`.
    -   [X] CompanyAdmin for Co. A (`$COMP_A_ADMIN_TOKEN`) creates ProjectManager (`$COMP_A_PM_EMAIL`, role `ProjectManager`, company `$COMPANY_A_GUID`) -> `201 Created`. Store `$COMP_A_PM_GUID`.
    -   [X] SystemAdmin tries to create user with existing email -> `400 Bad Request`.
    -   [X] CompanyAdmin tries to create SystemAdmin role -> `403 Forbidden`.
    -   [X] CompanyAdmin for Co. A tries to create user in Co. B -> `403 Forbidden`.
2.  **List Users (`GET /`)**
    -   [X] SystemAdmin lists users for `$COMPANY_A_GUID` (query param `company_guid`) -> `200 OK`. Includes created users.
    -   [X] CompanyAdmin for Co. A (`$COMP_A_ADMIN_TOKEN`) lists users (no query param) -> `200 OK`. Shows only Co. A users.
    -   [X] CompanyAdmin for Co. A tries to list for `$COMPANY_B_GUID` -> `403 Forbidden`.
    -   [X] Test `role` and `active` query filters.
3.  **Get User (`GET /{guid}`)**
    -   [X] SystemAdmin gets `$COMP_A_PM_GUID` -> `200 OK`.
    -   [X] CompanyAdmin for Co. A (`$COMP_A_ADMIN_TOKEN`) gets `$COMP_A_PM_GUID` -> `200 OK`.
    -   [X] CompanyAdmin for Co. A tries to get a user from Co. B (if one exists and GUID known) -> `403 Forbidden`.
4.  **Update User (`PUT /{guid}`)**
    -   [X] CompanyAdmin for Co. A (`$COMP_A_ADMIN_TOKEN`) updates `$COMP_A_PM_GUID` (e.g., `name`, `pin`) -> `200 OK`.
    -   [X] CompanyAdmin for Co. A tries to update `$COMP_A_PM_GUID` to `CompanyAdmin` role -> `403 Forbidden`.
    -   [X] User tries to update their own role (get token for `$COMP_A_PM_EMAIL`) -> `403 Forbidden`.
    -   [X] SystemAdmin updates any user's role (respecting hierarchy if applicable by design, or full power).
    -   [X] Update with email already registered to another user -> `400 Bad Request`.
5.  **Delete User (Soft Delete) (`DELETE /{guid}`)**
    -   [X] CompanyAdmin for Co. A (`$COMP_A_ADMIN_TOKEN`) deactivates `$COMP_A_PM_GUID` -> `200 OK` (message and GUID).
    -   [X] Verify: Get `$COMP_A_PM_GUID` (with Co. A admin) shows `is_active: false`.
    -   [X] SystemAdmin deactivates `$COMP_A_ADMIN_GUID` (created by SystemAdmin) -> `200 OK`.
    -   [X] Attempt to delete own account -> `400 Bad Request`.
    -   [X] CompanyAdmin attempts to delete SystemAdmin -> `403 Forbidden`.

#### VI. API Key Management Tests (`/api/v1/api-keys`) (Corresponds to Guide Section: 5)

(Requires `$COMP_A_ADMIN_TOKEN` for Co. A operations. `$ADMIN_ACCESS_TOKEN` for SystemAdmin specific cases.)
-   [X] **SETUP:** Define `$API_KEY_DESC`, `$API_KEY_SCOPES` (e.g., "sync:read sync:write").

1.  **Create API Key (`POST /`)**
    -   [X] Co. A Admin (`$COMP_A_ADMIN_TOKEN`) creates key (desc, scopes) -> `201 Created`. Key metadata + raw `key` returned. Store `$RAW_API_KEY_A` and `$API_KEY_A_GUID`.
    -   [X] SystemAdmin creates key for Co. B (specify `company_guid: $COMPANY_B_GUID`) -> `201 Created`.
    -   [X] Attempt to create key with non-existent `company_guid` (as SystemAdmin) -> `404 Not Found`.
    -   [X] Attempt to provide an existing key value during creation -> Error (e.g., `409 Conflict` or `500` depending on handling, should be graceful).
    -   [X] Attempt to create key with invalid scopes -> `422 Unprocessable Entity`.
2.  **List API Keys (`GET /`)**
    -   [X] Co. A Admin (`$COMP_A_ADMIN_TOKEN`) lists keys -> `200 OK`. Shows key `$API_KEY_A_GUID` (no raw key). Only Co. A keys.
3.  **Get API Key (`GET /{guid}`)**
    -   [X] Co. A Admin (`$COMP_A_ADMIN_TOKEN`) gets `$API_KEY_A_GUID` -> `200 OK`. Metadata, no raw key.
    -   [X] Co. A Admin tries to get API key from Co. B -> `403 Forbidden` or `404 Not Found`.
4.  **Update API Key (`PUT /{guid}`)**
    -   [X] Co. A Admin (`$COMP_A_ADMIN_TOKEN`) updates `$API_KEY_A_GUID` (description, scopes, `is_active: false`) -> `200 OK`.
    -   [X] Verify Get `$API_KEY_A_GUID` shows changes.
5.  **Delete API Key (`DELETE /{guid}`)**
    -   [X] Co. A Admin (`$COMP_A_ADMIN_TOKEN`) deletes `$API_KEY_A_GUID` -> `204 No Content`.
    -   [X] Verify Get `$API_KEY_A_GUID` -> `404 Not Found`.

#### VII. Workstation Management Tests (`/api/v1/workstations`) (Corresponds to Guide Section: 6)

(Requires `$COMP_A_ADMIN_TOKEN` for Co. A. `$ADMIN_ACCESS_TOKEN` can manage any if `company_guid` is specified).
-   [X] **SETUP:** Define `$WS_LOCATION` (e.g., "Assembly WS1 $(date +%N)"), `$WS_TYPE` ("Assembly").

1.  **Create Workstation (`POST /`)**
    -   [X] Co. A Admin (`$COMP_A_ADMIN_TOKEN`) creates workstation (`location`, `type`) for Co. A (implicit company) -> `201 Created`. Store `$WS_A_GUID`.
    -   [X] SystemAdmin creates workstation for Co. B (explicit `company_guid: $COMPANY_B_GUID`) -> `201 Created`.
    -   [X] Co. A Admin tries to create for Co. B (explicit `company_guid`) -> `403 Forbidden`.
    -   [X] Invalid `type` enum -> `422 Unprocessable Entity`.
2.  **List Workstations (`GET /`)**
    -   [X] Co. A Admin lists (no query param) -> `200 OK`. Only Co. A workstations. Includes `$WS_A_GUID`.
    -   [X] SystemAdmin lists for Co. A (query `company_guid=$COMPANY_A_GUID`) -> `200 OK`.
    -   [X] Test filters: `type`, `active`, `location` (substring match).
3.  **Get Workstation (`GET /{guid}`)**
    -   [X] Co. A Admin gets `$WS_A_GUID` -> `200 OK`.
4.  **Update Workstation (`PUT /{guid}`)**
    -   [X] Co. A Admin updates `$WS_A_GUID` (new `location`, `is_active: false`) -> `200 OK`.
5.  **Delete Workstation (Soft Delete) (`DELETE /{guid}`)**
    -   [X] Co. A Admin deactivates `$WS_A_GUID` -> `200 OK` (message and GUID).
    -   [X] Verify: Get `$WS_A_GUID` shows `is_active: false`. 