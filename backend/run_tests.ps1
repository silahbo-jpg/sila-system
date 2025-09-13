# SILA Backend Test Automation
# Usage: .\run_tests.ps1

Write-Host "🚀 Starting SILA Backend Test Sequence..." -ForegroundColor Green

# Check if Python is available
try {
    python --version | Out-Null
} catch {
    Write-Host "❌ Python not found. Please install Python and ensure it's in PATH." -ForegroundColor Red
    exit 1
}

# Check if server is already running
Write-Host "🔍 Checking if server is already running..." -ForegroundColor Yellow
$serverResponse = $null
try {
    $serverResponse = Invoke-WebRequest -Uri "http://localhost:8000/docs" -TimeoutSec 3
} catch {
    # Server is not running, we'll start it
}

if ($serverResponse -and $serverResponse.StatusCode -eq 200) {
    Write-Host "✅ Server is already running" -ForegroundColor Green
} else {
    Write-Host "🌐 Starting Uvicorn server..." -ForegroundColor Yellow
    Start-Process -NoNewWindow -FilePath "python" -ArgumentList "-m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
    
    # Wait for server to start
    Write-Host "⏳ Waiting for server to initialize..." -ForegroundColor Yellow
    $serverReady = $false
    for ($i = 0; $i -lt 10; $i++) {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8000/docs" -TimeoutSec 2 -ErrorAction SilentlyContinue
            if ($response.StatusCode -eq 200) {
                $serverReady = $true
                break
            }
        } catch {}
        Start-Sleep -Seconds 1
    }
    
    if (-not $serverReady) {
        Write-Host "❌ Server failed to start within expected time" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Server started successfully" -ForegroundColor Green
}

# Run the test script
Write-Host "🧪 Running endpoint tests..." -ForegroundColor Yellow
python scripts/test_endpoints.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Tests completed successfully!" -ForegroundColor Green
    Write-Host "📄 Open 'endpoint_report.html' in your browser to view results" -ForegroundColor Cyan
} else {
    Write-Host "❌ Tests failed with exit code $LASTEXITCODE" -ForegroundColor Red
}