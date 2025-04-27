import os
import sys
import psycopg
import argparse

# Add the parent directory to the path so we can import from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def try_connection(host, port, dbname, user, password):
    """Try to connect to a specific database."""
    try:
        conn_string = f"host={host} port={port} dbname={dbname} user={user} password={password}"
        with psycopg.connect(conn_string) as conn:
            print(f"✅ Connected to database '{dbname}' successfully!")
            
            # Get database version
            with conn.cursor() as cur:
                cur.execute("SELECT version()")
                version = cur.fetchone()[0]
                print(f"Database version: {version}")
                
                # List all tables
                cur.execute(
                    "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name"
                )
                tables = [row[0] for row in cur.fetchall()]
                
                print(f"\nFound {len(tables)} tables:")
                if tables:
                    for table in tables:
                        # Count records in each table
                        cur.execute(f"SELECT COUNT(*) FROM \"{table}\"")
                        record_count = cur.fetchone()[0]
                        
                        # Get column count
                        cur.execute(f"SELECT COUNT(*) FROM information_schema.columns WHERE table_name = %s", (table,))
                        column_count = cur.fetchone()[0]
                        
                        print(f"  - {table} (columns: {column_count}, records: {record_count})")
            return True
    except Exception as e:
        print(f"❌ Connection to '{dbname}' failed: {str(e)}")
        return False

def test_db_connection(env="dev"):
    """Test the database connection with a simple SELECT query using psycopg."""
    
    # Set connection parameters based on environment
    if env == "prod":
        # Based on production docker-compose.yml
        DB_HOST = os.getenv("PROD_DB_HOST", "172.19.0.2")  # The IP address used in prod
        DB_PORT = os.getenv("PROD_DB_PORT", "5432")
        DB_USER = os.getenv("PROD_DB_USER", "rafactory_rw")
        DB_PASS = os.getenv("PROD_DB_PASS", "StrongP@ss3.14")
        
        print(f"Testing PROD database connection...")
        print(f"Connection parameters:")
        print(f"  Host: {DB_HOST}")
        print(f"  Port: {DB_PORT}")
        print(f"  User: {DB_USER}")
        
        # Try both possible database names
        print("\nTrying 'rafactory_prod' database first...")
        if try_connection(DB_HOST, DB_PORT, "rafactory_prod", DB_USER, DB_PASS):
            return True
            
        print("\nTrying 'rafactory' database...")
        if try_connection(DB_HOST, DB_PORT, "rafactory", DB_USER, DB_PASS):
            return True
            
        # If both fail, try listing available databases
        try:
            print("\nAttempting to list available databases...")
            # Connect to 'postgres' database which is the default
            conn_string = f"host={DB_HOST} port={DB_PORT} dbname=postgres user={DB_USER} password={DB_PASS}"
            with psycopg.connect(conn_string) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
                    databases = [row[0] for row in cur.fetchall()]
                    print(f"Available databases: {', '.join(databases)}")
        except Exception as e:
            print(f"Could not list databases: {str(e)}")
        
        return False
    else:
        # Default to dev environment
        DB_HOST = os.getenv("DB_HOST", "localhost") 
        DB_PORT = os.getenv("DB_PORT", "5434")
        DB_NAME = os.getenv("DB_NAME", "rafactory_dev")
        DB_USER = os.getenv("DB_USER", "rafactory_rw")
        DB_PASS = os.getenv("DB_PASS", "StrongP@ss3.14")
        
        print(f"Testing DEV database connection...")
        print(f"Connection parameters:")
        print(f"  Host: {DB_HOST}")
        print(f"  Port: {DB_PORT}")
        print(f"  Database: {DB_NAME}")
        print(f"  User: {DB_USER}")
        
        return try_connection(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test database connection")
    parser.add_argument("--env", choices=["dev", "prod"], default="dev", help="Environment to test (dev or prod)")
    args = parser.parse_args()
    
    test_db_connection(args.env) 