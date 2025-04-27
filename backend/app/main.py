from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import time
from contextlib import asynccontextmanager
from sqlalchemy import text

from app.api.v1.api import api_router as api_v1_router
from app.schemas.auth import ErrorResponse
from app.models.base import engine

# Setup RLS policies on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Step 1: Enable RLS on all tables
    try:
        async with engine.begin() as conn:
            print("Attempting to enable RLS on all tables...")
            await conn.execute(text("""
            DO $$
            DECLARE t RECORD;
            BEGIN
              FOR t IN
                SELECT tablename FROM pg_tables WHERE schemaname = 'public'
              LOOP
                EXECUTE format('ALTER TABLE %I ENABLE ROW LEVEL SECURITY;', t.tablename);
              END LOOP;
            END$$;
            """))
            print("Successfully enabled RLS on all tables (within transaction).")
        print("Transaction for enabling RLS committed.")
    except Exception as e:
        print(f"Error enabling RLS on all tables: {e}")
        # Decide if we should proceed or yield/raise here

    # Step 2: Create individual RLS policies in separate transactions
    policies_to_create = [
        # Companies table - RLS removed for now, access controlled by endpoint
        ("companies", "guid", "tenant_isolation"), 
        # Users table
        ("users", "company_guid", "tenant_isolation"),
        # API Keys table
        ("api_keys", "company_guid", "tenant_isolation"),
        # Workstations table
        ("workstations", "company_guid", "tenant_isolation"),
        # UI Templates table
        ("ui_templates", "company_guid", "tenant_isolation"),
        # Projects table
        ("projects", "company_guid", "tenant_isolation"),
        # Components table
        ("components", "company_guid", "tenant_isolation"),
        # Assemblies table
        ("assemblies", "company_guid", "tenant_isolation"),
        # Pieces table
        ("pieces", "company_guid", "tenant_isolation"),
        # Articles table
        ("articles", "company_guid", "tenant_isolation"),
    ]

    for table, column, policy_name in policies_to_create:
        try:
            async with engine.begin() as conn:
                print(f"Attempting to create RLS policy '{policy_name}' on table '{table}'...")
                await conn.execute(text(f"""
                DO $$
                BEGIN
                  IF NOT EXISTS (
                    SELECT 1 FROM pg_policies WHERE tablename = '{table}' AND policyname = '{policy_name}'
                  ) THEN
                    EXECUTE 'CREATE POLICY {policy_name} ON {table}
                             USING ({column} = current_setting(\'\'app.tenant\'\')::uuid OR
                                    current_setting(\'\'app.bypass_rls\'\', true) = \'\'true\'\')';
                  END IF;
                END$$;
                """))
                print(f"Successfully created/verified RLS policy '{policy_name}' on table '{table}'.")
            print(f"Transaction for policy '{policy_name}' on table '{table}' committed.")
        except Exception as e:
            print(f"Error creating RLS policy '{policy_name}' on table '{table}': {e}")
            print(f"Skipping policy creation for {table} due to error.")
            # Continue to the next policy

    print("Finished attempting to set up RLS policies.")
    yield
    # No cleanup needed

app = FastAPI(
    title="Ra Factory API",
    description="Factory management API for RaWorkshop",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://admin.raworkshop.bg", "https://operator.raworkshop.bg", "http://localhost:5173", "http://localhost:5174"],  # Restrict to known origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Authorization", "Content-Type", "X-API-Key"],
)

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append(f"{error['loc'][-1]}: {error['msg']}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "Validation error", "detail": errors},
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
        headers=exc.headers,
    )

# Include API router
app.include_router(api_v1_router)

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    return {"status": "ok", "version": "0.1.0"}

# Add a more consistent health endpoint following API paths
@app.get("/api/v1/health")
async def api_health_check():
    """
    Health check endpoint for API v1.
    """
    return {"status": "ok", "version": "0.1.0"}

# API root with docs redirect
@app.get("/")
async def root():
    """
    Redirect to API documentation.
    """
    return {"message": "Ra Factory API", "docs": "/docs"} 