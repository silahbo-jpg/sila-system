"""
Test script to verify Python imports in the virtual environment.
"""
import sys
import os
import site
import pkg_resources

def print_section(title):
    """Print a section header."""
    print(f"\n{'-' * 80}\n{title}\n{'-' * 80}")

def check_import(module_name):
    """Check if a module can be imported."""
    try:
        __import__(module_name)
        version = sys.modules[module_name].__version__ if hasattr(sys.modules[module_name], '__version__') else 'unknown'
        print(f"✓ {module_name:<30} [IMPORTED] (version: {version})")
        return True
    except ImportError as e:
        print(f"✗ {module_name:<30} [IMPORT FAILED] {e}")
        return False
    except Exception as e:
        print(f"✗ {module_name:<30} [ERROR] {e}")
        return False

# Print environment information
print_section("PYTHON ENVIRONMENT")
print(f"Python Executable: {sys.executable}")
print(f"Python Path:")
for i, path in enumerate(sys.path, 1):
    print(f"  {i:>2}. {path}")

# Check required packages
print_section("CHECKING IMPORTS")
required_modules = [
    'opentelemetry',
    'opentelemetry.sdk.trace',
    'opentelemetry.sdk.resources',
    'opentelemetry.instrumentation.fastapi',
    'opentelemetry.instrumentation.sqlalchemy',
    'fastapi',
    'sqlalchemy',
    'pydantic',
    'pytest',
    'pytest_asyncio',
    'app.core.config',
    'app.db.session'
]

all_imports_ok = all(check_import(module) for module in required_modules)

print_section("TEST RESULT")
if all_imports_ok:
    print("✅ All imports successful!")
else:
    print("❌ Some imports failed. Check the output above for details.")
    print("\nTroubleshooting steps:")
    print("1. Make sure the virtual environment is activated")
    print("2. Run 'pip install -e .' in the backend directory")
    print("3. Check for any error messages during package installation")
