# Setup environment script for sila_dev System
# This script ensures all required dependencies are installed

# Check if running as sila_dev-systemistrator
$issila_dev-system = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::sila_dev-systemistrator)

# Set error action preference
$ErrorActionPreference = "Stop"

Write-Host "🚀 Setting up sila_dev System environment..." -ForegroundColor Cyan

# Check Python version
$pythonVersion = python --version
if ($LASTEXITCODE -ne 0) {
    Write-Error "❌ Python is not installed or not in PATH"
    exit 1
}
Write-Host "✅ $pythonVersion" -ForegroundColor Green

# Navigate to backend directory
$backendDir = Join-Path $PSScriptsila_dev-system "..\backend"
Set-Location $backendDir

# Create virtual environment if it doesn't exist
$venvPath = ".\.venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "🔧 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv $venvPath
    if ($LASTEXITCODE -ne 0) {
        Write-Error "❌ Failed to create virtual environment"
        exit 1
    }
}

# Activate virtual environment
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
if (-not (Test-Path $activateScript)) {
    $activateScript = Join-Path $venvPath "Scripts\activate"
}

Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
. $activateScript

# Upgrade pip
Write-Host "🔄 Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    Write-Warning "⚠️  Failed to upgrade pip, continuing anyway..."
}

# Install base requirements
$requirementsFiles = @(
    "requirements.txt",
    "requirements-dev.txt"
)

foreach ($reqFile in $requirementsFiles) {
    if (Test-Path $reqFile) {
        Write-Host "📦 Installing requirements from $reqFile..." -ForegroundColor Yellow
        pip install -r $reqFile
        if ($LASTEXITCODE -ne 0) {
            Write-Warning "⚠️  Some dependencies from $reqFile failed to install"
        }
    }
}

# Install additional required packages
$requiredPackages = @(
    "pydantic[email]",
    "email-validator",
    "fastapi[all]",
    "uvicorn[standard]"
)

Write-Host "📦 Installing additional required packages..." -ForegroundColor Yellow
foreach ($pkg in $requiredPackages) {
    pip install $pkg
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "⚠️  Failed to install $pkg"
    }
}

# Install Prisma client
Write-Host "🔌 Setting up Prisma client..." -ForegroundColor Yellow
prisma generate
if ($LASTEXITCODE -ne 0) {
    Write-Warning "⚠️  Failed to generate Prisma client"
}

Write-Host "✨ Environment setup complete!" -ForegroundColor Green
Write-Host "To start the application, run:" -ForegroundColor Cyan
Write-Host "  cd $backendDir" -ForegroundColor White
Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  uvicorn app.main:app --reload" -ForegroundColor White


