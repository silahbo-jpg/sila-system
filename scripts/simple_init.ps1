# Simple initialization script with basic functionality

# Set encoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

try {
    # Display script information
    Write-Host "=== SILA System Initialization ===" -ForegroundColor Cyan
    Write-Host "Current directory: $(Get-Location)"
    
    # Basic directory structure
    $dirs = @(
        "backend/app",
        "backend/tests",
        "frontend/src",
        "scripts/db",
        "scripts/deployment",
        "docs",
        "logs"
    )
    
    # Create directories
    Write-Host "`nCreating directories..." -ForegroundColor Yellow
    foreach ($dir in $dirs) {
        $fullPath = Join-Path -Path $PSScriptRoot -ChildPath $dir
        if (-not (Test-Path -Path $fullPath)) {
            New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
            Write-Host "- Created: $dir" -ForegroundColor Green
        } else {
            Write-Host "- Exists: $dir" -ForegroundColor Gray
        }
    }
    
    # Basic files to create
    $files = @{
        "README.md" = @"
# SILA System

Sistema Integrado de Licenciamento e Autorizações

## Estrutura do Projeto

- `backend/` - Código-fonte do backend
- `frontend/` - Código-fonte do frontend
- `scripts/` - Scripts de automação
- `docs/` - Documentação
- `logs/` - Arquivos de log
"@
        
        ".gitignore" = @"
# Python
__pycache__/
*.py[cod]
*$py.class

# Node
node_modules/
npm-debug.log*

# Environment
.env

# IDE
.idea/
.vscode/

# Logs
logs/
"@
    }
    
    # Create files
    Write-Host "`nCreating files..." -ForegroundColor Yellow
    foreach ($file in $files.GetEnumerator()) {
        $filePath = Join-Path -Path $PSScriptRoot -ChildPath $file.Key
        if (-not (Test-Path -Path $filePath)) {
            $file.Value | Out-File -FilePath $filePath -Encoding UTF8
            Write-Host "- Created: $($file.Key)" -ForegroundColor Green
        } else {
            Write-Host "- Exists: $($file.Key)" -ForegroundColor Gray
        }
    }
    
    Write-Host "`n=== Initialization Complete ===" -ForegroundColor Green
    Write-Host "Project structure has been created successfully!" -ForegroundColor Green
    
} catch {
    Write-Host "An error occurred: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
