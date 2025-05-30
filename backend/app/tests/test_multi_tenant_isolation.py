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
import pytest

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

# --- SOFT DELETE & RESTORE TESTS ---

@pytest.mark.asyncio
async def test_soft_delete_via_rest_endpoint(aiohttp_client, get_auth_token):
    """
    Test soft delete of a project via REST endpoint and verify cascade.
    """
    # 1. Authenticate as CompanyAdmin
    token = await get_auth_token("admin1.a@example.com", "password")
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create a project, component, assembly, piece, article (via sync endpoints)
    # Create project
    project_payload = {
        "projects": [{
            "code": "TEST_SOFTDEL_PROJ",
            "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71",
            "due_date": "2024-12-31T23:59:59Z"
        }]
    }
    async with aiohttp_client.post(f"{BASE_URL}/api/v1/sync/projects", json=project_payload, headers=headers) as resp:
        assert resp.status == 200
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/projects", headers=headers) as resp:
        data = await resp.json()
        project_guid = data["projects"][0]["guid"]

    # Create component
    component_payload = {
        "components": [{
            "code": "TEST_SOFTDEL_COMP",
            "project_guid": project_guid,
            "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71",
            "quantity": 1
        }]
    }
    async with aiohttp_client.post(f"{BASE_URL}/api/v1/sync/components", json=component_payload, headers=headers) as resp:
        assert resp.status == 200
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/components?project_guid={project_guid}", headers=headers) as resp:
        data = await resp.json()
        component_guid = data["components"][0]["guid"]

    # Create assembly
    assembly_payload = {
        "assemblies": [{
            "project_guid": project_guid,
            "component_guid": component_guid,
            "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71",
            "trolley": "T1",
            "cell_number": 1
        }]
    }
    async with aiohttp_client.post(f"{BASE_URL}/api/v1/sync/assemblies", json=assembly_payload, headers=headers) as resp:
        assert resp.status == 200
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/assemblies?component_guid={component_guid}", headers=headers) as resp:
        data = await resp.json()
        assembly_guid = data["assemblies"][0]["guid"]

    # Create piece
    piece_payload = {
        "pieces": [{
            "piece_id": "TEST_SOFTDEL_PIECE",
            "project_guid": project_guid,
            "component_guid": component_guid,
            "assembly_guid": assembly_guid,
            "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71",
            "outer_length": 100,
            "angle_left": 45,
            "angle_right": 45
        }]
    }
    async with aiohttp_client.post(f"{BASE_URL}/api/v1/sync/pieces", json=piece_payload, headers=headers) as resp:
        assert resp.status == 200
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/pieces?assembly_guid={assembly_guid}", headers=headers) as resp:
        data = await resp.json()
        piece_guid = data["pieces"][0]["guid"]

    # Create article
    article_payload = {
        "articles": [{
            "code": "TEST_SOFTDEL_ARTICLE",
            "project_guid": project_guid,
            "component_guid": component_guid,
            "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71",
            "designation": "Test Article",
            "quantity": 1.0,
            "unit": "pcs"
        }]
    }
    async with aiohttp_client.post(f"{BASE_URL}/api/v1/sync/articles", json=article_payload, headers=headers) as resp:
        assert resp.status == 200
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/articles?component_guid={component_guid}", headers=headers) as resp:
        data = await resp.json()
        article_guid = data["articles"][0]["guid"]

    # 3. Soft delete the project via REST endpoint
    async with aiohttp_client.delete(f"{BASE_URL}/api/v1/projects/{project_guid}", headers=headers) as resp:
        assert resp.status == 200

    # 4. Verify project and all children are is_active=False, deleted_at is set
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/projects/{project_guid}", headers=headers) as resp:
        project = await resp.json()
        assert not project["is_active"]
        assert project["deleted_at"] is not None
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/components/{component_guid}", headers=headers) as resp:
        component = await resp.json()
        assert not component["is_active"]
        assert component["deleted_at"] is not None
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/assemblies/{assembly_guid}", headers=headers) as resp:
        assembly = await resp.json()
        assert not assembly["is_active"]
        assert assembly["deleted_at"] is not None
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/pieces/{piece_guid}", headers=headers) as resp:
        piece = await resp.json()
        assert not piece["is_active"]
        assert piece["deleted_at"] is not None
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/articles/{article_guid}", headers=headers) as resp:
        article = await resp.json()
        assert not article["is_active"]
        assert article["deleted_at"] is not None

    # 5. GET with/without ?include_inactive=true
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/projects", headers=headers) as resp:
        data = await resp.json()
        assert all(p["is_active"] for p in data["projects"] if p["guid"] != project_guid)
        assert all(p["guid"] != project_guid for p in data["projects"])
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/projects?include_inactive=true", headers=headers) as resp:
        data = await resp.json()
        assert any(p["guid"] == project_guid and not p["is_active"] for p in data["projects"])

    # 6. Restore via POST /api/v1/projects/{guid}/restore
    async with aiohttp_client.post(f"{BASE_URL}/api/v1/projects/{project_guid}/restore", headers=headers) as resp:
        assert resp.status == 200

    # 7. Verify only children with matching deleted_at are restored
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/projects/{project_guid}", headers=headers) as resp:
        project = await resp.json()
        assert project["is_active"]
        assert project["deleted_at"] is None
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/components/{component_guid}", headers=headers) as resp:
        component = await resp.json()
        assert component["is_active"]
        assert component["deleted_at"] is None
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/assemblies/{assembly_guid}", headers=headers) as resp:
        assembly = await resp.json()
        assert assembly["is_active"]
        assert assembly["deleted_at"] is None
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/pieces/{piece_guid}", headers=headers) as resp:
        piece = await resp.json()
        assert piece["is_active"]
        assert piece["deleted_at"] is None
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/articles/{article_guid}", headers=headers) as resp:
        article = await resp.json()
        assert article["is_active"]
        assert article["deleted_at"] is None

    # 8. Reactivate via sync endpoint (simulate reactivation)
    project_update_payload = {
        "projects": [{
            "guid": project_guid,
            "code": "TEST_SOFTDEL_PROJ_UPDATED",
            "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71",
            "due_date": "2025-01-01T00:00:00Z"
        }]
    }
    async with aiohttp_client.post(f"{BASE_URL}/api/v1/sync/projects", json=project_update_payload, headers=headers) as resp:
        assert resp.status == 200
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/projects/{project_guid}", headers=headers) as resp:
        project = await resp.json()
        assert project["is_active"]
        assert project["deleted_at"] is None
        assert project["code"] == "TEST_SOFTDEL_PROJ_UPDATED"

