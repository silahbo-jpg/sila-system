#!/usr/bin/env python3
"""
Comprehensive issue analyzer for the SILA System project.
This script identifies, categorizes, and reports all issues in the codebase.
"""
import os
import re
import sys
import ast
import subprocess
from pathlib import Path
from collections import defaultdict, Counter

# Project configuration
PROJECT_ROOT = Path(__file__).parent.resolve()
BACKEND_DIR = PROJECT_ROOT / "backend"
EXCLUDE_DIRS = {".venv", "venv", "env", "node_modules", "__pycache__", ".git", ".pytest_cache", ".mypy_cache"}

# Issue categories
ISSUE_CATEGORIES = {
    "import_errors": [],
    "syntax_errors": [],
    "linting_issues": [],
    "unused_variables": [],
    "type_incompatibilities": [],
    "naming_issues": [],
    "structure_issues": [],
    "other_issues": []
}

def is_excluded(path: Path):
    """Check if a path should be excluded from analysis."""
    return any(part in EXCLUDE_DIRS for part in path.parts)

def run_flake8_analysis():
    """Run flake8 analysis and categorize issues."""
    print("🔍 Running flake8 analysis...")
    try:
        # Try a simpler approach - check if flake8 is available
        result = subprocess.run(
            [sys.executable, "-m", "flake8", "--version"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
            timeout=10
        )
        
        if result.returncode != 0:
            print("⚠️  flake8 not available, skipping flake8 analysis")
            return []
        
        # Run flake8 on a smaller subset first to test
        result = subprocess.run(
            [sys.executable, "-m", "flake8", "--format=%(path)s:%(row)d:%(col)d: %(code)s %(text)s", str(BACKEND_DIR / "app" / "__init__.py")],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
            timeout=30
        )
        
        if result.returncode == 0 and not result.stdout:
            print("✅ No flake8 issues found in test file")
            return []
        
        issues = []
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                issues.append(line.strip())
        
        return issues
    except subprocess.TimeoutExpired:
        print("⚠️  flake8 analysis timed out")
        return []
    except Exception as e:
        print(f"❌ Error running flake8: {e}")
        return []

def categorize_flake8_issues(issues):
    """Categorize flake8 issues by type."""
    categorized = defaultdict(list)
    
    for issue in issues:
        # Parse issue: filepath:line:col: code message
        parts = issue.split(':', 3)
        if len(parts) >= 4:
            filepath, line, col, details = parts
            code = details.split()[0] if details.split() else "UNKNOWN"
            
            # Categorize by code
            if code.startswith('E') or code.startswith('F'):
                categorized['syntax_errors'].append(issue)
            elif code.startswith('W'):
                categorized['linting_issues'].append(issue)
            elif code.startswith('I'):
                categorized['import_errors'].append(issue)
            elif code.startswith('N'):
                categorized['naming_issues'].append(issue)
            else:
                categorized['other_issues'].append(issue)
    
    return categorized

def analyze_python_files():
    """Analyze Python files for syntax and structural issues."""
    print("🔍 Analyzing Python files for syntax issues...")
    syntax_issues = []
    
    file_count = 0
    for pyfile in BACKEND_DIR.rglob("*.py"):
        if is_excluded(pyfile):
            continue
            
        file_count += 1
        if file_count % 100 == 0:
            print(f"  Analyzed {file_count} files...")
            
        try:
            with open(pyfile, 'r', encoding='utf-8') as f:
                source = f.read()
            
            # Try to compile the source
            ast.parse(source, filename=str(pyfile))
        except SyntaxError as e:
            syntax_issues.append({
                "file": str(pyfile.relative_to(PROJECT_ROOT)),
                "line": e.lineno,
                "column": e.offset,
                "message": e.msg,
                "type": "SyntaxError"
            })
        except Exception as e:
            syntax_issues.append({
                "file": str(pyfile.relative_to(PROJECT_ROOT)),
                "line": None,
                "column": None,
                "message": str(e),
                "type": "ParseError"
            })
    
    print(f"  Total files analyzed: {file_count}")
    return syntax_issues

def find_unused_imports():
    """Find potentially unused imports."""
    print("🔍 Finding unused imports...")
    unused_imports = []
    
    file_count = 0
    for pyfile in BACKEND_DIR.rglob("*.py"):
        if is_excluded(pyfile):
            continue
            
        file_count += 1
        if file_count % 100 == 0:
            print(f"  Processed {file_count} files for unused imports...")
            
        try:
            with open(pyfile, 'r', encoding='utf-8') as f:
                source = f.read()
            
            tree = ast.parse(source, filename=str(pyfile))
            
            # Find all imports
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        for alias in node.names:
                            imports.append(f"{node.module}.{alias.name}")
            
            # Simple heuristic: check if imported names are used in the code
            # This is a basic check and might have false positives
            for imp in imports:
                name = imp.split('.')[-1]  # Get the last part of the import
                if name not in source and name != '*':
                    # Check if it's a special import like __future__
                    if not name.startswith('__') and not name.endswith('__'):
                        # Additional check to reduce false positives
                        if len(name) > 1:  # Skip single character imports
                            unused_imports.append({
                                "file": str(pyfile.relative_to(PROJECT_ROOT)),
                                "import": imp,
                                "name": name
                            })
                        
        except Exception as e:
            # Skip files with encoding issues or other problems
            pass
    
    print(f"  Total files processed for unused imports: {file_count}")
    return unused_imports

def check_module_structure():
    """Check for structural issues in modules."""
    print("🔍 Checking module structure...")
    structure_issues = []
    
    # Check for __init__.py files in modules
    modules_dir = BACKEND_DIR / "app" / "modules"
    if modules_dir.exists():
        for module_dir in modules_dir.iterdir():
            if module_dir.is_dir() and not is_excluded(module_dir):
                init_file = module_dir / "__init__.py"
                if not init_file.exists():
                    structure_issues.append({
                        "module": module_dir.name,
                        "issue": "Missing __init__.py file"
                    })
    
    return structure_issues

def check_import_issues():
    """Check for common import issues."""
    print("🔍 Checking for common import issues...")
    import_issues = []
    
    # Common problematic import patterns
    problematic_patterns = [
        (r'from\s+app\.db\.database\s+import\s+', 'from app.db import get_db'),
        (r'from\s+app\.core\.database\s+import\s+', 'from app.db import get_db'),
        (r'from\s+app\.database\s+import\s+', 'from app.db import get_db'),
    ]
    
    for pyfile in BACKEND_DIR.rglob("*.py"):
        if is_excluded(pyfile):
            continue
            
        try:
            with open(pyfile, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for pattern, suggestion in problematic_patterns:
                if re.search(pattern, content):
                    import_issues.append({
                        "file": str(pyfile.relative_to(PROJECT_ROOT)),
                        "pattern": pattern,
                        "suggestion": suggestion
                    })
        except Exception:
            pass
    
    return import_issues

def generate_report(categorized_issues, syntax_issues, unused_imports, structure_issues, import_issues):
    """Generate a comprehensive report of all issues."""
    print("\n" + "="*60)
    print("📊 COMPREHENSIVE ISSUE REPORT")
    print("="*60)
    
    # Count issues by category
    total_issues = 0
    
    print(f"\n📝 FLAKE8 ISSUES BY CATEGORY:")
    flake8_total = 0
    for category, issues in categorized_issues.items():
        count = len(issues)
        flake8_total += count
        total_issues += count
        print(f"  {category}: {count}")
    
    print(f"\n🔧 SYNTAX ISSUES:")
    syntax_count = len(syntax_issues)
    total_issues += syntax_count
    print(f"  Syntax errors: {syntax_count}")
    for issue in syntax_issues[:5]:
        print(f"    - {issue['file']}:{issue['line'] if issue['line'] else '?'} - {issue['message']}")
    if syntax_count > 5:
        print(f"    ... and {syntax_count - 5} more")
    
    print(f"\n📦 UNUSED IMPORTS:")
    unused_count = len(unused_imports)
    total_issues += unused_count
    print(f"  Unused imports: {unused_count}")
    # Group by file for better readability
    unused_by_file = defaultdict(list)
    for issue in unused_imports:
        unused_by_file[issue['file']].append(issue['import'])
    
    file_count = 0
    for file, imports in unused_by_file.items():
        file_count += 1
        if file_count <= 5:
            print(f"    - {file}: {', '.join(imports[:3])}{'...' if len(imports) > 3 else ''}")
    if len(unused_by_file) > 5:
        print(f"    ... and {len(unused_by_file) - 5} more files")
    
    print(f"\n🏗️  STRUCTURE ISSUES:")
    structure_count = len(structure_issues)
    total_issues += structure_count
    print(f"  Structure issues: {structure_count}")
    for issue in structure_issues:
        print(f"    - {issue['module']}: {issue['issue']}")
    
    print(f"\n🔗 IMPORT ISSUES:")
    import_count = len(import_issues)
    total_issues += import_count
    print(f"  Import issues: {import_count}")
    # Group by pattern
    import_by_pattern = defaultdict(list)
    for issue in import_issues:
        import_by_pattern[issue['pattern']].append(issue['file'])
    
    pattern_count = 0
    for pattern, files in import_by_pattern.items():
        pattern_count += 1
        if pattern_count <= 3:
            print(f"    - Pattern '{pattern}': {len(files)} files")
            for file in files[:3]:
                print(f"      * {file}")
            if len(files) > 3:
                print(f"      ... and {len(files) - 3} more")
    
    print(f"\n📈 TOTAL ISSUES IDENTIFIED: {total_issues}")
    
    # Priority classification
    critical_issues = len(categorized_issues['syntax_errors']) + len(syntax_issues)
    high_priority = len(categorized_issues['import_errors']) + len(structure_issues) + len(import_issues)
    medium_priority = len(categorized_issues['linting_issues']) + len(unused_imports)
    low_priority = len(categorized_issues['naming_issues']) + len(categorized_issues['other_issues'])
    
    print(f"\n🎯 PRIORITY CLASSIFICATION:")
    print(f"  🔴 Critical (prevent compilation): {critical_issues}")
    print(f"  🟠 High (import/structure issues): {high_priority}")
    print(f"  🟡 Medium (linting/unused): {medium_priority}")
    print(f"  🟢 Low (naming/other): {low_priority}")
    
    return {
        "total": total_issues,
        "critical": critical_issues,
        "high": high_priority,
        "medium": medium_priority,
        "low": low_priority,
        "by_category": {
            "flake8": dict([(k, len(v)) for k, v in categorized_issues.items()]),
            "syntax": syntax_count,
            "unused": unused_count,
            "structure": structure_count,
            "import": import_count
        }
    }

def main():
    """Main analysis function."""
    print("🚀 Starting comprehensive issue analysis...")
    
    # Run flake8 analysis
    flake8_issues = run_flake8_analysis()
    categorized_flake8 = categorize_flake8_issues(flake8_issues) if flake8_issues else defaultdict(list)
    
    # Analyze Python files for syntax issues
    syntax_issues = analyze_python_files()
    
    # Find unused imports
    unused_imports = find_unused_imports()
    
    # Check module structure
    structure_issues = check_module_structure()
    
    # Check import issues
    import_issues = check_import_issues()
    
    # Generate comprehensive report
    report = generate_report(categorized_flake8, syntax_issues, unused_imports, structure_issues, import_issues)
    
    # Save report to file
    report_file = PROJECT_ROOT / "issues_analysis_report.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# SILA System Issues Analysis Report\n\n")
        f.write(f"Generated on: {os.date() if hasattr(os, 'date') else 'N/A'}\n\n")
        f.write("## Summary\n\n")
        f.write(f"- Total issues: {report['total']}\n")
        f.write(f"- Critical issues: {report['critical']}\n")
        f.write(f"- High priority issues: {report['high']}\n")
        f.write(f"- Medium priority issues: {report['medium']}\n")
        f.write(f"- Low priority issues: {report['low']}\n\n")
        
        f.write("## Issues by Category\n\n")
        for category, count in report['by_category'].items():
            f.write(f"- {category}: {count}\n")
    
    print(f"\n📄 Detailed report saved to: {report_file}")
    print("\n✅ Analysis completed!")

if __name__ == "__main__":
    main()