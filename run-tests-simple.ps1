# Run-Tests-Simple.ps1
# Simplified test runner for SILA system

# Set console output encoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['*:Encoding'] = 'utf8'
$ErrorActionPreference = 'Stop'

try {
    # Print header
    Write-Host "`n[INFO] Starting SILA System Tests..." -ForegroundColor Cyan
    
    # Define paths
    $venvPath = "$PSScriptRoot\backend\venv"
    $backendScript = "$PSScriptRoot\backend\run-tests.ps1"
    
    # Verify paths
    if (-not (Test-Path $venvPath)) {
        throw "Virtual environment not found at: $venvPath"
    }
    
    if (-not (Test-Path $backendScript)) {
        throw "Backend test script not found at: $backendScript"
    }
    
    # Activate virtual environment
    $activateScript = "$venvPath\Scripts\Activate.ps1"
    if (-not (Test-Path $activateScript)) {
        throw "Activation script not found at: $activateScript"
    }
    
    Write-Host "[INFO] Activating virtual environment..." -ForegroundColor Yellow
    & $activateScript
    
    if (-not $?) {
        throw "Failed to activate virtual environment"
    }
    
    # Change to backend directory and run tests
    $backendDir = Split-Path -Parent $backendScript
    Push-Location $backendDir
    
    try {
        Write-Host "[INFO] Running backend tests..." -ForegroundColor Cyan
        & $backendScript
        
        if ($LASTEXITCODE -ne 0) {
            throw "Tests failed with exit code $LASTEXITCODE"
        }
        
        Write-Host "`n[SUCCESS] All tests passed!" -ForegroundColor Green
    }
    finally {
        Pop-Location
    }
}
catch {
    Write-Host "`n[ERROR] $_" -ForegroundColor Red
    if ($_.ScriptStackTrace) {
        Write-Host "Stack Trace:" -ForegroundColor DarkGray
        Write-Host $_.ScriptStackTrace -ForegroundColor DarkGray
    }
    exit 1
}

exit 0

