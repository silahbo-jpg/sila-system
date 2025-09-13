# Test script to verify path resolution
Write-Host "Testing path resolution..." -ForegroundColor Green

# Get the correct base path (sila-system directory)
$basePath = Split-Path $PSScriptRoot -Parent
$backendPath = Join-Path $basePath "backend"
$appPath = Join-Path $backendPath "app"

Write-Host "Base path: $basePath"
Write-Host "Backend path: $backendPath" 
Write-Host "App path: $appPath"

# Check if directories exist
if (Test-Path $basePath) {
    Write-Host "Base path exists: OK" -ForegroundColor Green
} else {
    Write-Host "Base path does not exist: ERROR" -ForegroundColor Red
}

if (Test-Path $backendPath) {
    Write-Host "Backend path exists: OK" -ForegroundColor Green
} else {
    Write-Host "Backend path does not exist: ERROR" -ForegroundColor Red
}

if (Test-Path $appPath) {
    Write-Host "App path exists: OK" -ForegroundColor Green
} else {
    Write-Host "App path does not exist: ERROR" -ForegroundColor Red
}

# List some files in the app directory to verify it's correct
if (Test-Path $appPath) {
    Write-Host "Contents of app directory:" -ForegroundColor Yellow
    Get-ChildItem $appPath -Directory | Select-Object -First 5 | ForEach-Object {
        Write-Host "  $($_.Name)" -ForegroundColor Yellow
    }
}