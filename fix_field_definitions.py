#!/usr/bin/env python3
"""
Script to fix duplicate parameters in Field definitions in user.py
"""

import re
from pathlib import Path

def fix_duplicate_parameters():
    """Fix duplicate parameters in Field definitions in user.py"""
    file_path = Path("backend/app/schemas/user.py")
    backup_path = file_path.with_suffix(f'{file_path.suffix}.fixed_bak2')
    
    print(f"Processing: {file_path}")
    
    try:
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create a backup with a different name to avoid conflicts
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Created backup at: {backup_path}")
        
        # Pattern to find duplicate parameters in Field definitions
        # This will match patterns like "max_length=100max_length=100"
        pattern = r'\b(\w+)=([\w\[\]\{\}\'\"\s,.:]+?)\1='
        
        def replace_duplicate(match):
            param_name = match.group(1)
            param_value = match.group(2)
            return f"{param_name}={param_value}"
        
        # Apply the replacement
        new_content = re.sub(pattern, replace_duplicate, content)
        
        # Also fix any remaining issues with default=default=...
        new_content = re.sub(r'\b(default=\w+)default=', r'\1, default=', new_content)
        
        # Fix any remaining issues with default_factory=default_factory=...
        new_content = re.sub(r'\b(default_factory=[\w.<>]+)default_factory=', r'\1, default_factory=', new_content)
        
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
    fix_duplicate_parameters()
