"""
Multi-tenant Isolation Test Script.

This script tests the isolation between companies across all API endpoints.
It verifies that users from one company cannot access data from another company.

The script tests:
1. JWT Authentication Isolation - Users can only access their own company's data
2. API Key Authentication Isolation - API keys can only access their company's data
3. Sync Endpoint Isolation - API keys can only sync data for their company

Usage:
    python -m app.tests.test_multi_tenant_isolation
"""

import asyncio
import aiohttp
import uuid
import json
import sys
from typing import Dict, List, Any, Tuple, Optional

# Configuration
BASE_URL = "http://localhost:8000"
API_PREFIX = "/api/v1"
DEBUG = True  # Set to True for detailed output

# Test users (replace with actual credentials from your environment)
SYSTEM_ADMIN = {"email": "a.petrov@delice.bg", "password": "password"}
COMPANY_A_ADMIN = {"email": "admin1.a@example.com", "password": "password"}
COMPANY_B_ADMIN = {"email": "admin1.b@example.com", "password": "password"}

async def login(session: aiohttp.ClientSession, credentials: Dict[str, str]) -> Dict[str, Any]:
    """
    Login and get tokens.
    
    Args:
        session: The aiohttp ClientSession
        credentials: Dictionary containing email and password
    
    Returns:
        Dict with tokens and user info
    """
    async with session.post(
        f"{BASE_URL}{API_PREFIX}/auth/login",
        json=credentials
    ) as response:
        if response.status != 200:
            print(f"Login failed for {credentials['email']}: {await response.text()}")
            sys.exit(1)
        return await response.json()

async def get_companies(session: aiohttp.ClientSession, token: str) -> List[Dict[str, Any]]:
    """
    Get list of companies.
    
    Args:
        session: The aiohttp ClientSession
        token: JWT access token (should be for SystemAdmin)
    
    Returns:
        List of company dictionaries
    """
    async with session.get(
        f"{BASE_URL}{API_PREFIX}/companies",
        headers={"Authorization": f"Bearer {token}"}
    ) as response:
        if response.status != 200:
            print(f"Failed to get companies: {await response.text()}")
            return []
        data = await response.json()
        if isinstance(data, list):
            return data
        else:
            return data.get("companies", [])

async def create_api_key(
    session: aiohttp.ClientSession, 
    token: str,
    description: str = "Test API Key",
    scopes: str = "sync:read,sync:write"
) -> Optional[str]:
    """
    Create an API key for testing.
    
    Args:
        session: The aiohttp ClientSession
        token: JWT access token for a company admin
        description: Description for the API key
        scopes: Comma-separated list of scopes
    
    Returns:
        API key string or None if creation failed
    """
    async with session.post(
        f"{BASE_URL}{API_PREFIX}/api-keys",
        headers={"Authorization": f"Bearer {token}"},
        json={"description": description, "scopes": scopes}
    ) as response:
        if response.status not in (200, 201):  # Accept both 200 OK and 201 Created
            print(f"Failed to create API key: {await response.text()}")
            return None
        data = await response.json()
        
        # The response might be the full API key object, not just the key string
        if isinstance(data, dict) and "key" in data:
            return data["key"]
        else:
            print(f"API key not found in response: {data}")
            return None

async def test_endpoint(
    session: aiohttp.ClientSession,
    method: str,
    endpoint: str,
    auth_header: Dict[str, str],
    expected_status: int,
    json_data: Dict[str, Any] = None,
    debug_msg: str = ""
) -> Tuple[bool, Dict[str, Any]]:
    """
    Test an endpoint with given auth and expected status.
    
    Args:
        session: The aiohttp ClientSession
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint path
        auth_header: Authorization header (JWT or API Key)
        expected_status: Expected HTTP status code
        json_data: Optional JSON data for POST/PUT requests
        debug_msg: Message to display for this test
    
    Returns:
        Tuple of (success boolean, response data)
    """
    methods = {
        "GET": session.get,
        "POST": session.post,
        "PUT": session.put,
        "DELETE": session.delete
    }
    
    request_method = methods.get(method.upper())
    if not request_method:
        print(f"Invalid method: {method}")
        return False, {}
    
    full_url = f"{BASE_URL}{API_PREFIX}/{endpoint.lstrip('/')}"
    
    try:
        kwargs = {"headers": auth_header}
        if json_data:
            kwargs["json"] = json_data
            
        async with request_method(full_url, **kwargs) as response:
            response_data = {}
            try:
                response_data = await response.json()
            except:
                response_data = {"text": await response.text()}
                
            success = response.status == expected_status
            
            if DEBUG or not success:
                isolate = "✓" if success else "✗"
                print(f"{isolate} {debug_msg} - {method} {endpoint} - Expected: {expected_status}, Got: {response.status}")
                if not success and DEBUG:
                    print(f"    Response: {response_data}")
                    
            return success, response_data
    except Exception as e:
        print(f"Error testing {method} {endpoint}: {str(e)}")
        return False, {"error": str(e)}

