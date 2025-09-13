# scripts/pre_deploy_check.ps1
$ErrorActionPreference = "Stop"

Write-Host "Running pre-deployment validation..." -ForegroundColor Cyan

# Get the correct base path (sila-system directory)
$basePath = Split-Path $PSScriptRoot -Parent
$backendPath = Join-Path $basePath "backend"
$appPath = Join-Path $backendPath "app"

Write-Host "Base path: $basePath"
Write-Host "Backend path: $backendPath" 
Write-Host "App path: $appPath"

# Check if backend directory exists
if (-not (Test-Path $backendPath)) {
    Write-Host "ERROR: Backend directory not found at: $backendPath" -ForegroundColor Red
    exit 1
}

# Check if app directory exists within backend
if (-not (Test-Path $appPath)) {
    Write-Host "ERROR: App directory not found at: $appPath" -ForegroundColor Red
    exit 1
}

# Check for SQLite contamination in the correct app directory
Write-Host "Checking for SQLite contamination in: $appPath" -ForegroundColor Yellow
$sqliteMatches = Get-ChildItem -Path $appPath -Recurse -Include *.py, *.sh, *.env |
    Select-String -Pattern "sqlite" -CaseSensitive

if ($sqliteMatches) {
    Write-Host "ERROR: SQLite contamination detected!" -ForegroundColor Red
    $sqliteMatches | ForEach-Object { Write-Host "Found in: $($_.Path)" -ForegroundColor Red }
    exit 1
}

# Validate environment file in backend directory
$envFile = Join-Path $backendPath ".env"
if (-not (Test-Path $envFile)) {
    Write-Host "ERROR: .env file missing at: $envFile" -ForegroundColor Red
    exit 1
}

# Check database connection using backend directory
Set-Location $backendPath
if (Test-Path ".env") {
    # Load environment variables
    Get-Content .env | ForEach-Object {
        if ($_ -match "^\s*([^#][^=]+)=(.*)") {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim()
            [Environment]::SetEnvironmentVariable($name, $value)
        }
    }
}

# Test database connection
try {
    $dbUrl = [Environment]::GetEnvironmentVariable("DATABASE_URL")
    if (-not $dbUrl) {
        Write-Host "ERROR: DATABASE_URL not found in environment" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "Testing database connection..." -ForegroundColor Yellow
    python -c "
import os
import psycopg2
try:
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    print('Database connection successful')
except Exception as e:
    print(f'Database connection failed: {e}')
    exit(1)
"
} catch {
    Write-Host "ERROR: Database connection test failed: $_" -ForegroundColor Red
    exit 1
}

Write-Host "Pre-deployment validation passed" -ForegroundColor Green