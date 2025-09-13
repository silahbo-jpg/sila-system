#!/usr/bin/env python3
import sys
import os

# Add the backend directory to the path so we can check for files
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')

def test_route_files_exist():
    """Test that critical route files exist."""
    try:
        # Check if main app file exists
        main_app_path = os.path.join(backend_path, 'app', 'main.py')
        if os.path.exists(main_app_path):
            print("✅ Main app file exists")
        else:
            print("❌ Main app file missing")
            return False
        
        # Check if auth files exist
        auth_init_path = os.path.join(backend_path, 'app', 'auth', '__init__.py')
        if os.path.exists(auth_init_path):
            print("✅ Auth module exists")
        else:
            print("❌ Auth module missing")
            return False
        
        # Check if module route directories exist
        citizenship_routes_path = os.path.join(backend_path, 'app', 'modules', 'citizenship', 'routes')
        if os.path.exists(citizenship_routes_path):
            print("✅ Citizenship routes directory exists")
        else:
            print("❌ Citizenship routes directory missing")
            return False
        
        health_routes_path = os.path.join(backend_path, 'app', 'modules', 'health', 'routes')
        if os.path.exists(health_routes_path):
            print("✅ Health routes directory exists")
        else:
            print("❌ Health routes directory missing")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Route file check failed: {e}")
        return False

print("Testing critical routes...")
if test_route_files_exist():
    print("✅ Route validation passed")
    sys.exit(0)
else:
    print("❌ Route validation failed")
    sys.exit(1)