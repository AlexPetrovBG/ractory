#!/usr/bin/env python3
"""
Multi-tenant Isolation Test Script

This script provides a quick way to test the tenant isolation between companies 
across all API endpoints. It verifies that multi-tenant security is working correctly.

This script tests:
1. JWT authentication isolation - Users can only access their own company's data
2. API key authentication isolation - API keys can only access their own company's data 
3. Sync endpoint isolation - API keys can only sync data for their own company

Usage:
    python isolation_test.py
"""

import asyncio
import aiohttp
import json
import sys
from typing import Dict, Any, Optional, List

# Configuration
BASE_URL = "http://localhost:8000"
API_PREFIX = "/api/v1"

# Credentials - Change these to match your test environment
SYSTEM_ADMIN_CREDS = {"email": "a.petrov@delice.bg", "password": "password"}
COMPANY_A_ADMIN_CREDS = {"email": "admin1.a@example.com", "password": "password"}
COMPANY_B_ADMIN_CREDS = {"email": "admin1.b@example.com", "password": "password"}

async def login(session: aiohttp.ClientSession, credentials: Dict[str, str]) -> Dict[str, Any]:
    """Login and get auth tokens."""
    print(f"Logging in as {credentials['email']}...")
    async with session.post(
        f"{BASE_URL}{API_PREFIX}/auth/login",
        json=credentials
    ) as response:
        if response.status != 200:
            print(f"Login failed: {await response.text()}")
            sys.exit(1)
        data = await response.json()
        print(f"Successfully logged in as {credentials['email']}")
        return data

async def get_companies(session: aiohttp.ClientSession, token: str) -> List[Dict[str, Any]]:
    """
    Get list of companies.
    
    Args:
        session: The HTTP session
        token: SystemAdmin JWT token
    
    Returns:
        List of company objects
    """
    print("Fetching companies...")
    async with session.get(
        f"{BASE_URL}{API_PREFIX}/companies",
        headers={"Authorization": f"Bearer {token}"}
    ) as response:
        if response.status != 200:
            print(f"Failed to get companies: {await response.text()}")
            return []
        data = await response.json()
        if isinstance(data, list):
            companies = data
        else:
            companies = data.get("companies", [])
        print(f"Found {len(companies)} companies")
        return companies

async def create_api_key(session: aiohttp.ClientSession, token: str) -> Optional[str]:
    """
    Create API key for testing.
    
    Args:
        session: The HTTP session
        token: Company admin JWT token
    
    Returns:
        API key string or None if creation failed
    """
    print("Creating API key...")
    async with session.post(
        f"{BASE_URL}{API_PREFIX}/api-keys",
        headers={"Authorization": f"Bearer {token}"},
        json={"description": "Isolation Test", "scopes": "sync:read,sync:write"}
    ) as response:
        response_text = await response.text()
        print(f"API key creation response: {response_text}")
        
        if response.status not in (200, 201):  # Accept both 200 OK and 201 Created
            print(f"Failed to create API key: Status {response.status}")
            return None
        
        try:
            data = json.loads(response_text)
            # Extract the key directly from the response JSON
            if isinstance(data, dict) and "key" in data:
                api_key = data["key"]
                print(f"Created API key: {api_key}")
                return api_key
            else:
                print(f"API key not found in response JSON structure")
                return None
        except json.JSONDecodeError:
            print(f"Invalid JSON response")
            return None

async def test_endpoint(
    session: aiohttp.ClientSession,
    headers: Dict[str, str],
    endpoint: str,
    method: str = "GET",
    expected_status: int = 200,
    json_data: Optional[Dict[str, Any]] = None
) -> bool:
    """
    Test an endpoint with expected status code.
    
    Args:
        session: The HTTP session
        headers: Headers including authorization (JWT or API key)
        endpoint: API endpoint to test
        method: HTTP method (GET, POST, etc.)
        expected_status: Expected HTTP status code
        json_data: Optional JSON data for POST requests
    
    Returns:
        True if test passed (got expected status), False otherwise
    """
    full_url = f"{BASE_URL}{API_PREFIX}/{endpoint.lstrip('/')}"
    print(f"Testing {method} {endpoint}...")
    
    request_kwargs = {"headers": headers}
    if json_data:
        request_kwargs["json"] = json_data
    
    if method.upper() == "GET":
        async with session.get(full_url, **request_kwargs) as response:
            success = response.status == expected_status
            if not success:
                response_text = await response.text()
                print(f"  ✗ Expected status {expected_status}, got {response.status}: {response_text}")
            else:
                print(f"  ✓ Got expected status {expected_status}")
            return success
    elif method.upper() == "POST":
        async with session.post(full_url, **request_kwargs) as response:
            success = response.status == expected_status
            if not success:
                response_text = await response.text()
                print(f"  ✗ Expected status {expected_status}, got {response.status}: {response_text}")
            else:
                print(f"  ✓ Got expected status {expected_status}")
            return success
    else:
        print(f"Unsupported method: {method}")
        return False

