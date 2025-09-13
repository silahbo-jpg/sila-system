#!/bin/bash
set -euo pipefail

# Get the correct base directory
BASE_DIR="$(dirname "$(dirname "$0")")"
BACKEND_DIR="$BASE_DIR/backend"
APP_DIR="$BACKEND_DIR/app"

echo "🔍 Running pre-deployment validation..."
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

# Validate environment file in backend directory
ENV_FILE="$BACKEND_DIR/.env"
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ .env file missing at: $ENV_FILE"
    exit 1
fi

# Check database connection using backend directory
cd "$BACKEND_DIR"
if [ -f ".env" ]; then
    source .env
fi

# Test database connection
if [ -z "${DATABASE_URL:-}" ]; then
    echo "❌ DATABASE_URL not found in environment"
    exit 1
fi

echo "Testing database connection..."
if ! python -c "
import os
import psycopg2
try:
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    print('✅ Database connection successful')
except Exception as e:
    print(f'❌ Database connection failed: {e}')
    exit(1)
"; then
    exit 1
fi

echo "✅ Pre-deployment validation passed"