"""
Project Structure Validator for SILA System

This script validates the project structure to ensure all required modules and files exist.
"""
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Required module structure
REQUIRED_STRUCTURE = {
    "app": {
        "modules": {
            "auth": ["schemas.py", "__init__.py"],
            "health": ["schemas.py", "services.py", "__init__.py"],
        },
        "__init__.py": None,
    },
    "tests": {
        "modules": {
            "health": ["test_endpoints.py"],
        },
    },
}

def check_directory_structure(base_path: Path, structure: Dict, path: Path = None) -> List[str]:
    """Recursively check directory structure against expected structure."""
    if path is None:
        path = Path(".")
    
    errors = []
    
    for item, contents in structure.items():
        current_path = path / item
        full_path = base_path / current_path
        
        # Check if directory exists
        if not full_path.exists():
            errors.append(f"Missing directory: {current_path}")
            continue
            
        # If contents is None, this should be a file
        if contents is None:
            if not full_path.is_file():
                errors.append(f"Expected file, found directory: {current_path}")
            continue
            
        # If contents is a list, check for required files
        if isinstance(contents, list):
            for required_file in contents:
                file_path = full_path / required_file
                if not file_path.exists():
                    errors.append(f"Missing file: {current_path / required_file}")
        # If contents is a dict, it's a subdirectory
        elif isinstance(contents, dict):
            errors.extend(check_directory_structure(base_path, contents, current_path))
    
    return errors

def validate_imports() -> List[str]:
    """Validate that all required modules can be imported."""
    errors = []
    
    try:
        from app.modules.auth import schemas as auth_schemas
    except ImportError as e:
        errors.append(f"Failed to import auth.schemas: {str(e)}")
    
    try:
        from app.modules.health import schemas as health_schemas, services as health_services
    except ImportError as e:
        errors.append(f"Failed to import health modules: {str(e)}")
    
    return errors

def main():
    """Main validation function."""
    base_path = Path(os.getcwd())
    
    print("🔍 Validating project structure...")
    structure_errors = check_directory_structure(base_path, REQUIRED_STRUCTURE)
    
    print("🔍 Validating imports...")
    import_errors = validate_imports()
    
    all_errors = structure_errors + import_errors
    
    if all_errors:
        print("\n❌ Validation failed with the following errors:")
        for error in all_errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("\n✅ Project structure and imports are valid!")
        sys.exit(0)

if __name__ == "__main__":
    main()

