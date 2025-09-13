#!/usr/bin/env python3
"""
Import Standardization Script
Fixes and standardizes Python imports across the project.
"""

import os
import re
import ast
from pathlib import Path
from typing import List, Set, Dict

class ImportFixer:
    """Fixes and standardizes Python imports."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.backend_dir = project_root / "backend"
        self.fixes_applied = 0
        
    def fix_file(self, file_path: Path) -> bool:
        """Fix imports in a single Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix relative imports
            content = self.fix_relative_imports(content, file_path)
            
            # Fix import order
            content = self.fix_import_order(content)
            
            # Fix common import issues
            content = self.fix_common_issues(content)
            
            # Write back if changed
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.fixes_applied += 1
                return True
                
        except Exception as e:
            print(f"❌ Error fixing {file_path}: {e}")
            return False
        
        return False
    
    def fix_relative_imports(self, content: str, file_path: Path) -> str:
        """Fix relative imports to absolute imports."""
        lines = content.split('\n')
        fixed_lines = []
        
        for line in lines:
            # Fix relative imports like "from .module import something"
            if re.match(r'^\s*from\s+\.+\w+', line):
                # Convert to absolute import
                relative_match = re.match(r'^(\s*)from\s+(\.+)(\w+.*?)\s+import\s+(.+)$', line)
                if relative_match:
                    indent, dots, module_path, imports = relative_match.groups()
                    
                    # Calculate absolute path
                    if file_path.is_relative_to(self.backend_dir / "app"):
                        rel_path = file_path.relative_to(self.backend_dir / "app")
                        current_package = ".".join(rel_path.parent.parts)
                        
                        if current_package:
                            abs_import = f"{indent}from app.{current_package}.{module_path} import {imports}"
                        else:
                            abs_import = f"{indent}from app.{module_path} import {imports}"
                        
                        fixed_lines.append(abs_import)
                        continue
            
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def fix_import_order(self, content: str) -> str:
        """Fix import order according to PEP 8."""
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return content  # Can't parse, return as-is
        
        imports = []
        other_lines = []
        
        for node in tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                imports.append(ast.get_source_segment(content, node))
            else:
                # Find the line in original content
                other_lines.append(node)
        
        if not imports:
            return content
        
        # Sort imports: stdlib, third-party, local
        stdlib_imports = []
        third_party_imports = []
        local_imports = []
        
        for imp in imports:
            if imp is None:
                continue
                
            if re.match(r'^\s*from\s+app\.', imp) or re.match(r'^\s*import\s+app\.', imp):
                local_imports.append(imp)
            elif any(stdlib_mod in imp for stdlib_mod in ['os', 'sys', 'pathlib', 'datetime', 're', 'json']):
                stdlib_imports.append(imp)
            else:
                third_party_imports.append(imp)
        
        # Reconstruct content
        sorted_imports = []
        if stdlib_imports:
            sorted_imports.extend(sorted(stdlib_imports))
            sorted_imports.append('')  # Empty line
        if third_party_imports:
            sorted_imports.extend(sorted(third_party_imports))
            sorted_imports.append('')  # Empty line
        if local_imports:
            sorted_imports.extend(sorted(local_imports))
            sorted_imports.append('')  # Empty line
        
        # Get the rest of the content after imports
        lines = content.split('\n')
        import_end = 0
        for i, line in enumerate(lines):
            if not (line.strip().startswith(('import ', 'from ')) or line.strip() == '' or line.strip().startswith('#')):
                import_end = i
                break
        
        rest_content = '\n'.join(lines[import_end:])
        
        return '\n'.join(sorted_imports) + rest_content
    
    def fix_common_issues(self, content: str) -> str:
        """Fix common import issues."""
        # Remove duplicate imports
        lines = content.split('\n')
        seen_imports = set()
        fixed_lines = []
        
        for line in lines:
            if re.match(r'^\s*(import|from)\s+', line):
                normalized = re.sub(r'\s+', ' ', line.strip())
                if normalized not in seen_imports:
                    seen_imports.add(normalized)
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def scan_directory(self, directory: Path) -> List[Path]:
        """Scan directory for Python files."""
        python_files = []
        
        for file_path in directory.rglob('*.py'):
            # Skip __pycache__ and other ignored directories
            if any(ignored in str(file_path) for ignored in ['__pycache__', '.venv', 'venv', '.git']):
                continue
            python_files.append(file_path)
        
        return python_files

def main():
    """Main function to fix imports."""
    print("🔧 Python Import Standardization")
    print("=" * 40)
    
    project_root = Path(__file__).parent.parent.parent
    fixer = ImportFixer(project_root)
    
    # Scan backend directory
    backend_files = fixer.scan_directory(project_root / "backend")
    
    print(f"📁 Found {len(backend_files)} Python files")
    
    for file_path in backend_files:
        try:
            if fixer.fix_file(file_path):
                print(f"✅ Fixed: {file_path.relative_to(project_root)}")
        except Exception as e:
            print(f"❌ Error: {file_path.relative_to(project_root)}: {e}")
    
    print(f"\n🎉 Import fixes complete! Applied {fixer.fixes_applied} fixes.")
    
    return True

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)