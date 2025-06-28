### Checklist Part 1: Environment, Setup, Health, Auth, Companies

**Tester:**
**Date:**

#### I. Environment & Setup (Corresponds to Guide Section: Setup)

-   [x] Development environment (Docker, services) started successfully.
-   [x] Initial SystemAdmin user exists and credentials are known (`$ADMIN_EMAIL`, `$ADMIN_PASSWORD`).
-   [x] `$ADMIN_ACCESS_TOKEN` and `$ADMIN_REFRESH_TOKEN` obtained successfully for SystemAdmin.

#### II. Health Check Tests (Corresponds to Guide Section: 1) - DONE

-   [x] `GET /health` returns `200 OK`. ✅ DONE
-   [x] `GET /health` response contains `status: healthy` and `version`, `api_version`. ✅ DONE
-   [x] `GET /api/v1/health` returns `200 OK`. ✅ DONE
-   [x] `GET /api/v1/health` response contains `status: healthy`, `version`, `api_version`, `environment`, and `database: connected`. ✅ DONE

#### III. Authentication Tests (`/api/v1/auth/*`) (Corresponds to Guide Section: 2)

**A. JWT Authentication - DONE**
1.  **Login (`POST /login`) - DONE**
    -   [x] Valid SystemAdmin credentials (`$ADMIN_EMAIL`/`$ADMIN_PASSWORD`) -> `200 OK`, tokens, `role: SystemAdmin`, `expires_in`. ✅ DONE
    -   [ ] Valid regular user credentials (once created, e.g., `$COMP_A_ADMIN_EMAIL`) -> `200 OK`, tokens, correct role.
    -   [x] Invalid password for existing email -> `401 Unauthorized`. ✅ DONE
    -   [x] Non-existent email -> `401 Unauthorized`. ✅ DONE
    -   [x] Empty/missing credentials in request body -> `422 Unprocessable Entity`. ✅ DONE
2.  **Refresh Token (`POST /refresh`) - DONE**
    -   [x] Valid `$ADMIN_REFRESH_TOKEN` (from body) -> `200 OK`, new tokens, `role: SystemAdmin`. ✅ DONE
    -   [x] Invalid/expired `refresh_token` -> `401 Unauthorized`. ✅ DONE
    -   [x] Missing `refresh_token` (empty body and no cookie) -> `422 Unprocessable Entity`. ✅ DONE
3.  **Get Current User Info (`GET /me`) - DONE**
    -   [x] With `$ADMIN_ACCESS_TOKEN` -> `200 OK`, correct SystemAdmin details, `auth_type: jwt`. ✅ DONE
    -   [x] With invalid/expired token -> `401 Unauthorized`. ✅ DONE
    -   [x] With no token -> `401 Unauthorized`. ✅ DONE

**B. QR Authentication (`POST /qr`)**
    (Requires setup: Operator user `$OPERATOR_USER_GUID`, Workstation `$WORKSTATION_GUID`, valid `$OPERATOR_PIN`)
-   [ ] Valid QR data (`$OPERATOR_USER_GUID`, `$WORKSTATION_GUID`, `$OPERATOR_PIN`) -> `200 OK`, tokens, `role: Operator`.
-   [ ] Invalid `$OPERATOR_USER_GUID` -> `401 Unauthorized`.
-   [ ] Invalid `$WORKSTATION_GUID` (non-existent) -> `400 Bad Request` (Workstation not found).
-   [ ] Invalid `$OPERATOR_PIN` -> `401 Unauthorized`.

**C. Protected Route (`GET /protected`) - PARTIALLY DONE**
-   [x] With `$ADMIN_ACCESS_TOKEN` -> `200 OK`, correct response confirming SystemAdmin access. ✅ DONE
-   [ ] With a non-SystemAdmin token (e.g., `$COMP_A_ADMIN_TOKEN` once created) -> `403 Forbidden`.

**D. Mock Authentication (`POST /mock-auth`)**
-   [ ] Credentials `a.petrov@delice.bg / password` -> `200 OK`, mock tokens, `role: CompanyAdmin`.
-   [ ] Different credentials -> Mock response with `role: Guest` or similar.

#### IV. Company Management Tests (`/api/v1/companies`) (Corresponds to Guide Section: 3) - DONE

(All tests in this section require `$ADMIN_ACCESS_TOKEN`)
-   [x] **SETUP:** Shell variables `$COMPANY_A_NAME`, `$COMPANY_A_CODE`, `$COMPANY_A_INDEX` (e.g., 90), and similar for `$COMPANY_B_NAME` (e.g., index 91) are defined with unique values for the test run. ✅ DONE

1.  **Create Company (`POST /`) - DONE**
    -   [x] Create Company A (using defined variables) -> `201 Created`. Response has `guid`. Store `$COMPANY_A_GUID`. ✅ DONE
    -   [x] Create Company B -> `201 Created`. Store `$COMPANY_B_GUID`. ✅ DONE
    -   [x] Attempt to create with `$COMPANY_A_NAME` again -> `409 Conflict`. ✅ DONE
    -   [x] Attempt to create with `$COMPANY_A_INDEX` again -> `409 Conflict`. ✅ DONE
    -   [x] Attempt `company_index` < 0 -> `422 Unprocessable Entity`. ✅ DONE
    -   [x] Attempt `company_index` > 99 -> `422 Unprocessable Entity`. ✅ DONE
    -   [x] Request missing `name` -> `422 Unprocessable Entity`. ✅ DONE
2.  **List Companies (`GET /`) - DONE**
    -   [x] List -> `200 OK`. Response includes Company A & B. ✅ DONE
    -   [x] Test `skip` & `limit` (e.g., `limit=1`, then `skip=1, limit=1`). ✅ DONE
    -   [x] Get Company A (using `$COMPANY_A_GUID`) -> `200 OK`, correct details. ✅ DONE
    -   [x] Get with a non-existent GUID -> `404 Not Found`. ✅ DONE
3.  **Update Company A - DONE**
    -   [x] `PATCH` Company A: update `name` (append " Updated"), set `is_active: false` -> `200 OK`. Response shows changes. ✅ DONE
    -   [x] Get Company A again: verify updated `name` and `is_active: false`. ✅ DONE
    -   [x] `PATCH` Company A: try to set `company_index` to `$COMPANY_B_INDEX` -> `409 Conflict`. ✅ DONE
4.  **Update Company B - DONE**
    -   [x] `PUT` Company B: full update with new valid data (e.g., new code, index) -> `200 OK`. ✅ DONE
    -   [x] Delete Company B (using `$COMPANY_B_GUID`) -> `204 No Content`. ✅ DONE
    -   [x] Get Company B -> `404 Not Found`. ✅ DONE
    -   [x] Delete non-existent company GUID -> `404 Not Found`. ✅ DONE