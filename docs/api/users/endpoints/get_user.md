### 3. Get User (`GET /{guid}`)

**Description:** Retrieves a specific user by their GUID.

**Permissions:**
*   `SystemAdmin`: Can retrieve any user.
*   Others: Can retrieve users only from their own company.

**Path Parameter:**
*   `guid`: The GUID of the user.

**Response (Success - 200 OK, `UserResponse` schema).**
*   `404 Not Found`: If user does not exist.
*   `403 Forbidden`: If user attempts to access user from another company without sufficient permissions. 