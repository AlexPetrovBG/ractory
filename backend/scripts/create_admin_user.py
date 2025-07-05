import os
import asyncio
import uuid
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from dotenv import load_dotenv
from passlib.context import CryptContext

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'apps', 'ractory', 'prod', '.env')
load_dotenv(dotenv_path=dotenv_path)

# Database connection settings
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Admin user settings
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
ADMIN_NAME = os.getenv("ADMIN_NAME")
ADMIN_SURNAME = os.getenv("ADMIN_SURNAME")

# Password hashing context
PWD_CTX = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_admin_user():
    """Connects to the database and creates the admin user if it doesn't exist."""
    engine = create_async_engine(DATABASE_URL, echo=True)
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with AsyncSessionLocal() as session:
        async with session.begin():
            # Hash the admin password first
            hashed_password = PWD_CTX.hash(ADMIN_PASSWORD)
            print(f"Hashed password for admin user.")

            # Check if the admin user already exists
            result = await session.execute(text("SELECT guid FROM users WHERE email = :email"), {"email": ADMIN_EMAIL})
            user_guid = result.scalar_one_or_none()

            if user_guid is not None:
                print(f"Admin user with email {ADMIN_EMAIL} already exists. Updating password.")
                await session.execute(
                    text("UPDATE users SET pwd_hash = :pwd_hash WHERE guid = :guid"),
                    {"pwd_hash": hashed_password, "guid": user_guid}
                )
                print(f"Successfully updated password for admin user {ADMIN_EMAIL}")
            else:
                print("Admin user not found. Creating a new one.")
                # Create a default company for the admin user
                company_guid = uuid.uuid4()
                await session.execute(
                    text("INSERT INTO companies (guid, name, is_active) VALUES (:guid, :name, :is_active)"),
                    {"guid": company_guid, "name": "Default Company", "is_active": True}
                )
                print(f"Created default company with GUID: {company_guid}")

                # Create the admin user
                user_guid = uuid.uuid4()
                await session.execute(
                    text("""
                        INSERT INTO users (guid, company_guid, email, pwd_hash, role, is_active, name, surname)
                        VALUES (:guid, :company_guid, :email, :pwd_hash, :role, :is_active, :name, :surname)
                    """),
                    {
                        "guid": user_guid,
                        "company_guid": company_guid,
                        "email": ADMIN_EMAIL,
                        "pwd_hash": hashed_password,
                        "role": 'SystemAdmin',
                        "is_active": True,
                        "name": ADMIN_NAME,
                        "surname": ADMIN_SURNAME,
                    }
                )
                print(f"Successfully created admin user with email {ADMIN_EMAIL}")

if __name__ == "__main__":
    print("Starting admin user creation script...")
    asyncio.run(create_admin_user())
    print("Script finished.") 