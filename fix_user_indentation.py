#!/usr/bin/env python3
"""
Script to fix indentation and formatting issues in user.py
"""

from pathlib import Path

def fix_user_py():
    """Fix indentation and formatting in user.py"""
    file_path = Path("backend/app/schemas/user.py")
    backup_path = file_path.with_suffix(f'{file_path.suffix}.indent_bak')
    
    print(f"Processing: {file_path}")
    
    try:
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create a backup
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Created backup at: {backup_path}")
        
        # Split into lines for processing
        lines = content.splitlines()
        new_lines = []
        
        # Track class indentation level
        current_indent = 0
        in_class = False
        
        for line in lines:
            stripped = line.lstrip()
            
            # Skip empty lines
            if not stripped:
                new_lines.append(line)
                continue
                
            # Handle class definitions
            if stripped.startswith('class '):
                in_class = True
                current_indent = 4  # Standard Python class indentation
                new_lines.append(line)
                continue
                
            # Handle method/function definitions
            if stripped.startswith('def ') and '):' in line:
                # If inside a class, add extra indentation
                indent = ' ' * (current_indent + 4) if in_class else '    '
                new_line = indent + stripped
                new_lines.append(new_line)
                continue
                
            # Handle field definitions
            if '= Field(' in stripped and not stripped.startswith('#'):
                # Clean up field definition
                indent = ' ' * (current_indent + 4)  # Standard field indentation in Pydantic models
                
                # Remove any duplicate parameters
                clean_line = stripped
                
                # Fix common issues
                if 'default=user' in clean_line:
                    clean_line = clean_line.replace('default=user', 'default="user"')
                if 'default=citizen' in clean_line:
                    clean_line = clean_line.replace('default=citizen', 'default="citizen"')
                if 'default=NoneNone' in clean_line:
                    clean_line = clean_line.replace('default=NoneNone', 'default=None')
                if 'default_factory=<class' in clean_line and 'default_factory=' in clean_line[clean_line.find('default_factory=')+16:]:
                    clean_line = clean_line.replace('default_factory=<class', 'default_factory=')
                
                new_line = indent + clean_line
                new_lines.append(new_line)
                continue
                
            # Handle other lines
            if in_class and not stripped.startswith('@'):
                indent = ' ' * (current_indent + 4)
                new_line = indent + stripped
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        
        # Join the lines back together
        new_content = '\n'.join(new_lines)
        
        # Only write if changes were made
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("  Successfully updated user.py with proper indentation")
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
