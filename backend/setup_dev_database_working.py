#!/usr/bin/env python3
"""
Development Database Setup Script
Reads system admin credentials from environment file

USAGE INSTRUCTIONS:
==================

1. PREREQUISITES:
   - Docker containers must be running (docker-compose up -d)
   - Script must be run from the host machine

2. REQUIRED FILES:
   - This script: setup_dev_database_working.py
   - Admin config: /home/alex/admin_config.env
   - Dev environment: /home/alex/apps/ractory/dev/.env

3. COPY FILES TO CONTAINER:
   cd /home/alex/apps/ractory/dev
   docker cp /home/alex/setup_dev_database_working.py dev_dev-api_1:/app/
   docker cp /home/alex/admin_config.env dev_dev-api_1:/app/
   docker cp .env dev_dev-api_1:/app/

4. RUN THE SCRIPT:
   docker exec dev_dev-api_1 python setup_dev_database_working.py

5. WHAT THE SCRIPT DOES:
   - Reads admin credentials from admin_config.env
   - Reads database credentials from .env
   - Tests database connectivity
   - Clears all data from development database
   - Creates system company (Ra Factory System)
   - Creates system admin user with proper password hashing
   - Verifies the setup is working

6. EXPECTED OUTPUT:
   - All credentials loaded successfully
   - Database connection successful
   - Database cleared successfully
   - System company created
   - System admin user created
   - Final success message

7. TROUBLESHOOTING:
   - If "file not found" error: Make sure all files are copied to container
   - If "database connection failed": Check if containers are running
   - If "Invalid email or password": Restart API container after running script

8. TESTING AUTHENTICATION:
   After successful script execution, test with:
   curl -X POST https://rafactorydev.raworkshop.bg/api/v1/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"a.petrov@delice.bg","password":"SecureAdminPassword123"}'
"""

import os
import asyncio
import uuid
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from passlib.context import CryptContext

