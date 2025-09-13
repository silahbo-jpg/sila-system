"""
Script to verify Python environment and package installation.
"""
import sys
import os
import platform
import site
import pkgutil

def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f"{title:^80}")
    print("=" * 80)

def print_section(title):
    """Print a section header."""
    print(f"\n{title}")
    print("-" * len(title))

# Print environment information
print_header("PYTHON ENVIRONMENT INFORMATION")
print(f"Python Executable: {sys.executable}")
print(f"Python Version: {platform.python_version()}")
print(f"Platform: {platform.platform()}")
print(f"Current Working Directory: {os.getcwd()}")

# Print Python path
print_section("PYTHON PATH")
for i, path in enumerate(sys.path, 1):
    print(f"{i:>3}. {path}")

# Check for required packages
required_packages = [
    'opentelemetry',
    'opentelemetry-api',
    'opentelemetry-sdk',
    'opentelemetry-instrumentation-fastapi',
    'opentelemetry-instrumentation-sqlalchemy',
    'fastapi',
    'sqlalchemy',
    'pydantic',
    'pytest',
    'pytest-asyncio'
]

print_section("PACKAGE AVAILABILITY")
for package in required_packages:
    if pkgutil.find_loader(package):
        try:
            mod = __import__(package)
            version = getattr(mod, '__version__', 'version not found')
            print(f"✓ {package:<40} [INSTALLED] (version: {version})")
        except ImportError as e:
            print(f"✗ {package:<40} [ERROR] {e}")
    else:
        print(f"✗ {package:<40} [NOT FOUND]")
