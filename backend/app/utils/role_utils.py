from typing import Dict
from app.models.enums import UserRole

# Role hierarchy mapping (higher number = higher privileges)
ROLE_HIERARCHY: Dict[str, int] = {
    UserRole.OPERATOR.value: 1,
    UserRole.PROJECT_MANAGER.value: 2,
    UserRole.COMPANY_ADMIN.value: 3,
    UserRole.SYSTEM_ADMIN.value: 4,
    # Integration role is special and handled separately
    UserRole.INTEGRATION.value: 0
}

def can_manage_role(current_role: str, target_role: str) -> bool:
    """
    Check if a user with current_role can manage (create/update) a user with target_role.
    
    Rules:
    1. SystemAdmin can manage any role
    2. CompanyAdmin can only manage roles with lower hierarchy (ProjectManager, Operator)
    3. Other roles cannot manage any roles
    4. Integration role is special and can only be managed by SystemAdmin
    """
    # Special case: Integration role can only be managed by SystemAdmin
    if target_role == UserRole.INTEGRATION.value:
        return current_role == UserRole.SYSTEM_ADMIN.value
        
    # Get hierarchy levels
    current_level = ROLE_HIERARCHY.get(current_role, 0)
    target_level = ROLE_HIERARCHY.get(target_role, 0)
    
    # SystemAdmin can manage any role
    if current_role == UserRole.SYSTEM_ADMIN.value:
        return True
        
    # Other roles can only manage roles with lower hierarchy
    return current_level > target_level 