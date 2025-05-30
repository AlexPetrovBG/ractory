### Checklist Part 4: Advanced & General Tests

**Tester:**
**Date:**

(Assumes setup from previous parts, including multiple companies like `$COMPANY_A_GUID`, `$COMPANY_B_GUID`, and various user/API key tokens for them.)

#### XI. Multi-Tenant Isolation Tests (Corresponds to Guide Section: 10)

-   [x] **SETUP:** Ensure Co. A and Co. B exist, with their respective admins (`$COMP_A_ADMIN_TOKEN`, `$COMP_B_ADMIN_TOKEN`) and API keys (`$RAW_API_KEY_A`, `$RAW_API_KEY_B`). Ensure some distinct data (e.g., a project) exists in each.

1.  **Read Isolation:**
    -   [x] Co. A Admin tries to GET a specific project from Co. B -> `403 Forbidden` or `404 Not Found`.
    -   [x] API Key for Co. A tries to GET a project from Co. B -> `403` or `404`.
    -   [x] SystemAdmin (`$ADMIN_ACCESS_TOKEN`) GETs project from Co. B (using its GUID) -> `200 OK`.
    -   [x] SystemAdmin lists projects with `company_guid=$COMPANY_B_GUID` -> `200 OK`, only Co. B projects.
2.  **Create Isolation (e.g., Users, Workstations - non-Sync resources):**
    -   [x] Co. A Admin tries to create a Workstation with `company_guid` explicitly set to Co. B's GUID -> `403 Forbidden`.
3.  **Update Isolation:**
    -   [x] Co. A Admin tries to PATCH a Workstation in Co. B -> `403` or `404`. (Received `405 Method Not Allowed` - still a pass for isolation)
4.  **Delete Isolation:**
    -   [ ] Co. A Admin tries to DELETE a Workstation in Co. B -> `403` or `404`. (Received `500 Internal Server Error` - FAILED)
5.  **Sync Endpoint Isolation:**
    -   [x] API Key for Co. A (`$RAW_API_KEY_A`) syncs projects with payload items having `company_guid: $COMPANY_B_GUID` -> `403 Forbidden`.
    -   [x] Sync payload for Co. A key must only contain items for `$COMPANY_A_GUID`.
6.  **List Endpoint Tenant Enforcement:**
    -   [x] Co. A Admin (`$COMP_A_ADMIN_TOKEN`) lists projects (`GET /api/v1/projects` no filter) -> Only Co. A projects returned.

#### XII. Error Handling & General Tests (Corresponds to Guide Section: 11)

1.  **Invalid Input Validation (`422 Unprocessable Entity`, `400 Bad Request`):**
    -   [x] Create User: Missing `email` or `password` or `role` -> `422`.
    -   [x] Create Company: `company_index` = "abc" (string instead of int) -> `422`.
    -   [x] Sync Pieces: Payload with piece `outer_length` as string -> `422`.
    -   [x] Create API Key: Invalid scope value (not in enum) -> `422`.
    -   [ ] Malformed JSON body in any POST/PUT -> `400 Bad Request` (detail about JSON parsing error). (Received `422`)
2.  **Authentication Errors (`401 Unauthorized`):**
    -   [x] Access protected endpoint (e.g., `GET /api/v1/users`) with no token -> `401`.
    -   [ ] Use an expired JWT token -> `401`. (SKIPPED - difficult to automate expiry precisely)
    -   [x] Use a malformed/invalid signature JWT token -> `401`.
    -   [ ] Use an invalid/revoked API Key -> `401`. (SKIPPED - failed to create temp key for testing)
3.  **Authorization Errors (`403 Forbidden`):**
    -   [ ] ProjectManager token tries `POST /api/v1/users` -> `403`. (SKIPPED - token expired, got `401`)
    -   [ ] API Key without `sync:write` scope tries `POST /api/v1/sync/projects` -> `403`. (SKIPPED - failed to create temp key for testing)
4.  **Resource Not Found (`404 Not Found`):**
    -   [x] `GET /api/v1/projects/{non_existent_guid}` -> `404`.
    -   [x] `PUT /api/v1/users/{non_existent_guid}` -> `404`.
5.  **Method Not Allowed (`405 Method Not Allowed`):**
    -   [x] e.g. `PUT /api/v1/auth/login` (if login only supports POST) -> `405`.
6.  **Rate Limiting (if implemented - conceptual):**
    -   [ ] Script N+1 requests to an endpoint with limit N/minute -> `429 Too Many Requests` on last one. (SKIPPED - conceptual, requires specific limit info)
7.  **General API Behavior:**
    -   [ ] Consistent trailing slash handling (e.g. `/entities` and `/entities/` lead to same result or one redirects). (NEEDS REVIEW - /projects got 200, /projects/ got 307)
    -   [ ] Consistent use of UUIDs for GUIDs. (NEEDS MANUAL VERIFICATION)
    -   [ ] `created_at` and `updated_at` timestamps are correctly populated and updated. (NEEDS MANUAL VERIFICATION)
    -   [ ] `is_active` field present and correctly handled in GET lists and individual fetches for entities supporting soft delete. (NEEDS MANUAL VERIFICATION)
    -   [ ] `deleted_at` field is `null` for active items, and a timestamp for soft-deleted items (when fetched with `include_inactive=true`). (NEEDS MANUAL VERIFICATION)
    -   [ ] Pagination (`limit`, `offset`) works as expected on list endpoints that support it. (NEEDS MANUAL VERIFICATION)