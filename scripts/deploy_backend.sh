#!/bin/bash
set -euo pipefail

# Get the correct base directory
BASE_DIR="$(dirname "$(dirname "$0")")"
BACKEND_DIR="$BASE_DIR/backend"

echo "🚀 Starting backend deployment - $(date)"
echo "Base directory: $BASE_DIR"
echo "Backend directory: $BACKEND_DIR"
echo "========================================"

# Validate required paths
REQUIRED_PATHS=("backend" "backend/app" "backend/prisma")
for path in "${REQUIRED_PATHS[@]}"; do
    FULL_PATH="$BASE_DIR/$path"
    if [ ! -d "$FULL_PATH" ]; then
        echo "❌ Required path not found: $FULL_PATH"
        exit 1
    fi
done

cd "$BACKEND_DIR"

LOG_DIR="deploy_logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/deploy_$(date +%Y%m%d_%H%M%S).log"

exec > >(tee -a "$LOG_FILE") 2>&1

# Run pre-deployment check
PRE_DEPLOY_SCRIPT="$BASE_DIR/scripts/pre_deploy_check.sh"
if [ -f "$PRE_DEPLOY_SCRIPT" ]; then
    "$PRE_DEPLOY_SCRIPT"
else
    echo "❌ Pre-deployment check script not found at: $PRE_DEPLOY_SCRIPT"
    exit 1
fi

# Setup virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Validate Prisma schema
echo "🔧 Validating Prisma schema..."
npx prisma validate
npx prisma generate

# Apply migrations
echo "📊 Applying database migrations..."
if npx prisma migrate deploy; then
    echo "✅ Migrations applied successfully"
else
    echo "⚠️ Migrate deploy failed, trying migrate dev..."
    npx prisma migrate dev --name automated_migration
fi

# Start server
echo "🌐 Starting server..."
nohup python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > "$LOG_DIR/uvicorn.log" 2>&1 &
SERVER_PID=$!

# Wait for server to start
echo "⏳ Waiting for server to start..."
sleep 5

# Health check
if curl -f http://localhost:8000/health >/dev/null 2>&1; then
    echo "✅ Server started successfully (PID: $SERVER_PID)"
    echo "📊 Server logs: $LOG_DIR/uvicorn.log"
else
    echo "❌ Server failed to start"
    echo "🔍 Check logs: $LOG_DIR/uvicorn.log"
    exit 1
fi

# Test critical endpoints
echo "🧪 Testing critical endpoints..."
ENDPOINTS=("/health" "/api/protocols" "/api/auth/login")
for endpoint in "${ENDPOINTS[@]}"; do
    if curl -s http://localhost:8000$endpoint | grep -q "error\|404\|500"; then
        echo "❌ Endpoint $endpoint failed"
        exit 1
    else
        echo "✅ $endpoint responding correctly"
    fi
done

echo "========================================"
echo "🎉 Deployment completed successfully!"
echo "📋 Deployment log: $LOG_FILE"
echo "🌐 Server running on: http://localhost:8000"
echo "📊 API documentation: http://localhost:8000/docs"