import os
from pydantic import BaseModel


class Settings(BaseModel):
    """Application settings."""
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://rafactory_rw:StrongP@ss!@dev-db:5432/rafactory")
    
    # Security
    JWT_SECRET: str = os.getenv("JWT_SECRET", "change_me_in_production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    
    # Application
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Ra Factory"
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:5173",  # Dev admin
        "http://localhost:5174",  # Dev operator
        "https://admin.raworkshop.bg",
        "https://operator.raworkshop.bg",
    ]


settings = Settings() 