# Pydantic schemas - Complete exports for all modules

# Authentication schemas (updated names)
from app.schemas.auth import (
    TokenResponse, RefreshRequest, LoginRequest, QrLoginRequest, ErrorResponse
)

# User schemas
from app.schemas.user import (
    UserCreate, UserUpdate, UserResponse, UserInDB
)

# Workstation schemas  
from app.schemas.workstation import (
    WorkstationCreate, WorkstationUpdate, WorkstationResponse, WorkstationInDB, WorkstationType
)

# Company schemas (from both files for compatibility)
from app.schemas.companies import (
    CompanyBase, CompanyCreate, CompanyUpdate, CompanyRead, CompanyInDB
)

# API Key schemas
from app.schemas.api_key import (
    ApiKeyCreate, ApiKeyCreated, ApiKeyResponse, ApiKeyUpdate
)

# Workflow schemas
from app.schemas.workflow import (
    WorkflowCreate, WorkflowResponse, WorkflowFilter, WorkflowStatistics
)

# Sync/RaConnect schemas
from app.schemas.raconnect import (
    ProjectCreate, ComponentCreate, AssemblyCreate, ArticleCreate, PieceCreate, SyncResponse
)

# Backward compatibility exports (deprecated - use new names)
# These maintain compatibility while we transition
Token = TokenResponse  # Deprecated: use TokenResponse
TokenData = TokenResponse  # Deprecated: use TokenResponse 