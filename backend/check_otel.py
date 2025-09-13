"""
Simple script to verify OpenTelemetry package installation.
"""
import sys
import pkg_resources

def check_package(package_name):
    try:
        dist = pkg_resources.get_distribution(package_name)
        print(f"✓ {package_name} is installed (version: {dist.version})")
        return True
    except pkg_resources.DistributionNotFound:
        print(f"✗ {package_name} is NOT installed")
        return False

print("Checking OpenTelemetry packages...")
packages = [
    'opentelemetry-api',
    'opentelemetry-sdk',
    'opentelemetry-instrumentation-fastapi',
    'opentelemetry-instrumentation-sqlalchemy'
]

all_installed = all(check_package(pkg) for pkg in packages)

if all_installed:
    print("\nAll required OpenTelemetry packages are installed!")
else:
    print("\nSome required packages are missing. Please install them using:")
    print("pip install opentelemetry-api opentelemetry-sdk opentelemetry-instrumentation-fastapi opentelemetry-instrumentation-sqlalchemy")
