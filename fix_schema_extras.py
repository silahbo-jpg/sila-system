#!/usr/bin/env python3
"""
Script to safely convert schema_extra to json_schema_extra in Pydantic models.
This is a more reliable version that handles the conversion safely.
"""

import re
from pathlib import Path
import shutil

# Define the project root directory
PROJECT_ROOT = Path(__file__).parent.absolute()

def find_python_files(directory: Path):
    """Find all Python files in the given directory, excluding venv and other special dirs."""
    exclude_dirs = {'venv', '.venv', 'env', '.git', '__pycache__', '.mypy_cache', '.pytest_cache'}
    
    for path in directory.rglob('*.py'):
        # Skip files in excluded directories
        if not any(part in exclude_dirs for part in path.parts):
            yield path

def process_file(file_path: Path):
    """Process a single Python file to convert schema_extra to json_schema_extra."""
    print(f"Checking: {file_path}")
    
    try:
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if no schema_extra in the file
        if 'schema_extra' not in content:
            return False
        
        # Create a backup if one doesn't exist
        backup_path = file_path.with_suffix(f'{file_path.suffix}.bak')
        if not backup_path.exists():
            shutil.copy2(file_path, backup_path)
        
        # Simple string replacement for schema_extra -> json_schema_extra
        # This is safer than trying to parse the Python code
        new_content = content.replace('json_schema_extra=', 'json_json_schema_extra=')
        
        # Only write if changes were made
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  Updated: {file_path}")
            return True
            
        return False
    
    except Exception as e:
        print(f"  Error processing {file_path}: {e}")
        # Restore from backup if there was an error and we modified the file
        if 'new_content' in locals() and new_content != content:
            if backup_path.exists():
                shutil.copy2(backup_path, file_path)
                print(f"  Restored {file_path} from backup due to error")
        return False

def main():
    """Main function to run the script."""
    print(f"Starting conversion of schema_extra to json_schema_extra in {PROJECT_ROOT}")
    
    # Find all Python files in the project
    python_files = list(find_python_files(PROJECT_ROOT))
    print(f"Found {len(python_files)} Python files to check")
    
    # Process each file
    updated_files = 0
    for file_path in python_files:
        if process_file(file_path):
            updated_files += 1
    
    print(f"\nConversion complete!")
    print(f"- Files checked: {len(python_files)}")
    print(f"- Files updated: {updated_files}")
    print(f"- Backups created with .bak extension where needed")

if __name__ == "__main__":
    main()
