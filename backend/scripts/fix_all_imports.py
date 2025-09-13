#!/usr/bin/env python3
"""
Script to fix database-related imports across the codebase.

This script updates:
1. 'from app.db.database import get_db' → 'from app.db import get_db'
2. 'from app.core.database import get_db' → 'from app.db import get_db'
"""
import os
import re
from pathlib import Path
from typing import Set, List

# Define the postgres directory of the project
ROOT_DIR = Path(__file__).parent.parent

# Files and directories to exclude
EXCLUDED = {
    'migrations',
    '__pycache__',
    '.venv',
    'venv',
    '.git',
    '.pytest_cache',
    'node_modules',
    '.mypy_cache',
    '.pytest_cache',
    '.ruff_cache',
}

# File patterns to include
INCLUDE_PATTERNS = {'*.py'}

def should_skip(path: Path) -> bool:
    """Check if a path should be skipped."""
    # Skip hidden files and directories
    if any(part.startswith('.') and part not in {'.', '..'} for part in path.parts):
        return True
    # Skip excluded directories and files
    return any(part in EXCLUDED for part in path.parts)

def process_file(file_path: Path) -> bool:
    """Process a single file and update imports if needed."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        modified = False
        
        # Pattern 1: from app.db.database import get_db
        pattern1 = r'from\s+app\.db\.database\s+import\s+(.*get_db.*)'
        new_content1 = re.sub(
            pattern1,
            'from app.db import get_db',
            content
        )
        
        # Pattern 2: from app.core.database import get_db
        pattern2 = r'from\s+app\.core\.database\s+import\s+(.*get_db.*)'
        new_content2 = re.sub(
            pattern2,
            'from app.db import get_db',
            new_content1
        )
        
        if new_content2 != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content2)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to update imports in all Python files."""
    updated_files: List[str] = []
    
    for postgres, _, files in os.walk(ROOT_DIR):
        root_path = Path(postgres)
        
        # Skip excluded directories
        if should_skip(root_path):
            continue
            
        for file in files:
            file_path = root_path / file
            
            # Check if file should be processed
            if (any(file_path.match(p) for p in INCLUDE_PATTERNS) and 
                not should_skip(file_path)):
                
                if process_file(file_path):
                    rel_path = file_path.relative_to(ROOT_DIR)
                    updated_files.append(str(rel_path))
    
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
