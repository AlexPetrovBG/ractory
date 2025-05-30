### 4. Update User (`PUT /{guid}`)

**Description:** Updates a user's information.

**Permissions:**
*   A user can update their own `email` (if the new email is not already in use), `password`, `pin`, `name`, `surname`, and `picture_path`. Users cannot change their own `role` or `is_active` status unless they are a `SystemAdmin`.
*   `CompanyAdmin`: 
    *   **Note:** Currently, due to a logic path in the API, `CompanyAdmin`s are effectively prevented from updating other users in their company and receive a "You can only update your own account" error. The intended behavior (allowing updates within their company subject to role hierarchy) is not currently functional. They can update their own information as per the rules for a general user.
*   `SystemAdmin`: 
    *   Can update any user and any of their fields.
    *   Role changes are subject to `can_manage_role` logic for both the user's current role and the target role.

**Path Parameter:**
*   `guid`: The GUID of the user to update.

**Request Body (`UserUpdate` schema, all fields optional):
```json
{
  "email": "updated.email@example.com",
  "password": "new_secure_password",
  "role": "Operator",
  "is_active": false,
  "pin": "654321",
  "name": "UpdatedName",
  "surname": "UpdatedSurname",
  "picture_path": "/updated/path.jpg"
}
```

**Response (Success - 200 OK, `UserResponse` schema):** Updated user details.
*   `404 Not Found`: If user does not exist.
*   `403 Forbidden`: If insufficient permissions to update user or change role.
*   `400 Bad Request`: If trying to set an email that's already registered to another user. 