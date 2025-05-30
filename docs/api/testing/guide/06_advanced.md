## 10. Multi-Tenant Isolation Tests

These tests are critical for ensuring data security and integrity between different companies (tenants).

**Core Principle:** A user/API key belonging to Company A should **NEVER** be able to read, create, update, or delete data belonging to Company B, unless that user has a `SystemAdmin` role.

**Setup:**
1.  Ensure you have at least two companies created: Company A (`$COMPANY_A_GUID`) and Company B (`$COMPANY_B_GUID`).
2.  Ensure you have users and/or API keys specific to each company:
    *   `$COMP_A_ADMIN_TOKEN` (CompanyAdmin for Company A)
    *   `$RAW_API_KEY_A` (API Key for Company A)
    *   Create a CompanyAdmin for Company B (`$COMP_B_ADMIN_EMAIL`, `$COMP_B_ADMIN_PASSWORD`) and get their token (`$COMP_B_ADMIN_TOKEN`).
    *   Create an API Key for Company B (`$RAW_API_KEY_B`).
3.  Ensure some data (e.g., a project `$PROJECT_A_SAMPLE_GUID`) exists in Company A, and different data (e.g., `$PROJECT_B_SAMPLE_GUID`) exists in Company B.

**Test Scenarios (Repeat for various entity types - Users, Workstations, Projects, API Keys, etc.):**

1.  **Read Isolation:**
    *   User from Company A tries to GET data from Company B (e.g., `GET /api/v1/projects/$PROJECT_B_SAMPLE_GUID` using `$COMP_A_ADMIN_TOKEN`). **Expected: `403 Forbidden` or `404 Not Found`.**
    *   API Key for Company A tries to GET data from Company B. **Expected: `403` or `404`.**
    *   SystemAdmin (`$ADMIN_ACCESS_TOKEN`) attempts to GET data from Company B by specifying `company_guid=$COMPANY_B_GUID` in list endpoints, or by direct GUID access. **Expected: `200 OK` with Company B data.**

2.  **Create Isolation (for resources not managed by Sync, e.g., Users, Workstations, non-SystemAdmin API Keys):**
    *   User from Company A tries to POST new data intended for Company B (e.g., create a workstation and set `company_guid` to `$COMPANY_B_GUID`). **Expected: `403 Forbidden` (unless SystemAdmin).**

3.  **Update Isolation:**
    *   User from Company A tries to PUT/PATCH data in Company B. **Expected: `403` or `404`.**

4.  **Delete Isolation:**
    *   User from Company A tries to DELETE data in Company B. **Expected: `403` or `404`.**

5.  **Sync Endpoint Isolation:**
    *   API Key for Company A (`$RAW_API_KEY_A`) attempts to sync data with `company_guid` explicitly set to `$COMPANY_B_GUID` in the payload items. **Expected: `403 Forbidden`.**
    *   Sync payload items for Company A must all have `company_guid: $COMPANY_A_GUID` or be rejected if the key/token is for Company A.

6.  **List Endpoint Filtering:**
    *   When a non-SystemAdmin lists resources (e.g., `GET /api/v1/projects`), ensure only data from their own company is returned, even if no `company_guid` filter is applied by the client (RLS and backend logic should enforce this).
    *   SystemAdmin using list endpoints without `company_guid` filter might see data from their *own* default company or all, depending on implementation (clarify expected behavior). With `company_guid` filter, they should see specific company data.

**Automated Tests:**
Refer to `src/ractory/backend/isolation_test.py` and `src/ractory/backend/tests/test_multi_tenant_isolation.py` for more comprehensive automated test scenarios that should be run regularly.

## 11. Error Handling & Edge Case Tests

-   **Invalid Input Validation (`422 Unprocessable Entity`, `400 Bad Request`):**
    -   Send requests with missing required fields for POST/PUT operations.
    -   Send requests with invalid data types (e.g., string where int expected, invalid UUID format, invalid enum values).
    -   Test boundary conditions for numerical inputs (e.g., negative numbers where positive expected, values exceeding limits like `company_index`).
    -   Test string length limits if defined by schemas.
    -   Malformed JSON in request body.
-   **Authentication Errors (`401 Unauthorized`):**
    -   Request to protected endpoint with no `Authorization` or `X-API-Key` header.
    -   Expired JWT token.
    -   Invalid JWT token signature or malformed token.
    -   Invalid or revoked API key.
-   **Authorization Errors (`403 Forbidden`):**
    -   User with insufficient role attempts an action (e.g., ProjectManager tries to create a user).
    -   Cross-tenant access attempts by non-SystemAdmins (covered in multi-tenancy).
    -   API Key with insufficient scopes attempts an action (e.g., key with `sync:read` tries to use a `sync:write` endpoint).
-   **Resource Not Found (`404 Not Found`):**
    -   GET, PUT, DELETE requests using a non-existent GUID for an entity.
    -   Accessing a valid GUID but for an entity in another tenant (can also be 403 depending on specific check order).
-   **Method Not Allowed (`405 Method Not Allowed`):**
    -   e.g., Trying to `PUT` to an endpoint that only supports `POST`.
-   **Rate Limiting (`429 Too Many Requests`):**
    -   If rate limiting is implemented, script rapid requests to an endpoint to trigger it.
-   **Server Errors (`500 Internal Server Error`):**
    -   While harder to test predictably, consider if any specific inputs might cause unhandled exceptions (e.g., extremely large, malformed but parsable data for complex fields).
-   **Idempotency for Sync/Update:**
    -   For `sync` endpoints, sending the exact same payload multiple times should ideally result in the same state (e.g., first call inserts, subsequent calls update with no changes or report 0 updates if data matches).
-   **Cascade Operations (Soft Delete/Restore):**
    -   Verify that deleting a parent correctly soft-deletes active children.
    -   Verify that restoring a parent correctly restores children that were deleted *as part of that same cascade* (matching `deleted_at` timestamps).
    -   Children deleted independently prior to parent deletion should remain deleted upon parent restoration.
    -   An entity reactivated via sync should have `is_active: true` and `deleted_at: null`. 