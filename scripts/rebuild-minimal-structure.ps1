#!/usr/bin/env pwsh
# rebuild-minimal-structure.ps1
# Recria a estrutura minima do projeto SILA-System apos sanitizacao nuclear.
# Versao ASCII-safe, sem heredocs.

$ErrorActionPreference = "Stop"
$StartTime = Get-Date

# Raiz do projeto: um nivel acima da pasta scripts
$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot '..')
$Backend     = Join-Path $ProjectRoot 'backend'
$AppRoot     = Join-Path $Backend 'app'

Write-Host "Reconstruindo estrutura minima do SILA-System..."

# 1) Pastas minimas
$Dirs = @(
    $Backend,
    $AppRoot,
    (Join-Path $AppRoot 'models'),
    (Join-Path $AppRoot 'schemas'),
    (Join-Path $AppRoot 'services'),
    (Join-Path $AppRoot 'routes'),
    (Join-Path $AppRoot 'core'),
    (Join-Path $AppRoot 'utils')
)

foreach ($d in $Dirs) {
    if (-not (Test-Path $d)) {
        New-Item -ItemType Directory -Path $d | Out-Null
        Write-Host "[DIR] criado: $d"
    }
}

# 2) __init__.py para tornar pacotes
$PkgDirs = Get-ChildItem -Path $AppRoot -Directory
foreach ($pkg in $PkgDirs) {
    $init = Join-Path $pkg.FullName "__init__.py"
    if (-not (Test-Path $init)) {
        New-Item -ItemType File -Path $init | Out-Null
        Write-Host "[INIT] criado: $init"
    }
}
# __init__.py na raiz do app
$AppInit = Join-Path $AppRoot "__init__.py"
if (-not (Test-Path $AppInit)) {
    New-Item -ItemType File -Path $AppInit | Out-Null
    Write-Host "[INIT] criado: $AppInit"
}

# Helper para escrever arquivo a partir de array de linhas
function Write-LinesFile {
    param(
        [Parameter(Mandatory=$true)][string]$Path,
        [Parameter(Mandatory=$true)][string[]]$Lines
    )
    $dir = Split-Path -Parent $Path
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }
    # Usa UTF8 sem BOM
    $Lines | Out-File -FilePath $Path -Encoding UTF8 -Force
}

# 3) main.py minimal (FastAPI)
$MainFile = Join-Path $AppRoot "main.py"
if (-not (Test-Path $MainFile)) {
    $mainLines = @(
        "from fastapi import FastAPI",
        "",
        "app = FastAPI(title=""SILA-System API"")",
        "",
        "@app.get(""/"")",
        "async def root():",
        "    return {""message"": ""SILA-System API is alive""}"
    )
    Write-LinesFile -Path $MainFile -Lines $mainLines
    Write-Host "[FILE] criado: $MainFile"
}

# 4) requirements.txt basico
$ReqFile = Join-Path $Backend "requirements.txt"
if (-not (Test-Path $ReqFile)) {
    $reqLines = @(
        "fastapi",
        "uvicorn[standard]",
        "sqlalchemy",
        "pydantic",
        "alembic",
        "python-dotenv"
    )
    Write-LinesFile -Path $ReqFile -Lines $reqLines
    Write-Host "[REQ] criado: $ReqFile"
}

# 5) README.md do backend
$ReadmeFile = Join-Path $Backend "README.md"
if (-not (Test-Path $ReadmeFile)) {
    $readmeLines = @(
        "# SILA-System Backend",
        "",
        "Estrutura minima recriada apos sanitizacao nuclear.",
        "",
        "## Rodar local",
        "",
        "```bash",
        "cd backend",
        "python -m venv .venv",
        ".venv\Scripts\activate",
        "pip install -r requirements.txt",
        "uvicorn app.main:app --reload",
        "```"
    )
    Write-LinesFile -Path $ReadmeFile -Lines $readmeLines
    Write-Host "[DOC] criado: $ReadmeFile"
}

$EndTime = Get-Date
$Duration = $EndTime - $StartTime
Write-Host ("Estrutura minima reconstruida em " + [int]$Duration.TotalSeconds + "s")
