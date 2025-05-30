// ... existing code ...
**Response (Success - 200 OK, `WorkstationResponse` schema).**
*   `404 Not Found`: If workstation does not exist.
*   `403 Forbidden`: If user attempts to access workstation from another company (and is not `SystemAdmin`).
*   `500 Internal Server Error`: If an unexpected error occurs on the server.
