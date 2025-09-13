#!/usr/bin/env python3
"""
Database Setup Script
Sets up PostgreSQL database and runs Alembic migrations.
"""

import os
import sys
import subprocess
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.append(str(backend_path))

def run_command(cmd: str, cwd: Path = None) -> bool:
    """Run a command and return success status."""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {cmd}")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {cmd}: {e.stderr}")
        return False

def check_postgresql():
    """Check if PostgreSQL is running."""
    print("🔍 Checking PostgreSQL...")
    
    try:
        result = subprocess.run("pg_isready", capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ PostgreSQL is running")
            return True
        else:
            print("❌ PostgreSQL is not running")
            return False
    except FileNotFoundError:
        print("❌ PostgreSQL is not installed or not in PATH")
        return False

def create_database():
    """Create the database if it doesn't exist."""
    print("🗄️ Creating database...")
    
    try:
        from app.core.config import settings
        
        # Extract database name from URL
        db_name = settings.DATABASE_URL.split("/")[-1].split("?")[0]
        
        # Try to connect to postgres database to create our database
        create_cmd = f'createdb "{db_name}"'
        
        result = subprocess.run(create_cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Database '{db_name}' created")
            return True
        elif "already exists" in result.stderr:
            print(f"ℹ️ Database '{db_name}' already exists")
            return True
        else:
            print(f"❌ Failed to create database: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

def run_alembic_migrations():
    """Run Alembic database migrations."""
    print("🔄 Running database migrations...")
    
    backend_dir = Path(__file__).parent.parent.parent / "backend"
    
    commands = [
        "alembic upgrade head"
    ]
    
    for cmd in commands:
        if not run_command(cmd, backend_dir):
            return False
    
    return True

def test_connection():
    """Test database connection."""
    print("🔗 Testing database connection...")
    
    try:
        from app.db.session import engine
        
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            if result.fetchone():
                print("✅ Database connection successful")
                return True
                
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def main():
    """Main database setup function."""
    print("🗄️ SILA-System Database Setup")
    print("=" * 40)
    
    steps = [
        ("PostgreSQL Status", check_postgresql),
        ("Database Creation", create_database),
        ("Migrations", run_alembic_migrations),
        ("Connection Test", test_connection)
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        if not step_func():
            print(f"❌ Failed: {step_name}")
            return False
    
    print("\n🎉 Database setup complete!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)