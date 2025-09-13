#!/usr/bin/env python3
"""Check for credential policy violations.

This script scans the codebase for any credentials that don't match the allowed patterns.
"""
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Optional

# Allowed credentials
ALLOWED_CREDENTIALS = {
    'username': 'postgres',
    'password': 'Truman1_Marcelo1_1985',
    'database': 'postgres',
    'host': 'localhost',
    'port': '5432',
}

# Patterns to check for potential credentials
CREDENTIAL_PATTERNS = [
    # Database URLs
    (r'(?i)(postgres(?:ql)?://|DATABASE_URL\s*[=:]\s*["\']?)[^\s"\'<]+', 'db_url'),
    # Usernames
    (r'(?i)(user(name)?\s*[=:]\s*["\']?)(?!postgres)([^\s"\'<,;]+)', 'username'),
    # Passwords
    (r'(?i)(pass(word)?\s*[=:]\s*["\']?)(?!Truman1_Marcelo1_1985)([^\s"\'<,;]+)', 'password'),
    # Hosts
    (r'(?i)(host\s*[=:]\s*["\']?)(?!localhost)([^\s"\'<,;]+)', 'host'),
    # Ports
    (r'(?i)(port\s*[=:]\s*["\']?)(?!5432)(\d+)', 'port'),
]

# Files/directories to exclude from scanning
EXCLUDED_PATHS = [
    '.git',
    '__pycache__',
    'venv',
    'env',
    '.pytest_cache',
    'node_modules',
    'build',
    'dist',
    '*.pyc',
    '*.pyo',
    '*.pyd',
    '.DS_Store',
    '*.log',
]

def is_excluded(path: Path) -> bool:
    """Check if a path should be excluded from scanning."""
    path_str = str(path).replace('\\', '/')
    return any(
        path.name == exclude or path.suffix.lstrip('.') == exclude.lstrip('*')
        for exclude in EXCLUDED_PATHS
    ) or any(part.startswith('.') and part not in ('.github', '.vscode') for part in path.parts)

def check_file(file_path: Path) -> List[Tuple[int, str, str]]:
    """Check a single file for credential violations."""
    violations = []
    
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
    except (UnicodeDecodeError, PermissionError):
        return []
    
    for line_num, line in enumerate(content.splitlines(), 1):
        for pattern, cred_type in CREDENTIAL_PATTERNS:
            matches = re.finditer(pattern, line)
            for match in matches:
                if cred_type == 'db_url':
                    url = match.group(0)
                    if 'postgres:Truman1_Marcelo1_1985@' not in url and 'postgresql://postgres:Truman1_Marcelo1_1985@' not in url:
                        violations.append((line_num, cred_type, line.strip()))
                else:
                    value = match.group(3) if len(match.groups()) >= 3 else match.group(1)
                    if value and value.lower() not in (v.lower() for v in ALLOWED_CREDENTIALS.values()):
                        violations.append((line_num, cred_type, line.strip()))
    
    return violations

def main() -> int:
    """Main entry point for the credential checker."""
    root_dir = Path(__file__).parent.parent
    has_errors = False
    
    for file_path in root_dir.rglob('*'):
        if not file_path.is_file() or is_excluded(file_path):
            continue
            
        violations = check_file(file_path)
        if violations:
            has_errors = True
            rel_path = file_path.relative_to(root_dir)
            print(f"\n\033[91m✗ {rel_path}:")
            for line_num, cred_type, line in violations:
                print(f"  Line {line_num}: Potential {cred_type} violation")
                print(f"    {line}")
    
    if has_errors:
        print("\n\033[91m❌ Credential policy violations found!")
        print("Please ensure all credentials follow the project's security policy.")
        print("Allowed credentials:")
        for k, v in ALLOWED_CREDENTIALS.items():
            print(f"  {k}: {v}")
        return 1
    
    print("\033[92m✓ No credential policy violations found!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