@pytest.mark.asyncio
async def test_soft_delete_via_sync_endpoint(aiohttp_client, get_auth_token):
    """
    Test soft delete of a component via sync endpoint and verify cascade.
    """
    # 1. Authenticate as CompanyAdmin
    token = await get_auth_token("admin1.a@example.com", "password")
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create a project and component (via sync endpoints)
    project_payload = {
        "projects": [{
            "code": "SYNC_SOFTDEL_PROJ",
            "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71",
            "due_date": "2024-12-31T23:59:59Z"
        }]
    }
    async with aiohttp_client.post(f"{BASE_URL}/api/v1/sync/projects", json=project_payload, headers=headers) as resp:
        assert resp.status == 200
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/projects", headers=headers) as resp:
        data = await resp.json()
        project_guid = [p["guid"] for p in data["projects"] if p["code"] == "SYNC_SOFTDEL_PROJ"][0]

    component_payload = {
        "components": [{
            "code": "SYNC_SOFTDEL_COMP",
            "project_guid": project_guid,
            "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71",
            "quantity": 1
        }]
    }
    async with aiohttp_client.post(f"{BASE_URL}/api/v1/sync/components", json=component_payload, headers=headers) as resp:
        assert resp.status == 200
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/components?project_guid={project_guid}", headers=headers) as resp:
        data = await resp.json()
        component_guid = [c["guid"] for c in data["components"] if c["code"] == "SYNC_SOFTDEL_COMP"][0]

    # Create a piece and article for the component
    piece_payload = {
        "pieces": [{
            "piece_id": "SYNC_SOFTDEL_PIECE",
            "project_guid": project_guid,
            "component_guid": component_guid,
            "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71",
            "outer_length": 100,
            "angle_left": 45,
            "angle_right": 45
        }]
    }
    async with aiohttp_client.post(f"{BASE_URL}/api/v1/sync/pieces", json=piece_payload, headers=headers) as resp:
        assert resp.status == 200
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/pieces?component_guid={component_guid}", headers=headers) as resp:
        data = await resp.json()
        piece_guid = [p["guid"] for p in data["pieces"] if p["piece_id"] == "SYNC_SOFTDEL_PIECE"][0]

    article_payload = {
        "articles": [{
            "code": "SYNC_SOFTDEL_ARTICLE",
            "project_guid": project_guid,
            "component_guid": component_guid,
            "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71",
            "designation": "Test Article",
            "quantity": 1.0,
            "unit": "pcs"
        }]
    }
    async with aiohttp_client.post(f"{BASE_URL}/api/v1/sync/articles", json=article_payload, headers=headers) as resp:
        assert resp.status == 200
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/articles?component_guid={component_guid}", headers=headers) as resp:
        data = await resp.json()
        article_guid = [a["guid"] for a in data["articles"] if a["code"] == "SYNC_SOFTDEL_ARTICLE"][0]

    # 3. Soft delete the component by omitting it from a sync payload (simulate removal)
    # Sync only the project, omitting the component
    async with aiohttp_client.post(f"{BASE_URL}/api/v1/sync/projects", json=project_payload, headers=headers) as resp:
        assert resp.status == 200
    # Now the component should be soft deleted

    # 4. Verify component and its children are is_active=False, deleted_at is set
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/components/{component_guid}", headers=headers) as resp:
        component = await resp.json()
        assert not component["is_active"]
        assert component["deleted_at"] is not None
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/pieces/{piece_guid}", headers=headers) as resp:
        piece = await resp.json()
        assert not piece["is_active"]
        assert piece["deleted_at"] is not None
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/articles/{article_guid}", headers=headers) as resp:
        article = await resp.json()
        assert not article["is_active"]
        assert article["deleted_at"] is not None

    # 5. Restore the component via POST /api/v1/components/{guid}/restore
    async with aiohttp_client.post(f"{BASE_URL}/api/v1/components/{component_guid}/restore", headers=headers) as resp:
        assert resp.status == 200

    # 6. Verify only children with matching deleted_at are restored
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/components/{component_guid}", headers=headers) as resp:
        component = await resp.json()
        assert component["is_active"]
        assert component["deleted_at"] is None
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/pieces/{piece_guid}", headers=headers) as resp:
        piece = await resp.json()
        assert piece["is_active"]
        assert piece["deleted_at"] is None
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/articles/{article_guid}", headers=headers) as resp:
        article = await resp.json()
        assert article["is_active"]
        assert article["deleted_at"] is None

