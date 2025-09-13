"""
Script to update Pydantic model configurations from orm_mode to from_attributes
for Pydantic v2 compatibility.
"""
import os
import re
from pathlib import Path

def update_file(file_path):
    """Update orm_mode to from_attributes in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace orm_mode with from_attributes
        updated_content = re.sub(
            r'orm_mode\s*=\s*True',
            'from_attributes = True',
            content
        )
        
        # Only write if changes were made
        if updated_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"Updated: {file_path}")
            return True
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    # Define the root directory to search
    root_dir = Path(__file__).parent
    updated_count = 0
    
    # Find all Python files in the project
    for py_file in root_dir.glob('**/*.py'):
        # Skip virtual environment directories
        if any(part.startswith(('.', 'venv', 'env', '__pycache__')) for part in py_file.parts):
            continue
            
        # Check if file contains orm_mode
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                if 'orm_mode' in f.read():
                    if update_file(py_file):
                        updated_count += 1
        except Exception as e:
            print(f"Error checking {py_file}: {e}")
    
    print(f"\nUpdate complete. {updated_count} files were updated.")

if __name__ == "__main__":
    main()
