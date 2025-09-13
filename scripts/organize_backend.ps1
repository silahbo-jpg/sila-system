# Script to organize the backend structure
param(
    [string]$BackendRoot = (Join-Path (Get-Location).Parent.FullName "backend")
)

# Function to create directory if it doesn't exist
function Ensure-Directory {
    param([string]$path)
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path | Out-Null
        Write-Host "Created directory: $path" -ForegroundColor Green
    }
    return $path
}

# Standard backend structure
$structure = @{
    "app" = @{
        "api" = @("routes", "dependencies")
        "core" = @("config", "security", "middleware")
        "models" = @()
        "schemas" = @()
        "services" = @()
        "utils" = @()
        "tests" = @("unit", "integration")
    }
    "migrations" = @()
    "alembic" = @()
    "scripts" = @()
}

# Create the directory structure
Write-Host "Creating directory structure..." -ForegroundColor Cyan

foreach ($dir in $structure.Keys) {
    $fullPath = Join-Path $BackendRoot $dir
    $subDirs = $structure[$dir]
    
    $createdDir = Ensure-Directory -path $fullPath
    
    # Create __init__.py for Python packages
    if ($dir -ne "migrations" -and $dir -ne "scripts") {
        $initFile = Join-Path $createdDir "__init__.py"
        if (-not (Test-Path $initFile)) {
            Set-Content -Path $initFile -Value "# $dir package\n"
        }
    }
    
    # Create subdirectories
    foreach ($subDir in $subDirs) {
        $subDirPath = Join-Path $createdDir $subDir
        $createdSubDir = Ensure-Directory -path $subDirPath
        
        # Create __init__.py for Python subpackages
        if ($dir -ne "migrations" -and $dir -ne "scripts") {
            $subInitFile = Join-Path $createdSubDir "__init__.py"
            if (-not (Test-Path $subInitFile)) {
                Set-Content -Path $subInitFile -Value "# $subDir subpackage\n"
            }
        }
    }
}

# Create main FastAPI application file
$mainPyContent = @"
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    # Set up CORS
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Include routers
    from app.api.routes import api_router
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app

app = create_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"@

# Create settings file
$configPyContent = @"
from pydantic import AnyHttpUrl
from typing import List, Optional, Union
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "SILA Backend"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "Sistema Integrado de Licenciamento e Autorizações"
    API_V1_STR: str = "/api/v1"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/sila_db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
"@

# Create API router file
$routerPyContent = @"
from fastapi import APIRouter

api_router = APIRouter()

# Import and include your routers here
# Example:
# from app.api.routes import items, users
# api_router.include_router(items.router, prefix="/items", tags=["items"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
"@

# Write the files
$mainPyPath = Join-Path $BackendRoot "main.py"
$configPyPath = Join-Path $BackendRoot "app/core/config.py"
$routerPyPath = Join-Path $BackendRoot "app/api/routes/__init__.py"

if (-not (Test-Path $mainPyPath)) {
    Set-Content -Path $mainPyPath -Value $mainPyContent
    Write-Host "Created main.py" -ForegroundColor Green
}

if (-not (Test-Path $configPyPath)) {
    $configDir = Split-Path -Parent $configPyPath
    if (-not (Test-Path $configDir)) {
        New-Item -ItemType Directory -Path $configDir -Force | Out-Null
    }
    Set-Content -Path $configPyPath -Value $configPyContent
    Write-Host "Created config.py" -ForegroundColor Green
}

if (-not (Test-Path $routerPyPath)) {
    $routerDir = Split-Path -Parent $routerPyPath
    if (-not (Test-Path $routerDir)) {
        New-Item -ItemType Directory -Path $routerDir -Force | Out-Null
    }
    Set-Content -Path $routerPyPath -Value $routerPyContent
    Write-Host "Created API router" -ForegroundColor Green
}

# Create requirements.txt if it doesn't exist
$requirementsPath = Join-Path $BackendRoot "requirements.txt"
if (-not (Test-Path $requirementsPath)) {
    $requirements = @"
fastapi>=0.95.0
uvicorn>=0.21.0
sqlalchemy>=2.0.0
alembic>=1.10.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.5
python-dotenv>=1.0.0
psycopg2-binary>=2.9.5
pydantic>=1.10.0
pydantic-settings>=2.0.0
email-validator>=1.3.1
"@
    Set-Content -Path $requirementsPath -Value $requirements
    Write-Host "Created requirements.txt" -ForegroundColor Green
}

Write-Host "`nBackend structure organized successfully!" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Create a virtual environment: python -m venv venv"
Write-Host "2. Activate the virtual environment: .\venv\Scripts\Activate"
Write-Host "3. Install dependencies: pip install -r requirements.txt"
Write-Host "4. Set up your .env file with the necessary environment variables"
Write-Host "5. Start the development server: uvicorn main:app --reload"