@pytest.mark.asyncio
async def test_cascade_soft_delete(aiohttp_client, get_auth_token):
    """
    Test that soft deleting a parent cascades to all active children.
    """
    # 1. Authenticate as CompanyAdmin
    token = await get_auth_token("admin1.a@example.com", "password")
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create a project, component, assembly, and piece (via sync endpoints)
    project_payload = {
        "projects": [{
            "code": "CASCADE_SOFTDEL_PROJ",
            "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71",
            "due_date": "2024-12-31T23:59:59Z"
        }]
    }
    async with aiohttp_client.post(f"{BASE_URL}/api/v1/sync/projects", json=project_payload, headers=headers) as resp:
        assert resp.status == 200
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/projects", headers=headers) as resp:
        data = await resp.json()
        project_guid = [p["guid"] for p in data["projects"] if p["code"] == "CASCADE_SOFTDEL_PROJ"][0]

    component_payload = {
        "components": [{
            "code": "CASCADE_SOFTDEL_COMP",
            "project_guid": project_guid,
            "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71",
            "quantity": 1
        }]
    }
    async with aiohttp_client.post(f"{BASE_URL}/api/v1/sync/components", json=component_payload, headers=headers) as resp:
        assert resp.status == 200
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/components?project_guid={project_guid}", headers=headers) as resp:
        data = await resp.json()
        component_guid = [c["guid"] for c in data["components"] if c["code"] == "CASCADE_SOFTDEL_COMP"][0]

    assembly_payload = {
        "assemblies": [{
            "project_guid": project_guid,
            "component_guid": component_guid,
            "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71",
            "trolley": "T1",
            "cell_number": 1
        }]
    }
    async with aiohttp_client.post(f"{BASE_URL}/api/v1/sync/assemblies", json=assembly_payload, headers=headers) as resp:
        assert resp.status == 200
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/assemblies?component_guid={component_guid}", headers=headers) as resp:
        data = await resp.json()
        assembly_guid = [a["guid"] for a in data["assemblies"] if a["trolley"] == "T1"][0]

    piece_payload = {
        "pieces": [{
            "piece_id": "CASCADE_SOFTDEL_PIECE",
            "project_guid": project_guid,
            "component_guid": component_guid,
            "assembly_guid": assembly_guid,
            "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71",
            "outer_length": 100,
            "angle_left": 45,
            "angle_right": 45
        }]
    }
    async with aiohttp_client.post(f"{BASE_URL}/api/v1/sync/pieces", json=piece_payload, headers=headers) as resp:
        assert resp.status == 200
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/pieces?assembly_guid={assembly_guid}", headers=headers) as resp:
        data = await resp.json()
        piece_guid = [p["guid"] for p in data["pieces"] if p["piece_id"] == "CASCADE_SOFTDEL_PIECE"][0]

    # 3. Soft delete the component via REST endpoint
    async with aiohttp_client.delete(f"{BASE_URL}/api/v1/components/{component_guid}", headers=headers) as resp:
        assert resp.status == 200

    # 4. Verify the component and all its children are is_active=False, deleted_at is set
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/components/{component_guid}", headers=headers) as resp:
        component = await resp.json()
        assert not component["is_active"]
        assert component["deleted_at"] is not None
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/assemblies/{assembly_guid}", headers=headers) as resp:
        assembly = await resp.json()
        assert not assembly["is_active"]
        assert assembly["deleted_at"] is not None
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/pieces/{piece_guid}", headers=headers) as resp:
        piece = await resp.json()
        assert not piece["is_active"]
        assert piece["deleted_at"] is not None

