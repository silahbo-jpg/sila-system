#!/usr/bin/env pwsh

# rebuild-sqlalchemy-models.ps1
# Reconstrói todos os modelos com SQLAlchemy
# Move de modules/*/models/ para app/models/ com padronização
# Execução em pwsh

$StartTime   = Get-Date
$BasePath    = $PSScriptRoot | Split-Path -Parent
$ModelsPath  = Join-Path $BasePath "backend\app\models"
$ModulesPath = Join-Path $BasePath "backend\app\modules"
$LogPath     = Join-Path $BasePath "reports\setup\sqlalchemy-models-rebuild.log"

# Criar pastas se não existirem
New-Item -ItemType Directory -Path $ModelsPath -Force | Out-Null
New-Item -ItemType Directory -Path (Split-Path $LogPath -Parent) -Force | Out-Null

# Função de log
function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "HH:mm:ss"
    "[$timestamp] $Message" | Tee-Object -FilePath $LogPath -Append
}

Write-Log "🏗️ Iniciando reconstrução de modelos com SQLAlchemy"
Write-Log "📌 Origem: $ModulesPath"
Write-Log "📌 Destino: $ModelsPath"

# === 1. Limpar models/ (exceto __init__.py) ===
Get-ChildItem -Path $ModelsPath -Exclude "__init__.py" -Recurse -ErrorAction SilentlyContinue |
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Write-Log "🧹 models/ limpo"

# === 2. Copiar todos os modelos de modules/*/models/*.py ===
$ModelFiles = Get-ChildItem -Path $ModulesPath -Filter "*.py" -Recurse -ErrorAction SilentlyContinue | Where-Object {
    $_.DirectoryName -like "*\models" -and $_.Name -ne "__init__.py"
}

$Count = 0
foreach ($file in $ModelFiles) {
    $ModuleName = $file.Directory.Parent.Name
    $NewName    = "${ModuleName}_$($file.Name)"   # padronização segura
    $Dest       = Join-Path $ModelsPath $NewName

    Copy-Item -Path $file.FullName -Destination $Dest -Force
    Write-Log "📥 Copiado: $NewName"
    $Count++
}

Write-Log "✅ $Count modelos copiados para /models"

# === 3. Criar base_class.py se não existir ===
$BaseClass = Join-Path $BasePath "backend\app\db\base_class.py"
if (-not (Test-Path $BaseClass)) {
    @"
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
"@ | Out-File -FilePath $BaseClass -Encoding UTF8 -Force
    Write-Log "✅ Criado: base_class.py"
}

# === 4. Criar __init__.py com imports ===
$Init    = Join-Path $ModelsPath "__init__.py"
$Exports = @(Get-ChildItem -Path $ModelsPath -Filter "*.py" | Where-Object Name -ne "__init__.py" | ForEach-Object {
    "from . import $($_.BaseName)"
})
$Exports | Out-File -FilePath $Init -Encoding UTF8 -Force
Write-Log "✅ __init__.py gerado com $($Exports.Count) imports"

# === 5. Validar Alembic e garantir estrutura ===
$AlembicDir = Join-Path $BasePath "backend\alembic"
$VersionsDir = Join-Path $AlembicDir "versions"
$AlembicIni = Join-Path $BasePath "backend\alembic.ini"

# Cria pasta versions se não existir
if (-not (Test-Path $VersionsDir)) {
    New-Item -ItemType Directory -Path $VersionsDir -Force | Out-Null
    Write-Log "📁 Pasta 'versions' criada em $VersionsDir"
}

# Valida se o alembic.ini existe e contém target_metadata
if (Test-Path $AlembicIni) {
    $Content = Get-Content $AlembicIni -Raw
    if ($Content -like "*target_metadata*") {
        Write-Log "✅ Alembic configurado corretamente"
    } else {
        Write-Log "⚠️ Verifique: target_metadata em alembic.ini"
    }
} else {
    Write-Log "❌ Arquivo alembic.ini não encontrado em $AlembicIni"
    Write-Log "💡 Dica: Execute 'alembic init alembic' para configurar o Alembic"
}

# === 6. Resumo ===
$EndTime  = Get-Date
$Duration = $EndTime - $StartTime
Write-Log "✅ Reconstrução de modelos concluída em $($Duration.TotalSeconds)s"
Write-Log "💡 Próximo passo: alembic revision --autogenerate -m 'Initial models'"
