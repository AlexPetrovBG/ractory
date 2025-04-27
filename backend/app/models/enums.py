from enum import Enum, auto

class UserRole(str, Enum):
    """
    User roles for access control.
    
    Higher roles have more permissions.
    """
    SYSTEM_ADMIN = "SystemAdmin"  # Cross-tenant access, highest privileges
    COMPANY_ADMIN = "CompanyAdmin"  # Full CRUD within company
    PROJECT_MANAGER = "ProjectManager"  # Read projects, logistics
    OPERATOR = "Operator"  # Limited workstation actions
    INTEGRATION = "Integration"  # Machine-to-machine API access

class WorkstationType(str, Enum):
    """
    Types of workstations for shop floor operations.
    """
    CUTTER = "Cutter"
    WELDER = "Welder"
    ASSEMBLY = "Assembly"
    GLAZING = "Glazing"
    SHIPPING = "Shipping"
    QUALITY = "Quality"
    OTHER = "Other" 