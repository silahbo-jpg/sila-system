<#
.SYNOPSIS
    Inicializa estrutura limpa do projeto SILA System
.DESCRIPTION
    Cria diretórios essenciais e arquivos padrão para organização inicial.
    Inclui validação de permissões, restauração opcional de backup e logs detalhados.
.NOTES
    Versão: 3.5 (2025-08-17)
    Autor: SILA Team
#>

# Configuração robusta de encoding UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

[CmdletBinding()]
param(
    # Caminho raiz do projeto
    [Parameter(Mandatory=$false,
               HelpMessage='Especifique o diretório raiz do projeto')]
    [ValidateNotNullOrEmpty()]
    [string]$ProjectRoot,
    
    # Modo de simulação (não executa alterações)
    [Parameter(Mandatory=$false)]
    [switch]$DryRun,
    
    # Restaura arquivos essenciais do backup
    [Parameter(Mandatory=$false)]
    [switch]$RestoreEssentials,
    
    # Força a execução mesmo com avisos
    [Parameter(Mandatory=$false)]
    [switch]$Force
)

# Determina o diretório raiz padrão se não especificado
if (-not $ProjectRoot) {
    $ProjectRoot = if ($PSScriptRoot) { 
        $PSScriptRoot 
    } else { 
        $MyInvocation.MyCommand.Path | Split-Path -Parent 
    }
}

# === Função de log aprimorada ===
function Write-ProjectLog {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Message,
        [ValidateSet('INFO', 'WARN', 'ERROR', 'SUCCESS')]
        [string]$Level = 'INFO'
    )
    
    $timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    $logMessage = "[$timestamp] [$Level] $Message"
    
    # Cores para diferentes níveis de log
    $levelColors = @{
        'INFO'    = 'White'
        'WARN'    = 'Yellow'
        'ERROR'   = 'Red'
        'SUCCESS' = 'Green'
    }
    
    # Saída colorida para o console
    $color = $levelColors[$Level]
    Write-Host $logMessage -ForegroundColor $color
    
    # Garante que o diretório de logs existe
    $logDir = Join-Path -Path $ProjectRoot -ChildPath 'logs'
    if (-not (Test-Path -Path $logDir)) {
        New-Item -ItemType Directory -Path $logDir -Force | Out-Null
    }
    
    # Adiciona ao arquivo de log
    $logFile = Join-Path -Path $logDir -ChildPath "init_$(Get-Date -Format 'yyyyMMdd').log"
    Add-Content -Path $logFile -Value $logMessage -Encoding UTF8
}

# === Validação inicial ===
Write-ProjectLog -Message "Iniciando inicialização do projeto SILA System"
Write-ProjectLog -Message "Diretório raiz: $ProjectRoot"

# Verifica se o diretório raiz existe
if (-not (Test-Path -Path $ProjectRoot)) {
    if ($Force) {
        try {
            New-Item -ItemType Directory -Path $ProjectRoot -Force | Out-Null
            Write-ProjectLog -Message "Diretório raiz criado: $ProjectRoot"
        } catch {
            Write-ProjectLog -Message "Falha ao criar diretório raiz: $($_.Exception.Message)" -Level 'ERROR'
            exit 1
        }
    } else {
        Write-ProjectLog -Message "Diretório raiz não encontrado: $ProjectRoot" -Level 'ERROR'
        Write-ProjectLog -Message "Use -Force para criar automaticamente" -Level 'WARN'
        exit 1
    }
}

# === Estrutura de diretórios ===
$dirs = @(
    'backend/app',
    'backend/tests',
    'frontend/src',
    'frontend/public',
    'docs',
    'scripts',
    'infra',
    'logs'
)

Write-ProjectLog -Message "Criando estrutura de diretórios..."
foreach ($dir in $dirs) {
    $fullPath = Join-Path -Path $ProjectRoot -ChildPath $dir
    if (-not (Test-Path -Path $fullPath)) {
        if ($DryRun) {
            Write-ProjectLog -Message "[DRY RUN] Criaria diretório: $fullPath" -Level 'INFO'
        } else {
            try {
                New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
                Write-ProjectLog -Message "Diretório criado: $fullPath" -Level 'SUCCESS'
            } catch {
                Write-ProjectLog -Message "Falha ao criar diretório $dir : $($_.Exception.Message)" -Level 'ERROR'
                if (-not $Force) { exit 1 }
            }
        }
    } else {
        Write-ProjectLog -Message "Diretório já existe: $fullPath" -Level 'INFO'
    }
}

