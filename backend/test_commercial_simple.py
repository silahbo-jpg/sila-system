import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

try:
    # Test importing the commercial module specifically
    from app.modules.commercial.endpoints import router as commercial_router
    print("✅ Commercial module imported successfully!")
    
    # Test importing the schemas
    from app.modules.commercial.schemas import CommercialLicenseResponse, CommercialLicenseCreate
    print("✅ Commercial schemas imported successfully!")
    
    print("🎉 Commercial module is now fixed and working!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)