### Checklist Part 1: Environment, Setup, Health, Auth, Companies

**Tester:**
**Date:**

#### I. Environment & Setup (Corresponds to Guide Section: Setup)

-   [ ] Development environment (Docker, services) started successfully.
-   [ ] Database connection verified (e.g., via pgAdmin or DBeaver).
-   [ ] Initial SystemAdmin user exists and credentials are known (`$ADMIN_EMAIL`, `$ADMIN_PASSWORD`).
-   [ ] `$ADMIN_ACCESS_TOKEN` and `$ADMIN_REFRESH_TOKEN` obtained successfully for SystemAdmin.

#### II. Health Check Tests (Corresponds to Guide Section: 1)

-   [ ] `GET /health` returns `200 OK`.
-   [ ] `GET /health` response contains `status: healthy` and `version`, `api_version`.
-   [ ] `GET /api/v1/health` returns `200 OK`.
-   [ ] `GET /api/v1/health` response contains `status: healthy`, `version`, `api_version`, `environment`, and `database: connected`.

#### III. Authentication Tests (`/api/v1/auth/*`) (Corresponds to Guide Section: 2)

**A. JWT Authentication**
1.  **Login (`POST /login`)**
    -   [ ] Valid SystemAdmin credentials (`$ADMIN_EMAIL`/`$ADMIN_PASSWORD`) -> `200 OK`, tokens, `role: SystemAdmin`, `expires_in`.
    -   [ ] Valid regular user credentials (once created, e.g., `$COMP_A_ADMIN_EMAIL`) -> `200 OK`, tokens, correct role.
    -   [ ] Invalid password for existing email -> `401 Unauthorized`.
    -   [ ] Non-existent email -> `401 Unauthorized`.
    -   [ ] Empty/missing credentials in request body -> `422 Unprocessable Entity`.
2.  **Refresh Token (`POST /refresh`)**
    -   [ ] Valid `$ADMIN_REFRESH_TOKEN` (from body) -> `200 OK`, new tokens, `role: SystemAdmin`.
    -   [ ] Invalid/expired `refresh_token` -> `401 Unauthorized`.
    -   [ ] Missing `refresh_token` (empty body and no cookie) -> `401 Unauthorized`.
3.  **Get Current User Info (`GET /me`)**
    -   [ ] With `$ADMIN_ACCESS_TOKEN` -> `200 OK`, correct SystemAdmin details, `auth_type: jwt`.
    -   [ ] With an API Key (e.g., `$RAW_API_KEY_A` created later) -> `200 OK`, API key details, `auth_type: api_key`, correct scopes.
    -   [ ] With invalid/expired token -> `401 Unauthorized`.
    -   [ ] With no token -> `401 Unauthorized`.

**B. QR Authentication (`POST /qr`)**
    (Requires setup: Operator user `$OPERATOR_USER_GUID`, Workstation `$WORKSTATION_GUID`, valid `$OPERATOR_PIN`)
-   [ ] Valid QR data (`$OPERATOR_USER_GUID`, `$WORKSTATION_GUID`, `$OPERATOR_PIN`) -> `200 OK`, tokens, `role: Operator`.
-   [ ] Invalid `$OPERATOR_USER_GUID` -> `401 Unauthorized`.
-   [ ] Invalid `$WORKSTATION_GUID` (non-existent) -> `400 Bad Request` (Workstation not found).
-   [ ] Invalid `$OPERATOR_PIN` -> `401 Unauthorized`.

**C. Protected Route (`GET /protected`)**
-   [ ] With `$ADMIN_ACCESS_TOKEN` -> `200 OK`, correct response confirming SystemAdmin access.
-   [ ] With a non-SystemAdmin token (e.g., `$COMP_A_ADMIN_TOKEN` once created) -> `403 Forbidden`.

**D. Mock Authentication (`POST /mock-auth`)**
-   [ ] Credentials `a.petrov@delice.bg / password` -> `200 OK`, mock tokens, `role: CompanyAdmin`.
-   [ ] Different credentials -> Mock response with `role: Guest` or similar.

#### IV. Company Management Tests (`/api/v1/companies`) (Corresponds to Guide Section: 3)

(All tests in this section require `$ADMIN_ACCESS_TOKEN`)
-   [ ] **SETUP:** Shell variables `$COMPANY_A_NAME`, `$COMPANY_A_CODE`, `$COMPANY_A_INDEX` (e.g., 90), and similar for `$COMPANY_B_NAME` (e.g., index 91) are defined with unique values for the test run.

1.  **Create Company (`POST /`)**
    -   [ ] Create Company A (using defined variables) -> `201 Created`. Response has `guid`. Store `$COMPANY_A_GUID`.
    -   [ ] Create Company B -> `201 Created`. Store `$COMPANY_B_GUID`.
    -   [ ] Attempt to create with `$COMPANY_A_NAME` again -> `409 Conflict`.
    -   [ ] Attempt to create with `$COMPANY_A_INDEX` again -> `409 Conflict`.
    -   [ ] Attempt `company_index` < 0 -> `422 Unprocessable Entity`.
    -   [ ] Attempt `company_index` > 99 -> `422 Unprocessable Entity`.
    -   [ ] Request missing `name` -> `422 Unprocessable Entity`.
2.  **List Companies (`GET /`)**
    -   [ ] List -> `200 OK`. Response includes Company A & B.
    -   [ ] Test `skip` & `limit` (e.g., `limit=1`, then `skip=1, limit=1`).
3.  **Get Company (`GET /{company_guid}`)**
    -   [ ] Get Company A (using `$COMPANY_A_GUID`) -> `200 OK`, correct details.
    -   [ ] Get with a non-existent GUID -> `404 Not Found`.
4.  **Update Company (`PATCH` and `PUT`)**
    -   [ ] `PATCH` Company A: update `name` (append " Updated"), set `is_active: false` -> `200 OK`. Response shows changes.
    -   [ ] Get Company A again: verify updated `name` and `is_active: false`.
    -   [ ] `PATCH` Company A: try to set `company_index` to `$COMPANY_B_INDEX` -> `409 Conflict`.
    -   [ ] `PUT` Company B: full update with new valid data (e.g., new code, index) -> `200 OK`.
5.  **Delete Company (`DELETE /{company_guid}`)**
    -   [ ] Delete Company B (using `$COMPANY_B_GUID`) -> `204 No Content`.
    -   [ ] Get Company B -> `404 Not Found`.
    -   [ ] Delete non-existent company GUID -> `404 Not Found`. 