@pytest.mark.asyncio
async def test_restore_and_selective_child_restoration(aiohttp_client, get_auth_token):
    """
    Test that restoring a parent only restores children with matching deleted_at.
    """
    # 1. Authenticate as CompanyAdmin
    token = await get_auth_token("admin1.a@example.com", "password")
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create a project, component, and two pieces (via sync endpoints)
    project_payload = {
        "projects": [{
            "code": "SELECTIVE_RESTORE_PROJ",
            "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71",
            "due_date": "2024-12-31T23:59:59Z"
        }]
    }
    async with aiohttp_client.post(f"{BASE_URL}/api/v1/sync/projects", json=project_payload, headers=headers) as resp:
        assert resp.status == 200
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/projects", headers=headers) as resp:
        data = await resp.json()
        project_guid = [p["guid"] for p in data["projects"] if p["code"] == "SELECTIVE_RESTORE_PROJ"][0]

    component_payload = {
        "components": [{
            "code": "SELECTIVE_RESTORE_COMP",
            "project_guid": project_guid,
            "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71",
            "quantity": 1
        }]
    }
    async with aiohttp_client.post(f"{BASE_URL}/api/v1/sync/components", json=component_payload, headers=headers) as resp:
        assert resp.status == 200
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/components?project_guid={project_guid}", headers=headers) as resp:
        data = await resp.json()
        component_guid = [c["guid"] for c in data["components"] if c["code"] == "SELECTIVE_RESTORE_COMP"][0]

    # Create two pieces for the component
    piece_payload = {
        "pieces": [
            {
                "piece_id": "SELECTIVE_RESTORE_PIECE1",
                "project_guid": project_guid,
                "component_guid": component_guid,
                "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71",
                "outer_length": 100,
                "angle_left": 45,
                "angle_right": 45
            },
            {
                "piece_id": "SELECTIVE_RESTORE_PIECE2",
                "project_guid": project_guid,
                "component_guid": component_guid,
                "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71",
                "outer_length": 200,
                "angle_left": 90,
                "angle_right": 90
            }
        ]
    }
    async with aiohttp_client.post(f"{BASE_URL}/api/v1/sync/pieces", json=piece_payload, headers=headers) as resp:
        assert resp.status == 200
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/pieces?component_guid={component_guid}", headers=headers) as resp:
        data = await resp.json()
        piece1_guid = [p["guid"] for p in data["pieces"] if p["piece_id"] == "SELECTIVE_RESTORE_PIECE1"][0]
        piece2_guid = [p["guid"] for p in data["pieces"] if p["piece_id"] == "SELECTIVE_RESTORE_PIECE2"][0]

    # 3. Soft delete the component via REST endpoint
    async with aiohttp_client.delete(f"{BASE_URL}/api/v1/components/{component_guid}", headers=headers) as resp:
        assert resp.status == 200

    # 4. Manually soft delete one piece with a different deleted_at (simulate an older soft delete)
    # (This step would require direct DB access or a PATCH endpoint; here we simulate by soft deleting piece2 again)
    # For the test, we assume both pieces have the same deleted_at after cascade, so we restore the component, then soft delete piece2 again
    async with aiohttp_client.post(f"{BASE_URL}/api/v1/components/{component_guid}/restore", headers=headers) as resp:
        assert resp.status == 200
    # Soft delete piece2 only
    async with aiohttp_client.delete(f"{BASE_URL}/api/v1/pieces/{piece2_guid}", headers=headers) as resp:
        assert resp.status == 200
    # Soft delete the component again to cascade to piece1 only
    async with aiohttp_client.delete(f"{BASE_URL}/api/v1/components/{component_guid}", headers=headers) as resp:
        assert resp.status == 200

    # 5. Restore the component via POST /api/v1/components/{guid}/restore
    async with aiohttp_client.post(f"{BASE_URL}/api/v1/components/{component_guid}/restore", headers=headers) as resp:
        assert resp.status == 200

    # 6. Verify only the piece with matching deleted_at is restored, the other remains soft deleted
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/pieces/{piece1_guid}", headers=headers) as resp:
        piece1 = await resp.json()
        assert piece1["is_active"]
        assert piece1["deleted_at"] is None
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/pieces/{piece2_guid}", headers=headers) as resp:
        piece2 = await resp.json()
        assert not piece2["is_active"]
        assert piece2["deleted_at"] is not None

