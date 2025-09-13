<#
.SYNOPSIS
    Start script for SILA System - Integrated Backend and Frontend
.DESCRIPTION
    This script automates the startup of the SILA System, including:
    - Environment validation
    - Backend server startup
    - Frontend development server
    - Health checks
    - Database initialization
.NOTES
    Author: VITRONIS Team
    Version: 2.0.0
#>

param(
    [switch]$NoFrontend,
    [switch]$NoBackend
)

$ErrorActionPreference = 'Stop'

# Configuration
$ProjectRoot = $PSScriptRoot
$BackendDir = Join-Path $ProjectRoot "backend"
$FrontendDir = Join-Path $ProjectRoot "frontend\webapp"
$LogDir = Join-Path $ProjectRoot "logs"
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$LogFile = Join-Path $LogDir "sila_startup_$($Timestamp).log"

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $logMessage = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] [$Level] $Message"
    Add-Content -Path $LogFile -Value $logMessage
    switch ($Level) {
        "ERROR" { Write-Host $logMessage -ForegroundColor Red }
        "WARN" { Write-Host $logMessage -ForegroundColor Yellow }
        default { Write-Host $logMessage }
    }
}

try {
    # Initialize environment
    if (-not (Test-Path $LogDir)) {
        New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
    }

    Write-Log "🚀 Starting SILA System Initialization..."
    Write-Log "📁 Project Root: $ProjectRoot"

    # 1. Environment Setup
    $envFile = Join-Path $ProjectRoot ".env"
    $envExample = Join-Path $ProjectRoot ".env.example"
    
    if (-not (Test-Path $envFile)) {
        if (Test-Path $envExample)) {
            Write-Log "ℹ️ Creating .env file from example"
            Copy-Item $envExample $envFile
        } else {
            Write-Log "⚠️ Warning: .env file not found and no .env.example available" -Level "WARN"
        }
    }

    # Load environment variables
    if (Test-Path $envFile) {
        Get-Content $envFile | ForEach-Object {
            if ($_ -match "^\s*([^#=]+?)\s*=\s*(.*?)\s*$") {
                $key = $matches[1]
                $value = $matches[2]
                [Environment]::SetEnvironmentVariable($key, $value)
            }
        }
    }

    # 2. Database Initialization
    Write-Log "💾 Initializing Database..."
    $dbInitScript = Join-Path $BackendDir "scripts\init_db.ps1"
    if (Test-Path $dbInitScript)) {
        & $dbInitScript
        if ($LASTEXITCODE -ne 0) {
            Write-Log "⚠️ Database initialization script exited with code $LASTEXITCODE" -Level "WARN"
        }
    } else {
        Write-Log "ℹ️ Database initialization script not found at $dbInitScript" -Level "INFO"
    }

    # 3. Backend Startup
    if (-not $NoBackend) {
        $venvDir = Join-Path $BackendDir ".venv"
        $venvActivate = Join-Path $venvDir "Scripts\Activate.ps1"
        
        if (Test-Path $venvActivate)) {
            Write-Log "🔧 Activating Python virtual environment..."
            & $venvActivate
            
            # Install dependencies if needed
            $requirements = Join-Path $BackendDir "requirements.txt"
            if (Test-Path $requirements)) {
                Write-Log "📦 Installing Python dependencies..."
                pip install -r $requirements
            }

            # Start FastAPI server
            Write-Log "🚀 Starting Backend Server..."
            $backendJob = Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "cd '$BackendDir'; uvicorn app.main:app --reload --host 127.0.0.1 --port 8000" -PassThru
            
            # Health check with retries
            $healthCheckUrl = "http://localhost:8000/health"
            $maxRetries = 5
            $retryDelay = 3 # seconds
            
            for ($i = 1; $i -le $maxRetries; $i++) {
                try {
                    $response = Invoke-WebRequest -Uri $healthCheckUrl -UseBasicParsing -ErrorAction Stop
                    if ($response.StatusCode -eq 200) {
                        Write-Log "✅ Backend server is healthy at $healthCheckUrl"
                        Write-Log "📚 API Docs: http://localhost:8000/docs"
                        break
                    }
                } catch {
                    Write-Log "⏳ Waiting for backend to start... (Attempt $i/$maxRetries)" -Level "WARN"
                    if ($i -eq $maxRetries) {
                        Write-Log "⚠️ Backend health check failed after $maxRetries attempts" -Level "WARN"
                    }
                    Start-Sleep -Seconds $retryDelay
                }
            }
        } else {
            Write-Log "❌ Python virtual environment not found at $venvDir" -Level "ERROR"
            exit 1
        }
    }

    # 4. Frontend Startup
    if (-not $NoFrontend) {
        if (Test-Path $FrontendDir)) {
            Write-Log "🖥️ Starting Frontend Development Server..."
            
            # Install dependencies if needed
            if (Test-Path (Join-Path $FrontendDir "node_modules")) {
                Write-Log "📦 Node modules already installed"
            } else {
                Write-Log "📦 Installing Node dependencies..."
                Set-Location $FrontendDir
                npm install
            }
            
            # Determine port from config
            $viteConfig = Join-Path $FrontendDir "vite.config.ts"
            $frontendPort = 5173
            if (Test-Path $viteConfig)) {
                $configContent = Get-Content $viteConfig -Raw
                if ($configContent -match "port:\s*(\d+)") {
                    $frontendPort = $matches[1]
                }
            }
            
            # Start dev server
            $frontendJob = Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "cd '$FrontendDir'; npm run dev" -PassThru
            
            # Open browser
            $frontendUrl = "http://localhost:$frontendPort"
            try {
                Start-Process $frontendUrl
                Write-Log "🌐 Opening frontend at $frontendUrl"
            } catch {
                Write-Log "⚠️ Could not open browser automatically" -Level "WARN"
            }
        } else {
            Write-Log "❌ Frontend directory not found at $FrontendDir" -Level "ERROR"
        }
    }

    Write-Log "✅ SILA System startup completed successfully!"
    Write-Log "📋 Logs saved to: $LogFile"
    Write-Log "👉 Press Ctrl+C to stop all servers"

    # Keep the script running
    while ($true) {
        Start-Sleep -Seconds 60
    }

} catch {
    Write-Log "❌ Critical error during startup: $_" -Level "ERROR"
    Write-Log $_.ScriptStackTrace -Level "ERROR"
    exit 1
}