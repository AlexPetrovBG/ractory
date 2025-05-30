### 5. Delete User (`DELETE /{guid}`)

**Description:** Soft-deletes a user by setting their `is_active` status to `false`.

**Permissions:**
*   `SystemAdmin`: Can deactivate any user except themselves.
*   `CompanyAdmin`: Can deactivate users in their own company, except `SystemAdmin`, `Integration` users, or themselves.

**Path Parameter:**
*   `guid`: The GUID of the user to deactivate.

**Response (Success - 200 OK):**
```json
{
  "message": "User deactivated successfully",
  "guid": "deactivated-user-guid"
}
```
*   `404 Not Found`: If user does not exist.
*   `403 Forbidden`: If insufficient permissions.
*   `400 Bad Request`: If attempting to delete own account. 