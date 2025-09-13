#!/usr/bin/env python3
"""
Final script to fix the user.py file by cleaning up Field definitions.
"""

import re
from pathlib import Path

def fix_user_py():
    """Fix the user.py file by cleaning up Field definitions."""
    file_path = Path("backend/app/schemas/user.py")
    backup_path = file_path.with_suffix(f'{file_path.suffix}.final_bak')
    
    print(f"Processing: {file_path}")
    
    try:
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create a backup
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Created backup at: {backup_path}")
        
        # Split into lines for easier processing
        lines = content.splitlines()
        new_lines = []
        
        for line in lines:
            # Fix duplicate values in Field parameters
            # e.g., max_length=100100 -> max_length=100
            line = re.sub(r'(max_length|min_length|default|default_factory)=(\d+)\2', r'\1=\2', line)
            
            # Fix duplicate boolean values
            line = line.replace('default=TrueTrue', 'default=True')
            line = line.replace('default=FalseFalse', 'default=False')
            
            # Fix duplicate default_factory values
            line = re.sub(r'(default_factory=<class \'[^\']+\'>)default_factory=', r'\1, ', line)
            
            # Fix duplicate variable names
            line = re.sub(r'(default=user)user', r'\1', line)
            line = re.sub(r'(default=citizen)citizen', r'\1', line)
            
            # Fix missing comma between parameters
            line = re.sub(r'(\w+=\w+)(\s+\w+=)', r'\1, \2', line)
            
            new_lines.append(line)
        
        # Join the lines back together
        new_content = '\n'.join(new_lines)
        
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
