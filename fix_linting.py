#!/usr/bin/env python3
"""
Automated linting fixer for the SILA System project.
This script helps fix common linting issues automatically.
"""
import os
import re
from typing import List, Set, Tuple

# Files to process
PYTHON_FILES = [
    "app/services/permission_service.py",
    "app/services/user_service.py",
    "app/utils/pdf_generator.py",
    "app/tests/conftest.py",
    "app/utils/qrcode_gen.py",
    "app/utils/qrcode_generator.py",
    "app/utils/validador_foto.py"
]

def remove_trailing_whitespace(content: str) -> str:
    """Remove trailing whitespace from all lines."""
    return '\n'.join(line.rstrip() for line in content.splitlines())

def clean_blank_lines(content: str) -> str:
    """Remove whitespace from blank lines."""
    return re.sub(r'^\s+$', '', content, flags=re.MULTILINE)

def fix_unused_imports(content: str) -> Tuple[str, List[str]]:
    """Identify and remove unused imports."""
    lines = content.splitlines()
    unused_imports = []
    
    # This is a simple check - for a more robust solution, consider using autoflake
    for i, line in enumerate(lines):
        if line.strip().startswith('import ') or 'from ' in line:
            # Skip if line has a comment indicating it's used
            if '# noqa' in line or '# type: ignore' in line:
                continue
                
            # This is a very basic check - in a real scenario, you'd want to analyze the code
            # to see if the imported names are actually used
            if 'unused' in line.lower() or 'typing.' in line:
                unused_imports.append(line.strip())
    
    return '\n'.join(lines), unused_imports

def process_file(file_path: str):
    """Process a single file to fix linting issues."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply fixes
        content = remove_trailing_whitespace(content)
        content = clean_blank_lines(content)
        content, unused_imports = fix_unused_imports(content)
        
        # Save changes if any
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Fixed issues in {file_path}")
            if unused_imports:
                print(f"   Found potentially unused imports (review manually):")
                for imp in unused_imports:
                    print(f"   - {imp}")
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {str(e)}")

def main():
    print("🚀 Starting linting fixes...\n")
    
    # Convert relative paths to absolute
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    for file_path in PYTHON_FILES:
        abs_path = os.path.join(base_dir, file_path)
        if os.path.exists(abs_path):
            process_file(abs_path)
        else:
            print(f"⚠️  File not found: {file_path}")
    
    print("\n✨ Linting fixes completed!")
    print("\nNext steps:")
    print("1. Review the changes made")
    print("2. Run 'flake8 .' to check remaining issues")
    print("3. Let me know if you want to address specific remaining issues")

if __name__ == "__main__":
    main()

