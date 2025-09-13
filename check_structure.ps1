# Script to check and create basic project structure
Write-Host "=== Checking SILA System Structure ===" -ForegroundColor Cyan

# Define required directories
$requiredDirs = @(
    "backend/app/api/v1",
    "backend/app/core",
    "backend/app/models",
    "backend/app/services",
    "backend/tests",
    "frontend/src/components",
    "frontend/src/pages",
    "frontend/public",
    "scripts/db",
    "scripts/deployment",
    "docs/api",
    "logs"
)

# Check directories
Write-Host "`nChecking directories..." -ForegroundColor Yellow
$missingDirs = @()

foreach ($dir in $requiredDirs) {
    $fullPath = Join-Path -Path $PSScriptRoot -ChildPath $dir
    if (Test-Path -Path $fullPath) {
        Write-Host "✓ $dir" -ForegroundColor Green
    } else {
        Write-Host "✗ $dir" -ForegroundColor Red
        $missingDirs += $dir
    }
}

# Summary
if ($missingDirs.Count -gt 0) {
    Write-Host "`nMissing directories:" -ForegroundColor Red
    $missingDirs | ForEach-Object { Write-Host "- $_" }
    
    $create = Read-Host "`nWould you like to create the missing directories? (y/n)"
    if ($create -eq 'y') {
        foreach ($dir in $missingDirs) {
            $fullPath = Join-Path -Path $PSScriptRoot -ChildPath $dir
            New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
            Write-Host "Created: $dir" -ForegroundColor Green
        }
    }
} else {
    Write-Host "`nAll required directories are present." -ForegroundColor Green
}

# Check for required files
$requiredFiles = @(
    "backend/requirements.txt",
    "backend/README.md",
    "frontend/package.json",
    "README.md"
)

Write-Host "`nChecking files..." -ForegroundColor Yellow
$missingFiles = @()

foreach ($file in $requiredFiles) {
    $fullPath = Join-Path -Path $PSScriptRoot -ChildPath $file
    if (Test-Path -Path $fullPath) {
        Write-Host "✓ $file" -ForegroundColor Green
    } else {
        Write-Host "✗ $file" -ForegroundColor Red
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Host "`nMissing files:" -ForegroundColor Red
    $missingFiles | ForEach-Object { Write-Host "- $_" }
    
    $create = Read-Host "`nWould you like to create basic versions of these files? (y/n)"
    if ($create -eq 'y') {
        # Create basic files if they don't exist
        foreach ($file in $missingFiles) {
            $fullPath = Join-Path -Path $PSScriptRoot -ChildPath $file
            $directory = Split-Path -Path $fullPath -Parent
            
            if (-not (Test-Path -Path $directory)) {
                New-Item -ItemType Directory -Path $directory -Force | Out-Null
            }
            
            switch -Wildcard ($file) {
                "*requirements.txt" {
                    @"
fastapi>=0.68.0
uvicorn>=0.15.0
sqlalchemy>=1.4.0
pydantic>=1.8.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.5
alembic>=1.7.0
psycopg2-binary>=2.9.0
python-dotenv>=0.19.0
"@ | Out-File -FilePath $fullPath -Encoding utf8
                }
                "backend/README.md" {
                    @"
# SILA Backend

Backend service for SILA System.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
"@ | Out-File -FilePath $fullPath -Encoding utf8
                }
                "frontend/package.json" {
                    @"
{
  "name": "sila-frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@testing-library/jest-dom": "^5.14.1",
    "@testing-library/react": "^12.0.0",
    "@testing-library/user-event": "^13.2.1",
    "axios": "^0.25.0",
    "react": "^17.0.2",
    "react-dom": "^17.0.2",
    "react-router-dom": "^6.2.1",
    "react-scripts": "4.0.3",
    "web-vitals": "^2.1.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
"@ | Out-File -FilePath $fullPath -Encoding utf8
                }
                "README.md" {
                    @"
# SILA System

Sistema Integrado de Licenciamento e Autorizações

## Project Structure

- `backend/` - Backend service (FastAPI)
- `frontend/` - Frontend application (React)
- `scripts/` - Automation scripts
- `docs/` - Documentation
- `logs/` - Log files

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL

### Installation

1. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Set up the frontend:
   ```bash
   cd frontend
   npm install
   ```
"@ | Out-File -FilePath $fullPath -Encoding utf8
                }
            }
            
            Write-Host "Created: $file" -ForegroundColor Green
        }
    }
} else {
    Write-Host "`nAll required files are present." -ForegroundColor Green
}

Write-Host "`n=== Structure Check Complete ===" -ForegroundColor Cyan
