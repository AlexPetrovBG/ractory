from enum import Enum

class UserRole(str, Enum):
    """User roles in the system."""
    SYSTEM_ADMIN = "SystemAdmin"
    COMPANY_ADMIN = "CompanyAdmin" 
    PROJECT_MANAGER = "ProjectManager"
    OPERATOR = "Operator"
    INTEGRATION = "Integration"

    def __str__(self) -> str:
        return self.value

class WorkstationType(str, Enum):
    """Types of workstations for shop floor operations."""
    MACHINE = "Machine"
    ASSEMBLY = "Assembly"
    CONTROL = "Control"
    LOGISTICS = "Logistics"
    SUPPLY = "Supply"

    def __str__(self) -> str:
        return self.value

class WorkflowActionType(str, Enum):
    """Types of workflow actions that can be performed in the system."""
    CREATE = "Create"
    UPDATE = "Update"
    DELETE = "Delete"
    SOFT_DELETE = "SoftDelete"
    RESTORE = "Restore"
    SYNC = "Sync"
    IMPORT = "Import"
    EXPORT = "Export"
    APPROVE = "Approve"
    REJECT = "Reject"

    def __str__(self) -> str:
        return self.value 