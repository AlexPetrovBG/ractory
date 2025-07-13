### 1. Create Workflow Entry (`POST /`)

**Description:** Creates a new workflow entry to record an action or event.

**Permissions:** Minimum `ProjectManager` role.

**Request Body (`WorkflowCreate` schema):
```json
{
  "action_type": "barcode_scan", // Must be a valid WorkflowActionType
  "company_guid": "optional-company-guid", // Optional. If provided, its access is validated. If omitted, defaults to the authenticated user's company.
  "workstation_guid": "optional-workstation-guid",
  "user_guid": "optional-user-guid", // Optional, defaults to current authenticated user
  "api_key_guid": "optional-api-key-guid", // If action performed by an API key
  "action_value": "{\"barcode\": \"12345ABC\", \"item_type\": \"piece\"}" // Optional JSON string or simple string
}
```

**Response (Success - 201 Created, `WorkflowResponse` schema):**
```json
{
  "guid": "new-workflow-entry-guid",
  "company_guid": "company-guid",
  "company_name": "Derived Company Name", // Derived
  "workstation_guid": "workstation-guid",
  "workstation_name": "Derived Workstation Name", // Derived
  "api_key_guid": "api-key-guid",
  "user_guid": "user-guid",
  "user_name": "Derived User Name", // Derived
  "action_type": "barcode_scan",
  "action_value": "{\"barcode\": \"12345ABC\", \"item_type\": \"piece\"}",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

**Error Responses:**
*   `422 Unprocessable Entity`: If `action_type` is invalid, or other validation errors occur (e.g., invalid GUID format).
*   `403 Forbidden`: If a non-`SystemAdmin` user attempts to create an entry for a `company_guid` they don't have access to.
*   `500 Internal Server Error`: If an unexpected error occurs on the server. 