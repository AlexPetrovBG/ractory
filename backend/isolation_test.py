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
import pytest
import os

# Configuration
BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_PREFIX = "/api/v1"

# Credentials - Change these to match your test environment
SYSTEM_ADMIN_CREDS = {"email": "a.petrov@delice.bg", "password": "SecureAdminPassword123"}
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
            pytest.fail(f"Login failed: {await response.text()}")
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

async def check_endpoint(
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

@pytest.mark.asyncio
async def test_full_isolation_flow():
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
            pytest.fail("ERROR: Not enough companies for isolation testing")
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
        assert company_a_api_key, "Failed to create API key for Company A"
        
        company_b_api_key = await create_api_key(session, company_b_token)
        assert company_b_api_key, "Failed to create API key for Company B"
        
        # --- JWT Isolation Tests ---
        print("\n--- Testing JWT Isolation ---")
        headers_a = {"Authorization": f"Bearer {company_a_token}"}
        headers_b = {"Authorization": f"Bearer {company_b_token}"}
        
        # Company A should access its own data
        assert await check_endpoint(session, headers_a, f"/projects?company_guid={company_a_guid}", expected_status=200)
        # Company A should NOT access Company B's data
        assert await check_endpoint(session, headers_a, f"/projects?company_guid={company_b_guid}", expected_status=403)
        
        # --- API Key Isolation Tests ---
        print("\n--- Testing API Key Isolation ---")
        api_headers_a = {"X-API-Key": company_a_api_key}
        api_headers_b = {"X-API-Key": company_b_api_key}
        
        # API key A should access its own data
        assert await check_endpoint(session, api_headers_a, f"/projects?company_guid={company_a_guid}", expected_status=200)
        # API key A should NOT access Company B's data
        assert await check_endpoint(session, api_headers_a, f"/projects?company_guid={company_b_guid}", expected_status=403)
        
        # --- Sync Endpoint Isolation Tests ---
        print("\n--- Testing Sync Endpoint Isolation ---")
        
        # API key A should be able to sync its own projects
        sync_payload_a = {"projects": [{"code": "PROJ_A_SYNC", "company_guid": company_a_guid}]}
        assert await check_endpoint(session, api_headers_a, "/sync/projects", method="POST", json_data=sync_payload_a, expected_status=200)
        
        # API key A should NOT be able to sync projects for Company B
        sync_payload_b = {"projects": [{"code": "PROJ_B_SYNC_FAIL", "company_guid": company_b_guid}]}
        assert await check_endpoint(session, api_headers_a, "/sync/projects", method="POST", json_data=sync_payload_b, expected_status=403)
        
        print("\n✅ All isolation tests passed!")

if __name__ == "__main__":
    asyncio.run(test_full_isolation_flow()) 