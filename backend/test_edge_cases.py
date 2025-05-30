#!/usr/bin/env python3
"""
Test script for soft delete business logic edge cases.
This script tests multiple generations of soft-deleted children and other edge cases.
"""

import requests
import json
import uuid
import time
from datetime import datetime, timezone

# Set these constants at the top of the file for all tests
BASE_URL = "http://localhost:8000"
COMPANY_GUID = "28fbeed6-5e09-4b75-ad74-ab1cdc4dec71"
EMAIL = "a.petrov@delice.bg"
PASSWORD = "password"

def get_auth_token(base_url: str, email: str, password: str) -> str:
    """Get authentication token for a user."""
    print(f"  → Authenticating as {email}...")
    response = requests.post(
        f"{base_url}/api/v1/auth/login",
        json={"email": email, "password": password}
    )
    if response.status_code == 200:
        print(f"  ✓ Authentication successful")
        return response.json()["access_token"]
    else:
        raise Exception(f"Failed to authenticate: {response.status_code} - {response.text}")

def test_multiple_generations_soft_delete():
    """Test soft delete cascade across multiple generations of entities."""
    print("Testing multiple generations soft delete cascade...")
    
    # Authenticate
    token = get_auth_token(BASE_URL, EMAIL, PASSWORD)
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Create a project
    print("  → Creating project...")
    project_payload = {
        "projects": [{
            "code": "MULTI_GEN_PROJ",
            "company_guid": COMPANY_GUID,
            "due_date": "2024-12-31T23:59:59Z"
        }]
    }
    response = requests.post(f"{BASE_URL}/api/v1/sync/projects", json=project_payload, headers=headers)
    assert response.status_code == 200, f"Failed to create project: {response.text}"
    print(f"  ✓ Project created (status: {response.status_code})")
    
    # Get project GUID
    print("  → Fetching project GUID...")
    response = requests.get(f"{BASE_URL}/api/v1/projects", headers=headers)
    projects = response.json()
    project_guid = next(p["guid"] for p in projects if p["code"] == "MULTI_GEN_PROJ")
    print(f"  ✓ Project GUID: {project_guid}")
    
    # 2. Create multiple components
    print("  → Creating components...")
    component_payload = {
        "components": [
            {
                "code": "MULTI_GEN_COMP1",
                "project_guid": project_guid,
                "company_guid": COMPANY_GUID,
                "quantity": 1
            },
            {
                "code": "MULTI_GEN_COMP2", 
                "project_guid": project_guid,
                "company_guid": COMPANY_GUID,
                "quantity": 1
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/api/v1/sync/components", json=component_payload, headers=headers)
    assert response.status_code == 200, f"Failed to create components: {response.text}"
    print(f"  ✓ Components created (status: {response.status_code})")
    
    # Get component GUIDs
    print("  → Fetching component GUIDs...")
    response = requests.get(f"{BASE_URL}/api/v1/components?project_guid={project_guid}", headers=headers)
    components = response.json()
    comp1_guid = next(c["guid"] for c in components if c["code"] == "MULTI_GEN_COMP1")
    comp2_guid = next(c["guid"] for c in components if c["code"] == "MULTI_GEN_COMP2")
    print(f"  ✓ Component 1 GUID: {comp1_guid}")
    print(f"  ✓ Component 2 GUID: {comp2_guid}")
    
    # 3. Create assemblies for each component
    print("  → Creating assemblies...")
    assembly_payload = {
        "assemblies": [
            {
                "project_guid": project_guid,
                "component_guid": comp1_guid,
                "company_guid": COMPANY_GUID,
                "trolley": "T1",
                "cell_number": 1
            },
            {
                "project_guid": project_guid,
                "component_guid": comp2_guid,
                "company_guid": COMPANY_GUID,
                "trolley": "T2",
                "cell_number": 2
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/api/v1/sync/assemblies", json=assembly_payload, headers=headers)
    assert response.status_code == 200, f"Failed to create assemblies: {response.text}"
    print(f"  ✓ Assemblies created (status: {response.status_code})")
    
    # Get assembly GUIDs
    print("  → Fetching assembly GUIDs...")
    response = requests.get(f"{BASE_URL}/api/v1/assemblies?project_guid={project_guid}", headers=headers)
    assemblies = response.json()
    assembly1_guid = next(a["guid"] for a in assemblies if a["trolley"] == "T1")
    assembly2_guid = next(a["guid"] for a in assemblies if a["trolley"] == "T2")
    print(f"  ✓ Assembly 1 GUID: {assembly1_guid}")
    print(f"  ✓ Assembly 2 GUID: {assembly2_guid}")
    
    # 4. Create pieces for each assembly
    print("  → Creating pieces...")
    piece_payload = {
        "pieces": [
            {
                "piece_id": "MULTI_GEN_PIECE1",
                "project_guid": project_guid,
                "component_guid": comp1_guid,
                "assembly_guid": assembly1_guid,
                "company_guid": COMPANY_GUID,
                "outer_length": 100
            },
            {
                "piece_id": "MULTI_GEN_PIECE2",
                "project_guid": project_guid,
                "component_guid": comp2_guid,
                "assembly_guid": assembly2_guid,
                "company_guid": COMPANY_GUID,
                "outer_length": 200
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/api/v1/sync/pieces", json=piece_payload, headers=headers)
    assert response.status_code == 200, f"Failed to create pieces: {response.text}"
    print(f"  ✓ Pieces created (status: {response.status_code})")
    
    # Get piece GUIDs
    print("  → Fetching piece GUIDs...")
    response = requests.get(f"{BASE_URL}/api/v1/pieces?project_guid={project_guid}", headers=headers)
    pieces = response.json()
    piece1_guid = next(p["guid"] for p in pieces if p["piece_id"] == "MULTI_GEN_PIECE1")
    piece2_guid = next(p["guid"] for p in pieces if p["piece_id"] == "MULTI_GEN_PIECE2")
    print(f"  ✓ Piece 1 GUID: {piece1_guid}")
    print(f"  ✓ Piece 2 GUID: {piece2_guid}")
    
    # 5. Create articles for each component
    print("  → Creating articles...")
    article_payload = {
        "articles": [
            {
                "code": "MULTI_GEN_ART1",
                "project_guid": project_guid,
                "component_guid": comp1_guid,
                "company_guid": COMPANY_GUID,
                "designation": "Test Article 1",
                "quantity": 1.0,
                "unit": "pcs"
            },
            {
                "code": "MULTI_GEN_ART2",
                "project_guid": project_guid,
                "component_guid": comp2_guid,
                "company_guid": COMPANY_GUID,
                "designation": "Test Article 2",
                "quantity": 2.0,
                "unit": "pcs"
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/api/v1/sync/articles", json=article_payload, headers=headers)
    assert response.status_code == 200, f"Failed to create articles: {response.text}"
    print(f"  ✓ Articles created (status: {response.status_code})")
    
    # Get article GUIDs
    print("  → Fetching article GUIDs...")
    response = requests.get(f"{BASE_URL}/api/v1/articles?project_guid={project_guid}", headers=headers)
    articles = response.json()
    article1_guid = next(a["guid"] for a in articles if a["code"] == "MULTI_GEN_ART1")
    article2_guid = next(a["guid"] for a in articles if a["code"] == "MULTI_GEN_ART2")
    print(f"  ✓ Article 1 GUID: {article1_guid}")
    print(f"  ✓ Article 2 GUID: {article2_guid}")
    
    # 6. Soft delete the project (should cascade to all children)
    print("  → Soft deleting project (testing cascade)...")
    response = requests.delete(f"{BASE_URL}/api/v1/projects/{project_guid}", headers=headers)
    assert response.status_code in (200, 204), f"Failed to soft delete project: {response.text}"
    print(f"  ✓ Project soft deleted (status: {response.status_code})")
    
    # 7. Verify all entities are soft deleted with same deleted_at timestamp
    print("  → Verifying cascade soft delete...")
    entities_to_check = [
        ("projects", project_guid),
        ("components", comp1_guid),
        ("components", comp2_guid),
        ("assemblies", assembly1_guid),
        ("assemblies", assembly2_guid),
        ("pieces", piece1_guid),
        ("pieces", piece2_guid),
        ("articles", article1_guid),
        ("articles", article2_guid)
    ]
    
    deleted_timestamps = []
    for i, (entity_type, entity_guid) in enumerate(entities_to_check, 1):
        print(f"    → Checking {entity_type} {entity_guid} ({i}/{len(entities_to_check)})...")
        response = requests.get(f"{BASE_URL}/api/v1/{entity_type}/{entity_guid}?include_inactive=true", headers=headers)
        assert response.status_code == 200, f"Failed to get {entity_type} {entity_guid}: {response.text}"
        entity = response.json()
        assert not entity["is_active"], f"{entity_type} {entity_guid} should be inactive"
        assert entity["deleted_at"] is not None, f"{entity_type} {entity_guid} should have deleted_at set"
        deleted_timestamps.append(entity["deleted_at"])
        print(f"    ✓ {entity_type} is soft deleted (deleted_at: {entity['deleted_at']})")
    
    # All entities should have the same deleted_at timestamp (cascade delete)
    print("  → Verifying cascade timestamp consistency...")
    assert len(set(deleted_timestamps)) == 1, "All cascaded entities should have the same deleted_at timestamp"
    print(f"  ✓ All entities have same deleted_at timestamp: {deleted_timestamps[0]}")
    
    # 8. Test selective restoration - restore the project
    print("  → Restoring project (testing selective restoration)...")
    response = requests.post(f"{BASE_URL}/api/v1/projects/{project_guid}/restore", headers=headers)
    assert response.status_code in (200, 204), f"Failed to restore project: {response.text}"
    print(f"  ✓ Project restored (status: {response.status_code})")
    
    # 9. Verify all entities with matching deleted_at are restored
    print("  → Verifying selective restoration...")
    for i, (entity_type, entity_guid) in enumerate(entities_to_check, 1):
        print(f"    → Checking restored {entity_type} {entity_guid} ({i}/{len(entities_to_check)})...")
        response = requests.get(f"{BASE_URL}/api/v1/{entity_type}/{entity_guid}", headers=headers)
        assert response.status_code == 200, f"Failed to get {entity_type} {entity_guid}: {response.text}"
        entity = response.json()
        assert entity["is_active"], f"{entity_type} {entity_guid} should be active after restore"
        assert entity["deleted_at"] is None, f"{entity_type} {entity_guid} should have deleted_at cleared"
        print(f"    ✓ {entity_type} is restored (is_active: {entity['is_active']}, deleted_at: {entity['deleted_at']})")
    
    print("✓ Multiple generations soft delete cascade test passed")

def test_partial_soft_delete_and_selective_restore():
    """Test partial soft delete and selective restoration."""
    print("Testing partial soft delete and selective restoration...")
    
    # Authenticate
    token = get_auth_token(BASE_URL, EMAIL, PASSWORD)
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Create a project with components
    print("  → Creating project for partial test...")
    project_payload = {
        "projects": [{
            "code": "PARTIAL_SOFTDEL_PROJ",
            "company_guid": COMPANY_GUID,
            "due_date": "2024-12-31T23:59:59Z"
        }]
    }
    response = requests.post(f"{BASE_URL}/api/v1/sync/projects", json=project_payload, headers=headers)
    assert response.status_code == 200
    print(f"  ✓ Project created (status: {response.status_code})")
    
    # Get project GUID
    print("  → Fetching project GUID...")
    response = requests.get(f"{BASE_URL}/api/v1/projects", headers=headers)
    projects = response.json()
    project_guid = next(p["guid"] for p in projects if p["code"] == "PARTIAL_SOFTDEL_PROJ")
    print(f"  ✓ Project GUID: {project_guid}")
    
    # 2. Create components
    print("  → Creating components for partial test...")
    component_payload = {
        "components": [
            {
                "code": "PARTIAL_COMP1",
                "project_guid": project_guid,
                "company_guid": COMPANY_GUID,
                "quantity": 1
            },
            {
                "code": "PARTIAL_COMP2",
                "project_guid": project_guid,
                "company_guid": COMPANY_GUID,
                "quantity": 1
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/api/v1/sync/components", json=component_payload, headers=headers)
    assert response.status_code == 200
    print(f"  ✓ Components created (status: {response.status_code})")
    
    # Get component GUIDs
    print("  → Fetching component GUIDs...")
    response = requests.get(f"{BASE_URL}/api/v1/components?project_guid={project_guid}", headers=headers)
    components = response.json()
    comp1_guid = next(c["guid"] for c in components if c["code"] == "PARTIAL_COMP1")
    comp2_guid = next(c["guid"] for c in components if c["code"] == "PARTIAL_COMP2")
    print(f"  ✓ Component 1 GUID: {comp1_guid}")
    print(f"  ✓ Component 2 GUID: {comp2_guid}")
    
    # 3. Soft delete first component
    print("  → Soft deleting first component...")
    response = requests.delete(f"{BASE_URL}/api/v1/components/{comp1_guid}", headers=headers)
    assert response.status_code in (200, 204)
    print(f"  ✓ First component soft deleted (status: {response.status_code})")
    
    # Get the deleted_at timestamp
    print("  → Getting first component deleted_at timestamp...")
    response = requests.get(f"{BASE_URL}/api/v1/components/{comp1_guid}", headers=headers)
    comp1_deleted_at = response.json()["deleted_at"]
    print(f"  ✓ First component deleted_at: {comp1_deleted_at}")
    
    # 4. Later, soft delete second component (different timestamp)
    print("  → Waiting 1 second for different timestamp...")
    time.sleep(1)  # Ensure different timestamp
    print("  → Soft deleting second component...")
    response = requests.delete(f"{BASE_URL}/api/v1/components/{comp2_guid}", headers=headers)
    assert response.status_code in (200, 204)
    print(f"  ✓ Second component soft deleted (status: {response.status_code})")
    
    # Get the deleted_at timestamp
    print("  → Getting second component deleted_at timestamp...")
    response = requests.get(f"{BASE_URL}/api/v1/components/{comp2_guid}", headers=headers)
    comp2_deleted_at = response.json()["deleted_at"]
    print(f"  ✓ Second component deleted_at: {comp2_deleted_at}")
    
    # Verify different timestamps
    print("  → Verifying different timestamps...")
    assert comp1_deleted_at != comp2_deleted_at, "Components should have different deleted_at timestamps"
    print("  ✓ Components have different deleted_at timestamps")
    
    # 5. Restore first component
    print("  → Restoring first component...")
    response = requests.post(f"{BASE_URL}/api/v1/components/{comp1_guid}/restore", headers=headers)
    assert response.status_code in (200, 204)
    print(f"  ✓ First component restored (status: {response.status_code})")
    
    # 6. Verify only first component is restored
    print("  → Verifying selective restoration...")
    response = requests.get(f"{BASE_URL}/api/v1/components/{comp1_guid}", headers=headers)
    comp1 = response.json()
    assert comp1["is_active"], "First component should be restored"
    assert comp1["deleted_at"] is None, "First component deleted_at should be cleared"
    print(f"  ✓ First component is restored (is_active: {comp1['is_active']}, deleted_at: {comp1['deleted_at']})")
    
    response = requests.get(f"{BASE_URL}/api/v1/components/{comp2_guid}", headers=headers)
    comp2 = response.json()
    assert not comp2["is_active"], "Second component should still be soft deleted"
    assert comp2["deleted_at"] is not None, "Second component deleted_at should still be set"
    print(f"  ✓ Second component still soft deleted (is_active: {comp2['is_active']}, deleted_at: {comp2['deleted_at']})")
    
    print("✓ Partial soft delete and selective restoration test passed")

def test_sync_reactivation_edge_cases():
    """Test edge cases for sync reactivation."""
    print("Testing sync reactivation edge cases...")
    
    # Authenticate
    token = get_auth_token(BASE_URL, EMAIL, PASSWORD)
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Create and soft delete a component
    print("  → Creating project for sync reactivation test...")
    project_payload = {
        "projects": [{
            "code": "SYNC_REACTIVATE_PROJ",
            "company_guid": COMPANY_GUID,
            "due_date": "2024-12-31T23:59:59Z"
        }]
    }
    response = requests.post(f"{BASE_URL}/api/v1/sync/projects", json=project_payload, headers=headers)
    assert response.status_code == 200
    print(f"  ✓ Project created (status: {response.status_code})")
    
    # Get project GUID
    print("  → Fetching project GUID...")
    response = requests.get(f"{BASE_URL}/api/v1/projects", headers=headers)
    projects = response.json()
    project_guid = next(p["guid"] for p in projects if p["code"] == "SYNC_REACTIVATE_PROJ")
    print(f"  ✓ Project GUID: {project_guid}")
    
    # Create component with specific GUID
    component_guid = str(uuid.uuid4())
    print(f"  → Creating component with GUID: {component_guid}...")
    component_payload = {
        "components": [{
            "guid": component_guid,
            "code": "SYNC_REACTIVATE_COMP",
            "project_guid": project_guid,
            "company_guid": COMPANY_GUID,
            "quantity": 1
        }]
    }
    response = requests.post(f"{BASE_URL}/api/v1/sync/components", json=component_payload, headers=headers)
    assert response.status_code == 200
    print(f"  ✓ Component created (status: {response.status_code})")
    
    # 2. Soft delete the component
    print("  → Soft deleting component...")
    response = requests.delete(f"{BASE_URL}/api/v1/components/{component_guid}", headers=headers)
    assert response.status_code == 200
    print(f"  ✓ Component soft deleted (status: {response.status_code})")
    
    # 3. Reactivate via sync with updated data
    print("  → Reactivating component via sync with updated data...")
    reactivate_payload = {
        "components": [{
            "guid": component_guid,
            "code": "SYNC_REACTIVATE_COMP_UPDATED",
            "project_guid": project_guid,
            "company_guid": COMPANY_GUID,
            "quantity": 5
        }]
    }
    response = requests.post(f"{BASE_URL}/api/v1/sync/components", json=reactivate_payload, headers=headers)
    assert response.status_code == 200
    print(f"  ✓ Component reactivated via sync (status: {response.status_code})")
    
    # 4. Verify component is reactivated with updated data
    print("  → Verifying component reactivation and data update...")
    response = requests.get(f"{BASE_URL}/api/v1/components/{component_guid}", headers=headers)
    component = response.json()
    assert component["is_active"], "Component should be reactivated"
    assert component["deleted_at"] is None, "Component deleted_at should be cleared"
    assert component["code"] == "SYNC_REACTIVATE_COMP_UPDATED", "Component code should be updated"
    assert component["quantity"] == 5, "Component quantity should be updated"
    print(f"  ✓ Component reactivated with updated data:")
    print(f"    - is_active: {component['is_active']}")
    print(f"    - deleted_at: {component['deleted_at']}")
    print(f"    - code: {component['code']}")
    print(f"    - quantity: {component['quantity']}")
    
    print("✓ Sync reactivation edge cases test passed")

def main():
    """Run all edge case tests."""
    print("Starting soft delete business logic edge case tests...")
    print("=" * 60)
    
    try:
        test_multiple_generations_soft_delete()
        print()
        test_partial_soft_delete_and_selective_restore()
        print()
        test_sync_reactivation_edge_cases()
        
        print("=" * 60)
        print("✓ All edge case tests passed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 