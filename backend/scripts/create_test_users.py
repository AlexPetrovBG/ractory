import os
import asyncio
import uuid
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from dotenv import load_dotenv
from passlib.context import CryptContext

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

# Database connection settings
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Password hashing context
PWD_CTX = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Test users configuration
TEST_USERS = [
    {
        "email": "admin1.a@example.com",
        "password": "password",
        "role": "CompanyAdmin",
        "name": "Admin",
        "surname": "CompanyA",
        "company_name": "Test Company A",
        "company_code": "TCA",
        "company_index": 90
    },
    {
        "email": "admin1.b@example.com", 
        "password": "password",
        "role": "CompanyAdmin",
        "name": "Admin",
        "surname": "CompanyB",
        "company_name": "Test Company B",
        "company_code": "TCB",
        "company_index": 91
    }
]

async def create_test_users():
    """Creates test users and companies for pytest tests."""
    engine = create_async_engine(DATABASE_URL, echo=True)
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with AsyncSessionLocal() as session:
        async with session.begin():
            print("Creating test users and companies for pytest...")
            
            for user_config in TEST_USERS:
                # Check if user already exists
                result = await session.execute(
                    text("SELECT guid FROM users WHERE email = :email"), 
                    {"email": user_config["email"]}
                )
                user_guid = result.scalar_one_or_none()
                
                if user_guid is not None:
                    print(f"User {user_config['email']} already exists, skipping...")
                    continue
                
                # Check if company already exists
                result = await session.execute(
                    text("SELECT guid FROM companies WHERE company_index = :company_index"), 
                    {"company_index": user_config["company_index"]}
                )
                company_guid = result.scalar_one_or_none()
                
                if company_guid is None:
                    # Create company for this user
                    company_guid = uuid.uuid4()
                    await session.execute(
                        text("""
                            INSERT INTO companies (guid, name, short_name, company_index, is_active) 
                            VALUES (:guid, :name, :short_name, :company_index, :is_active)
                        """),
                        {
                            "guid": company_guid,
                            "name": user_config["company_name"],
                            "short_name": user_config["company_code"],
                            "company_index": user_config["company_index"],
                            "is_active": True
                        }
                    )
                    print(f"Created company '{user_config['company_name']}' with GUID: {company_guid}")
                else:
                    print(f"Company with index {user_config['company_index']} already exists, using existing company GUID: {company_guid}")
                
                # Hash password and create user
                hashed_password = PWD_CTX.hash(user_config["password"])
                user_guid = uuid.uuid4()
                
                await session.execute(
                    text("""
                        INSERT INTO users (guid, company_guid, email, pwd_hash, role, is_active, name, surname)
                        VALUES (:guid, :company_guid, :email, :pwd_hash, :role, :is_active, :name, :surname)
                    """),
                    {
                        "guid": user_guid,
                        "company_guid": company_guid,
                        "email": user_config["email"],
                        "pwd_hash": hashed_password,
                        "role": user_config["role"],
                        "is_active": True,
                        "name": user_config["name"],
                        "surname": user_config["surname"]
                    }
                )
                print(f"Created user {user_config['email']} with role {user_config['role']}")

if __name__ == "__main__":
    print("Starting test user creation script...")
    asyncio.run(create_test_users())
    print("Test users creation script finished.") 