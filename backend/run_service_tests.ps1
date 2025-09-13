# SILA Service Testing Automation Pipeline
# =====================================
# 
# Comprehensive automation script for the SILA system that:
# 1. Discovers all API endpoints from FastAPI modules
# 2. Tests endpoints with intelligent error handling
# 3. Generates detailed HTML reports
# 4. Manages server lifecycle automatically
#
# Part of SILA's centralized automation hub
# Compatible with Windows PowerShell and PowerShell Core

param(
    [switch]$SkipServerStart,
    [switch]$OpenReport,
    [string]$ServerUrl = "http://localhost:8000",
    [int]$ServerStartTimeout = 30,
    [switch]$Verbose,
    [switch]$Help
)

# Display help information
if ($Help) {
    Write-Host @"
SILA Service Testing Automation Pipeline
========================================

USAGE:
    .\run_service_tests.ps1 [OPTIONS]

OPTIONS:
    -SkipServerStart       Skip automatic server startup (use if server is already running)
    -OpenReport           Automatically open the HTML report in default browser
    -ServerUrl <url>      Server URL to test against (default: http://localhost:8000)
    -ServerStartTimeout   Timeout in seconds for server startup (default: 30)
    -Verbose              Enable verbose output for debugging
    -Help                 Display this help message

EXAMPLES:
    .\run_service_tests.ps1                    # Full automated pipeline
    .\run_service_tests.ps1 -SkipServerStart   # Test existing running server
    .\run_service_tests.ps1 -OpenReport        # Auto-open report after testing
    .\run_service_tests.ps1 -Verbose           # Detailed logging

REQUIREMENTS:
    - Python 3.8+ with required packages
    - SILA backend environment properly configured
    - Network access to test endpoints

"@
    exit 0
}

# Enhanced logging functions
function Write-Header {
    param([string]$Message)
    Write-Host ""
    Write-Host "🚀 $Message" -ForegroundColor Green
    Write-Host ("=" * 70) -ForegroundColor Gray
}

function Write-Step {
    param([string]$Message)
    Write-Host ""
    Write-Host "📋 $Message" -ForegroundColor Yellow
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠️  $Message" -ForegroundColor Yellow
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ️  $Message" -ForegroundColor Cyan
}

function Write-VerboseCustom {
    param([string]$Message)
    if ($Verbose) {
        Write-Host "🔍 $Message" -ForegroundColor Gray
    }
}
}

# Validate environment
function Test-Environment {
    Write-Step "Validating Environment"
    
    # Check if we're in the correct directory
    if (-not (Test-Path "app\main.py")) {
        Write-Error-Custom "Not in backend directory. Please run from SILA backend root."
        Write-Info "Expected structure: backend\app\main.py"
        return $false
    }
    
    # Check Python availability
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Python found: $pythonVersion"
            Write-VerboseCustom "Python executable: $(Get-Command python | Select-Object -ExpandProperty Source)"
        } else {
            throw "Python command failed"
        }
    } catch {
        Write-Error-Custom "Python not found or not working properly."
        Write-Info "Please ensure Python 3.8+ is installed and in PATH"
        return $false
    }
    
    # Check if required directories exist
    $requiredDirs = @("app\modules", "scripts")
    foreach ($dir in $requiredDirs) {
        if (-not (Test-Path $dir)) {
            Write-Error-Custom "Required directory not found: $dir"
            return $false
        }
    }
    
    Write-Success "Environment validation complete"
    return $true
}

# Check if required Python packages are available
function Test-PythonPackages {
    Write-Step "Checking Python Dependencies"
    
    $requiredPackages = @("fastapi", "requests", "uvicorn")
    $missingPackages = @()
    
    foreach ($package in $requiredPackages) {
        try {
            python -c "import $package" 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-VerboseCustom "Package available: $package"
            } else {
                $missingPackages += $package
            }
        } catch {
            $missingPackages += $package
        }
    }
    
    if ($missingPackages.Count -gt 0) {
        Write-Warning "Missing Python packages: $($missingPackages -join ', ')"
        Write-Info "Consider running: pip install -r requirements.txt"
        return $false
    }
    
    Write-Success "All required Python packages are available"
    return $true
}

