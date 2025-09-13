#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility to scan and detect broken imports and missing classes/functions.

Run with:
    # From sila-system/backend
    python scripts/check_imports.py

    # Or from sila-system
    PYTHONPATH=backend python -m scripts.check_imports
"""

import os
import sys
import ast
import importlib
import traceback
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple

# Set console output encoding to UTF-8
if sys.platform == "win32":
    import io
    import sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Add backend to Python path
BACKEND_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BACKEND_DIR))

# Configuration
BASE_DIR = BACKEND_DIR / "app"
IGNORE_DIRS = {"__pycache__", ".pytest_cache", "venv", ".venv"}
IGNORE_IMPORTS = {"pydantic", "fastapi", "sqlalchemy", "passlib"}

# Simple text-based status indicators
STATUS = {
    "check": "[CHECK]",
    "error": "[ERROR]",
    "warning": "[WARN]",
    "success": "[OK]",
    "fail": "[FAIL]"
}

class ImportChecker(ast.NodeVisitor):
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.issues: List[Tuple[str, str]] = []
        self.imported_modules: Set[str] = set()
        self.imported_names: Dict[str, Set[str]] = {}

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            mod = alias.name
            asname = alias.asname or alias.name
            if mod.split('.')[0] in IGNORE_IMPORTS:
                continue
                
            self.imported_modules.add(mod)
            self.imported_names[asname] = set()
            
            try:
                importlib.import_module(mod)
            except (ImportError, ModuleNotFoundError, AttributeError) as e:
                self.issues.append((f"[BROKEN IMPORT] {mod}", str(e)))
            except Exception as e:
                self.issues.append((f"[ERROR] {mod}", str(e)))

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if not node.module:
            return
            
        mod = node.module
        if mod.split('.')[0] in IGNORE_IMPORTS:
            return
            
        self.imported_modules.add(mod)
        
        # Handle relative imports
        if node.level > 0:
            rel_path = self.file_path.parent
            for _ in range(node.level - 1):
                rel_path = rel_path.parent
            rel_import = '.'.join(rel_path.parts[rel_path.parts.index('app'):] + (mod,))
            mod = rel_import.replace('\\', '.').replace('/', '.')
        
        for name in node.names:
            asname = name.asname or name.name
            if asname == '*':
                continue
                
            try:
                module = importlib.import_module(mod)
                if not hasattr(module, name.name):
                    self.issues.append((
                        f"[MISSING] {mod}.{name.name}",
                        f"Cannot import name '{name.name}' from '{mod}'",
                    ))
                else:
                    if mod not in self.imported_names:
                        self.imported_names[mod] = set()
                    self.imported_names[mod].add(asname)
            except (ImportError, ModuleNotFoundError) as e:
                self.issues.append((f"[BROKEN MODULE] {mod}", str(e)))
            except Exception as e:
                self.issues.append((f"[ERROR] {mod}.{name.name}", str(e)))

def check_imports_in_file(file_path: Path) -> ImportChecker:
    """Check imports in a single Python file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                tree = ast.parse(f.read(), filename=str(file_path))
            except SyntaxError as e:
                print(f"[SYNTAX ERROR] {file_path}: {e}")
                return None
                
        checker = ImportChecker(file_path)
        checker.visit(tree)
        return checker
        
    except Exception as e:
        print(f"[ERROR] Failed to process {file_path}: {e}")
        return None

def check_missing_classes_functions():
    """Check for missing classes and functions in the codebase."""
    print(f"\n{STATUS['check']} Checking for missing classes and functions...")
    
    # Check for missing schemas
    missing = []
    
    # Check for JudicialCertificateCreate
    try:
        from app.modules.justice.schemas import JudicialCertificateCreate
    except (ImportError, AttributeError) as e:
        missing.append(("JudicialCertificateCreate", "app.modules.justice.schemas", str(e)))
    
    # Check for ComplaintService
    try:
        from app.modules.complaints.services import ComplaintService
    except (ImportError, AttributeError) as e:
        missing.append(("ComplaintService", "app.modules.complaints.services", str(e)))
    
    # Check for HealthCreate
    try:
        from app.modules.health.schemas import HealthCreate
    except (ImportError, AttributeError) as e:
        missing.append(("HealthCreate", "app.modules.health.schemas", str(e)))
    
    if missing:
        print(f"\n{STATUS['error']} Missing classes/functions:")
        for name, module, error in missing:
            print(f"  - {name} from {module}: {error}")
    else:
        print(f"{STATUS['success']} All required classes and functions are present")

def main():
    print(f"{STATUS['check']} Checking imports in {BASE_DIR}...\n")
    
    issues_found = False
    
    for py_file in sorted(BASE_DIR.rglob("*.py")):
        # Skip ignored directories
        if any(part in IGNORE_DIRS for part in py_file.parts):
            continue
            
        rel_path = py_file.relative_to(BACKEND_DIR)
        print(f"{STATUS['check']} {rel_path}")
        
        checker = check_imports_in_file(py_file)
        if checker and checker.issues:
            issues_found = True
            print(f"  {STATUS['error']} Found {len(checker.issues)} issue(s):")
            for issue, detail in checker.issues:
                print(f"    - {issue}: {detail}")
    
    check_missing_classes_functions()
    
    if issues_found:
        print(f"\n{STATUS['fail']} Issues found. Please fix the above problems.")
        sys.exit(1)
    else:
        print(f"\n{STATUS['success']} No import issues found!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n{STATUS['error']} An error occurred: {e}")
        if os.getenv("DEBUG"):
            import traceback
            traceback.print_exc()
        sys.exit(1)
