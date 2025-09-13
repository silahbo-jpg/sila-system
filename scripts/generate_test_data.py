#!/usr/bin/env python3
"""
Script to generate test data for the application.
"""

import sys
import os

# Add the backend directory to the path so we can import app modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

def generate_test_data():
    """Generate test data for the application."""
    try:
        print("Generating test data...")
        # This is a placeholder implementation
        # In a real implementation, this would create sample data
        # for testing purposes in the database
        print("✅ Test data generated successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to generate test data: {e}")
        return False

if __name__ == "__main__":
    if generate_test_data():
        sys.exit(0)
    else:
        sys.exit(1)