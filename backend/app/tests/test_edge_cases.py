#!/usr/bin/env python3
"""
Test script for soft delete business logic edge cases.
This script tests multiple generations of soft-deleted children and other edge cases.
"""

import pytest
import aiohttp
import os
from typing import Dict, Any

# --- Constants ---
BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_PREFIX = "/api/v1"
COMPANY_GUID = "11111111-1111-1111-1111-111111111111"  # Test Company A (admin1.a@example.com) - predefined
EMAIL = "admin1.a@example.com"
PASSWORD = "password"

# --- Helper Functions ---

async def get_auth_token(session: aiohttp.ClientSession) -> str:
    """Get authentication token for a user."""
    login_url = f"{BASE_URL}{API_PREFIX}/auth/login"
    credentials = {"email": EMAIL, "password": PASSWORD}
    async with session.post(login_url, json=credentials) as response:
        response.raise_for_status()
        data = await response.json()
        return data["access_token"]

async def find_guid_by_code(session: aiohttp.ClientSession, headers: Dict[str, Any], endpoint: str, params: Dict[str, Any], code: str, collection_key: str) -> str:
    """Helper to find a GUID for an entity with a given code."""
    url = f"{BASE_URL}{API_PREFIX}/{endpoint}"
    async with session.get(url, headers=headers, params=params) as response:
        response.raise_for_status()
        data = await response.json()
        # API returns a list directly, not an object with a collection key
        items = data if isinstance(data, list) else data.get(collection_key, [])
        item = next((p for p in items if p["code"] == code), None)
        assert item, f"Could not find entity with code '{code}'"
        return item["guid"]

# --- Tests ---

@pytest.mark.asyncio
async def test_multiple_generations_soft_delete():
    """Test soft delete cascade across multiple generations of entities."""
    async with aiohttp.ClientSession() as session:
        token = await get_auth_token(session)
        headers = {"Authorization": f"Bearer {token}"}

        # 1. Create a project
        project_payload = {"projects": [{"code": "MULTI_GEN_PROJ", "company_guid": COMPANY_GUID}]}
        async with session.post(f"{BASE_URL}{API_PREFIX}/sync/projects", json=project_payload, headers=headers) as resp:
            assert resp.status == 200

        project_guid = await find_guid_by_code(session, headers, "projects", {}, "MULTI_GEN_PROJ", "projects")

        # 2. Create components, assemblies, pieces, etc.
        component_payload = {"components": [{"code": "MULTI_GEN_COMP", "project_guid": project_guid, "company_guid": COMPANY_GUID}]}
        async with session.post(f"{BASE_URL}{API_PREFIX}/sync/components", json=component_payload, headers=headers) as resp:
            assert resp.status == 200
        component_guid = await find_guid_by_code(session, headers, "components", {"project_guid": project_guid}, "MULTI_GEN_COMP", "components")

        assembly_payload = {"assemblies": [{"trolley": "MULTI_GEN_ASSY", "project_guid": project_guid, "component_guid": component_guid, "company_guid": COMPANY_GUID}]}
        async with session.post(f"{BASE_URL}{API_PREFIX}/sync/assemblies", json=assembly_payload, headers=headers) as resp:
            assert resp.status == 200
        # Get assembly by trolley instead of code
        async with session.get(f"{BASE_URL}{API_PREFIX}/assemblies", headers=headers, params={"component_guid": component_guid}) as resp:
            assemblies = await resp.json()
            assembly = next((a for a in assemblies if a.get("trolley") == "MULTI_GEN_ASSY"), None)
            assert assembly, "Could not find assembly with trolley 'MULTI_GEN_ASSY'"
            assembly_guid = assembly["guid"]

        # 3. Soft delete the project
        async with session.delete(f"{BASE_URL}{API_PREFIX}/projects/{project_guid}", headers=headers) as resp:
            assert resp.status in (200, 204)

        # 4. Verify all children are inactive
        async with session.get(f"{BASE_URL}{API_PREFIX}/projects/{project_guid}?include_inactive=true", headers=headers) as resp:
            assert not (await resp.json())["is_active"]
        async with session.get(f"{BASE_URL}{API_PREFIX}/components/{component_guid}?include_inactive=true", headers=headers) as resp:
            assert not (await resp.json())["is_active"]
        async with session.get(f"{BASE_URL}{API_PREFIX}/assemblies/{assembly_guid}?include_inactive=true", headers=headers) as resp:
            assert not (await resp.json())["is_active"]

