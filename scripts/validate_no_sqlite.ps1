# scripts/validate_no_sqlite.ps1
$ErrorActionPreference = "Stop"

Write-Host "🔍 Validating no SQLite contamination..." -ForegroundColor Cyan

# Get the correct base path (sila-system directory)
$basePath = Split-Path $PSScriptRoot -Parent
$backendPath = Join-Path $basePath "backend"
$appPath = Join-Path $backendPath "app"

Write-Host "Base path: $basePath"
Write-Host "Backend path: $backendPath" 
Write-Host "App path: $appPath"

# Check if backend directory exists
if (-not (Test-Path $backendPath)) {
    Write-Host "❌ Backend directory not found at: $backendPath" -ForegroundColor Red
    exit 1
}

# Check if app directory exists within backend
if (-not (Test-Path $appPath)) {
    Write-Host "❌ App directory not found at: $appPath" -ForegroundColor Red
    exit 1
}

# Check for SQLite contamination in the correct app directory
Write-Host "Checking for SQLite contamination in: $appPath" -ForegroundColor Yellow
$sqliteMatches = Get-ChildItem -Path $appPath -Recurse -Include *.py, *.sh, *.env |
    Select-String -Pattern "sqlite" -CaseSensitive

if ($sqliteMatches) {
    Write-Host "❌ SQLite contamination detected!" -ForegroundColor Red
    $sqliteMatches | ForEach-Object { Write-Host "Found in: $($_.Path)" -ForegroundColor Red }
    exit 1
}

Write-Host "✅ No SQLite contamination found" -ForegroundColor Green