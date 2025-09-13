#!/usr/bin/env python3
"""
Script to safely fix the user.py file by converting schema_extra to json_schema_extra.
This script is specifically designed to handle the user.py file with care.
"""

import re
from pathlib import Path

def fix_user_py():
    """Fix the user.py file by converting schema_extra to json_schema_extra."""
    file_path = Path("backend/app/schemas/user.py")
    backup_path = file_path.with_suffix(f'{file_path.suffix}.fixed_bak')
    
    print(f"Processing: {file_path}")
    
    try:
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create a backup with a different name to avoid conflicts
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Created backup at: {backup_path}")
        
        # Simple string replacement for schema_extra -> json_schema_extra
        # Only replace standalone schema_extra, not json_schema_extra
        new_content = re.sub(r'(?<!json_)schema_extra=', 'json_schema_extra=', content)
        
        # Only write if changes were made
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("  Successfully updated user.py")
            return True
        
        print("  No changes needed")
        return False
    
    except Exception as e:
        print(f"  Error processing file: {e}")
        # Restore from backup if there was an error
        try:
            if backup_path.exists():
                with open(backup_path, 'r', encoding='utf-8') as f:
                    backup_content = f.read()
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(backup_content)
                print(f"  Restored from backup due to error")
        except Exception as restore_error:
            print(f"  Could not restore from backup: {restore_error}")
        return False

if __name__ == "__main__":
    fix_user_py()
