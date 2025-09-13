#!/usr/bin/env python3
"""
Create Superuser Script
Creates an administrative user for the SILA-System.
"""

import os
import sys
import getpass
from pathlib import Path

# Add backend to path for imports
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.append(str(backend_path))

def main():
    """Create a superuser."""
    print("🔐 SILA-System Superuser Creation")
    print("=" * 40)
    
    try:
        # Import after adding path
        from app.core.config import settings
        from app.db.session import get_db
        from app.crud.user import create_user
        from app.schemas.user import UserCreate
        from app.core.security import get_password_hash
        
        # Get user input
        email = input("Email: ").strip()
        if not email:
            print("❌ Email is required")
            return False
            
        password = getpass.getpass("Password: ")
        if not password:
            print("❌ Password is required")
            return False
            
        confirm_password = getpass.getpass("Confirm Password: ")
        if password != confirm_password:
            print("❌ Passwords do not match")
            return False
        
        full_name = input("Full Name (optional): ").strip() or None
        
        # Create user
        db = next(get_db())
        user_data = UserCreate(
            email=email,
            password=password,
            full_name=full_name,
            is_superuser=True,
            is_active=True
        )
        
        user = create_user(db=db, obj_in=user_data)
        
        print(f"✅ Superuser created successfully!")
        print(f"📧 Email: {user.email}")
        print(f"👤 Name: {user.full_name or 'Not provided'}")
        print(f"🔑 ID: {user.id}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure the backend dependencies are installed")
        return False
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)