@pytest.mark.asyncio
async def test_partial_soft_delete_and_selective_restore():
    """Test selectively restoring parts of a soft-deleted hierarchy."""
    async with aiohttp.ClientSession() as session:
        token = await get_auth_token(session)
        headers = {"Authorization": f"Bearer {token}"}

        # 1. Create a project and components
        project_payload = {"projects": [{"code": "PARTIAL_DEL_PROJ", "company_guid": COMPANY_GUID}]}
        async with session.post(f"{BASE_URL}{API_PREFIX}/sync/projects", json=project_payload, headers=headers) as resp:
            assert resp.status == 200
        project_guid = await find_guid_by_code(session, headers, "projects", {}, "PARTIAL_DEL_PROJ", "projects")

        comp_payload = {"components": [
            {"code": "COMP_A", "project_guid": project_guid, "company_guid": COMPANY_GUID},
            {"code": "COMP_B", "project_guid": project_guid, "company_guid": COMPANY_GUID}
        ]}
        async with session.post(f"{BASE_URL}{API_PREFIX}/sync/components", json=comp_payload, headers=headers) as resp:
            assert resp.status == 200
        comp_a_guid = await find_guid_by_code(session, headers, "components", {"project_guid": project_guid}, "COMP_A", "components")
        comp_b_guid = await find_guid_by_code(session, headers, "components", {"project_guid": project_guid}, "COMP_B", "components")

        # 2. Soft delete only one component
        async with session.delete(f"{BASE_URL}{API_PREFIX}/components/{comp_a_guid}", headers=headers) as resp:
            assert resp.status in (200, 204)

        # 3. Soft delete the whole project
        async with session.delete(f"{BASE_URL}{API_PREFIX}/projects/{project_guid}", headers=headers) as resp:
            assert resp.status in (200, 204)

        # 4. Restore the project
        async with session.post(f"{BASE_URL}{API_PREFIX}/projects/{project_guid}/restore", headers=headers) as resp:
            assert resp.status in (200, 204)

        # 5. Verify only the component deleted with the project is restored
        async with session.get(f"{BASE_URL}{API_PREFIX}/components/{comp_a_guid}?include_inactive=true", headers=headers) as resp:
            assert not (await resp.json())["is_active"], "Component A should remain deleted"
        async with session.get(f"{BASE_URL}{API_PREFIX}/components/{comp_b_guid}", headers=headers) as resp:
            assert (await resp.json())["is_active"], "Component B should be restored"

@pytest.mark.asyncio
async def test_sync_reactivation_edge_cases():
    """Test that syncing a deleted entity reactivates it."""
    async with aiohttp.ClientSession() as session:
        token = await get_auth_token(session)
        headers = {"Authorization": f"Bearer {token}"}

        # 1. Create and delete a project
        project_payload = {"projects": [{"code": "SYNC_REACT_PROJ", "company_guid": COMPANY_GUID}]}
        async with session.post(f"{BASE_URL}{API_PREFIX}/sync/projects", json=project_payload, headers=headers) as resp:
            assert resp.status == 200
        project_guid = await find_guid_by_code(session, headers, "projects", {}, "SYNC_REACT_PROJ", "projects")
        async with session.delete(f"{BASE_URL}{API_PREFIX}/projects/{project_guid}", headers=headers) as resp:
            assert resp.status in (200, 204)

        # 2. Reactivate via sync
        reactivate_payload = {"projects": [{"guid": project_guid, "code": "SYNC_REACT_PROJ_UPDATED", "company_guid": COMPANY_GUID}]}
        async with session.post(f"{BASE_URL}{API_PREFIX}/sync/projects", json=reactivate_payload, headers=headers) as resp:
            assert resp.status == 200

        # 3. Verify it's active and updated
        async with session.get(f"{BASE_URL}{API_PREFIX}/projects/{project_guid}", headers=headers) as resp:
            data = await resp.json()
            assert data["is_active"]
            assert data["code"] == "SYNC_REACT_PROJ_UPDATED" 