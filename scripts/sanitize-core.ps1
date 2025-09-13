#!/usr/bin/env pwsh

# sanitize-core.ps1
# Sanitização radical do backend/app/core
# Remove lixo, consolida arquivos e reestrutura para modernização
# Execução otimizada para pwsh

$StartTime = Get-Date
$CorePath = Join-Path $PSScriptRoot "..\backend\app\core"
$LogPath = Join-Path $PSScriptRoot "..\reports\cleanup\core-sanitization.log"
$BackupPath = Join-Path $PSScriptRoot "..\backup\core-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

# Validar caminho
if (-not (Test-Path $CorePath)) {
    Write-Host "❌ ERRO: Pasta core não encontrada: $CorePath" -ForegroundColor Red
    exit 1
}

# Criar pastas de log e backup
New-Item -ItemType Directory -Path (Split-Path $LogPath -Parent) -Force | Out-Null
New-Item -ItemType Directory -Path $BackupPath -Force | Out-Null

# Função de log
function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "HH:mm:ss"
    "[$timestamp] $Message" | Tee-Object -FilePath $LogPath -Append
}

Write-Log "🚀 Iniciando sanitização de: $CorePath"

# === 1. Backup completo ===
Write-Log "📁 Criando backup em: $BackupPath"
Copy-Item -Path $CorePath -Destination $BackupPath -Recurse -Force
Write-Log "✅ Backup concluído"

# === 2. Remover __pycache__ e .pyc ===
Write-Log "🧹 Removendo __pycache__ e .pyc..."
Get-ChildItem -Path $CorePath -Include "__pycache__" -Recurse -Directory | Remove-Item -Recurse -Force
Get-ChildItem -Path $CorePath -Include "*.pyc" -Recurse -File | Remove-Item -Force

# === 3. Remover arquivos obsoletos ou duplicados ===
$ToRemove = @(
    "regra_negocio.py"          # duplicado
    "notificador.py"            # substituído por /notification
    "middleware.py"             # conflita com /middleware e observability_middleware.py
    "event_setup.py"            # se não usado
    "form_generator.py"         # se não usado
    "formatters.py"             # mover para utils/ ou remover
    "deps.py"                   # se já estiver em outro lugar
)

foreach ($file in $ToRemove) {
    $path = Join-Path $CorePath $file
    if (Test-Path $path) {
        Remove-Item $path -Force
        Write-Log "🗑️ Removido: $file"
    }
}

# === 4. Reorganizar: Mover módulos de domínio para /modules ===
$ModulesPath = Join-Path (Split-Path $CorePath -Parent) "modules"
if (-not (Test-Path $ModulesPath)) { New-Item -ItemType Directory -Path $ModulesPath -Force }

$Domains = @("identity", "location", "payment", "notification")
foreach ($domain in $Domains) {
    $source = Join-Path $CorePath $domain
    $dest = Join-Path $ModulesPath $domain
    if (Test-Path $source) {
        if (-not (Test-Path $dest)) {
            Move-Item -Path $source -Destination $dest -Force
            Write-Log "🔄 Movido: $domain → /modules"
        } else {
            Write-Log "⚠️ Já existe: $dest – pulando"
        }
    }
}

# === 5. Consolidar autenticação em /core/auth ===
$AuthDir = Join-Path $CorePath "auth"
if (-not (Test-Path $AuthDir)) { New-Item -ItemType Directory -Path $AuthDir -Force }

$AuthFiles = @("auth.py", "auth_utils.py", "enhanced_auth.py", "security.py", "permissions.py")
foreach ($file in $AuthFiles) {
    $path = Join-Path $CorePath $file
    if (Test-Path $path) {
        Move-Item -Path $path -Destination $AuthDir -Force
        Write-Log "🔐 Consolidado: $file → /auth"
    }
}

# === 6. Criar lógica de negócios unificada ===
$RulesFile = Join-Path $CorePath "business_rules.py"
$OldRules = Join-Path $CorePath "regras_negocio.py"
if (Test-Path $OldRules) {
    if (-not (Test-Path $RulesFile)) {
        Rename-Item -Path $OldRules -NewName "business_rules.py" -Force
        Write-Log "✅ Renomeado: regras_negocio.py → business_rules.py"
    } else {
        Remove-Item $OldRules -Force
        Write-Log "🗑️ Removido: regras_negocio.py (duplicado)"
    }
}

# === 7. Criar pasta de logging/observabilidade ===
$LogDir = Join-Path $CorePath "logging"
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir -Force }

$LogFiles = @("logging_config.py", "structured_logging.py", "metrics.py", "prometheus_metrics.py", "observability_middleware.py")
foreach ($file in $LogFiles) {
    $path = Join-Path $CorePath $file
    if (Test-Path $path) {
        Move-Item -Path $path -Destination $LogDir -Force
        Write-Log "📊 Movido: $file → /logging"
    }
}

# === 8. Mover i18n para pasta própria ===
$I18nDir = Join-Path $CorePath "i18n"
if (-not (Test-Path $I18nDir)) { New-Item -ItemType Directory -Path $I18nDir -Force }
$PathI18n = Join-Path $CorePath "i18n.py"
if (Test-Path $PathI18n) {
    Move-Item -Path $PathI18n -Destination $I18nDir -Force
    Write-Log "🌍 Movido: i18n.py → /i18n/"
}

# === 9. Limpeza final: diretórios vazios ===
Write-Log "🧹 Removendo diretórios vazios..."
Get-ChildItem -Path $CorePath -Directory -Recurse | Sort-Object FullName -Descending | ForEach-Object {
    if ((Get-ChildItem $_.FullName -Recurse -File | Measure-Object).Count -eq 0) {
        Remove-Item $_.FullName -Force
        Write-Log "EmptyEntries] Diretório vazio removido: $($_.FullName)"
    }
}

# === 10. Resumo final ===
$EndTime = Get-Date
$Duration = $EndTime - $StartTime

Write-Log "✅ Sanitização do 'backend/app/core' concluída!"
Write-Log "⏱️ Duração: $($Duration.TotalSeconds) segundos"
Write-Log "📄 Log salvo em: $LogPath"
Write-Log "💡 Próximo passo: Valide com 'generate_project_trees.ps1' e teste o sistema"