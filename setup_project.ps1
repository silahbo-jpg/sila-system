# SILA System Project Setup Script
Write-Host "=== SILA System Setup ===" -ForegroundColor Cyan

# Create directories
$directories = @(
    "backend/app",
    "backend/tests",
    "frontend/src",
    "scripts/db",
    "scripts/deployment",
    "docs",
    "logs"
)

Write-Host "`nCreating directories..." -ForegroundColor Yellow
foreach ($dir in $directories) {
    $fullPath = Join-Path -Path $PSScriptRoot -ChildPath $dir
    if (-not (Test-Path -Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        Write-Host "- Created: $dir" -ForegroundColor Green
    } else {
        Write-Host "- Exists: $dir" -ForegroundColor Gray
    }
}

# Create README.md
$readmePath = Join-Path -Path $PSScriptRoot -ChildPath "README.md"
if (-not (Test-Path -Path $readmePath)) {
    @"
# SILA System

Sistema Integrado de Licenciamento e Autorizações

## Project Structure

- `backend/` - Backend source code
  - `app/` - Application code
  - `tests/` - Test files
- `frontend/` - Frontend source code
  - `src/` - Source files
- `scripts/` - Automation scripts
  - `db/` - Database scripts
  - `deployment/` - Deployment scripts
- `docs/` - Project documentation
- `logs/` - Log files

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- Docker (optional)

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
   uvicorn main:app --reload
   ```
2. Start the frontend:
   ```bash
   cd frontend
   npm start
   ```

## License
Proprietary - SILA System
"@ | Out-File -FilePath $readmePath -Encoding utf8
    Write-Host "- Created: README.md" -ForegroundColor Green
} else {
    Write-Host "- Exists: README.md" -ForegroundColor Gray
}

# Create .gitignore
$gitignorePath = Join-Path -Path $PSScriptRoot -ChildPath ".gitignore"
if (-not (Test-Path -Path $gitignorePath)) {
    @"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDEs and editors
.idea/
.vscode/
*.swp
*.swo
*~

# Environment variables
.env

# Logs
logs/
*.log

# Local development
.DS_Store
"@ | Out-File -FilePath $gitignorePath -Encoding utf8
    Write-Host "- Created: .gitignore" -ForegroundColor Green
} else {
    Write-Host "- Exists: .gitignore" -ForegroundColor Gray
}

Write-Host "`n=== Setup Complete ===" -ForegroundColor Green
Write-Host "Project structure has been initialized successfully!" -ForegroundColor Green
