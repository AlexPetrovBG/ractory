### 3. Get Workflow Statistics (`GET /statistics`)

**Description:** Retrieves aggregated statistics about workflow entries for the user's company.

**Permissions:** Minimum `ProjectManager` role.

**Query Parameters:**
*   `start_date` (datetime, optional): Filter statistics for entries created on or after this date.
*   `end_date` (datetime, optional): Filter statistics for entries created on or before this date.

**Response (Success - 200 OK, `WorkflowStatistics` schema):**
```json
{
  "total_entries": 1520,
  "entries_by_type": {
    "barcode_scan": 500,
    "piece_cut": 300,
    // ... other action types and their counts
  },
  "entries_today": 55,
  "entries_last_7_days": 450
}
```
*(The exact structure of `WorkflowStatistics` should be verified from its Pydantic schema definition)*

**Error Responses:**
*   `422 Unprocessable Entity`: If query parameters are invalid (e.g., bad date format).
*   `500 Internal Server Error`: If an unexpected error occurs on the server. 