#!/usr/bin/env python3
"""
Script to fix corrupted __init__.py files with unterminated string literals
"""
import os
import re
from pathlib import Path

def fix_init_file(file_path):
    """Fix a single __init__.py file with unterminated string literals"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match unterminated string literals like:
        # "# module name module
        # # Este arquivo foi gerado automaticamente pelo script fix_module_structure.ps1
        # "
        pattern = r'^"(# .* module)\n(# Este arquivo foi gerado automaticamente pelo script fix_module_structure\.ps1)\n"$'
        
        if re.search(pattern, content, re.MULTILINE):
            # Replace with proper comments
            fixed_content = re.sub(pattern, r'\1\n\2', content, flags=re.MULTILINE)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            print(f"Fixed: {file_path}")
            return True
        
        # Also handle the variant with extra newlines
        pattern2 = r'^"(# .* module)\n(# Este modulo foi gerado automaticamente pelo script fix_module_structure\.ps1)\n\n"$'
        
        if re.search(pattern2, content, re.MULTILINE):
            fixed_content = re.sub(pattern2, r'\1\n\2', content, flags=re.MULTILINE)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            print(f"Fixed: {file_path}")
            return True
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False
    
    return False

def main():
    """Main function to find and fix all corrupted __init__.py files"""
    backend_path = Path("backend/app/modules")
    
    if not backend_path.exists():
        print(f"Backend path not found: {backend_path}")
        return
    
    fixed_count = 0
    total_count = 0
    
    # Find all __init__.py files
    for init_file in backend_path.rglob("__init__.py"):
        total_count += 1
        if fix_init_file(init_file):
            fixed_count += 1
    
    print(f"\nSummary: Fixed {fixed_count} out of {total_count} __init__.py files")

if __name__ == "__main__":
    main()