# Execute service discovery
function Invoke-ServiceDiscovery {
    Write-Step "Discovering API Services"
    
    if (-not (Test-Path "scripts\generate_services_map.py")) {
        Write-Error-Custom "Service discovery script not found: scripts\generate_services_map.py"
        return $false
    }
    
    try {
        Write-VerboseCustom "Running: python scripts\generate_services_map.py"
        python scripts\generate_services_map.py
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Service discovery completed successfully"
            
            # Check if output file was created
            if (Test-Path "modules_services.json") {
                $serviceConfig = Get-Content "modules_services.json" | ConvertFrom-Json
                $moduleCount = $serviceConfig.PSObject.Properties.Count
                $endpointCount = ($serviceConfig.PSObject.Properties.Value | ForEach-Object { $_.services.Count } | Measure-Object -Sum).Sum
                
                Write-Info "Discovered $moduleCount modules with $endpointCount total endpoints"
                return $true
            } else {
                Write-Warning "Service discovery completed but no output file generated"
                return $false
            }
        } else {
            Write-Error-Custom "Service discovery failed with exit code: $LASTEXITCODE"
            return $false
        }
    } catch {
        Write-Error-Custom "Error during service discovery: $($_.Exception.Message)"
        return $false
    }
}

# Check server status
function Test-ServerStatus {
    param([string]$Url, [int]$TimeoutSeconds = 5)
    
    $endpoints = @("/docs", "/health", "/ping", "/api/v1")
    
    foreach ($endpoint in $endpoints) {
        try {
            $testUrl = "$Url$endpoint"
            Write-VerboseCustom "Testing endpoint: $testUrl"
            
            $response = Invoke-WebRequest -Uri $testUrl -TimeoutSec $TimeoutSeconds -ErrorAction SilentlyContinue
            if ($response.StatusCode -eq 200) {
                Write-VerboseCustom "Server responded successfully at $endpoint"
                return $true
            }
        } catch {
            Write-VerboseCustom "Endpoint $endpoint not accessible: $($_.Exception.Message)"
            continue
        }
    }
    
    return $false
}

# Start SILA server
function Start-SilaServer {
    Write-Step "Managing SILA Server"
    
    if ($SkipServerStart) {
        Write-Info "Skipping server startup (-SkipServerStart specified)"
        
        if (Test-ServerStatus -Url $ServerUrl) {
            Write-Success "Server is already running and accessible"
            return $true
        } else {
            Write-Error-Custom "Server is not accessible at $ServerUrl"
            Write-Info "Please start the server manually or remove -SkipServerStart flag"
            return $false
        }
    }
    
    # Check if server is already running
    if (Test-ServerStatus -Url $ServerUrl) {
        Write-Success "Server is already running and accessible"
        return $true
    }
    
    Write-Info "Starting SILA server..."
    Write-VerboseCustom "Command: python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
    
    # Start server in background
    try {
        $serverProcess = Start-Process -NoNewWindow -PassThru -FilePath "python" -ArgumentList @(
            "-m", "uvicorn", "app.main:app", 
            "--reload", "--host", "0.0.0.0", "--port", "8000"
        )
        
        Write-Info "Server process started (PID: $($serverProcess.Id))"
        Write-Info "Waiting for server to initialize..."
        
        # Wait for server to become ready
        $startTime = Get-Date
        $timeout = $ServerStartTimeout
        
        do {
            Start-Sleep -Seconds 2
            $elapsed = ((Get-Date) - $startTime).TotalSeconds
            
            if (Test-ServerStatus -Url $ServerUrl) {
                Write-Success "Server is ready and responding (took $([math]::Round($elapsed, 1))s)"
                return $true
            }
            
            Write-VerboseCustom "Server not ready yet... ($([math]::Round($elapsed, 1))s/$($timeout)s)"
            
        } while ($elapsed -lt $timeout)
        
        Write-Error-Custom "Server failed to start within $timeout seconds"
        Write-Info "Check server logs for errors"
        
        # Attempt to stop the process if it's still running
        if (-not $serverProcess.HasExited) {
            Write-Info "Stopping server process..."
            $serverProcess | Stop-Process -Force
        }
        
        return $false
        
    } catch {
        Write-Error-Custom "Failed to start server: $($_.Exception.Message)"
        return $false
    }
}

