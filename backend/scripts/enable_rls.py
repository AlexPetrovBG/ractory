"""
Script to enable Row-Level Security (RLS) on all tables
and create tenant isolation policies.
"""
import asyncio
import os
import sys

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.models.base import engine

async def enable_rls():
    """
    Enable RLS on all tables in the public schema and create tenant policies.
    """
    async with engine.begin() as conn:
        # Get all tables in the public schema
        result = await conn.execute(text(
            "SELECT tablename FROM pg_tables WHERE schemaname = 'public'"
        ))
        tables = [row[0] for row in result]

        print(f"Found {len(tables)} tables")
        
        # Enable RLS on all tables
        for table in tables:
            print(f"Enabling RLS on {table}")
            await conn.execute(text(f'ALTER TABLE {table} ENABLE ROW LEVEL SECURITY;'))
            
            # Create tenant isolation policy for tables with company_guid
            has_company_guid = await conn.execute(text(
                f"SELECT COUNT(*) FROM information_schema.columns "
                f"WHERE table_name = '{table}' AND column_name = 'company_guid'"
            ))
            
            if has_company_guid.scalar() > 0:
                print(f"Creating tenant isolation policy on {table}")
                await conn.execute(text(
                    f"DROP POLICY IF EXISTS tenant_isolation ON {table};"
                ))
                await conn.execute(text(
                    f"CREATE POLICY tenant_isolation ON {table} "
                    f"USING (company_guid = current_setting('app.tenant')::uuid);"
                ))
                print(f"  Policy created on {table}")
            else:
                print(f"  Table {table} does not have company_guid column, skipping policy")
                
        print("RLS enabled on all tables")

if __name__ == "__main__":
    asyncio.run(enable_rls()) 