@pytest.mark.asyncio
async def test_sync_after_soft_delete_reactivation(aiohttp_client, get_auth_token):
    """
    Test that syncing a soft-deleted entity reactivates it and updates fields.
    """
    # 1. Authenticate as CompanyAdmin
    token = await get_auth_token("admin1.a@example.com", "password")
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create a project and component (via sync endpoints)
    project_payload = {
        "projects": [{
            "code": "REACTIVATE_PROJ",
            "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71",
            "due_date": "2024-12-31T23:59:59Z"
        }]
    }
    async with aiohttp_client.post(f"{BASE_URL}/api/v1/sync/projects", json=project_payload, headers=headers) as resp:
        assert resp.status == 200
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/projects", headers=headers) as resp:
        data = await resp.json()
        project_guid = [p["guid"] for p in data["projects"] if p["code"] == "REACTIVATE_PROJ"][0]

    component_payload = {
        "components": [{
            "code": "REACTIVATE_COMP",
            "project_guid": project_guid,
            "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71",
            "quantity": 1
        }]
    }
    async with aiohttp_client.post(f"{BASE_URL}/api/v1/sync/components", json=component_payload, headers=headers) as resp:
        assert resp.status == 200
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/components?project_guid={project_guid}", headers=headers) as resp:
        data = await resp.json()
        component_guid = [c["guid"] for c in data["components"] if c["code"] == "REACTIVATE_COMP"][0]

    # 3. Soft delete the component via REST endpoint
    async with aiohttp_client.delete(f"{BASE_URL}/api/v1/components/{component_guid}", headers=headers) as resp:
        assert resp.status == 200

    # 4. Reactivate the component by syncing it again (with the same GUID)
    component_update_payload = {
        "components": [{
            "guid": component_guid,
            "code": "REACTIVATE_COMP_UPDATED",
            "project_guid": project_guid,
            "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71",
            "quantity": 2
        }]
    }
    async with aiohttp_client.post(f"{BASE_URL}/api/v1/sync/components", json=component_update_payload, headers=headers) as resp:
        assert resp.status == 200

    # 5. Verify the component is_active=True, deleted_at is None, and fields are updated
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/components/{component_guid}", headers=headers) as resp:
        component = await resp.json()
        assert component["is_active"]
        assert component["deleted_at"] is None
        assert component["code"] == "REACTIVATE_COMP_UPDATED"
        assert component["quantity"] == 2

