#!/usr/bin/env python3
"""
Module Tree Visualization Script
Generates a clean tree structure of the modules directory.
"""

import os
from pathlib import Path

# 🧹 Patterns to ignore
IGNORED_NAMES = {
    '__pycache__', '.git', '.vscode', '.idea', 'node_modules', 'dist', 'build',
    '.cache', '.pytest_cache', '.venv', 'env', 'venv', 'docs/_build', 'docgen',
    'Thumbs.db', '.DS_Store', 'desktop.ini'
}
IGNORED_EXTENSIONS = {
    '.log', '.tmp', '.bak', '.swp', '.db', '.pyc'
}
IGNORED_FILES = {
    '.env', '.env.local', '.env.test', '.gitignore', '.gitattributes'
}

def format_size(size_bytes):
    """Format file size in human-readable format."""
    for unit in ['B','KB','MB','GB','TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"

def should_ignore(name):
    """Check if a file or directory should be ignored."""
    if name in IGNORED_NAMES or name in IGNORED_FILES:
        return True
    _, ext = os.path.splitext(name)
    return ext in IGNORED_EXTENSIONS

def print_tree(path, prefix=""):
    """Print directory tree with file sizes."""
    total_size = 0
    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        print(f"{prefix}⚠️ Permissão negada: {path}")
        return 0

    filtered = [e for e in entries if not should_ignore(e)]
    for i, entry in enumerate(filtered):
        full_path = os.path.join(path, entry)
        connector = "└── " if i == len(filtered) - 1 else "├── "
        if os.path.isdir(full_path):
            print(f"{prefix}{connector}{entry}/")
            size = print_tree(full_path, prefix + ("    " if i == len(filtered) - 1 else "│   "))
            total_size += size
        else:
            try:
                size = os.path.getsize(full_path)
                print(f"{prefix}{connector}{entry} ({format_size(size)})")
                total_size += size
            except OSError:
                print(f"{prefix}{connector}{entry} ⚠️ [Erro ao obter tamanho]")
    return total_size

def show():
    """Show the modules tree structure."""
    backend_dir = Path(__file__).parent.parent.parent / "backend"
    root_folder = backend_dir / "app" / "modules"
    
    if not root_folder.exists():
        print(f"❌ Modules directory not found: {root_folder}")
        return False
    
    print(f"\n📁 Estrutura de: {root_folder}/\n")
    total = print_tree(str(root_folder))
    print(f"\n📦 Tamanho total (curado): {format_size(total)}")
    
    return True

def main():
    """Main function for command-line usage."""
    success = show()
    return success

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)