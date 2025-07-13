### Checklist Part 2: Resource Management (Users, API Keys, Workstations)

**Tester:**
**Date:**

(Assumes `$ADMIN_ACCESS_TOKEN`, `$COMPANY_A_GUID`, `$COMPANY_B_GUID` are available from previous setup)

#### V. User Management Tests (`/api/v1/users`) (Corresponds to Guide Section: 4) - DONE

-   [x] **SETUP:** Define unique user emails (e.g., `$COMP_A_ADMIN_EMAIL`, `$COMP_A_PM_EMAIL`), password (`$USER_PASSWORD`). ✅ DONE

1.  **Create User (`POST /`) - DONE**
    -   [x] SystemAdmin creates CompanyAdmin for Co. A (`$COMP_A_ADMIN_EMAIL`, role `CompanyAdmin`, company `$COMPANY_A_GUID`) -> `201 Created`. Store `$COMP_A_ADMIN_GUID`. ✅ DONE
    -   [x] **LOGIN:** Obtain `$COMP_A_ADMIN_TOKEN` by logging in as `$COMP_A_ADMIN_EMAIL`. ✅ DONE
    -   [x] CompanyAdmin for Co. A (`$COMP_A_ADMIN_TOKEN`) creates ProjectManager (`$COMP_A_PM_EMAIL`, role `ProjectManager`, company `$COMPANY_A_GUID`) -> `201 Created`. Store `$COMP_A_PM_GUID`. ✅ DONE
    -   [x] SystemAdmin tries to create user with existing email -> `400 Bad Request`. ✅ DONE
    -   [x] CompanyAdmin tries to create SystemAdmin role -> `403 Forbidden`. ✅ DONE
    -   [x] CompanyAdmin for Co. A tries to create user in Co. B -> `403 Forbidden`. ✅ DONE
2.  **List Users (`GET /`) - DONE**
    -   [x] SystemAdmin lists users for `$COMPANY_A_GUID` (query param `company_guid`) -> `200 OK`. Includes created users. ✅ DONE
    -   [x] CompanyAdmin for Co. A (`$COMP_A_ADMIN_TOKEN`) lists users (no query param) -> `200 OK`. Shows only Co. A users. ✅ DONE
    -   [x] CompanyAdmin for Co. A tries to list for `$COMPANY_B_GUID` -> `403 Forbidden`. ✅ DONE
    -   [x] Test `role` and `active` query filters. ✅ DONE
3.  **Get User (`GET /{guid}) - DONE**
    -   [x] SystemAdmin gets `$COMP_A_PM_GUID` -> `200 OK`. ✅ DONE
    -   [x] CompanyAdmin for Co. A (`$COMP_A_ADMIN_TOKEN`) gets `$COMP_A_PM_GUID` -> `200 OK`. ✅ DONE
    -   [ ] CompanyAdmin for Co. A tries to get a user from Co. B (if one exists and GUID known) -> `403 Forbidden`.
4.  **Update User (`PUT /{guid}) - DONE**
    -   [x] CompanyAdmin for Co. A (`$COMP_A_ADMIN_TOKEN`) updates `$COMP_A_PM_GUID` (e.g., `name`, `pin`) -> `200 OK`. ✅ DONE
    -   [x] CompanyAdmin for Co. A tries to update `$COMP_A_PM_GUID` to `CompanyAdmin` role -> `403 Forbidden`. ✅ DONE
    -   [x] User tries to update their own role (get token for `$COMP_A_PM_EMAIL`) -> `403 Forbidden`. ✅ DONE
    -   [x] SystemAdmin updates any user's role (respecting hierarchy if applicable by design, or full power). ✅ DONE
    -   [x] Update with email already registered to another user -> `400 Bad Request`. ✅ DONE
