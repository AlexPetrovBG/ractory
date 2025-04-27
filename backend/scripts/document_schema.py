import os
import sys
import psycopg
import argparse
import json
from datetime import datetime

# Add the parent directory to the path so we can import from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def document_database_schema(env="dev"):
    """Connect to the database and document its schema."""
    
    # Set connection parameters based on environment
    if env == "prod":
        DB_HOST = os.getenv("PROD_DB_HOST", "172.19.0.2")
        DB_PORT = os.getenv("PROD_DB_PORT", "5432")
        DB_NAME = os.getenv("PROD_DB_NAME", "rafactory")
        DB_USER = os.getenv("PROD_DB_USER", "rafactory_rw")
        DB_PASS = os.getenv("PROD_DB_PASS", "StrongP@ss3.14")
    else:
        # Default to dev environment
        DB_HOST = os.getenv("DB_HOST", "localhost") 
        DB_PORT = os.getenv("DB_PORT", "5434")
        DB_NAME = os.getenv("DB_NAME", "rafactory_dev")
        DB_USER = os.getenv("DB_USER", "rafactory_rw")
        DB_PASS = os.getenv("DB_PASS", "StrongP@ss3.14")
    
    try:
        print(f"Connecting to {env.upper()} database '{DB_NAME}'...")
        
        # Create a new connection
        conn_string = f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} user={DB_USER} password={DB_PASS}"
        
        # Use psycopg directly
        with psycopg.connect(conn_string) as conn:
            print(f"✅ Connected to database successfully!")
            
            schema = {
                "database": DB_NAME,
                "environment": env,
                "documented_at": datetime.now().isoformat(),
                "tables": {}
            }
            
            with conn.cursor() as cur:
                # Get list of tables
                cur.execute("""
                    SELECT 
                        table_name 
                    FROM 
                        information_schema.tables 
                    WHERE 
                        table_schema = 'public'
                    ORDER BY 
                        table_name
                """)
                tables = [row[0] for row in cur.fetchall()]
                
                print(f"Found {len(tables)} tables")
                
                # For each table, get column information
                for table in tables:
                    print(f"Documenting table: {table}")
                    
                    # Get column information
                    cur.execute("""
                        SELECT 
                            column_name, 
                            data_type, 
                            is_nullable, 
                            column_default,
                            character_maximum_length
                        FROM 
                            information_schema.columns 
                        WHERE 
                            table_schema = 'public' AND 
                            table_name = %s
                        ORDER BY 
                            ordinal_position
                    """, (table,))
                    
                    columns = []
                    for col in cur.fetchall():
                        column_info = {
                            "name": col[0],
                            "type": col[1],
                            "nullable": col[2] == "YES",
                            "default": col[3],
                        }
                        if col[4] is not None:
                            column_info["max_length"] = col[4]
                        columns.append(column_info)
                    
                    # Get primary key information
                    cur.execute("""
                        SELECT 
                            kcu.column_name
                        FROM 
                            information_schema.table_constraints tc
                        JOIN 
                            information_schema.key_column_usage kcu
                        ON 
                            tc.constraint_name = kcu.constraint_name AND
                            tc.table_schema = kcu.table_schema
                        WHERE 
                            tc.constraint_type = 'PRIMARY KEY' AND
                            tc.table_schema = 'public' AND
                            tc.table_name = %s
                        ORDER BY 
                            kcu.ordinal_position
                    """, (table,))
                    
                    primary_keys = [row[0] for row in cur.fetchall()]
                    
                    # Count records
                    cur.execute(f"SELECT COUNT(*) FROM \"{table}\"")
                    record_count = cur.fetchone()[0]
                    
                    # Store table information
                    schema["tables"][table] = {
                        "columns": columns,
                        "primary_keys": primary_keys,
                        "record_count": record_count
                    }
                    
                    # Get foreign key information
                    cur.execute("""
                        SELECT
                            kcu.column_name,
                            ccu.table_name AS foreign_table_name,
                            ccu.column_name AS foreign_column_name
                        FROM
                            information_schema.table_constraints AS tc
                        JOIN
                            information_schema.key_column_usage AS kcu
                        ON
                            tc.constraint_name = kcu.constraint_name AND
                            tc.table_schema = kcu.table_schema
                        JOIN
                            information_schema.constraint_column_usage AS ccu
                        ON
                            ccu.constraint_name = tc.constraint_name AND
                            ccu.table_schema = tc.table_schema
                        WHERE
                            tc.constraint_type = 'FOREIGN KEY' AND
                            tc.table_schema = 'public' AND
                            tc.table_name = %s
                    """, (table,))
                    
                    foreign_keys = []
                    for fk in cur.fetchall():
                        foreign_keys.append({
                            "column": fk[0],
                            "references_table": fk[1],
                            "references_column": fk[2]
                        })
                    
                    if foreign_keys:
                        schema["tables"][table]["foreign_keys"] = foreign_keys
            
            # Write schema to file
            output_file = f"db_schema_{env}_{datetime.now().strftime('%Y%m%d')}.json"
            with open(output_file, 'w') as f:
                json.dump(schema, f, indent=2)
            
            print(f"\nSchema documentation completed and saved to {output_file}")
            return schema
                
    except Exception as e:
        print(f"❌ Error documenting schema: {str(e)}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Document database schema")
    parser.add_argument("--env", choices=["dev", "prod"], default="dev", help="Environment to document (dev or prod)")
    args = parser.parse_args()
    
    document_database_schema(args.env) 