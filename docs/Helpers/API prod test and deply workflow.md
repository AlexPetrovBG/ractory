# Ra Factory API: Development, Testing, and Production Workflow

This document outlines the standard workflow for developing, testing, and deploying the Ra Factory backend API using Docker Compose profiles.

## Environments Overview

Our `docker-compose.yml` defines three main environments using profiles:

1.  **Development (`dev` profile):** Used for active coding. Changes are reflected live without manual image rebuilds. Services: `api`, `db_dev`, `admin`, `operator`.
2.  **Testing (`test` profile):** Used for running automated tests (`pytest`) against the codebase in an isolated environment. Services: `api_test`, `db_test`.
3.  **Production (`prod` profile):** Represents the live environment. Runs a pre-built, stable Docker image. Services: `api_prod`, `db_prod`.

## Managing User Passwords

The system uses bcrypt for password hashing via the `passlib` library. Password hashes are stored in the `pwd_hash` column of the `users` table.

### Password Update Tool

For managing passwords across environments (especially for admin users), use the provided script template:

```python
# update_admin_password.py
from passlib.context import CryptContext
import psycopg2

PWD_CTX = CryptContext(schemes=["bcrypt"], deprecated="auto")

def update_user_password(email, new_password, db_name, db_port):
    hashed_password = PWD_CTX.hash(new_password)
    conn = psycopg2.connect(
        dbname=db_name,
        user="rafactory_rw",
        password="R4fDBP4ssw0rd9X",
        host="localhost",
        port=db_port
    )
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET pwd_hash = %s WHERE email = %s",
            (hashed_password, email)
        )
        conn.commit()
    finally:
        conn.close()

# Usage:
# For development: update_user_password("user@example.com", "new_password", "rafactory_dev", "5434")
# For production: update_user_password("user@example.com", "new_password", "rafactory", "5432")
```

### Environment-Specific Considerations

- **Development:** Password hashes are stored in the `rafactory_dev` database (port 5434). 
- **Testing:** The test database is ephemeral. User credentials are typically created programmatically during test setup.
- **Production:** Password hashes are stored in the `rafactory` database (port 5432).

**Important:** Direct database manipulation of passwords should be avoided in production environments when possible. Use the API endpoints or controlled maintenance scripts.

**Note:** Always verify that password hashes are stored correctly in the database to avoid authentication issues. The hash format should begin with `$2b$12$`.

## 1. Development Workflow (`dev` profile)

This is your primary environment for writing code.

**Steps:**

1.  **Start Services:** Navigate to the `src/ractory` directory in your terminal and run:
    ```bash
    docker compose --profile dev up -d
    ```
    This starts the `api`, `db_dev`, `admin`, and `operator` services. The `api` service runs using `uvicorn` with the `--reload` flag enabled.

2.  **Code Changes:** Edit Python files directly within the `src/ractory/backend` directory on your host machine.

3.  **Live Reloading:** The development `api` service uses a volume mount (`./backend:/app`) in `docker-compose.yml`. This means your local `src/ractory/backend` directory is directly mapped into the container at `/app`. The `uvicorn --reload` command inside the container watches this `/app` directory for changes and automatically restarts the server when you save a file.

4.  **Check Logs (Optional):** To monitor the `uvicorn` reload process or check for runtime errors, view the logs:
    ```bash
    docker compose logs -f api
    ```

5.  **Manual Testing:** Use API clients (like Postman, Insomnia, curl) or your frontend applications to send requests to the API. The `api` service exposes port 8000, so endpoints are typically accessed at:
    `http://localhost:8000/api/v1/...`

6.  **Verify API/DB Connection:** After starting the services, you can test the login endpoint to confirm the `api` service can connect to the `db_dev` database and authenticate users. Use the following `curl` command (replace credentials if needed):
    ```bash
    curl -X POST -H "Content-Type: application/json" \
         -d '{"email": "a.petrov@delice.bg", "password": "password"}' \
         http://localhost:8000/api/v1/auth/login | cat
    ```
    A successful connection will return a JSON object containing `access_token` and `refresh_token`.

## 2. Automated Testing Workflow (`test` profile)

Run the automated test suite (`pytest`) to ensure code quality and prevent regressions.

**Steps:**

1.  **Ensure Test Database is Running:** The test profile uses a separate database (`db_test`). Start it if it's not already running:
    ```bash
    docker compose --profile test up -d db_test
    ```
    *Note: `db_test` runs in `tmpfs` and data is not persisted.*

2.  **Run Tests:** Execute the tests using the `api_test` service definition from the `src/ractory` directory:
    ```bash
    docker compose --profile test run --rm api_test
    ```
    *   This command builds the image using `src/ractory/backend/Dockerfile` (if not already built), starts a temporary container, and runs the `pytest -v` command defined in `docker-compose.yml`.
    *   `--rm` removes the container after tests complete.
    *   Review the terminal output for test results.

## 3. Production Deployment Workflow (`prod` profile)

Deploying to production involves building a self-contained Docker image and running it on the production server.

**Steps:**

1.  **Prerequisites:**
    *   Ensure your code changes are merged into the main branch (e.g., `main` or `master`).
    *   Verify all automated tests (`api_test` service) pass successfully.

2.  **Build the Production Image:**
    *   Create a tagged, production-ready image containing your backend code. From your workspace root (`/home/alex`), run:
        ```bash
        docker build -t prod-api:latest -f src/ractory/backend/Dockerfile src/ractory/backend
        ```
    *   **IMPORTANT:** For actual production deployments, replace `:latest` with a specific version tag (e.g., `:v1.0.1`, `:$(git rev-parse --short HEAD)`). Using `latest` can lead to unpredictable deployments.

3.  **(Recommended) Push Image to Registry:**
    *   Push the tagged image to a container registry (e.g., Docker Hub, AWS ECR, Google GCR). This makes it accessible to your production server.
        ```bash
        # Example: Tag with a version and registry path
        docker tag prod-api:latest your-registry/rafactory/prod-api:v1.0.1
        # Push the versioned tag
        docker push your-registry/rafactory/prod-api:v1.0.1
        ```
        *(Replace `your-registry/rafactory/prod-api` with your actual registry path)*

4.  **Deploy on Production Server:**
    *   Connect to your production server.
    *   Ensure Docker and Docker Compose are installed.
    *   Obtain the *production* `docker-compose.yml` file (this might be different from your development one, especially regarding secrets, volumes, and networks). It should define the `api_prod` service to use the image you pushed (e.g., `image: your-registry/rafactory/prod-api:v1.0.1`).
    *   **Critical:** The production `docker-compose.yml` for the `api_prod` service **must not** include the development volume mount (`volumes: - ./backend:/app`). The code must run *from within the image*.
    *   Pull the new image version from the registry:
        ```bash
        docker pull your-registry/rafactory/prod-api:v1.0.1
        ```
    *   Navigate to the directory containing the production `docker-compose.yml`.
    *   Start the production services using the `prod` profile:
        ```bash
        docker compose --profile prod up -d
        ```

5.  **Verify Deployment:**
    *   Check the logs of the production API container:
        ```bash
        docker compose logs api_prod
        ```
    *   Test the live API endpoints through their public URL to ensure the new version is running correctly.
