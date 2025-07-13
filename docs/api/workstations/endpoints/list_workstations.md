### 2. List Workstations (`GET /`)

**Description:** Retrieves a list of workstations.

**Permissions:** Any authenticated user (data is scoped by company).

**Query Parameters:**
*   `type` (enum, optional): Filter by workstation type (e.g., `Assembly`, `Logistics`).
*   `active` (bool, optional): Filter by active status.
*   `location` (str, optional): Filter by location (substring match, case-insensitive).
*   `company_guid` (UUID, optional): Filter by company GUID (`SystemAdmin` only).

**Response (Success - 200 OK, List of `WorkstationResponse` schema).**
*   `403 Forbidden`: If non-`SystemAdmin` tries to use `company_guid` filter for a different company.
*   `500 Internal Server Error`: If an unexpected error occurs on the server. 