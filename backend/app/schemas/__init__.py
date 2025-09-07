# Pydantic schemas
from app.schemas.companies import CompanyBase, CompanyCreate, CompanyUpdate, CompanyRead, CompanyInDB
from app.schemas.auth import TokenResponse, TokenData

# Backward compatibility alias
Token = TokenResponse 