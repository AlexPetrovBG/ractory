### 2. List Workflow Entries (`GET /`)

**Description:** Retrieves a list of workflow entries, scoped to the authenticated user's company.

**Permissions:** Minimum `ProjectManager` role.

**Query Parameters:**
*   `action_type` (enum, optional): Filter by `WorkflowActionType`.
*   `workstation_guid` (UUID, optional): Filter by workstation GUID.
*   `user_guid` (UUID, optional): Filter by user GUID.
*   `start_date` (datetime, optional): Filter entries created on or after this date.
*   `end_date` (datetime, optional): Filter entries created on or before this date.
*   `limit` (int, optional, default: 100, max: 1000): Pagination limit.
*   `offset` (int, optional, default: 0): Pagination offset.

**Response (Success - 200 OK, `WorkflowList` schema):**
```json
{
  "workflows": [
    // ... list of WorkflowResponse objects ...
  ]
}
```

**Error Responses:**
*   `422 Unprocessable Entity`: If query parameters are invalid (e.g., bad date format).
*   `500 Internal Server Error`: If an unexpected error occurs on the server. 