# Script to set up the backend structure
$ErrorActionPreference = "Stop"

# Define paths
$backendRoot = "c:\Users\User5\Music\MEGA1\sila\sila-system\backend"
$appDir = Join-Path $backendRoot "app"

# Create directory structure
$dirs = @(
    "app/api/routes",
    "app/core/config",
    "app/core/security",
    "app/core/middleware",
    "app/models",
    "app/schemas",
    "app/services",
    "app/utils",
    "app/tests/unit",
    "app/tests/integration",
    "migrations",
    "alembic"
)

# Create directories
foreach ($dir in $dirs) {
    $fullPath = Join-Path $backendRoot $dir
    if (-not (Test-Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        Write-Host "Created directory: $fullPath" -ForegroundColor Green
    }
}

# Create __init__.py files
Get-ChildItem -Path $appDir -Recurse -Directory | ForEach-Object {
    $initFile = Join-Path $_.FullName "__init__.py"
    if (-not (Test-Path $initFile)) {
        Set-Content -Path $initFile -Value "# $($_.Name) package"
        Write-Host "Created: $initFile" -ForegroundColor Blue
    }
}

# Create main.py if it doesn't exist
$mainPyPath = Join-Path $backendRoot "main.py"
if (-not (Test-Path $mainPyPath)) {
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

    # CORS
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
    Set-Content -Path $mainPyPath -Value $mainPyContent
    Write-Host "Created: $mainPyPath" -ForegroundColor Green
}

# Create config.py
$configPyPath = Join-Path $backendRoot "app\core\config.py"
if (-not (Test-Path $configPyPath)) {
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
    Set-Content -Path $configPyPath -Value $configPyContent
    Write-Host "Created: $configPyPath" -ForegroundColor Green
}

# Create API router
$routerPyPath = Join-Path $backendRoot "app\api\routes\__init__.py"
if (-not (Test-Path $routerPyPath)) {
    $routerPyContent = @"
from fastapi import APIRouter

api_router = APIRouter()

# Import and include your routers here
# Example:
# from app.api.routes import items, users
# api_router.include_router(items.router, prefix="/items", tags=["items"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
"@
    Set-Content -Path $routerPyPath -Value $routerPyContent
    Write-Host "Created: $routerPyPath" -ForegroundColor Green
}

# Create requirements.txt
$requirementsPath = Join-Path $backendRoot "requirements.txt"
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
    Write-Host "Created: $requirementsPath" -ForegroundColor Green
}

Write-Host "`n✅ Backend structure has been set up successfully!" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Create a virtual environment: python -m venv venv"
Write-Host "2. Activate the virtual environment: .\venv\Scripts\Activate"
Write-Host "3. Install dependencies: pip install -r requirements.txt"
Write-Host "4. Create a .env file with your configuration"
Write-Host "5. Start the development server: uvicorn main:app --reload"
