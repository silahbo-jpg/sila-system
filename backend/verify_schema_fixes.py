#!/usr/bin/env python3
"""
Simple verification script to test that schema conflicts have been resolved.
This script tests imports without requiring the full test environment.
"""

import sys
import os
from pathlib import Path

# Add the backend directory to the path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

def test_module_import(module_name):
    """Test importing a module and return success status."""
    try:
        # Try to import the module
        module = __import__(f"app.modules.{module_name}", fromlist=[''])
        print(f"✅ {module_name.capitalize()} module imported successfully")
        
        # Try to import the schemas
        schemas = __import__(f"app.modules.{module_name}.schemas", fromlist=[''])
        print(f"✅ {module_name.capitalize()} schemas imported successfully")
        
        # Try to import the endpoints
        endpoints = __import__(f"app.modules.{module_name}.endpoints", fromlist=[''])
        print(f"✅ {module_name.capitalize()} endpoints imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ Error importing {module_name}: {e}")
        return False

def main():
    print("🔍 Verifying schema conflict fixes...")
    print("=" * 50)
    
    # List of modules we fixed
    modules_to_test = [
        "citizenship",
        "commercial", 
        "education",
        "health",
        "complaints",
        "social",
        "urbanism",
        "service_hub",
        "internal",
        "justice",
        "sanitation",
        "statistics",
        "common",
        "auth"
    ]
    
    success_count = 0
    total_count = len(modules_to_test)
    
    for module in modules_to_test:
        if test_module_import(module):
            success_count += 1
        print()
    
    print("=" * 50)
    print(f"📊 Results: {success_count}/{total_count} modules imported successfully")
    
    if success_count == total_count:
        print("🎉 All modules are working correctly!")
        print("✅ Schema conflicts have been successfully resolved")
        return 0
    else:
        print("⚠️  Some modules still have issues")
        return 1

if __name__ == "__main__":
    sys.exit(main())