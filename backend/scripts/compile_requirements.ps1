# Script to compile requirements files using pip-tools

function Test-CommandExists {
    param($command)
    $exists = $null -ne (Get-Command $command -ErrorAction SilentlyContinue)
    return $exists
}

function Test-RequirementsFile {
    param($filePath)
    if (-not (Test-Path $filePath)) {
        Write-Error "Required file not found: $filePath"
        return $false
    }
    if ((Get-Item $filePath).Length -eq 0) {
        Write-Error "File is empty: $filePath"
        return $false
    }
    return $true
}

try {
    # Check if pip-tools is installed
    if (-not (Test-CommandExists "pip-compile")) {
        Write-Host "Installing pip-tools..."
        python -m pip install --upgrade pip
        python -m pip install pip-tools
    }

    # Set working directory to project root
    $projectRoot = Split-Path -Parent $PSScriptRoot
    Set-Location $projectRoot
    Write-Host "Working directory: $projectRoot"

    # Check if requirements directory exists
    $requirementsDir = Join-Path $projectRoot "requirements"
    if (-not (Test-Path $requirementsDir)) {
        throw "Requirements directory not found at: $requirementsDir"
    }

    # Check for required input files
    $requiredFiles = @("base.in", "dev.in", "prod.in")
    foreach ($file in $requiredFiles) {
        $filePath = Join-Path $requirementsDir $file
        if (-not (Test-RequirementsFile $filePath)) {
            throw "Missing or invalid requirements file: $filePath"
        }
    }

    # Compile requirements files
    Write-Host "`nCompiling requirements files..."
    
    # Base requirements
    Write-Host "`n[1/3] Compiling base requirements..."
    $baseIn = Join-Path $requirementsDir "base.in"
    pip-compile --no-emit-index-url --output-file=requirements.txt $baseIn
    
    # Development requirements
    Write-Host "`n[2/3] Compiling development requirements..."
    $devIn = Join-Path $requirementsDir "dev.in"
    pip-compile --no-emit-index-url --output-file=requirements-dev.txt $devIn
    
    # Production requirements
    Write-Host "`n[3/3] Compiling production requirements..."
    $prodIn = Join-Path $requirementsDir "prod.in"
    pip-compile --no-emit-index-url --output-file=requirements-prod.txt $prodIn

    Write-Host "`n✅ Requirements files have been compiled successfully!" -ForegroundColor Green
    Write-Host "`nNext steps:"
    Write-Host "1. Install base requirements: pip install -r requirements.txt"
    Write-Host "2. For development: pip install -r requirements-dev.txt"
    Write-Host "3. For production: pip install -r requirements-prod.txt"
    
} catch {
    Write-Host "`n❌ Error: $_" -ForegroundColor Red
    exit 1
}

