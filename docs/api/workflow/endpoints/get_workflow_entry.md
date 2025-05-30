### 4. Get Workflow Entry (`GET /{guid}`)

**Description:** Retrieves a specific workflow entry by its GUID.

**Permissions:** Minimum `ProjectManager` role.

**Path Parameter:**
*   `guid`: The GUID of the workflow entry.

**Response (Success - 200 OK, `WorkflowResponse` schema).**
*   `404 Not Found`: If workflow entry does not exist.
*   `403 Forbidden`: If user attempts to access an entry from another company (and is not `SystemAdmin`).
*   `500 Internal Server Error`: If an unexpected error occurs on the server. 