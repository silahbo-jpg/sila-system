#!/usr/bin/env python3
"""
Credential Sanitizer for SILA System

Scans the project for sensitive credentials and replaces them with standardized values.
Generates a detailed report of all changes made.
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Pattern, Union, Callable
from dataclasses import dataclass

# Standard credentials to use as replacements
STANDARD_CREDENTIALS = {
    'username': 'postgres',
    'password': 'Truman1_Marcelo1_1985'
}

def replace_credential(match: re.Match, credential_type: str) -> str:
    """Helper function to replace credentials with standardized values."""
    try:
        if credential_type == 'db_url':
            # Handle database URLs - preserve the protocol and host parts
            if len(match.groups()) >= 3:
                protocol = match.group(3)  # postgresql:// or postgres://
                return f"{match.group(1)}{protocol}postgres:Truman1_Marcelo1_1985@"
            return match.group(0)
            
        elif credential_type == 'secret_key':
            # Only replace the value part, keep the key
            if len(match.groups()) >= 1:
                return f"{match.group(1)}SECRET_KEY_PLACEHOLDER"
            return match.group(0)
            
        else:
            # Handle username/password in configs
            if len(match.groups()) >= 3:
                prefix = match.group(1) or ''
                suffix = match.group(3) or ''
                
                if credential_type == 'username':
                    return f"{prefix}{STANDARD_CREDENTIALS['username']}{suffix}"
                elif credential_type == 'password':
                    return f"{prefix}{STANDARD_CREDENTIALS['password']}{suffix}"
                elif credential_type == 'email':
                    return f"{prefix}user@example.com{suffix}"
    except Exception as e:
        print(f"Error in replace_credential: {e}")
    return match.group(0)

def is_config_file(filepath: str) -> bool:
    """Check if a file is a configuration file."""
    config_extensions = {'.env', '.ini', '.cfg', '.conf', '.yaml', '.yml', '.json', '.toml'}
    config_filenames = {'docker-compose.yml', 'docker-compose.yaml', 'docker-compose.override.yml'}
    
    path = Path(filepath)
    return (path.suffix.lower() in config_extensions or 
            path.name.lower() in config_filenames or
            'config' in path.name.lower() or
            'secret' in path.name.lower())

# Patterns to search for and their replacements
CREDENTIAL_PATTERNS = [
    # Database URLs in various formats
    {
        'pattern': r'(?i)((DATABASE|POSTGRES|DB)_URL\s*[=:]\s*[\"\']?)(postgres(?:ql)?://)[^:]+:[^@]+@',
        'replacement': lambda m: replace_credential(m, 'db_url'),
        'description': 'Database URL with credentials',
        'file_pattern': '.*'  # Apply to all files
    },
    
    # Username in configs
    {
        'pattern': r'(?i)(USER(?:NAME)?\s*[=:]\s*[\"\']?)(sila[-_]?system|admin|root|user)([\"\']?)',
        'replacement': lambda m: replace_credential(m, 'username'),
        'description': 'Username in configuration',
        'file_pattern': r'.*\.(env|ini|cfg|conf|yaml|yml|json|toml)$'
    },
    
    # Password in configs
    {
        'pattern': r'(?i)(PASS(?:WORD)?\s*[=:]\s*[\"\']?)(test123|password|pass123|admin123|temp123|Temp@sila_dev123)([\"\']?)',
        'replacement': lambda m: replace_credential(m, 'password'),
        'description': 'Password in configuration',
        'file_pattern': r'.*\.(env|ini|cfg|conf|yaml|yml|json|toml)$'
    },
    
    # Email in configs
    {
        'pattern': r'(?i)(EMAIL\s*[=:]\s*[\"\']?)[\w.-]+@[\w.-]+\.[A-Za-z]{2,}([\"\']?)',
        'replacement': lambda m: replace_credential(m, 'email'),
        'description': 'Email in configuration',
        'file_pattern': r'.*\.(env|ini|cfg|conf|yaml|yml|json|toml)$'
    },
    
    # Secret keys in config files only
    {
        'pattern': r'(?i)^\s*(SECRET_(?:KEY|TOKEN)|API_?KEY|SECRET_KEY_BASE)\s*[=:]\s*[\"\']?[\w.-]+[\"\']?',
        'replacement': lambda m: replace_credential(m, 'secret_key'),
        'description': 'Secret key or token',
        'file_pattern': r'.*\.(env|ini|cfg|conf|yaml|yml|json|toml)$'
    },
    # Secret keys in Python files (only in variable assignments)
    {
        'pattern': r'(?i)^\s*([A-Z_][A-Z0-9_]*)\s*=\s*[\"\']?[\w.-]+[\"\']?\s*(?:#.*)?$',
        'replacement': lambda m: replace_credential(m, 'secret_key'),
        'description': 'Possible secret key in Python file',
        'file_pattern': r'.*\.py$',
        'validate': lambda m: any(kw in m.group(1).upper() for kw in ['SECRET', 'KEY', 'TOKEN', 'PASSWORD', 'PWD', 'PASS'])
    }
]

# Suspicious patterns to flag (but not replace by default)
SUSPICIOUS_PATTERNS = {
    'email': r'(?i)(?<!\w)([a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,})(?!\w)',
    'password_in_code': r'(?i)(?<![\w-])(password|pwd|secret|key|token)\s*[=:]\s*[\'\"][^\s\'\"]+[\'\"]',
    'ip_address': r'(?<!\d)(?:\d{1,3}\.){3}\d{1,3}(?!\d)',
    'jwt_token': r'eyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*',
    'aws_key': r'(?i)AKIA[0-9A-Z]{16}',
    'aws_secret': r'(?i)(?<![A-Z0-9])[A-Z0-9]{40}(?![A-Z0-9])',
}

# File patterns to include/exclude
INCLUDE_EXTENSIONS = {
    # Config files
    '.env', '.yaml', '.yml', '.json', '.toml', '.ini', '.conf',
    # Source files
    '.py', '.js', '.ts', '.jsx', '.tsx',
    # Documentation
    '.md', '.txt'
}

# Directories to exclude
EXCLUDE_DIRS = {
    '.git', 'node_modules', 'venv', '.venv',
    'build', 'dist', '__pycache__', '.pytest_cache',
    '.mypy_cache', '.pytest_cache', '.tox', 'htmlcov',
    'coverage', '.coverage', '.hypothesis', '.eggs',
    '*.egg-info', '.idea', '.vscode', '.vs', 'venv*',
    'env*', 'ENV*', 'env.bak', 'venv.bak', '*.pyc',
    '*.pyo', '*.pyd', '*.so', '*.dll', '*.dylib',
    '*.class', '*.jar', '*.war', '*.ear', '*.zip',
    '*.tar.gz', '*.tar', '*.exe', '*.dll', '*.obj',
    '*.o', '*.a', '*.lib', '*.so', '*.dylib', '*.ncb',
    '*.sdf', '*.suo', '*.user', '*.userosscache', '*.sln.docstates',
    '*.jfm', '*.pfx', '*.publishsettings', '*.pyproj.user', '*.dbmdl',
    '*.pfx', '*.publishsettings', 'pubspec.lock', '.dart_tool/',
    '.flutter-plugins', '.flutter-plugins-dependencies', '.packages',
    '*.iml', '.gradle', 'local.properties', '.DS_Store', 'Thumbs.db'
}

# File patterns to exclude (glob patterns)
EXCLUDE_PATTERNS = {
    '**/.git/**', '**/node_modules/**', '**/venv/**', '**/.venv/**',
    '**/build/**', '**/dist/**', '**/__pycache__/**', '**/.pytest_cache/**'
}

@dataclass
class FileChange:
    line_number: int
    original: str
    replacement: str

@dataclass
class FileResult:
    path: str
    changes: List[FileChange] = None
    error: Optional[str] = None
    suspicious: List[Tuple[int, str, str]] = None

def is_binary_file(file_path: str) -> bool:
    """Check if a file is binary."""
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            if b'\x00' in chunk:
                return True
        return False
    except Exception:
        return True

def should_skip_file(filepath: str) -> bool:
    """Check if a file should be skipped based on patterns."""
    path = str(filepath).replace('\\', '/')
    
    # Skip files in virtual environments, node_modules, etc.
    if any(part in path.lower() for part in ['/venv/', '/env/', '/.venv/', '/node_modules/', '/.git/', '/.idea/']):
        return True
    
    # Skip binary files
    if any(path.lower().endswith(ext) for ext in [
        '.pyc', '.pyo', '.pyd', '.so', '.dll', '.exe', '.jpg', '.jpeg', 
        '.png', '.gif', '.pdf', '.zip', '.tar', '.gz', '.whl', '.egg',
        '.pyz', '.pyzw', '.pyd', '.pyd', '.pyd', '.pyd', '.pyd', '.pyd'
    ]):
        return True
    
    # Skip non-text files
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(1024)
            # Check for null bytes which indicate binary file
            if b'\x00' in chunk:
                return True
    except Exception:
        return True
        
    return False

def scan_file(filepath: str, dry_run: bool = True) -> FileResult:
    """Scan a file for credentials and replace them if not in dry-run mode."""
    result = FileResult(path=filepath, changes=[], suspicious=[])
    
    try:
        if should_skip_file(filepath) or is_binary_file(filepath):
            return None
            
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            
        original_content = content
        modified_content = content
        
        # Only scan Python files for suspicious patterns, not for credential replacements
        is_python_file = filepath.lower().endswith('.py')
        
        # Check for credential patterns
        for cred_pattern in CREDENTIAL_PATTERNS:
            # Skip patterns that don't match the file pattern
            file_pattern = cred_pattern.get('file_pattern', '.*')
            if not re.match(file_pattern, filepath, re.IGNORECASE):
                continue
                
            pattern = cred_pattern['pattern']
            replacement = cred_pattern['replacement']
            validate = cred_pattern.get('validate', lambda m: True)
            
            # Find all matches first to get line numbers
            for match in re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE):
                if not validate(match):
                    continue
                    
                line_num = content.count('\n', 0, match.start()) + 1
                original = match.group(0)
                
                try:
                    # Apply the replacement
                    new_content = re.sub(
                        pattern,
                        replacement,
                        modified_content,
                        flags=re.IGNORECASE
                    )
                    
                    # If the content changed, record it
                    if new_content != modified_content:
                        modified_content = new_content
                        result.changes.append(FileChange(
                            line_number=line_num,
                            original=original,
                            replacement=match.expand(replacement(match))
                        ))
                        
                except Exception as e:
                    result.error = f"Error applying pattern {pattern}: {str(e)}"
        
        # Check for suspicious patterns
        for pattern_name, pattern in SUSPICIOUS_PATTERNS.items():
            for match in re.finditer(pattern, content, re.IGNORECASE):
                line_num = content.count('\n', 0, match.start()) + 1
                matched_text = match.group(0)
                
                # Skip if this matches any of our credential patterns
                is_credential = False
                for cred_pattern in CREDENTIAL_PATTERNS:
                    if re.search(cred_pattern['pattern'], matched_text, re.IGNORECASE):
                        is_credential = True
                        break
                
                if not is_credential:
                    result.suspicious.append((
                        line_num,
                        pattern_name,
                        matched_text
                    ))
        
        # Write changes if there are actual changes and we're not in dry run mode
        if not dry_run and modified_content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(modified_content)
                
    except Exception as e:
        result.error = str(e)
        
    return result if (result.changes or result.suspicious or result.error) else None

def should_skip_path(path: Path) -> bool:
    """Check if a path should be skipped based on exclusion patterns."""
    path_str = str(path).replace('\\', '/')
    
    # Skip hidden files and directories
    if any(part.startswith('.') and part not in ('.', '..') for part in path.parts):
        return True
    
    # Skip excluded directories and files
    if any(part.lower() in EXCLUDE_DIRS for part in path.parts):
        return True
    
    # Skip files with excluded extensions
    if path.suffix.lower() not in INCLUDE_EXTENSIONS:
        return True
    
    return False

def scan_directory(root_dir: str, dry_run: bool = True) -> List[FileResult]:
    """Scan a directory recursively for credentials."""
    results = []
    root_path = Path(root_dir).resolve()
    
    # First, check specific directories that commonly contain configs
    target_dirs = [
        root_path,
        root_path / 'app',
        root_path / 'config',
        root_path / 'scripts',
        root_path / 'tests'
    ]
    
    # Only include directories that exist
    target_dirs = [d for d in target_dirs if d.exists() and d.is_dir()]
    
    # If no specific directories found, use the root
    if not target_dirs:
        target_dirs = [root_path]
    
    for target_dir in target_dirs:
        for file_path in target_dir.rglob('*'):
            if file_path.is_file() and not should_skip_path(file_path):
                try:
                    result = scan_file(str(file_path), dry_run)
                    if result and (result.changes or result.suspicious or result.error):
                        results.append(result)
                except Exception as e:
                    results.append(FileResult(
                        path=str(file_path),
                        error=str(e),
                        changes=[],
                        suspicious=[]
                    ))
                
    return results

def generate_report(results: List[FileResult], output_file: str = None) -> str:
    """Generate a report of the scan results."""
    report = []
    changed_files = [r for r in results if r.changes]
    suspicious_files = [r for r in results if r.suspicious]
    
    # Summary
    report.append("# Credential Sanitization Report")
    report.append(f"- Files scanned: {len(results)}")
    report.append(f"- Files modified: {len(changed_files)}")
    report.append(f"- Files with suspicious content: {len(suspicious_files)}")
    report.append("")
    
    # Detailed changes
    if changed_files:
        report.append("## Files Modified")
        for file_result in changed_files:
            report.append(f"### {file_result.path}")
            for change in file_result.changes:
                report.append(f"- Line {change.line_number}:")
                report.append(f"  - Original: {change.original}")
                report.append(f"  - Changed:  {change.replacement}")
            report.append("")
    
    # Suspicious content
    if suspicious_files:
        report.append("## Suspicious Content Found")
        report.append("The following patterns were found that might need attention:")
        for file_result in suspicious_files:
            report.append(f"### {file_result.path}")
            for line_num, pattern_name, content in file_result.suspicious:
                report.append(f"- Line {line_num}: {pattern_name} - {content}")
    
    # Errors
    error_files = [r for r in results if r.error]
    if error_files:
        report.append("## Errors")
        for file_result in error_files:
            report.append(f"- {file_result.path}: {file_result.error}")
    
    report_text = "\n".join(report)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_text)
    
    return report_text

def main():
    parser = argparse.ArgumentParser(description='Scan and sanitize credentials in project files.')
    parser.add_argument('path', nargs='?', default='.', help='Directory to scan (default: current directory)')
    parser.add_argument('--dry-run', action='store_true', help='Run without making changes')
    parser.add_argument('--output', '-o', help='Output report file (default: print to console)')
    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        print(f"Error: Path '{args.path}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    print(f"Scanning directory: {os.path.abspath(args.path)}")
    print(f"Mode: {'Dry run (no changes will be made)' if args.dry_run else 'Live (changes will be made)'}")
    
    results = scan_directory(args.path, dry_run=args.dry_run)
    report = generate_report(results, args.output)
    
    if args.output:
        print(f"\nReport saved to: {os.path.abspath(args.output)}")
    else:
        print("\n" + "="*80)
        print(report)
    
    print("\nScan complete!")

if __name__ == '__main__':
    main()
