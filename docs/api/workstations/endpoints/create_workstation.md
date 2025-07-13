### 1. Create Workstation (`POST /`)

**Description:** Creates a new workstation.

**Permissions:** `SystemAdmin` or `CompanyAdmin`.

**Request Body (`WorkstationCreate` schema):
```json
{
  "location": "Assembly Line 1, Bay 2",
  "type": "Assembly", // Valid types: Assembly, Logistics, Cutting, Welding, Painting, Packaging, QualityControl, Other
  "company_guid": "company-guid-if-systemadmin-else-optional", // Optional for CompanyAdmin (defaults to their company)
  "is_active": true // Optional, defaults to true
}
```

**Response (Success - 201 Created, `WorkstationResponse` schema):**
```json
{
  "guid": "new-workstation-guid",
  "location": "Assembly Line 1, Bay 2",
  "type": "Assembly",
  "company_guid": "company-guid",
  "is_active": true,
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

**Error Responses:**
*   `403 Forbidden`: If `CompanyAdmin` tries to create for another company.
*   `404 Not Found`: If specified `company_guid` does not exist.
*   `422 Unprocessable Entity`: For invalid input data (e.g., invalid `type`).
*   `500 Internal Server Error`: If an unexpected error occurs on the server. 