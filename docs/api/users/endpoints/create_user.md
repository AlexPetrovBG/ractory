### 1. Create User (`POST /`)

**Description:** Creates a new user.

**Permissions:**
*   `SystemAdmin`: Can create users in any company with any role, provided they have the authority to manage the target role.
*   `CompanyAdmin`: Can create users within their own company, provided they have the authority to manage the target role (typically `ProjectManager` or `Operator`).

**Request Body (`UserCreate` schema):**
```json
{
  "email": "new.user@example.com",
  "password": "secure_password",
  "role": "ProjectManager", // e.g., SystemAdmin, CompanyAdmin, ProjectManager, Operator
  "company_guid": "company-guid-for-the-user",
  "pin": "123456",         // Optional, typically for Operator
  "name": "UserFirstName",    // Optional
  "surname": "UserLastName",   // Optional
  "picture_path": "/path/to/image.jpg" // Optional
}
```

**Response (Success - 201 Created, `UserResponse` schema):**
```json
{
  "guid": "new-user-guid",
  "email": "new.user@example.com",
  "role": "ProjectManager",
  "company_guid": "company-guid-for-the-user",
  "is_active": true,
  "pin": "123456",
  "name": "UserFirstName",
  "surname": "UserLastName",
  "picture_path": "/path/to/image.jpg",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

**Error Responses:**
*   `400 Bad Request`: If email already registered.
*   `403 Forbidden`: If current user lacks permission to create user with specified role or in specified company. 