# === Arquivos padrão ===
$defaultFiles = @{
    "README.md" = @"
# SILA System

Sistema Integrado de Licenciamento e Autorizações

## Estrutura do Projeto

- `backend/` - Código-fonte do backend
- `frontend/` - Código-fonte do frontend
- `docs/` - Documentação do projeto
- `scripts/` - Scripts de automação
- `infra/` - Configurações de infraestrutura
- `logs/` - Arquivos de log

## Como executar

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm start
```
"@

    ".gitignore" = @"
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
"@

    "backend/.env.example" = @"
# Configurações do banco de dados
DATABASE_URL=postgresql://user:password@localhost:5432/sila_db

# Configurações da aplicação
DEBUG=True
SECRET_KEY=change-me-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Configurações de email
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=user@example.com
EMAIL_HOST_PASSWORD=your-email-password
"@

    "backend/requirements.txt" = @"
fastapi>=0.68.0,<0.69.0
uvicorn>=0.15.0,<0.16.0
sqlalchemy>=1.4.0,<2.0.0
pydantic>=1.8.0,<2.0.0
python-jose[cryptography]>=3.3.0,<4.0.0
passlib[bcrypt]>=1.7.4,<2.0.0
python-multipart>=0.0.5,<0.0.6
alembic>=1.7.0,<2.0.0
psycopg2-binary>=2.9.0,<3.0.0
python-dotenv>=0.19.0,<0.20.0
"@

    "frontend/package.json" = @"
{
  "name": "sila-frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@testing-library/jest-dom": "^5.14.1",
    "@testing-library/react": "^12.0.0",
    "@testing-library/user-event": "^13.2.1",
    "react": "^17.0.2",
    "react-dom": "^17.0.2",
    "react-router-dom": "^6.2.1",
    "react-scripts": "4.0.3",
    "web-vitals": "^2.1.0",
    "axios": "^0.25.0"
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

    "docker-compose.yml" = @"
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: sila_user
      POSTGRES_PASSWORD: sila_password
      POSTGRES_DB: sila_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data/

  backend:
    build: ./backend
    command: uvicorn main:app --reload --host 0.0.0.0 --port 8000
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://sila_user:sila_password@db:5432/sila_db

  frontend:
    build: 
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    depends_on:
      - backend

volumes:
  postgres_data:
"@
}

Write-ProjectLog -Message "Criando arquivos padrão..."
foreach ($file in $defaultFiles.GetEnumerator()) {
    $filePath = Join-Path -Path $ProjectRoot -ChildPath $file.Key
    if (-not (Test-Path -Path $filePath)) {
        if ($DryRun) {
            Write-ProjectLog -Message "[DRY RUN] Criaria arquivo: $($file.Key)" -Level 'INFO'
        } else {
            try {
                $fileDir = Split-Path -Path $filePath -Parent
                if (-not (Test-Path -Path $fileDir)) {
                    New-Item -ItemType Directory -Path $fileDir -Force | Out-Null
                }
                Set-Content -Path $filePath -Value $file.Value -Encoding UTF8 -NoNewline
                Write-ProjectLog -Message "Arquivo criado: $($file.Key)" -Level 'SUCCESS'
            } catch {
                Write-ProjectLog -Message "Falha ao criar arquivo $($file.Key) : $($_.Exception.Message)" -Level 'ERROR'
                if (-not $Force) { exit 1 }
            }
        }
    } else {
        Write-ProjectLog -Message "Arquivo já existe: $($file.Key)" -Level 'INFO'
    }
}

# === Restauração de backup ===
if ($RestoreEssentials -and (-not $DryRun)) {
    Write-ProjectLog -Message "Verificando backups disponíveis..."
    $backupDir = Join-Path -Path $ProjectRoot -ChildPath "backups"
    if (Test-Path -Path $backupDir) {
        $latestBackup = Get-ChildItem -Path $backupDir -Filter "*.zip" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
        if ($latestBackup) {
            Write-ProjectLog -Message "Restaurando backup: $($latestBackup.Name)"
            try {
                Expand-Archive -Path $latestBackup.FullName -DestinationPath $ProjectRoot -Force
                Write-ProjectLog -Message "Backup restaurado com sucesso"
            } catch {
                Write-ProjectLog -Message "Falha ao restaurar backup: $($_.Exception.Message)" -Level "ERROR"
            }
        } else {
            Write-ProjectLog -Message "Nenhum backup encontrado para restaurar" -Level "WARN"
        }
    } else {
        Write-ProjectLog -Message "Diretório de backups não encontrado" -Level "WARN"
    }
}

# === Conclusão ===
Write-ProjectLog -Message "Inicialização do projeto concluída com sucesso!"
Write-ProjectLog -Message "Log completo disponível em: $(Join-Path -Path $ProjectRoot -ChildPath "logs")"