@pytest.mark.asyncio
async def test_get_with_and_without_inactive_entities(aiohttp_client, get_auth_token):
    """
    Test GET endpoints with and without ?include_inactive=true.
    """
    # 1. Authenticate as CompanyAdmin
    token = await get_auth_token("admin1.a@example.com", "password")
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create a project and component (via sync endpoints)
    project_payload = {
        "projects": [{
            "code": "GET_INACTIVE_PROJ",
            "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71",
            "due_date": "2024-12-31T23:59:59Z"
        }]
    }
    async with aiohttp_client.post(f"{BASE_URL}/api/v1/sync/projects", json=project_payload, headers=headers) as resp:
        assert resp.status == 200
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/projects", headers=headers) as resp:
        data = await resp.json()
        project_guid = [p["guid"] for p in data["projects"] if p["code"] == "GET_INACTIVE_PROJ"][0]

    component_payload = {
        "components": [{
            "code": "GET_INACTIVE_COMP",
            "project_guid": project_guid,
            "company_guid": "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71",
            "quantity": 1
        }]
    }
    async with aiohttp_client.post(f"{BASE_URL}/api/v1/sync/components", json=component_payload, headers=headers) as resp:
        assert resp.status == 200
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/components?project_guid={project_guid}", headers=headers) as resp:
        data = await resp.json()
        component_guid = [c["guid"] for c in data["components"] if c["code"] == "GET_INACTIVE_COMP"][0]

    # 3. Soft delete the component via REST endpoint
    async with aiohttp_client.delete(f"{BASE_URL}/api/v1/components/{component_guid}", headers=headers) as resp:
        assert resp.status == 200

    # 4. Call GET /api/v1/components (should not include soft-deleted component)
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/components?project_guid={project_guid}", headers=headers) as resp:
        data = await resp.json()
        assert all(c["guid"] != component_guid for c in data["components"])

    # 5. Call GET /api/v1/components?include_inactive=true (should include soft-deleted component)
    async with aiohttp_client.get(f"{BASE_URL}/api/v1/components?project_guid={project_guid}&include_inactive=true", headers=headers) as resp:
        data = await resp.json()
        assert any(c["guid"] == component_guid and not c["is_active"] for c in data["components"])

if __name__ == "__main__":
    asyncio.run(main()) 