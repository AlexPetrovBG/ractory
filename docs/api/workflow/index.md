---
title: Workflow API
slug: /workflow
---

# Workflow Management

Endpoints for creating and querying workflow entries. Workflow entries track various actions and events within the system.

All endpoints are prefixed with `/api/v1/workflow` and require at least `ProjectManager` role.

## Workflow Action Types

The `action_type` field in a workflow entry specifies the nature of the event. Valid types are defined in the `WorkflowActionType` enum (e.g., `barcode_scan`, `piece_cut`, `assembly_weld`, `quality_check`, `system_event`, etc.).

## Endpoints

- **[Create Workflow Entry](./endpoints/create_workflow_entry.md)**: `POST /` - Creates a new workflow entry.
- **[List Workflow Entries](./endpoints/list_workflow_entries.md)**: `GET /` - Retrieves a list of workflow entries.
- **[Get Workflow Statistics](./endpoints/get_workflow_statistics.md)**: `GET /statistics` - Retrieves aggregated statistics.
- **[Get Workflow Entry](./endpoints/get_workflow_entry.md)**: `GET /{guid}` - Retrieves a specific workflow entry.

### 1. Create Workflow Entry (`POST /`)

**Description:** Creates a new workflow entry to record an action or event.

**Permissions:** Minimum `ProjectManager` role.

**Request Body (`WorkflowCreate` schema):
```json
{
  "action_type": "barcode_scan", // Must be a valid WorkflowActionType
  "company_guid": "optional-company-guid", // Optional, defaults to user's company if not SystemAdmin
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
*   `422 Unprocessable Entity`: If `action_type` is invalid, or other validation errors.
*   `403 Forbidden`: If user attempts to create entry for a `company_guid` they don't have access to (non-`SystemAdmin`).

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

### 4. Get Workflow Entry (`GET /{guid}`)

**Description:** Retrieves a specific workflow entry by its GUID.

**Permissions:** Minimum `ProjectManager` role.

**Path Parameter:**
*   `guid`: The GUID of the workflow entry.

**Response (Success - 200 OK, `WorkflowResponse` schema).**
*   `404 Not Found`: If workflow entry does not exist.
*   `403 Forbidden`: If user attempts to access an entry from another company (and is not `SystemAdmin`). 