async def run_entity_tests(
    session: aiohttp.ClientSession,
    company_a_token: str,
    company_b_token: str,
    company_a_guid: str,
    company_b_guid: str,
    entity_type: str
):
    """
    Run isolation tests for a specific entity type.
    
    Tests:
    1. Company A user viewing Company A data (should succeed with status 200)
    2. Company A user viewing Company B data (should fail with status 403)
    3. Company B user viewing Company A data (should fail with status 403)
    
    Args:
        session: The aiohttp ClientSession
        company_a_token: JWT token for Company A user
        company_b_token: JWT token for Company B user
        company_a_guid: Company A GUID
        company_b_guid: Company B GUID
        entity_type: Entity type to test (projects, components, etc.)
    """
    # Test company A user viewing company A data (should succeed)
    await test_endpoint(
        session, "GET", f"/{entity_type}",
        {"Authorization": f"Bearer {company_a_token}"},
        200,
        debug_msg=f"Company A user viewing own {entity_type}"
    )
    
    # Test company A user viewing company B data (should fail)
    # Try explicit filtering by company_guid
    await test_endpoint(
        session, "GET", f"/{entity_type}?company_guid={company_b_guid}",
        {"Authorization": f"Bearer {company_a_token}"},
        403,  # Should be 403 Forbidden
        debug_msg=f"Company A user viewing Company B {entity_type}"
    )
    
    # Test company B user viewing company A data (should fail)
    await test_endpoint(
        session, "GET", f"/{entity_type}?company_guid={company_a_guid}",
        {"Authorization": f"Bearer {company_b_token}"},
        403,  # Should be 403 Forbidden
        debug_msg=f"Company B user viewing Company A {entity_type}"
    )

async def run_api_key_tests(
    session: aiohttp.ClientSession,
    company_a_api_key: str,
    company_b_api_key: str,
    company_a_guid: str,
    company_b_guid: str,
    entity_type: str
):
    """
    Run isolation tests using API keys.
    
    Tests:
    1. Company A API key accessing Company A data (should succeed with status 200)
    2. Company A API key accessing Company B data (should fail with status 403)
    3. Company B API key accessing Company A data (should fail with status 403)
    
    Args:
        session: The aiohttp ClientSession
        company_a_api_key: API key for Company A
        company_b_api_key: API key for Company B
        company_a_guid: Company A GUID
        company_b_guid: Company B GUID
        entity_type: Entity type to test (projects, components, etc.)
    """
    # Test company A API key accessing company A data (should succeed)
    await test_endpoint(
        session, "GET", f"/{entity_type}",
        {"X-API-Key": company_a_api_key},
        200,
        debug_msg=f"Company A API key accessing own {entity_type}"
    )
    
    # Test company A API key accessing company B data (should fail)
    await test_endpoint(
        session, "GET", f"/{entity_type}?company_guid={company_b_guid}",
        {"X-API-Key": company_a_api_key},
        403,  # Should be 403 Forbidden
        debug_msg=f"Company A API key accessing Company B {entity_type}"
    )
    
    # Test company B API key accessing company A data (should fail)
    await test_endpoint(
        session, "GET", f"/{entity_type}?company_guid={company_a_guid}",
        {"X-API-Key": company_b_api_key},
        403,  # Should be 403 Forbidden
        debug_msg=f"Company B API key accessing Company A {entity_type}"
    )

