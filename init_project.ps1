# SILA System Project Initialization Script
Write-Host "=== SILA System Project Initialization ===" -ForegroundColor Cyan

# Function to create directory if it doesn't exist
function Ensure-Directory {
    param([string]$Path)
    if (-not (Test-Path -Path $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
        Write-Host "Created directory: $Path" -ForegroundColor Green
    } else {
        Write-Host "Directory exists: $Path" -ForegroundColor Gray
    }
}

# Function to create file if it doesn't exist
function Ensure-File {
    param([string]$Path, [string]$Content)
    if (-not (Test-Path -Path $Path)) {
        $directory = Split-Path -Path $Path -Parent
        if (-not (Test-Path -Path $directory)) {
            New-Item -ItemType Directory -Path $directory -Force | Out-Null
        }
        $Content | Out-File -FilePath $Path -Encoding utf8
        Write-Host "Created file: $Path" -ForegroundColor Green
    } else {
        Write-Host "File exists: $Path" -ForegroundColor Gray
    }
}

# Create directory structure
Write-Host "`nCreating directory structure..." -ForegroundColor Yellow

# Backend directories
$backendDirs = @(
    "backend/app/api/v1",
    "backend/app/core",
    "backend/app/models",
    "backend/app/services",
    "backend/tests/unit",
    "backend/tests/integration"
)

# Frontend directories
$frontendDirs = @(
    "frontend/src/components",
    "frontend/src/pages",
    "frontend/src/services",
    "frontend/public"
)

# Other directories
$otherDirs = @(
    "scripts/db",
    "scripts/deployment",
    "docs/api",
    "docs/architecture",
    "logs"
)

# Create all directories
$allDirs = $backendDirs + $frontendDirs + $otherDirs
foreach ($dir in $allDirs) {
    $fullPath = Join-Path -Path $PSScriptRoot -ChildPath $dir
    Ensure-Directory -Path $fullPath
}

# Create essential files
Write-Host "`nCreating essential files..." -ForegroundColor Yellow

# Backend requirements
$requirementsContent = @"
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
"@

Ensure-File -Path (Join-Path $PSScriptRoot "backend/requirements.txt") -Content $requirementsContent

# Backend README
$backendReadmeContent = @"
# SILA Backend

Backend service for SILA System built with FastAPI.

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

3. Set up environment variables in `.env` file

4. Run migrations:
   ```bash
   alembic upgrade head
   ```

5. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```
"@

Ensure-File -Path (Join-Path $PSScriptRoot "backend/README.md") -Content $backendReadmeContent

# Frontend package.json
$packageJsonContent = @"
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
"@

Ensure-File -Path (Join-Path $PSScriptRoot "frontend/package.json") -Content $packageJsonContent

# Main README
$mainReadmeContent = @"
# SILA System

Sistema Integrado de Licenciamento e Autorizações

## Project Structure

- `backend/` - Backend service (FastAPI)
  - `app/` - Application code
    - `api/` - API endpoints
    - `core/` - Core functionality
    - `models/` - Database models
    - `services/` - Business logic
  - `tests/` - Test files

- `frontend/` - Frontend application (React)
  - `src/` - Source files
    - `components/` - Reusable components
    - `pages/` - Page components
    - `services/` - API services
  - `public/` - Static files

- `scripts/` - Automation scripts
  - `db/` - Database scripts
  - `deployment/` - Deployment scripts

- `docs/` - Documentation
  - `api/` - API documentation
  - `architecture/` - System architecture

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

### Running the Application

1. Start the backend:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. Start the frontend:
   ```bash
   cd frontend
   npm start
   ```

## License
Proprietary - SILA System
"@

Ensure-File -Path (Join-Path $PSScriptRoot "README.md") -Content $mainReadmeContent

# Create empty .gitkeep files in empty directories to ensure they're tracked by git
Write-Host "`nEnsuring empty directories are tracked by git..." -ForegroundColor Yellow

$emptyDirs = @(
    "backend/app/__init__.py",
    "backend/app/api/__init__.py",
    "backend/app/api/v1/__init__.py",
    "backend/app/core/__init__.py",
    "backend/app/models/__init__.py",
    "backend/app/services/__init__.py",
    "backend/tests/__init__.py",
    "backend/tests/unit/__init__.py",
    "backend/tests/integration/__init__.py",
    "frontend/src/components/.gitkeep",
    "frontend/src/pages/.gitkeep",
    "frontend/src/services/.gitkeep",
    "scripts/db/.gitkeep",
    "scripts/deployment/.gitkeep",
    "docs/api/.gitkeep",
    "docs/architecture/.gitkeep",
    "logs/.gitkeep"
)

foreach ($file in $emptyDirs) {
    $fullPath = Join-Path -Path $PSScriptRoot -ChildPath $file
    if (-not (Test-Path -Path $fullPath)) {
        $directory = Split-Path -Path $fullPath -Parent
        if (-not (Test-Path -Path $directory)) {
            New-Item -ItemType Directory -Path $directory -Force | Out-Null
        }
        New-Item -ItemType File -Path $fullPath -Force | Out-Null
        Write-Host "Created placeholder: $file" -ForegroundColor DarkGray
    }
}

Write-Host "`n=== SILA System Project Initialization Complete ===" -ForegroundColor Green
Write-Host "Project structure has been set up successfully!" -ForegroundColor Green
