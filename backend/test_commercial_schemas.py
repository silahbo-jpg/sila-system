#!/usr/bin/env python3
"""
Debug commercial schemas import issue
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Test direct import from commercial.schemas
    print("Testing direct import from app.modules.commercial.schemas...")
    from app.modules.commercial.schemas import CommercialLicenseResponse, CommercialLicenseCreate
    print("✅ Direct import successful!")
    print(f"✅ CommercialLicenseResponse: {CommercialLicenseResponse}")
    print(f"✅ CommercialLicenseCreate: {CommercialLicenseCreate}")
    
except ImportError as e:
    print(f"❌ Direct import failed: {e}")

try:
    # Test import the way endpoints.py does it
    print("\nTesting import the way endpoints.py does it...")
    from app.modules.commercial import schemas
    print("✅ Module import successful!")
    print(f"✅ schemas module: {schemas}")
    
    # Check what attributes are available
    available_attrs = [attr for attr in dir(schemas) if not attr.startswith('_')]
    print(f"✅ Available attributes: {available_attrs}")
    
    # Try to access the specific schemas
    if hasattr(schemas, 'CommercialLicenseResponse'):
        print(f"✅ CommercialLicenseResponse found: {schemas.CommercialLicenseResponse}")
    else:
        print("❌ CommercialLicenseResponse not found in schemas module")
        
    if hasattr(schemas, 'CommercialLicenseCreate'):
        print(f"✅ CommercialLicenseCreate found: {schemas.CommercialLicenseCreate}")
    else:
        print("❌ CommercialLicenseCreate not found in schemas module")
    
except ImportError as e:
    print(f"❌ Module import failed: {e}")

print("\n🎉 Commercial schemas import test complete!")