5.  **Delete User (Soft Delete) (`DELETE /{guid}) - DONE**
    -   [x] CompanyAdmin for Co. A (`$COMP_A_ADMIN_TOKEN`) deactivates `$COMP_A_PM_GUID` -> `200 OK` (message and GUID). ✅ DONE
    -   [x] Verify: Get `$COMP_A_PM_GUID` (with Co. A admin) shows `is_active: false`. ✅ DONE
    -   [x] SystemAdmin deactivates `$COMP_A_ADMIN_GUID` (created by SystemAdmin) -> `200 OK`. ✅ DONE
    -   [x] Attempt to delete own account -> `400 Bad Request`. ✅ DONE
    -   [x] CompanyAdmin attempts to delete SystemAdmin -> `403 Forbidden`. ✅ DONE

#### VI. API Key Management Tests (`/api/v1/api-keys`) (Corresponds to Guide Section: 5) - DONE

(Requires `$COMP_A_ADMIN_TOKEN` for Co. A operations. `$ADMIN_ACCESS_TOKEN` for SystemAdmin specific cases.)
-   [x] **SETUP:** Define `$API_KEY_DESC`, `$API_KEY_SCOPES` (e.g., "sync:read sync:write"). ✅ DONE

1.  **Create API Key (`POST /`) - DONE**
    -   [x] Co. A Admin (`$COMP_A_ADMIN_TOKEN`) creates key (desc, scopes) -> `201 Created`. Key metadata + raw `key` returned. Store `$RAW_API_KEY_A` and `$API_KEY_A_GUID`. ✅ DONE
    -   [x] SystemAdmin creates key for Co. B (specify `company_guid: $COMPANY_B_GUID`) -> `201 Created`. ✅ DONE
    -   [x] Attempt to create key with non-existent `company_guid` (as SystemAdmin) -> `404 Not Found`. ✅ DONE
    -   [ ] Attempt to provide an existing key value during creation -> Error (e.g., `409 Conflict` or `500` depending on handling, should be graceful).
    -   [x] Attempt to create key with invalid scopes -> `422 Unprocessable Entity`. ✅ DONE
2.  **List API Keys (`GET /) - DONE**
    -   [x] Co. A Admin (`$COMP_A_ADMIN_TOKEN`) lists keys -> `200 OK`. Shows key `$API_KEY_A_GUID` (no raw key). Only Co. A keys. ✅ DONE
3.  **Get API Key (`GET /{guid}) - DONE**
    -   [x] Co. A Admin (`$COMP_A_ADMIN_TOKEN`) gets `$API_KEY_A_GUID` -> `200 OK`. Metadata, no raw key. ✅ DONE
    -   [x] Co. A Admin tries to get API key from Co. B -> `403 Forbidden` or `404 Not Found`. ✅ DONE
4.  **Update API Key (`PUT /{guid}) - DONE**
    -   [x] Co. A Admin (`$COMP_A_ADMIN_TOKEN`) updates `$API_KEY_A_GUID` (description, scopes, `is_active: false`) -> `200 OK`. ✅ DONE
    -   [x] Verify Get `$API_KEY_A_GUID` shows changes. ✅ DONE
5.  **Delete API Key (`DELETE /{guid}) - DONE**
    -   [x] Co. A Admin (`$COMP_A_ADMIN_TOKEN`) deletes `$API_KEY_A_GUID` -> `204 No Content`. ✅ DONE
    -   [x] Verify Get `$API_KEY_A_GUID` -> `404 Not Found`. ✅ DONE

#### VII. Workstation Management Tests (`/api/v1/workstations`) (Corresponds to Guide Section: 6) - DONE

(Requires `$COMP_A_ADMIN_TOKEN` for Co. A. `$ADMIN_ACCESS_TOKEN` can manage any if `company_guid` is specified).
-   [x] **SETUP:** Define `$WS_LOCATION` ✅ DONE

1.  **Create Workstation (`POST /`) - DONE**
    -   [x] CompanyAdmin creates workstation (location, type) -> `201 Created`. Store `$WS_A_GUID`. ✅ DONE
    -   [x] Test validation: missing required fields -> `422 Unprocessable Entity`. ✅ DONE
    -   [x] SystemAdmin creates workstation for different company (with company_guid) -> `201 Created`. ✅ DONE
    -   [x] Test invalid workstation type validation -> `422 Unprocessable Entity`. ✅ DONE
2.  **List Workstations (`GET /`) - DONE**
    -   [x] CompanyAdmin lists workstations -> `200 OK`. Shows only company workstations. ✅ DONE
3.  **Get Workstation (`GET /{guid}) - DONE**
    -   [x] CompanyAdmin gets workstation -> `200 OK`. ✅ DONE
    -   [x] CompanyAdmin tries to get workstation from other company -> `403 Forbidden`. ✅ DONE
4.  **Update Workstation (`PUT /{guid}) - DONE**
    -   [x] CompanyAdmin updates workstation (location, type, is_active) -> `200 OK`. ✅ DONE
5.  **Delete Workstation (Soft Delete) (`DELETE /{guid}) - DONE**
    -   [x] CompanyAdmin deactivates workstation -> Success message with GUID. ✅ DONE
    -   [x] Verify workstation shows `is_active: false` after soft delete. ✅ DONE