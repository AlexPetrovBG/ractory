from fastapi import APIRouter

from app.api.v1 import auth
from app.api.v1 import sync
from app.api.v1 import companies as companies_router
from app.api.v1 import users as users_router
from app.api.v1 import workstations as workstations_router
from app.api.v1 import api_keys as api_keys_router
from app.schemas.auth import LoginRequest, TokenResponse

# Main API router for v1
api_router = APIRouter(prefix="/api/v1")

# Include routers
api_router.include_router(auth.router)
api_router.include_router(sync.router)

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
api_router.include_router(users_router.router, prefix="/users", tags=["users"])
api_router.include_router(workstations_router.router, prefix="/workstations", tags=["workstations"])
api_router.include_router(companies_router.router)
api_router.include_router(api_keys_router.router, prefix="/api-keys", tags=["api-keys"])
# etc. 