# Password hashing context - same as API
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt - same as API."""
    return PWD_CONTEXT.hash(password)

def read_env_file(file_path):
    """Read environment variables from a file"""
    env_file_path = Path(file_path)
    
    if not env_file_path.exists():
        raise FileNotFoundError(f"Environment file not found: {env_file_path}")
    
    credentials = {}
    
    with open(env_file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    credentials[key.strip()] = value.strip()
    
    return credentials

def read_admin_credentials():
    """Read system admin credentials from admin_config.env file"""
    # Try different possible paths for the admin config file
    possible_paths = [
        "/home/alex/admin_config.env",  # Host machine path
        "/app/admin_config.env",        # Container path
        "admin_config.env"              # Current directory
    ]
    
    for path in possible_paths:
        try:
            credentials = read_env_file(path)
            break
        except FileNotFoundError:
            continue
    else:
        raise FileNotFoundError(f"Admin config file not found in any of these locations: {possible_paths}")
    
    # Validate required credentials
    required_keys = ['ADMIN_EMAIL', 'ADMIN_PASSWORD', 'ADMIN_NAME', 'ADMIN_SURNAME', 
                     'SYSTEM_COMPANY_NAME', 'SYSTEM_COMPANY_SHORT_NAME']
    
    missing_keys = [key for key in required_keys if key not in credentials]
    if missing_keys:
        raise ValueError(f"Missing required admin credentials: {missing_keys}")
    
    return credentials

def read_db_credentials():
    """Read database credentials from dev environment file"""
    # Try different possible paths for the dev environment file
    possible_paths = [
        "/home/alex/apps/ractory/dev/.env",  # Host machine path
        "/app/.env",                         # Container path
        ".env"                               # Current directory
    ]
    
    for path in possible_paths:
        try:
            credentials = read_env_file(path)
            break
        except FileNotFoundError:
            continue
    else:
        raise FileNotFoundError(f"Dev environment file not found in any of these locations: {possible_paths}")
    
    # Validate required database credentials
    required_keys = ['DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
    
    missing_keys = [key for key in required_keys if key not in credentials]
    if missing_keys:
        raise ValueError(f"Missing required database credentials: {missing_keys}")
    
    return credentials

async def test_database_connection(db_credentials):
    """Test if the database is accessible with the provided credentials"""
    try:
        # Build database URL
        db_url = f"postgresql+asyncpg://{db_credentials['DB_USER']}:{db_credentials['DB_PASSWORD']}@{db_credentials['DB_HOST']}:{db_credentials['DB_PORT']}/{db_credentials['DB_NAME']}"
        
        print(f"🔗 Testing database connection to: {db_credentials['DB_HOST']}:{db_credentials['DB_PORT']}/{db_credentials['DB_NAME']}")
        
        # Create async engine
        engine = create_async_engine(db_url, echo=False)
        
        # Test connection
        async with engine.begin() as conn:
            # Simple query to test connectivity
            result = await conn.execute(text("SELECT 1 as test"))
            test_value = result.scalar()
            
            if test_value == 1:
                print("✅ Database connection successful!")
                
                # Get database version
                result = await conn.execute(text("SELECT version()"))
                db_version = result.scalar()
                print(f"   Database version: {db_version.split(',')[0]}")
                
                # Get current database name
                result = await conn.execute(text("SELECT current_database()"))
                current_db = result.scalar()
                print(f"   Connected to database: {current_db}")
                
                return True
            else:
                print("❌ Database connection test failed!")
                return False
                
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    finally:
        if 'engine' in locals():
            await engine.dispose()

async def clear_database(db_credentials):
    """Clear all data from the development database"""
    try:
        # Build database URL
        db_url = f"postgresql+asyncpg://{db_credentials['DB_USER']}:{db_credentials['DB_PASSWORD']}@{db_credentials['DB_HOST']}:{db_credentials['DB_PORT']}/{db_credentials['DB_NAME']}"
        
        print(f"🗑️  Clearing all data from database: {db_credentials['DB_NAME']}")
        
        # Create async engine
        engine = create_async_engine(db_url, echo=False)
        
        async with engine.begin() as conn:
            # Get all table names
            result = await conn.execute(text("""
                SELECT tablename 
                FROM pg_tables 
                WHERE schemaname = 'public' 
                AND tablename NOT LIKE 'alembic%'
                ORDER BY tablename
            """))
            tables = [row[0] for row in result.fetchall()]
            
            if not tables:
                print("   No tables found to clear.")
                return True
            
            print(f"   Found {len(tables)} tables to clear: {', '.join(tables)}")
            
            # Disable foreign key checks temporarily
            await conn.execute(text("SET session_replication_role = replica"))
            
            # Clear all tables
            for table in tables:
                await conn.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE"))
                print(f"   ✅ Cleared table: {table}")
            
            # Re-enable foreign key checks
            await conn.execute(text("SET session_replication_role = DEFAULT"))
            
            print("✅ Database cleared successfully!")
            return True
                
    except Exception as e:
        print(f"❌ Failed to clear database: {e}")
        return False
    finally:
        if 'engine' in locals():
            await engine.dispose()

async def create_companies(db_credentials, admin_credentials):
    """Create system company"""
    try:
        # Build database URL
        db_url = f"postgresql+asyncpg://{db_credentials['DB_USER']}:{db_credentials['DB_PASSWORD']}@{db_credentials['DB_HOST']}:{db_credentials['DB_PORT']}/{db_credentials['DB_NAME']}"
        
        print(f"🏢 Creating system company in database: {db_credentials['DB_NAME']}")
        
        # Create async engine
        engine = create_async_engine(db_url, echo=False)
        
        async with engine.begin() as conn:
            # Define system company to create
            companies = [
                {
                    'guid': str(uuid.uuid4()),
                    'name': admin_credentials['SYSTEM_COMPANY_NAME'],
                    'short_name': admin_credentials['SYSTEM_COMPANY_SHORT_NAME'],
                    'company_index': 1,
                    'subscription_tier': 'system',
                    'subscription_status': 'active'
                }
            ]
            
            created_companies = []
            
            for company in companies:
                # Insert company
                await conn.execute(text("""
                    INSERT INTO companies (guid, name, short_name, company_index, subscription_tier, subscription_status, 
                                         user_count, projects_count, workstations_count, created_at, updated_at, is_active, deleted_at)
                    VALUES (:guid, :name, :short_name, :company_index, :subscription_tier, :subscription_status, 
                            0, 0, 0, NOW(), NULL, true, NULL)
                """), {
                    'guid': company['guid'],
                    'name': company['name'],
                    'short_name': company['short_name'],
                    'company_index': company['company_index'],
                    'subscription_tier': company['subscription_tier'],
                    'subscription_status': company['subscription_status']
                })
                
                print(f"   ✅ Created company: {company['name']} ({company['short_name']}) - GUID: {company['guid']}")
                created_companies.append(company)
            
            print(f"✅ Successfully created system company!")
            return created_companies
                
    except Exception as e:
        print(f"❌ Failed to create companies: {e}")
        return None
    finally:
        if 'engine' in locals():
            await engine.dispose()

async def create_system_admin_user(db_credentials, admin_credentials, system_company_guid):
    """Create system admin user with proper password hashing"""
    try:
        # Build database URL
        db_url = f"postgresql+asyncpg://{db_credentials['DB_USER']}:{db_credentials['DB_PASSWORD']}@{db_credentials['DB_HOST']}:{db_credentials['DB_PORT']}/{db_credentials['DB_NAME']}"
        
        print(f"👤 Creating system admin user in database: {db_credentials['DB_NAME']}")
        
        # Hash the password using the same method as the API
        hashed_password = hash_password(admin_credentials['ADMIN_PASSWORD'])
        print(f"   Password hashed successfully (length: {len(hashed_password)})")
        
        # Create async engine
        engine = create_async_engine(db_url, echo=False)
        
        async with engine.begin() as conn:
            # Create system admin user
            user_guid = str(uuid.uuid4())
            
            await conn.execute(text("""
                INSERT INTO users (guid, company_guid, email, pwd_hash, role, pin, is_active, created_at, updated_at)
                VALUES (:guid, :company_guid, :email, :pwd_hash, :role, :pin, :is_active, NOW(), NULL)
            """), {
                'guid': user_guid,
                'company_guid': system_company_guid,
                'email': admin_credentials['ADMIN_EMAIL'],
                'pwd_hash': hashed_password,
                'role': 'SystemAdmin',
                'pin': None,
                'is_active': True
            })
            
            print(f"   ✅ Created system admin user:")
            print(f"      Email: {admin_credentials['ADMIN_EMAIL']}")
            print(f"      Role: SystemAdmin")
            print(f"      Company GUID: {system_company_guid}")
            print(f"      User GUID: {user_guid}")
            
            print(f"✅ Successfully created system admin user!")
            return {
                'user_guid': user_guid,
                'email': admin_credentials['ADMIN_EMAIL'],
                'role': 'SystemAdmin',
                'company_guid': system_company_guid
            }
                
    except Exception as e:
        print(f"❌ Failed to create system admin user: {e}")
        return None
    finally:
        if 'engine' in locals():
            await engine.dispose()

async def main():
    """Main function to read and display credentials"""
    try:
        print("🔍 Reading system admin credentials from environment file...")
        
        admin_credentials = read_admin_credentials()
        
        print("✅ Successfully read admin credentials:")
        print(f"   Email: {admin_credentials['ADMIN_EMAIL']}")
        print(f"   Password: {'*' * len(admin_credentials['ADMIN_PASSWORD'])}")
        print(f"   Name: {admin_credentials['ADMIN_NAME']}")
        print(f"   Surname: {admin_credentials['ADMIN_SURNAME']}")
        print(f"   Company Name: {admin_credentials['SYSTEM_COMPANY_NAME']}")
        print(f"   Company Short Name: {admin_credentials['SYSTEM_COMPANY_SHORT_NAME']}")
        
        print("\n🔍 Reading database credentials from dev environment file...")
        
        db_credentials = read_db_credentials()
        
        print("✅ Successfully read database credentials:")
        print(f"   Host: {db_credentials['DB_HOST']}")
        print(f"   Port: {db_credentials['DB_PORT']}")
        print(f"   Database: {db_credentials['DB_NAME']}")
        print(f"   User: {db_credentials['DB_USER']}")
        print(f"   Password: {'*' * len(db_credentials['DB_PASSWORD'])}")
        
        print("\n🔍 Testing database connectivity...")
        
        db_accessible = await test_database_connection(db_credentials)
        
        if not db_accessible:
            print("\n⚠️  Credentials loaded but database is not accessible!")
            return None
        
        print("\n🗑️  Clearing all data from development database...")
        
        db_cleared = await clear_database(db_credentials)
        
        if not db_cleared:
            print("\n⚠️  Database accessible but failed to clear data!")
            return None
        
        print("\n🏢 Creating system company...")
        
        companies = await create_companies(db_credentials, admin_credentials)
        
        if not companies:
            print("\n⚠️  Database cleared but failed to create system company!")
            return None
        
        # Get the system company GUID (first and only company created)
        system_company_guid = companies[0]['guid']
        
        print("\n👤 Creating system admin user...")
        
        system_admin = await create_system_admin_user(db_credentials, admin_credentials, system_company_guid)
        
        if system_admin:
            print(f"\n🎉 All credentials loaded, database cleared, system company and admin user created!")
        else:
            print("\n⚠️  System company created but failed to create admin user!")
        
        return {
            'admin': admin_credentials,
            'database': db_credentials,
            'db_accessible': db_accessible,
            'db_cleared': db_cleared,
            'companies': companies,
            'system_admin': system_admin
        }
        
    except Exception as e:
        print(f"❌ Error reading credentials: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(main())