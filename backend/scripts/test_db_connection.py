#!/usr/bin/env python3
"""
Test script to verify database connection and imports.
"""
import sys
import os
from pathlib import Path

# Add the project postgres to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

def test_db_imports():
    """Test that database imports work correctly."""
    try:
        from app.db import Base, engine, SessionLocal, get_db
        print("✅ Successfully imported database components")
        return True
    except ImportError as e:
        print(f"❌ Error importing database components: {e}")
        return False

def test_db_connection():
    """Test the database connection."""
    from sqlalchemy import text
    from app.db import engine
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            if result.scalar() == 1:
                print("✅ Successfully connected to the database")
                return True
            else:
                print("❌ Database connection test failed: Unexpected result")
                return False
    except Exception as e:
        print(f"❌ Error connecting to the database: {e}")
        return False

def test_session():
    """Test that database sessions work correctly."""
    from app.db import SessionLocal, get_db
    
    try:
        # Test SessionLocal
        db = SessionLocal()
        db.close()
        
        # Test get_db context manager
        with get_db() as db:
            pass
            
        print("✅ Database session tests passed")
        return True
    except Exception as e:
        print(f"❌ Database session test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🔍 Running database tests...\n")
    
    tests = [
        ("Import Tests", test_db_imports),
        ("Connection Test", test_db_connection),
        ("Session Tests", test_session)
    ]
    
    all_passed = True
    for name, test_func in tests:
        print(f"🧪 {name}:")
        if not test_func():
            all_passed = False
        print()
    
    if all_passed:
        print("✅ All database tests passed!")
        return 0
    else:
        print("❌ Some database tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
