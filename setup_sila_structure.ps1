# SILA System Project Structure Setup
Write-Host "=== SILA System Structure Setup ===" -ForegroundColor Cyan

# Base directories
$baseDirs = @(
    "backend/app/api/v1",
    "backend/app/core",
    "backend/app/models",
    "backend/app/services",
    "backend/app/utils",
    "backend/tests",
    "frontend/src/components",
    "frontend/src/pages",
    "frontend/src/services",
    "frontend/public",
    "scripts/db",
    "scripts/deployment",
    "scripts/utils",
    "docs/api",
    "docs/architecture",
    "logs"
)

# Create directories
Write-Host "`nCreating directory structure..." -ForegroundColor Yellow
foreach ($dir in $baseDirs) {
    $fullPath = Join-Path -Path $PSScriptRoot -ChildPath $dir
    if (-not (Test-Path -Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        Write-Host "- Created: $dir" -ForegroundColor Green
    } else {
        Write-Host "- Exists: $dir" -ForegroundColor Gray
    }
}

# Create basic files
$files = @{
    # Backend
    "backend/requirements.txt" = @"
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
    
    "backend/README.md" = @"
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

    # Frontend
    "frontend/package.json" = @"
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

    # Root
    "README.md" = @"
# SILA System

Sistema Integrado de Licenciamento e Autorizações

## Project Structure

- `backend/` - Backend service (FastAPI)
  - `app/` - Application code
    - `api/` - API endpoints
    - `core/` - Core functionality
    - `models/` - Database models
    - `services/` - Business logic
    - `utils/` - Utility functions
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
  - `utils/` - Utility scripts

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

1. Clone the repository
2. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Set up the frontend:
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
}

# Create files
Write-Host "`nCreating files..." -ForegroundColor Yellow
foreach ($file in $files.GetEnumerator()) {
    $filePath = Join-Path -Path $PSScriptRoot -ChildPath $file.Key
    $directory = Split-Path -Path $filePath -Parent
    
    # Create directory if it doesn't exist
    if (-not (Test-Path -Path $directory)) {
        New-Item -ItemType Directory -Path $directory -Force | Out-Null
    }
    
    if (-not (Test-Path -Path $filePath)) {
        $file.Value | Out-File -FilePath $filePath -Encoding utf8
        Write-Host "- Created: $($file.Key)" -ForegroundColor Green
    } else {
        Write-Host "- Exists: $($file.Key)" -ForegroundColor Gray
    }
}

Write-Host "`n=== Setup Complete ===" -ForegroundColor Green
Write-Host "SILA System project structure has been created successfully!" -ForegroundColor Green
