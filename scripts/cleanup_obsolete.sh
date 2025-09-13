#!/bin/bash
set -euo pipefail

echo "🧹 Cleaning up obsolete files and references..."
echo "=============================================="

# Remove any SQLite database files
find . -name "*.db" -o -name "*.sqlite" -o -name "*.sqlite3" | grep -v ".git" | grep -v "node_modules" | grep -v "venv" | xargs -r rm

# Remove any SQLite-related configuration files
find . -name "*sqlite*" | grep -v ".git" | grep -v "node_modules" | grep -v "venv" | xargs -r rm

# Clean up any temporary files
find . -name "*.tmp" -o -name "*.temp" | grep -v ".git" | grep -v "node_modules" | grep -v "venv" | xargs -r rm

echo "✅ Obsolete file cleanup completed"