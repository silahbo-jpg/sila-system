"""
Environment check script to diagnose Python environment and package issues.
"""
import os
import sys
import subprocess
import pkg_resources
from pathlib import Path

def print_section(title):
    """Print a section header."""
    print(f"\n{'=' * 80}\n{title}\n{'=' * 80}")

def run_command(cmd, cwd=None):
    """Run a shell command and return its output."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Command failed with error: {e.stderr}"

def main():
    """Main function to check the environment."""
    # Basic environment info
    print_section("PYTHON ENVIRONMENT")
    print(f"Python Executable: {sys.executable}")
    print(f"Python Version: {sys.version}")
    print(f"Current Working Directory: {os.getcwd()}")
    
    # Check if running in a virtual environment
    print_section("VIRTUAL ENVIRONMENT")
    print(f"Virtual Environment: {'Yes' if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 'No'}")
    print(f"sys.prefix: {sys.prefix}")
    print(f"sys.base_prefix: {sys.base_prefix}")
    
    # Check Python path
    print_section("PYTHON PATH")
    for i, path in enumerate(sys.path, 1):
        print(f"{i:>3}. {path}")
    
    # Check installed packages
    print_section("INSTALLED PACKAGES")
    installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    
    # Check for required packages
    required_packages = [
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
    
    for pkg in required_packages:
        if pkg in installed_packages:
            print(f"✓ {pkg:<40} [INSTALLED] (version: {installed_packages[pkg]})")
        else:
            print(f"✗ {pkg:<40} [NOT FOUND]")
    
    # Check if we can import opentelemetry
    print_section("OPENTELEMETRY IMPORT TEST")
    try:
        import opentelemetry
        print(f"✓ opentelemetry imported successfully (version: {opentelemetry.__version__ if hasattr(opentelemetry, '__version__') else 'unknown'})")
    except ImportError as e:
        print(f"✗ Failed to import opentelemetry: {e}")
    
    # Check if we can import the app
    print_section("APP IMPORT TEST")
    try:
        from app.core.config import settings
        print(f"✓ app.core.config imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import app.core.config: {e}")
    
    # Check if we can run pytest
    print_section("PYTEST CHECK")
    try:
        import pytest
        print(f"✓ pytest imported successfully (version: {pytest.__version__})")
        print("\nRunning 'pytest --version':")
        print(run_command("pytest --version"))
    except ImportError as e:
        print(f"✗ Failed to import pytest: {e}")

if __name__ == "__main__":
    main()