async def run_sync_tests(
    session: aiohttp.ClientSession,
    company_a_api_key: str,
    company_b_api_key: str,
    company_a_guid: str,
    company_b_guid: str
):
    """
    Test sync endpoints which use API keys.
    
    Tests:
    1. Company A API key trying to sync Company B data (should fail with status 403)
    2. Company B API key trying to sync Company A data (should fail with status 403)
    
    This ensures API keys can only sync data for their own company.
    
    Args:
        session: The aiohttp ClientSession
        company_a_api_key: API key for Company A
        company_b_api_key: API key for Company B
        company_a_guid: Company A GUID
        company_b_guid: Company B GUID
    """
    # Test sync endpoints with wrong company_guid (should fail)
    for entity in ["projects", "components", "assemblies", "pieces", "articles"]:
        # Company A trying to sync data for Company B
        await test_endpoint(
            session, "POST", f"/sync/{entity}",
            {"X-API-Key": company_a_api_key},
            403,  # Should be 403 Forbidden
            json_data={f"{entity}": [{"company_guid": company_b_guid}]},
            debug_msg=f"Company A API key syncing Company B {entity}"
        )
        
        # Company B trying to sync data for Company A
        await test_endpoint(
            session, "POST", f"/sync/{entity}",
            {"X-API-Key": company_b_api_key},
            403,  # Should be 403 Forbidden
            json_data={f"{entity}": [{"company_guid": company_a_guid}]},
            debug_msg=f"Company B API key syncing Company A {entity}"
        )

async def main():
    """
    Main test execution function.
    
    This runs a comprehensive series of tests to verify that:
    1. JWT tokens can only access their own company's data
    2. API keys can only access their own company's data
    3. Sync endpoints enforce company isolation
    
    The tests cover all entity types in the system.
    """
    print("Starting multi-tenant isolation tests...")
    
    async with aiohttp.ClientSession() as session:
        # Login with different user roles
        system_admin_data = await login(session, SYSTEM_ADMIN)
        system_admin_token = system_admin_data["access_token"]
        
        # Get companies
        companies = await get_companies(session, system_admin_token)
        if len(companies) < 2:
            print("Not enough companies for isolation testing. Please create at least two companies.")
            return
            
        # Get GUIDs for two companies
        company_a_guid = companies[0]["guid"]
        company_b_guid = companies[1]["guid"]
        
        print(f"Testing isolation between Company A ({company_a_guid}) and Company B ({company_b_guid})")
        
        # Login as Company A admin
        company_a_data = await login(session, COMPANY_A_ADMIN)
        company_a_token = company_a_data["access_token"]
        
        # Login as Company B admin
        company_b_data = await login(session, COMPANY_B_ADMIN)
        company_b_token = company_b_data["access_token"]
        
        # Create API keys for both companies
        company_a_api_key = await create_api_key(session, company_a_token)
        company_b_api_key = await create_api_key(session, company_b_token)
        
        if not company_a_api_key or not company_b_api_key:
            print("Failed to create API keys. Aborting tests.")
            return
            
        print("\n=== Testing JWT Authentication Isolation ===")
        # Test isolation for each entity type with JWT auth
        for entity in ["projects", "components", "assemblies", "pieces", "articles", "workstations", "users"]:
            await run_entity_tests(
                session, company_a_token, company_b_token, 
                company_a_guid, company_b_guid, entity
            )
            
        print("\n=== Testing API Key Authentication Isolation ===")
        # Test isolation for each entity type with API key auth
        for entity in ["projects", "components", "assemblies", "pieces", "articles"]:
            await run_api_key_tests(
                session, company_a_api_key, company_b_api_key,
                company_a_guid, company_b_guid, entity
            )
            
        print("\n=== Testing Sync Endpoint Isolation ===")
        # Test sync endpoints (which use API keys)
        await run_sync_tests(
            session, company_a_api_key, company_b_api_key,
            company_a_guid, company_b_guid
        )
        
        print("\nTests completed!")

if __name__ == "__main__":
    asyncio.run(main()) 