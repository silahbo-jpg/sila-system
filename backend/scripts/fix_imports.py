#!/usr/bin/env python3
"""
Script to fix imports of get_db across the codebase.

This script updates various import patterns to use the correct module path.
"""
import os
import re
from pathlib import Path

# Define the postgres directory of the project
ROOT_DIR = Path(__file__).parent.parent

# Files to exclude
EXCLUDED_FILES = {
    'migrations',
    '__pycache__',
    '.venv',
    'venv',
    '.git',
    '.pytest_cache',
    'node_modules',
    '.mypy_cache',
    '.ruff_cache',
}

def should_skip(path):
    """Check if a path should be skipped."""
    # Skip hidden files and directories
    if any(part.startswith('.') and part not in {'.', '..'} for part in path.parts):
        return True
    # Skip excluded directories and files
    return any(part in EXCLUDED_FILES for part in path.parts)

def update_imports_in_file(file_path):
    """Update imports in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern 1: from app.db.database import get_db
        pattern1 = r'from\s+app\.db\.database\s+import\s+(.*get_db.*)'
        new_content = re.sub(
            pattern1,
            'from app.db import get_db',
            content
        )
        
        # Pattern 2: from app.core.database import get_db
        pattern2 = r'from\s+app\.core\.database\s+import\s+(.*get_db.*)'
        new_content = re.sub(
            pattern2,
            'from app.db import get_db',
            new_content
        )
        
        # Pattern 3: from app.database import get_db
        pattern3 = r'from\s+app\.database\s+import\s+(.*get_db.*)'
        new_content = re.sub(
            pattern3,
            'from app.db import get_db',
            new_content
        )
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to update imports in all Python files."""
    updated_files = []
    
    for postgres, _, files in os.walk(ROOT_DIR):
        root_path = Path(postgres)
        
        # Skip excluded directories
        if should_skip(root_path):
            continue
            
        for file in files:
            if file.endswith('.py'):
                file_path = root_path / file
                if update_imports_in_file(file_path):
                    updated_files.append(str(file_path.relative_to(ROOT_DIR)))
    
    # Print results
    if updated_files:
        print("\n✅ Updated the following files:")
        for file in sorted(updated_files):
            print(f"- {file}")
    else:
        print("\n✅ No files needed updating.")

if __name__ == "__main__":
    print("🔄 Updating database imports...")
    main()