# Execute comprehensive service testing
function Invoke-ServiceTesting {
    Write-Step "Running Comprehensive Service Tests"
    
    if (-not (Test-Path "scripts\test_all_services.py")) {
        Write-Error-Custom "Service testing script not found: scripts\test_all_services.py"
        return $false
    }
    
    if (-not (Test-Path "modules_services.json")) {
        Write-Error-Custom "Services configuration not found. Run service discovery first."
        return $false
    }
    
    try {
        Write-VerboseCustom "Running: python scripts\test_all_services.py"
        python scripts\test_all_services.py
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Service testing completed successfully"
            
            # Check if report was generated
            if (Test-Path "services_test_report.html") {
                $reportSize = (Get-Item "services_test_report.html").Length
                Write-Info "Generated HTML report ($([math]::Round($reportSize/1KB, 1)) KB)"
                return $true
            } else {
                Write-Warning "Testing completed but no report file generated"
                return $false
            }
        } else {
            Write-Error-Custom "Service testing failed with exit code: $LASTEXITCODE"
            return $false
        }
    } catch {
        Write-Error-Custom "Error during service testing: $($_.Exception.Message)"
        return $false
    }
}

# Generate final summary
function Show-FinalSummary {
    Write-Header "Testing Pipeline Summary"
    
    $summaryItems = @()
    
    # Check service discovery results
    if (Test-Path "modules_services.json") {
        try {
            $serviceConfig = Get-Content "modules_services.json" | ConvertFrom-Json
            $moduleCount = $serviceConfig.PSObject.Properties.Count
            $endpointCount = ($serviceConfig.PSObject.Properties.Value | ForEach-Object { $_.services.Count } | Measure-Object -Sum).Sum
            $summaryItems += "📦 Modules scanned: $moduleCount"
            $summaryItems += "🔗 Endpoints discovered: $endpointCount"
        } catch {
            $summaryItems += "⚠️  Service configuration file exists but couldn't be parsed"
        }
    }
    
    # Check test report
    if (Test-Path "services_test_report.html") {
        $reportFile = Get-Item "services_test_report.html"
        $summaryItems += "📄 Test report generated: $(Split-Path $reportFile.FullName -Leaf)"
        $summaryItems += "📅 Report date: $($reportFile.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss'))"
        $summaryItems += "💾 Report size: $(($reportFile.Length/1KB).ToString('F1')) KB"
    }
    
    # Check reports directory
    if (Test-Path "reports") {
        $reportCount = (Get-ChildItem "reports" -File).Count
        $summaryItems += "📁 Additional reports: $reportCount files in reports/"
    }
    
    foreach ($item in $summaryItems) {
        Write-Host "   $item"
    }
    
    Write-Host ""
    Write-Success "SILA Service Testing Pipeline Complete!"
    
    # Provide next steps
    Write-Host ""
    Write-Info "Next Steps:"
    Write-Host "   1. Open services_test_report.html to view detailed results"
    Write-Host "   2. Review modules_services.json to add frontend mappings"
    Write-Host "   3. Check reports/ directory for additional analysis"
    Write-Host "   4. Integrate successful endpoints into frontend applications"
    
    # Auto-open report if requested
    if ($OpenReport -and (Test-Path "services_test_report.html")) {
        Write-Info "Opening test report in default browser..."
        try {
            Start-Process "services_test_report.html"
            Write-Success "Report opened in browser"
        } catch {
            Write-Warning "Could not automatically open report: $($_.Exception.Message)"
            Write-Info "Please manually open: $(Resolve-Path 'services_test_report.html')"
        }
    }
}

# Main execution
function Main {
    $startTime = Get-Date
    
    Write-Header "SILA Service Testing Automation Pipeline"
    Write-Info "Part of SILA's comprehensive automation hub"
    Write-Info "Server URL: $ServerUrl"
    
    # Validate environment
    if (-not (Test-Environment)) {
        Write-Error-Custom "Environment validation failed"
        exit 1
    }
    
    # Check Python dependencies
    if (-not (Test-PythonPackages)) {
        Write-Warning "Some Python packages may be missing, but continuing..."
    }
    
    # Execute service discovery
    if (-not (Invoke-ServiceDiscovery)) {
        Write-Error-Custom "Service discovery failed"
        exit 1
    }
    
    # Manage server
    if (-not (Start-SilaServer)) {
        Write-Error-Custom "Server startup/verification failed"
        exit 1
    }
    
    # Run comprehensive tests
    if (-not (Invoke-ServiceTesting)) {
        Write-Error-Custom "Service testing failed"
        exit 1
    }
    
    # Show summary
    $duration = (Get-Date) - $startTime
    Write-Host ""
    Write-Info "Total execution time: $($duration.ToString('mm\:ss'))"
    
    Show-FinalSummary
}

# Error handling and cleanup
try {
    Main
} catch {
    Write-Host ""
    Write-Error-Custom "Pipeline failed with unexpected error:"
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host $_.ScriptStackTrace -ForegroundColor Gray
    exit 1
} finally {
    Write-Host ""
    Write-Info "Pipeline execution completed"
}