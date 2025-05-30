### 5. Delete Workstation (`DELETE /{guid}`)

**Description:** Soft-deletes a workstation by setting its `is_active` status to `false`.

**Permissions:** `SystemAdmin` or `CompanyAdmin`.

**Path Parameter:**
*   `guid`: The GUID of the workstation to deactivate.

**Response (Success - 200 OK):**
```json
{
  "message": "Workstation deactivated successfully",
  "guid": "deactivated-workstation-guid",
  "location": "Workstation Location"
}
```
*   `404 Not Found`: If workstation does not exist.
*   `403 Forbidden`: If `CompanyAdmin` attempts to delete workstation from another company.
*   `500 Internal Server Error`: If an unexpected error occurs on the server. 