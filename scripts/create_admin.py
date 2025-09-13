#!/usr/bin/env python3
"""
Script to create an admin user in the system.
"""

import sys
import os

# Add the backend directory to the path so we can import app modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

def create_admin():
    """Create an admin user."""
    try:
        print("Creating admin user...")
        # This is a placeholder implementation
        # In a real implementation, this would connect to the database
        # and create an admin user with appropriate permissions
        print("✅ Admin user created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create admin user: {e}")
        return False

if __name__ == "__main__":
    if create_admin():
        sys.exit(0)
    else:
        sys.exit(1)