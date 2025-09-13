# SILA System Startup Script
# This script starts the SILA backend with proper configuration

param (
    [string]$env = "development",
    [switch]$reload = $true,
    [int]$workers = 1,
    [string]$hostname = "0.0.0.0",
    [int]$port = 8000
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Set environment variables
$env:ENVIRONMENT = $env

# Check if running in development mode
$isDev = $env -eq "development"
$reloadFlag = if ($isDev -and $reload) { "--reload" } else { "" }

# Build the command
$command = "uvicorn app.main:app --host $hostname --port $port $reloadFlag"

# Add workers if not in development mode
if (-not $isDev) {
    $command += " --workers $workers"
}

# Add environment info
Write-Host "Starting SILA System API..." -ForegroundColor Cyan
Write-Host "Environment: $env" -ForegroundColor Cyan
Write-Host "Host: $($hostname):$port" -ForegroundColor Cyan
if ($isDev) {
    Write-Host "Development mode: Enabled" -ForegroundColor Yellow
    Write-Host "Auto-reload: $($reload ? 'Enabled' : 'Disabled')" -ForegroundColor Yellow
} else {
    Write-Host "Workers: $workers" -ForegroundColor Cyan
}
Write-Host ""

# Start the application
Write-Host "Starting server with command:" -ForegroundColor Cyan
Write-Host "$command" -ForegroundColor DarkCyan
Write-Host ""

Invoke-Expression $command

