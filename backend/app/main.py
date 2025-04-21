from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Ra Factory API",
    description="Factory management API for RaWorkshop",
    version="0.1.0",
)

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    return {"status": "ok", "version": "0.1.0"}

@app.get("/api/v1")
async def api_root():
    """
    API root endpoint with version information.
    """
    return {
        "name": "Ra Factory API",
        "version": "0.1.0",
        "status": "running",
    } 