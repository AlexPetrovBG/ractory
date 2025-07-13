from fastapi import FastAPI, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.api.v1.api import api_router

app = FastAPI(
    title="Ra Factory API",
    description="Multi-tenant factory management API",
    version="0.1.0"
)

# Enable CORS with specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": exc.body},
    )

# Include the main API router (which includes all v1 routes including health)
app.include_router(api_router)

@app.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {"status": "ok", "version": "0.1.0"}

@app.get("/api/v1")
async def api_root():
    """API root information."""
    return {
        "name": "Ra Factory API",
        "version": "0.1.0",
        "description": "Multi-tenant factory management API"
    } 