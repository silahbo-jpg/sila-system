import psycopg2
from urllib.parse import urlparse
import sys

def test_connection():
    # Using the credentials you provided
    db_url = "postgresql://postgres:Truman1_Marcelo1_1985@localhost:5432/postgres"
    
    print(f"[TEST] Testing connection to: {db_url}")
    
    try:
        # Parse the URL
        result = urlparse(db_url)
        
        # Extract connection parameters
        dbname = result.path[1:] or 'postgres'  # Default to 'postgres' if not specified
        user = result.username or 'postgres'
        password = result.password or ''
        host = result.hostname or 'localhost'
        port = result.port or 5432  # Default PostgreSQL port
        
        print(f"\n[PARAMS] Connection parameters:")
        print(f"  • Database: {dbname}")
        print(f"  • User: {user}")
        print(f"  • Host: {host}")
        print(f"  • Port: {port}")
        
        # Try to connect
        print("\n[CONNECT] Connecting to database...")
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        
        # If we get here, connection was successful
        print("[SUCCESS] Connected to the database!")
        
        # Get PostgreSQL version and database info
        with conn.cursor() as cur:
            # Get version
            cur.execute("SELECT version();")
            version = cur.fetchone()
            print(f"\n[VERSION] PostgreSQL version: {version[0]}")
            
            # Get current database and user
            cur.execute("SELECT current_database(), current_user, inet_server_addr(), inet_server_port();")
            db_info = cur.fetchone()
            print(f"\n[INFO] Database Info:")
            print(f"  • Current database: {db_info[0]}")
            print(f"  • Current user: {db_info[1]}")
            print(f"  • Server address: {db_info[2]}")
            print(f"  • Server port: {db_info[3]}")
        
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"\nERROR: Failed to connect to the database.")
        print(f"Error details: {e}")
        print("\nTroubleshooting steps:")
        print("1. Make sure PostgreSQL is running")
        print("2. Verify the database 'sila_test' exists")
        print("3. Check if the user 'postgres' has the correct password")
        print("4. Verify the pg_hba.conf file allows password authentication")
        return False
    except Exception as e:
        print(f"\nUNEXPECTED ERROR: {e}")
        return False

def check_postgres_service():
    """Check if PostgreSQL service is running."""
    try:
        import subprocess
        result = subprocess.run(
            ["net", "start"], 
            capture_output=True, 
            text=True,
            check=True
        )
        if "postgresql" in result.stdout.lower():
            print("PostgreSQL service is running.")
            return True
        else:
            print("PostgreSQL service is NOT running.")
            return False
    except Exception as e:
        print(f"Error checking PostgreSQL service: {e}")
        return False

if __name__ == "__main__":
    print("=== PostgreSQL Connection Test ===\n")
    check_postgres_service()
    print()
    test_connection()
    
    print("\n=== Connection Test Complete ===")
