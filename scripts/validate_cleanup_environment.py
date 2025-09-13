#!/usr/bin/env python3
"""
validate_cleanup_environment.py

Validates that the environment is properly set up for the final project cleanup.
"""

import os
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version is adequate."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"❌ Python version too old: {version.major}.{version.minor}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True


def check_required_files():
    """Check if required files and directories exist."""
    project_root = Path(__file__).parent.parent.resolve()
    required_paths = [
        ("Project root", project_root),
        ("Backend directory", project_root / "backend"),
        ("Scripts directory", project_root / "scripts"),
        ("Frontend directory", project_root / "frontend"),
        ("Reports directory", project_root / "reports"),
        ("Docker files", project_root / "docker-compose.yml"),
        ("Requirements files", project_root / "backend" / "requirements.txt")
    ]
    
    all_good = True
    for name, path in required_paths:
        if path.exists():
            print(f"✅ {name}: Found")
        else:
            print(f"⚠️  {name}: Not found ({path})")
            all_good = False
    
    return all_good


def check_required_scripts():
    """Check if required cleanup scripts exist."""
    project_root = Path(__file__).parent.parent.resolve()
    scripts_dir = project_root / "scripts"
    backend_dir = project_root / "backend"
    
    required_scripts = [
        ("Main cleanup script", scripts_dir / "finalize_project_cleanup.py"),
        ("PowerShell wrapper", scripts_dir / "finalize_project_cleanup.ps1"),
        ("Fix scripts", scripts_dir / "fix-all.ps1"),
        ("Structure scripts", scripts_dir / "organize_backend.ps1"),
        ("Validation scripts", scripts_dir / "run_all_validations.ps1")
    ]
    
    all_good = True
    for name, script_path in required_scripts:
        if script_path.exists():
            print(f"✅ {name}: Found")
        else:
            print(f"⚠️  {name}: Not found ({script_path})")
            all_good = False
    
    return all_good


def check_powershell():
    """Check if PowerShell is available."""
    try:
        result = subprocess.run(
            ["powershell", "-Command", "echo 'PowerShell available'"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✅ PowerShell: Available")
            return True
        else:
            print("⚠️  PowerShell: Not available or not in PATH")
            return False
    except Exception as e:
        print(f"⚠️  PowerShell: Error checking availability: {e}")
        return False


def check_docker():
    """Check if Docker is available."""
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print(f"✅ Docker: {result.stdout.strip()}")
            return True
        else:
            print("⚠️  Docker: Not available or not in PATH")
            return False
    except Exception as e:
        print(f"⚠️  Docker: Error checking availability: {e}")
        return False


def main():
    """Main validation function."""
    print("🔍 VALIDATING CLEANUP ENVIRONMENT")
    print("=" * 50)
    
    checks = [
        check_python_version,
        check_required_files,
        check_required_scripts,
        check_powershell,
        check_docker
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"❌ Error during {check.__name__}: {e}")
            results.append(False)
        print()
    
    print("=" * 50)
    if all(results):
        print("🎉 All environment checks passed!")
        print("✅ Ready to run final project cleanup")
        return 0
    else:
        failed_count = len([r for r in results if not r])
        print(f"⚠️  {failed_count} environment check(s) failed")
        print("Please address the issues above before running cleanup")
        return 1


if __name__ == "__main__":
    sys.exit(main())