async def run_tests():
    """
    Run all isolation tests.
    
    This function:
    1. Logs in as SystemAdmin to get company information
    2. Logs in as company admins for both test companies
    3. Creates API keys for testing
    4. Tests JWT isolation (users can only access their company's data)
    5. Tests API key isolation (API keys can only access their company's data)
    6. Tests sync endpoint isolation (API keys can only sync their company's data)
    """
    async with aiohttp.ClientSession() as session:
        # Login as system admin
        system_admin_data = await login(session, SYSTEM_ADMIN_CREDS)
        system_admin_token = system_admin_data["access_token"]
        
        # Get companies
        companies = await get_companies(session, system_admin_token)
        if len(companies) < 2:
            print("ERROR: Not enough companies for isolation testing")
            return
        
        company_a = companies[0]
        company_b = companies[1]
        company_a_guid = company_a["guid"]
        company_b_guid = company_b["guid"]
        
        print(f"\nCompany A: {company_a['name']} ({company_a_guid})")
        print(f"Company B: {company_b['name']} ({company_b_guid})")
        
        # Login as company admins
        company_a_data = await login(session, COMPANY_A_ADMIN_CREDS)
        company_a_token = company_a_data["access_token"]
        
        company_b_data = await login(session, COMPANY_B_ADMIN_CREDS)
        company_b_token = company_b_data["access_token"]
        
        # Create API keys
        company_a_api_key = await create_api_key(session, company_a_token)
        company_b_api_key = await create_api_key(session, company_b_token)
        
        if not company_a_api_key or not company_b_api_key:
            print("ERROR: Failed to create API keys")
            return
        
        # Test JWT isolation
        print("\n=== Testing JWT Authentication Isolation ===")
        
        # Company A user accessing own data (should succeed)
        own_access = await test_endpoint(
            session, 
            {"Authorization": f"Bearer {company_a_token}"}, 
            "/projects"
        )
        
        # Company A user trying to access Company B data via param (should fail)
        cross_access_param = await test_endpoint(
            session,
            {"Authorization": f"Bearer {company_a_token}"},
            f"/projects?company_guid={company_b_guid}",
            expected_status=403
        )
        
        # Test API key isolation
        print("\n=== Testing API Key Authentication Isolation ===")
        
        # Company A API key accessing own data (should succeed)
        api_own_access = await test_endpoint(
            session,
            {"X-API-Key": company_a_api_key},
            "/projects"
        )
        
        # Company A API key trying to access Company B data (should fail)
        api_cross_access = await test_endpoint(
            session,
            {"X-API-Key": company_a_api_key},
            f"/projects?company_guid={company_b_guid}",
            expected_status=403
        )
        
        # Test sync endpoint isolation
        print("\n=== Testing Sync Endpoint Isolation ===")
        
        # Company A API key trying to sync Company B data (should fail)
        sync_cross_access = await test_endpoint(
            session,
            {"X-API-Key": company_a_api_key},
            "/sync/projects",
            method="POST",
            json_data={"projects": [{"company_guid": company_b_guid, "code": "TEST"}]},
            expected_status=403
        )
        
        # Report results
        print("\n=== Test Results ===")
        tests = [
            ("Company A user accessing own data", own_access),
            ("Company A user accessing Company B data (parameter)", cross_access_param),
            ("Company A API key accessing own data", api_own_access),
            ("Company A API key accessing Company B data", api_cross_access),
            ("Company A API key syncing Company B data", sync_cross_access)
        ]
        
        for name, result in tests:
            status = "✓ PASS" if result else "✗ FAIL"
            print(f"{status} - {name}")
        
        success_count = sum(1 for _, result in tests if result)
        print(f"\nPassed {success_count} of {len(tests)} tests")

if __name__ == "__main__":
    asyncio.run(run_tests()) 