#!/usr/bin/env pwsh
# sanitize-backend-modules.ps1
# Reestrutura e sanitiza o monstro de 547 arquivos em backend/app/modules

$StartTime   = Get-Date
$ModulesPath = Join-Path $PSScriptRoot "..\backend\app\modules"
$LegacyPath  = Join-Path $ModulesPath "legacy"
$LogPath     = Join-Path $PSScriptRoot "..\reports\cleanup\modules-sanitization.log"

if (-not (Test-Path $ModulesPath)) {
    Write-Host "❌ ERRO: Pasta 'modules' nao encontrada" -ForegroundColor Red
    exit 1
}

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "HH:mm:ss"
    "[$timestamp] $Message" | Tee-Object -FilePath $LogPath -Append
}

Write-Log "🚀 Iniciando sanitizacao de modules"

# Criar pasta legacy se nao existir
if (-not (Test-Path $LegacyPath)) {
    New-Item -ItemType Directory -Path $LegacyPath -Force | Out-Null
    Write-Log "📁 Criado: $LegacyPath"
}

# Padrao de subpastas que cada modulo deveria ter
$ExpectedSubdirs = @("schemas", "services", "routes", "tests")

# Reestruturar cada submodulo dentro de modules/
Get-ChildItem -Path $ModulesPath -Directory | ForEach-Object {
    $module = $_.Name
    $modulePath = $_.FullName

    Write-Log "📦 Processando modulo: $module"

    foreach ($sub in $ExpectedSubdirs) {
        $subdir = Join-Path $modulePath $sub
        if (-not (Test-Path $subdir)) {
            New-Item -ItemType Directory -Path $subdir -Force | Out-Null
            Write-Log "📁 Criado subdiretorio padrao: $module/$sub"
        }
    }

    # Tratar arquivos soltos (sem categoria) → mover para legacy/<module>/
    $orphans = Get-ChildItem -Path $modulePath -File -Filter "*.py" | Where-Object { $_.Name -ne "__init__.py" }
    if ($orphans.Count -gt 0) {
        $legacyTarget = Join-Path $LegacyPath $module
        if (-not (Test-Path $legacyTarget)) {
            New-Item -ItemType Directory -Path $legacyTarget -Force | Out-Null
        }
        foreach ($file in $orphans) {
            Move-Item -Path $file.FullName -Destination $legacyTarget -Force
            Write-Log "♻️ Arquivo solto movido: $($file.Name) → legacy/$module/"
        }
    }
}

# Log final
$elapsed = (Get-Date) - $StartTime
Write-Log "✅ Sanitizacao concluida em $($elapsed.TotalSeconds) segundos"
Write-Host "✅ Sanitizacao de modules finalizada. Veja o log em $LogPath" -ForegroundColor Green
