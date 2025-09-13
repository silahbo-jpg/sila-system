# Run-Tests.ps1 - SILA System Test Orchestrator
# Executes backend test suite with UTF-8 support, logging, and error handling

# ─── Encoding & Error Preferences ─────────────────────────────────────────────
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['*:Encoding'] = 'utf8'
$ErrorActionPreference = 'Stop'

# ─── Configuration ────────────────────────────────────────────────────────────
$config = @{
    VirtualEnvPath      = "$PSScriptRoot\backend\venv"
    BackendTestScript   = "$PSScriptRoot\backend\run-tests.ps1"
}

# ─── Execution ────────────────────────────────────────────────────────────────
try {
    Write-Host "`n🚀 SILA System Test Runner" -ForegroundColor Cyan
    Write-Host "=============================`n" -ForegroundColor DarkCyan

    # 1. Validate environment paths
    if (-not (Test-Path $config.VirtualEnvPath)) {
        throw "❌ Virtual environment not found at: $($config.VirtualEnvPath)"
    }

    if (-not (Test-Path $config.BackendTestScript)) {
        throw "❌ Backend test script not found at: $($config.BackendTestScript)"
    }

    # 2. Activate virtual environment
    Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
    $activateScript = Join-Path $config.VirtualEnvPath "Scripts\Activate.ps1"
    if (-not (Test-Path $activateScript)) {
        throw "❌ Activation script not found at: $activateScript"
    }

    . $activateScript

    # 3. Switch to backend directory
    $backendDir = Split-Path -Parent $config.BackendTestScript
    Push-Location $backendDir

    try {
        # 4. Execute backend tests
        Write-Host "🧪 Running backend tests..." -ForegroundColor Cyan
        & $config.BackendTestScript

        if ($LASTEXITCODE -ne 0) {
            throw "❌ Backend tests failed with exit code $LASTEXITCODE"
        }

        Write-Host "`n✅ All tests completed successfully!" -ForegroundColor Green
    }
    finally {
        Pop-Location
    }
}
catch {
    Write-Host "`n❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.ScriptStackTrace) {
        Write-Host "`n📌 Stack Trace:" -ForegroundColor DarkGray
        Write-Host $_.ScriptStackTrace -ForegroundColor DarkGray
    }
    exit 1
}

exit 0

