### 4. Update Workstation (`PUT /{guid}`)

**Description:** Updates a workstation's information.

**Permissions:** `SystemAdmin` or `CompanyAdmin`.

**Path Parameter:**
*   `guid`: The GUID of the workstation to update.

**Request Body (`WorkstationUpdate` schema, all fields optional):
```json
{
  "location": "New Location",
  "type": "Logistics",
  "is_active": false
}
```

**Response (Success - 200 OK, `WorkstationResponse` schema):** Updated workstation details.
*   `404 Not Found`: If workstation does not exist.
*   `403 Forbidden`: If `CompanyAdmin` attempts to update workstation from another company.
*   `500 Internal Server Error`: If an unexpected error occurs on the server. 