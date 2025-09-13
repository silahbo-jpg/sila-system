# scripts/deploy_backend.ps1
$ErrorActionPreference = "Stop"

# Get the correct base directory
$baseDir = Split-Path $PSScriptRoot -Parent
$backendDir = Join-Path $baseDir "backend"

Write-Host "🚀 Starting backend deployment" -ForegroundColor Green
Write-Host "Base directory: $baseDir" -ForegroundColor Cyan
Write-Host "Backend directory: $backendDir" -ForegroundColor Cyan

# Validate required paths
$requiredPaths = @("backend", "backend/app", "backend/prisma")
foreach ($path in $requiredPaths) {
    $fullPath = Join-Path $baseDir $path
    if (-not (Test-Path $fullPath)) {
        Write-Host "❌ Required path not found: $fullPath" -ForegroundColor Red
        exit 1
    }
}

$LogDir = Join-Path $backendDir "deploy_logs"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$LogFile = Join-Path $LogDir "deploy_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"

Start-Transcript -Path $LogFile

# Pre-deployment check
$preDeployScript = Join-Path $baseDir "scripts\pre_deploy_check.ps1"
if (Test-Path $preDeployScript) {
    & $preDeployScript
} else {
    Write-Host "❌ Pre-deployment check script not found at: $preDeployScript" -ForegroundColor Red
    exit 1
}

Set-Location $backendDir

# Virtual environment
$venvPath = Join-Path $backendDir "venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
} else {
    Write-Host "❌ Virtual environment activation script not found at: $activateScript" -ForegroundColor Red
    exit 1
}

# Dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip
pip install -r requirements.txt

# Prisma
Write-Host "🔧 Validating Prisma schema..." -ForegroundColor Yellow
npx prisma validate
npx prisma generate

# Migrations
Write-Host "📊 Applying migrations..." -ForegroundColor Yellow
try {
    npx prisma migrate deploy
    Write-Host "✅ Migrations applied" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Migrate deploy failed, trying migrate dev..." -ForegroundColor Yellow
    npx prisma migrate dev --name automated_migration
}

# Start server
Write-Host "🌐 Starting server..." -ForegroundColor Yellow
$uvicornLog = Join-Path $LogDir "uvicorn.log"
$uvicornErr = Join-Path $LogDir "uvicorn.err"

$process = Start-Process -FilePath "python" `
    -ArgumentList "-m uvicorn app.main:app --host 0.0.0.0 --port 8000" `
    -RedirectStandardOutput $uvicornLog `
    -RedirectStandardError $uvicornErr `
    -PassThru

Start-Sleep -Seconds 5

# Health check
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Server started successfully" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Server failed to start" -ForegroundColor Red
    Write-Host "🔍 Check logs: $uvicornLog" -ForegroundColor Yellow
    exit 1
}

Write-Host "🎉 Deployment completed!" -ForegroundColor Green
Write-Host "📋 Deployment log: $LogFile" -ForegroundColor Cyan
Write-Host "📊 Server logs: $uvicornLog" -ForegroundColor Cyan
Write-Host "🌐 Server running on: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📊 API documentation: http://localhost:8000/docs" -ForegroundColor Cyan
Stop-Transcript
}