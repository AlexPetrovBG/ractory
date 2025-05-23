from fastapi import APIRouter

from app.api.v1 import auth
from app.api.v1 import sync
from app.api.v1 import companies as companies_router
from app.api.v1 import users as users_router
from app.api.v1 import workstations as workstations_router
from app.api.v1 import api_keys
from app.api.v1 import projects as projects_router
from app.api.v1 import workflow as workflow_router
from app.api import components as components_router
from app.api import assemblies as assemblies_router
from app.api import pieces as pieces_router
from app.api import articles as articles_router
from app.schemas.auth import LoginRequest, TokenResponse

# Main API router for v1
api_router = APIRouter(prefix="/api/v1")

# Include routers
api_router.include_router(auth.router)
api_router.include_router(sync.router)
api_router.include_router(companies_router.router)
api_router.include_router(users_router.router, prefix="/users", tags=["users"])
api_router.include_router(workstations_router.router, prefix="/workstations", tags=["workstations"])
api_router.include_router(api_keys.router)
api_router.include_router(projects_router.router, prefix="/projects", tags=["projects"])
api_router.include_router(workflow_router.router)

# Include the new entity routers
api_router.include_router(components_router.router, prefix="/components", tags=["components"])
api_router.include_router(assemblies_router.router, prefix="/assemblies", tags=["assemblies"])
api_router.include_router(pieces_router.router, prefix="/pieces", tags=["pieces"])
api_router.include_router(articles_router.router, prefix="/articles", tags=["articles"])

# Emergency mock auth endpoint for testing without DB
@api_router.post("/mock-auth", response_model=TokenResponse)
async def mock_auth(login_data: LoginRequest):
    """
    Mock auth endpoint for testing without database.
    For development/testing purposes only.
    """
    if login_data.email == "a.petrov@delice.bg" and login_data.password == "password":
        return {
            "access_token": "mock_access_token",
            "refresh_token": "mock_refresh_token",
            "role": "CompanyAdmin",
            "expires_in": 900,
        }
    return {
        "access_token": "",
        "refresh_token": "",
        "role": "Guest",
        "expires_in": 0,
    }

# Add user and workstation routers
api_router.include_router(companies_router.router)
api_router.include_router(api_keys.router)
# etc. 