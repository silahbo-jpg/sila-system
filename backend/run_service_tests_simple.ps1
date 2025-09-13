# SILA Service Testing Pipeline - Simplified Version
# ==================================================

param(
    [switch]$SkipServerStart,
    [switch]$OpenReport,
    [switch]$Help
)

if ($Help) {
    Write-Host @"
SILA Service Testing Automation Pipeline
========================================

USAGE:
    .\run_service_tests_simple.ps1 [OPTIONS]

OPTIONS:
    -SkipServerStart    Skip automatic server startup
    -OpenReport         Open HTML report in browser after completion
    -Help               Show this help message

EXAMPLES:
    .\run_service_tests_simple.ps1                # Full pipeline
    .\run_service_tests_simple.ps1 -SkipServerStart  # Test existing server
    .\run_service_tests_simple.ps1 -OpenReport       # Auto-open report

"@
    exit 0
}

Write-Host ""
Write-Host "🚀 SILA Service Testing Pipeline Starting..." -ForegroundColor Green
Write-Host ("=" * 60)

# Check environment
Write-Host ""
Write-Host "📋 Checking Environment..." -ForegroundColor Yellow

if (-not (Test-Path "app\main.py")) {
    Write-Host "❌ Not in backend directory. Please run from SILA backend root." -ForegroundColor Red
    exit 1
}

try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python failed"
    }
} catch {
    Write-Host "❌ Python not found. Please install Python and add to PATH." -ForegroundColor Red
    exit 1
}

# Step 1: Service Discovery
Write-Host ""
Write-Host "📋 Step 1: Running Service Discovery..." -ForegroundColor Yellow

if (-not (Test-Path "scripts\generate_services_map.py")) {
    Write-Host "❌ Service discovery script not found" -ForegroundColor Red
    exit 1
}

python scripts\generate_services_map.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Service discovery failed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Service discovery completed" -ForegroundColor Green

# Step 2: Check Server (simplified)
Write-Host ""
Write-Host "📋 Step 2: Checking Server..." -ForegroundColor Yellow

if ($SkipServerStart) {
    Write-Host "ℹ️  Skipping server startup (SkipServerStart specified)" -ForegroundColor Cyan
} else {
    Write-Host "⚠️  Server management simplified - please start server manually:" -ForegroundColor Yellow
    Write-Host "   python -m uvicorn app.main:app --reload" -ForegroundColor Gray
    Write-Host "   Then run this script with -SkipServerStart" -ForegroundColor Gray
    Write-Host ""
}

# Step 3: Service Testing
Write-Host ""
Write-Host "📋 Step 3: Running Service Tests..." -ForegroundColor Yellow

if (-not (Test-Path "scripts\test_all_services.py")) {
    Write-Host "❌ Service testing script not found" -ForegroundColor Red
    exit 1
}

python scripts\test_all_services.py
$testExitCode = $LASTEXITCODE

# Step 4: Results
Write-Host ""
Write-Host "📋 Step 4: Processing Results..." -ForegroundColor Yellow

if ($testExitCode -eq 0) {
    Write-Host "✅ Service testing completed successfully!" -ForegroundColor Green
    
    if (Test-Path "services_test_report.html") {
        $reportSize = (Get-Item "services_test_report.html").Length
        $sizeKB = [math]::Round($reportSize / 1KB, 1)
        Write-Host "📄 HTML report generated: services_test_report.html ($sizeKB KB)" -ForegroundColor Green
        
        if ($OpenReport) {
            Write-Host "🌐 Opening report in browser..." -ForegroundColor Cyan
            try {
                Start-Process "services_test_report.html"
                Write-Host "✅ Report opened in default browser" -ForegroundColor Green
            } catch {
                Write-Host "⚠️  Could not open browser automatically" -ForegroundColor Yellow
                Write-Host "   Please open: $((Resolve-Path 'services_test_report.html').Path)" -ForegroundColor Gray
            }
        }
    }
    
    if (Test-Path "modules_services.json") {
        Write-Host "📁 Service configuration: modules_services.json" -ForegroundColor Green
    }
    
    if (Test-Path "reports") {
        $reportCount = (Get-ChildItem "reports" -File -ErrorAction SilentlyContinue).Count
        if ($reportCount -gt 0) {
            Write-Host "📊 Additional reports: $reportCount files in reports/" -ForegroundColor Green
        }
    }
} else {
    Write-Host "❌ Service testing failed or incomplete" -ForegroundColor Red
    Write-Host "   Check the output above for details" -ForegroundColor Gray
}

# Summary
Write-Host ""
Write-Host ("=" * 60)
if ($testExitCode -eq 0) {
    Write-Host "✅ SILA Service Testing Pipeline Complete!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Pipeline completed with issues" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "💡 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. Review the generated HTML report for detailed results" -ForegroundColor Gray
Write-Host "   2. Update modules_services.json with frontend mappings" -ForegroundColor Gray
Write-Host "   3. Address any failed endpoint tests" -ForegroundColor Gray
Write-Host "   4. Integrate working endpoints into frontend applications" -ForegroundColor Gray

Write-Host ""