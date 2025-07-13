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

# Mock auth endpoint removed - use proper authentication endpoints

# Add user and workstation routers
api_router.include_router(companies_router.router)
api_router.include_router(api_keys.router)
# etc. 