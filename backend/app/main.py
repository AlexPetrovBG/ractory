from fastapi import FastAPI, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response, HTMLResponse
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

# Custom middleware to handle CSP for documentation
@app.middleware("http")
async def csp_middleware(request: Request, call_next):
    response = await call_next(request)
    
    # Only modify CSP for documentation endpoints
    if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
        # Allow Swagger UI resources while keeping main app secure
        csp_policy = (
            "default-src 'self'; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src-elem 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "script-src-elem 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https://fastapi.tiangolo.com; "
            "font-src 'self' https://cdn.jsdelivr.net; "
            "connect-src 'self'"
        )
        # Remove any existing CSP headers first, then set our own
        if "Content-Security-Policy" in response.headers:
            del response.headers["Content-Security-Policy"]
        if "X-Content-Security-Policy" in response.headers:
            del response.headers["X-Content-Security-Policy"]
        if "X-WebKit-CSP" in response.headers:
            del response.headers["X-WebKit-CSP"]
        # Set our CSP headers
        response.headers["Content-Security-Policy"] = csp_policy
        response.headers["X-Content-Security-Policy"] = csp_policy
        response.headers["X-WebKit-CSP"] = csp_policy
    else:
        # Keep strict CSP for main API endpoints
        response.headers["Content-Security-Policy"] = "default-src 'self'"
    
    return response

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Convert errors to JSON-serializable format
    errors = []
    for error in exc.errors():
        error_dict = {
            "type": error.get("type"),
            "loc": error.get("loc"),
            "msg": str(error.get("msg", "")),
            "input": error.get("input")
        }
        # Handle the ctx field which might contain non-serializable objects
        if "ctx" in error:
            ctx = error["ctx"]
            if isinstance(ctx, dict):
                # Convert any non-serializable objects in ctx to strings
                serializable_ctx = {}
                for key, value in ctx.items():
                    if hasattr(value, '__dict__'):
                        serializable_ctx[key] = str(value)
                    else:
                        serializable_ctx[key] = value
                error_dict["ctx"] = serializable_ctx
            else:
                error_dict["ctx"] = str(ctx)
        errors.append(error_dict)
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": errors},
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

@app.get("/docs", response_class=HTMLResponse, include_in_schema=False)
async def custom_docs():
    """Custom documentation endpoint with proper CSP."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta http-equiv="Content-Security-Policy" content="default-src 'self'; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; img-src 'self' data: https://fastapi.tiangolo.com; font-src 'self' https://cdn.jsdelivr.net; connect-src 'self'">
    <link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css">
    <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">
    <title>Ra Factory API - Swagger UI</title>
    </head>
    <body>
    <div id="swagger-ui">
    </div>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js"></script>
    <script>
    const ui = SwaggerUIBundle({
        url: '/openapi.json',
        "dom_id": "#swagger-ui",
        "layout": "BaseLayout",
        "deepLinking": true,
        "showExtensions": true,
        "showCommonExtensions": true,
        oauth2RedirectUrl: window.location.origin + '/docs/oauth2-redirect',
        presets: [
            SwaggerUIBundle.presets.apis,
            SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
    })
    </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content) 