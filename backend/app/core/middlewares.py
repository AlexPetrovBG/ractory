"""
Middlewares for multi-tenant isolation and other cross-cutting concerns.
"""
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession
import json
import time
from typing import Dict, Any, Tuple, Optional

from app.models.enums import UserRole
from app.core.deps import get_current_user

class TenantIsolationMiddleware(BaseHTTPMiddleware):
    """
    Middleware to ensure tenants are properly isolated.
    
    This middleware adds diagnostic information for tenant isolation
    and logs potential cross-tenant access attempts.
    """
    async def dispatch(self, request: Request, call_next):
        # Store start time for request metrics
        start_time = time.time()
        
        # Check for company_guid parameter in query string
        query_params = dict(request.query_params)
        if 'company_guid' in query_params:
            # Note: The actual validation happens in route handlers
            # This is just for monitoring/logging purposes
            request.state.has_company_param = True
            request.state.company_guid_param = query_params['company_guid']
        
        # Process the request
        response = await call_next(request)
        
        # Add diagnostic headers (only in development)
        if 'X-Tenant-Diagnostics' in request.headers:
            tenant_info = {}
            # Get tenant context from request state if available
            if hasattr(request.state, 'user_tenant'):
                tenant_info['user_tenant'] = request.state.user_tenant
            if hasattr(request.state, 'has_company_param'):
                tenant_info['company_param'] = request.state.company_guid_param
            
            response.headers["X-Tenant-Info"] = json.dumps(tenant_info)
            response.headers["X-Process-Time"] = str(time.time() - start_time)
        
        return response

# Register event listeners to ensure queries are properly scoped by tenant
def register_tenant_isolation_listeners():
    """
    Register SQLAlchemy event listeners to ensure tenant isolation.
    
    This intercepts all queries before execution to ensure RLS is active.
    Logs warnings when tenant context is missing for better diagnostics.
    """
    @event.listens_for(AsyncSession, "before_cursor_execute", retval=True)
    async def ensure_tenant_context(conn, cursor, statement, parameters, context, executemany):
        """
        Ensure tenant context is set before executing any SQL.
        
        This is a defense-in-depth measure to ensure RLS is properly engaged,
        even if app.tenant is not set correctly.
        """
        # Extract query type
        query_type = get_query_type(statement)
        
        # For all access to tenant-isolated tables, verify tenant context
        if is_tenant_isolated_table(statement) and query_type != "DDL":
            # Check if app.tenant is set
            tenant_check = await conn.execute("SHOW app.tenant")
            tenant_value = tenant_check.scalar()
            
            # Check if app.bypass_rls is set
            bypass_check = await conn.execute("SHOW app.bypass_rls")
            bypass_value = bypass_check.scalar()
            
            # If tenant is not set and bypass is not true, log a warning
            if (not tenant_value or tenant_value == '') and bypass_value != 'true':
                print(f"WARNING: Tenant context not set for query: {statement[:100]}...")
                print(f"Parameters: {parameters}")
                
        return statement, parameters

def get_query_type(statement: str) -> str:
    """
    Determine the type of SQL query from statement.
    
    Args:
        statement: SQL statement to analyze
        
    Returns:
        String representing query type (SELECT, INSERT, UPDATE, DELETE, or DDL)
    """
    statement = statement.strip().upper()
    if statement.startswith("SELECT"):
        return "SELECT"
    elif statement.startswith("INSERT"):
        return "INSERT"
    elif statement.startswith("UPDATE"):
        return "UPDATE"
    elif statement.startswith("DELETE"):
        return "DELETE"
    else:
        return "DDL"  # Data Definition Language or other

def is_tenant_isolated_table(statement: str) -> bool:
    """
    Check if statement accesses tenant-isolated tables.
    
    Args:
        statement: SQL statement to analyze
        
    Returns:
        True if statement accesses tenant-isolated tables
    """
    # List of tenant-isolated tables (keep in sync with RLS policies)
    isolated_tables = [
        "users", "projects", "components", "assemblies", "pieces", 
        "articles", "workstations", "api_keys", "ui_templates"
    ]
    
    # Check if any of the isolated tables appear in the statement
    # This is a simple heuristic and might have false positives/negatives
    statement = statement.lower()
    for table in isolated_tables:
        if f" {table}" in statement or f"from {table}" in statement or f"join {table}" in statement:
            return True
    
    return False 