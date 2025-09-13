import psycopg2
import subprocess
import os

def get_pgpass_path():
    """Get the path to the .pgpass file."""
    return os.path.join(os.path.expanduser('~'), '.pgpass')

def check_pgpass():
    """Check if .pgpass file exists and has correct permissions."""
    pgpass_path = get_pgpass_path()
    if not os.path.exists(pgpass_path):
        print(f"\nWARNING: .pgpass file not found at {pgpass_path}")
        print("You can create it with the following format:")
        print("  hostname:port:database:username:password")
        return False
    
    # Check file permissions (should be 600)
    mode = os.stat(pgpass_path).st_mode & 0o777
    if mode != 0o600:
        print(f"\nWARNING: .pgpass file has incorrect permissions {oct(mode)} (should be 600)")
        print(f"Run: icacls \"{pgpass_path}\" /inheritance:r")
        print(f"      icacls \"{pgpass_path}\" /grant:r \"%USERNAME%:R\"")
        return False
    
    print(f"\n.pgpass file found at {pgpass_path} with correct permissions")
    return True

def list_databases():
    """List all databases in the PostgreSQL server."""
    try:
        # Connect to the default 'postgres' database
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="localhost",
            port=5432
        )
        conn.autocommit = True
        
        with conn.cursor() as cur:
            # List all databases
            cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
            dbs = [row[0] for row in cur.fetchall()]
            
            print("\nAvailable databases:")
            for db in dbs:
                print(f"- {db}")
            
            # Check if sila_test exists
            if 'sila_test' in dbs:
                print("\n✅ sila_test database exists")
            else:
                print("\n❌ sila_test database does not exist")
                print("To create it, run:")
                print("  createdb -U postgres sila_test")
        
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"\nERROR: Could not connect to PostgreSQL server: {e}")
        print("\nTroubleshooting steps:")
        print("1. Make sure PostgreSQL is running")
        print("2. Verify the password for user 'postgres'")
        print("3. Check pg_hba.conf for authentication settings")
        return False

def check_pg_hba():
    """Check pg_hba.conf for authentication settings."""
    try:
        # Try to find pg_hba.conf location
        result = subprocess.run(
            ["psql", "-U", "postgres", "-t", "-c", "SHOW hba_file;"],
            capture_output=True,
            text=True,
            input="postgres\n"  # Password prompt
        )
        
        if result.returncode == 0:
            hba_file = result.stdout.strip()
            print(f"\npg_hba.conf location: {hba_file}")
            
            # Try to read the file (might need admin privileges)
            try:
                with open(hba_file, 'r') as f:
                    content = f.read()
                    
                print("\nCurrent authentication methods:")
                for line in content.split('\n'):
                    if line.strip() and not line.startswith('#'):
                        print(f"  {line}")
                        
            except PermissionError:
                print("\nInsufficient permissions to read pg_hba.conf")
                print("You may need to run this script as administrator")
                
        else:
            print("\nCould not determine pg_hba.conf location")
            print(f"psql error: {result.stderr}")
            
    except FileNotFoundError:
        print("\npsql command not found. Make sure PostgreSQL bin directory is in your PATH")

def main():
    print("=== PostgreSQL Configuration Check ===\n")
    
    # Check if psycopg2 is installed
    try:
        import psycopg2
    except ImportError:
        print("ERROR: psycopg2 package not installed.")
        print("Install it with: pip install psycopg2-binary")
        return
    
    # Check .pgpass file
    check_pgpass()
    
    # List databases
    list_databases()
    
    # Check pg_hba.conf
    check_pg_hba()
    
    print("\n=== Check Complete ===")

if __name__ == "__main__":
    main()
