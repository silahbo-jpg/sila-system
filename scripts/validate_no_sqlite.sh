#!/bin/bash
set -euo pipefail

# Get the correct base directory
BASE_DIR="$(dirname "$(dirname "$0")")"
BACKEND_DIR="$BASE_DIR/backend"
APP_DIR="$BACKEND_DIR/app"

echo "🔍 Validating no SQLite contamination..."
echo "Base path: $BASE_DIR"
echo "Backend path: $BACKEND_DIR"
echo "App path: $APP_DIR"

# Check if backend directory exists
if [ ! -d "$BACKEND_DIR" ]; then
    echo "❌ Backend directory not found at: $BACKEND_DIR"
    exit 1
fi

# Check if app directory exists within backend
if [ ! -d "$APP_DIR" ]; then
    echo "❌ App directory not found at: $APP_DIR"
    exit 1
fi

# Check for SQLite contamination in the correct app directory
echo "Checking for SQLite contamination in: $APP_DIR"
if grep -r "sqlite" --include="*.py" --include="*.sh" --include="*.env" "$APP_DIR/" | grep -v "validate_no_sqlite"; then
    echo "❌ SQLite contamination detected!"
    exit 1
fi

echo "✅ No SQLite contamination found"