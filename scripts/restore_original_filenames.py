#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Restore Original Filenames Script

This script restores the original filenames of files that were previously
renamed by the fix-corrupted-filenames.ps1 script.
"""

import os
import re
import sys
from pathlib import Path

def find_corrupted_files():
    """Find all files with corrupted names in the project."""
    corrupted_patterns = [
        (r'^n+otifications?\.py$', 'notifications.py'),
        (r'^n+otificacoes?\.py$', 'notificacoes.py'),
        (r'^n+otifica[dt]or(?:_service)?\.py$', lambda x: re.sub(r'^n+', '', x)),
        (r'^test_n+otifications?\.py$', lambda x: 'test_' + re.sub(r'^test_n+', '', x)),
        (r'^fix-n+otification-files\.py$', 'fix-notification-files.py'),
        (r'^restore_n+otification_filenames\.py$', 'restore_notification_filenames.py'),
    ]
    
    project_sila_dev-system = Path(__file__).parent.parent
    corrupted_files = []
    
    for file_path in project_sila_dev-system.rglob('*'):
        if file_path.is_file():
            filename = file_path.name
            for pattern, replacement in corrupted_patterns:
                if re.search(pattern, filename, re.IGNORECASE):
                    if callable(replacement):
                        new_name = replacement(filename)
                    else:
                        new_name = replacement
                    corrupted_files.append((file_path, file_path.parent / new_name))
                    break
    
    return corrupted_files

def restore_filenames():
    """Restore original filenames for all corrupted files."""
    corrupted_files = find_corrupted_files()
    
    if not corrupted_files:
        print("No corrupted filenames found to restore.")
        return 0
    
    print(f"Found {len(corrupted_files)} files to restore:")
    for old_path, new_path in corrupted_files:
        print(f"  - {old_path.name} -> {new_path.name}")
    
    print("\nProceeding with filename restoration...")
    
    success_count = 0
    for old_path, new_path in corrupted_files:
        try:
            old_path.rename(new_path)
            print(f"Restored: {old_path.name} -> {new_path.name}")
            success_count += 1
        except Exception as e:
            print(f"Error restoring {old_path}: {str(e)}")
    
    print(f"\nSuccessfully restored {success_count} out of {len(corrupted_files)} files.")
    return 0

if __name__ == "__main__":
    sys.exit(restore_filenames())


