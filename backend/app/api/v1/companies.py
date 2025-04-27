from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.company import CompanyCreate, CompanyRead
from app.services.company_service import CompanyService
from app.core.deps import get_session
from app.core.rbac import require_roles # Assuming require_roles checks for one or more roles
from app.models.enums import UserRole

router = APIRouter(
    prefix="/companies",
    tags=["companies"],
    dependencies=[Depends(require_roles(UserRole.SYSTEM_ADMIN))] # Temporarily commented out for testing
)

@router.post("/", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
async def create_company(
    company_in: CompanyCreate,
    db: AsyncSession = Depends(get_session),
    # current_user: CurrentUser = Depends(get_current_user) # Inject if needed for logging/audit
):
    """
    Create a new company. Only accessible by System Administrators.
    """
    # Check if company already exists by name
    existing_company = await CompanyService.get_company_by_name(db, name=company_in.name)
    if existing_company:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Company with name '{company_in.name}' already exists."
        )
    
    # Create company
    try:
        new_company = await CompanyService.create_company(db=db, company=company_in)
        return new_company
    except Exception as e:
        # Log the error properly in a real application
        print(f"Error creating company: {e}") 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create company."
        )

# Add other company endpoints here (GET, PUT, DELETE) as needed
# Remember to apply appropriate role checks (e.g., CompanyAdmin for GET/PUT within their own company) 