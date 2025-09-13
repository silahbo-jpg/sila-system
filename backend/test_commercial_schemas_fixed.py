import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

try:
    # Test importing the schemas that were causing issues
    from app.modules.commercial.schemas import CommercialLicenseResponse, CommercialLicenseCreate
    print("✅ Commercial schemas import successfully!")
    print(f"CommercialLicenseResponse: {CommercialLicenseResponse}")
    print(f"CommercialLicenseCreate: {CommercialLicenseCreate}")
except Exception as e:
    print(f"❌ Error importing commercial schemas: {e}")
    sys.exit(1)