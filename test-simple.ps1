# Test-Simple.ps1 - Minimal test script

# Set encoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['*:Encoding'] = 'utf8'

try {
    Write-Host "`n=== Starting SILA Test ===" -ForegroundColor Cyan
    
    # 1. Check Python
    Write-Host "`n[1/3] Checking Python..." -ForegroundColor Yellow
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found or not in PATH"
    }
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
    
    # 2. Check virtual environment
    Write-Host "`n[2/3] Checking virtual environment..." -ForegroundColor Yellow
    $venvPath = ".\backend\venv"
    if (-not (Test-Path $venvPath)) {
        throw "Virtual environment not found at: $venvPath"
    }
    Write-Host "✅ Virtual environment found" -ForegroundColor Green
    
    # 3. Run a simple Python command
    Write-Host "`n[3/3] Running test command..." -ForegroundColor Yellow
    $testCmd = "import sys; print(f'Python {sys.version}')"
    python -c $testCmd
    
    if ($LASTEXITCODE -ne 0) {
        throw "Test command failed with exit code $LASTEXITCODE"
    }
    
    Write-Host "`n✅ Basic tests completed successfully!" -ForegroundColor Green
}
catch {
    Write-Host "`n❌ Error: $_" -ForegroundColor Red
    if ($_.ScriptStackTrace) {
        Write-Host "`nStack Trace:" -ForegroundColor DarkGray
        Write-Host $_.ScriptStackTrace -ForegroundColor DarkGray
    }
    exit 1
}

exit 0

