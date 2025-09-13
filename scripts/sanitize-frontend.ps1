#!/usr/bin/env pwsh

# sanitize-frontend.ps1
# Sanitização da raiz do frontend (múltiplos apps)
# Coordena limpeza de webapp, mobileapp, etc.

$StartTime = Get-Date
$FrontendPath = Join-Path $PSScriptRoot "..\frontend"
$LogPath = Join-Path $PSScriptRoot "..\reports\cleanup\frontend-sanitization.log"

if (-not (Test-Path $FrontendPath)) {
    Write-Host "❌ ERRO: Pasta 'frontend' não encontrada" -ForegroundColor Red
    exit 1
}

function Write-Log { param([string]$Message) $t = Get-Date -Format "HH:mm:ss"; "[$t] $Message" | Tee-Object -FilePath $LogPath -Append }

Write-Log "🚀 Iniciando sanitização do frontend: $FrontendPath"

# === 1. Remover node_modules da raiz ===
$RootNodeModules = Join-Path $FrontendPath "node_modules"
if (Test-Path $RootNodeModules) {
    Remove-Item $RootNodeModules -Recurse -Force
    Write-Log "🗑️ Removido: node_modules (raiz)"
}

# === 2. Executar sanitização de subapps (se existirem) ===
$SubApps = @("webapp", "mobileapp", "admin")
foreach ($app in $SubApps) {
    $appPath = Join-Path $FrontendPath $app
    $scriptPath = Join-Path $PSScriptRoot "sanitize-frontend-$app.ps1"
    if (Test-Path $appPath) {
        if (Test-Path $scriptPath) {
            Write-Log "🔁 Executando script para: $app"
            & $scriptPath
        } else {
            Write-Log "⚠️ Script não encontrado para: $app"
        }
    }
}

# === 3. Atualizar .gitignore geral ===
$GitIgnore = Join-Path $FrontendPath ".gitignore"
if (-not (Test-Path $GitIgnore)) {
    "@webapp\node_modules/" | Out-File -FilePath $GitIgnore -Encoding UTF8
    Write-Log "✅ .gitignore criado"
}

# === 4. Resumo ===
$EndTime = Get-Date
$Duration = $EndTime - $StartTime
Write-Log "✅ Sanitização do frontend concluída em $($Duration.TotalSeconds)s"