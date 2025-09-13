#!/usr/bin/env python3
"""
Script to fix syntax errors in citizenship route files
Adds missing commas and db parameters in function definitions
"""

import os
import re
from pathlib import Path

def fix_route_file(file_path):
    """Fix syntax errors in a single route file"""
    print(f"Processing: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match function definitions with missing commas
    patterns = [
        # Pattern 1: data: SomeCreate current_user = Depends(...)
        (r'(def \w+\(\s*)(data: \w+Create)\s+(current_user = Depends\(get_current_active_user\)\s*\):)', 
         r'\1\2,\n    db: Session = Depends(get_db),\n    \3'),
        
        # Pattern 2: item_id: int current_user = Depends(...)
        (r'(def \w+\(\s*)(item_id: int)\s+(current_user = Depends\(get_current_active_user\)\s*\):)', 
         r'\1\2,\n    db: Session = Depends(get_db),\n    \3'),
        
        # Pattern 3: skip: int = 0, limit: int = 100 current_user = Depends(...)
        (r'(def \w+\(\s*)(skip: int = 0,\s*limit: int = 100)\s+(current_user = Depends\(get_current_active_user\)\s*\):)', 
         r'\1\2,\n    db: Session = Depends(get_db),\n    \3'),
        
        # Pattern 4: item_id: int, data: SomeUpdate current_user = Depends(...)
        (r'(def \w+\(\s*)(item_id: int,\s*data: \w+Update)\s+(current_user = Depends\(get_current_active_user\)\s*\):)', 
         r'\1\2,\n    db: Session = Depends(get_db),\n    \3'),
    ]
    
    modified = False
    for pattern, replacement in patterns:
        new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        if new_content != content:
            content = new_content
            modified = True
    
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Fixed: {file_path}")
        return True
    else:
        print(f"⏭️ No changes needed: {file_path}")
        return False

def main():
    """Main function to fix all route files"""
    backend_dir = Path(__file__).resolve().parents[1]
    routes_dir = backend_dir / "app" / "modules" / "citizenship" / "routes"
    
    if not routes_dir.exists():
        print(f"❌ Routes directory not found: {routes_dir}")
        return
    
    print("🔧 Fixing syntax errors in citizenship route files...")
    print("=" * 60)
    
    fixed_count = 0
    for py_file in routes_dir.glob("*.py"):
        if py_file.name != "__init__.py":
            if fix_route_file(py_file):
                fixed_count += 1
    
    print("=" * 60)
    print(f"✅ Complete! Fixed {fixed_count} files")

if __name__ == "__main__":
    main()