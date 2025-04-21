from enum import Enum

class Role(str, Enum):
    """User roles in the system."""
    SYSTEM_ADMIN = "SystemAdmin"
    COMPANY_ADMIN = "CompanyAdmin" 
    PROJECT_MANAGER = "ProjectManager"
    OPERATOR = "Operator"
    INTEGRATION = "Integration"

    def __str__(self) -> str:
        return self.value 