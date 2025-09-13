param (
    [switch]$Restore,
    [switch]$DryRun,
    [switch]$Help
)

# Diretório raiz do backend
$projectRoot = Join-Path $PSScriptRoot "..\backend"
$logPath = Join-Path $projectRoot "logs\deps_check.log"
$jsonPath = Join-Path $projectRoot "logs\deps_status.json"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# Lista de pacotes com versão mínima
$requiredPackages = @{
    "fastapi"           = "0.110.0"
    "sqlalchemy"        = "2.0.0"
    "uvicorn"           = "0.22.0"
    "prometheus_client" = "0.17.0"
    "pydantic"          = "2.0.0"
    "httpx"             = "0.24.0"
    "python-dotenv"     = "1.0.0"
}

# Função de logging
function Write-Log {
    param ([string]$message)
    $entry = "$timestamp | $message"
    Add-Content -Path $logPath -Value $entry
    Write-Host $entry
}

# Função de ajuda
if ($Help) {
    Write-Host "`n🆘 Uso do script:"
    Write-Host "  --DryRun     Simula sem instalar pacotes"
    Write-Host "  --Restore    Modo reversível (sem efeito real)"
    Write-Host "  --Help       Exibe esta ajuda"
    return
}

# Validação de ambiente virtual
$venvActive = $env:VIRTUAL_ENV -or ($env:PATH -match "\.venv")
if (-not $venvActive) {
    Write-Log "⚠️ Ambiente virtual não detectado. Recomenda-se ativar .venv antes de continuar."
}

# Modo reversível
if ($Restore) {
    Write-Log "Modo RESTORE ativado — nenhuma ação executada."
    return
}

# Inicialização
$results = @()
$installedCount = 0
$missingCount = 0
$fixedCount = 0
$versionIssues = 0

# Validação de pacotes
foreach ($pkg in $requiredPackages.Keys) {
    $minVersion = [version]$requiredPackages[$pkg]
    $pkgInfo = pip show $pkg 2>$null

    if ($pkgInfo) {
        $versionLine = ($pkgInfo | Select-String "Version").ToString()
        $installedVersion = [version]($versionLine.Split(":")[1].Trim())

        if ($installedVersion -lt $minVersion) {
            Write-Log "⚠️ $pkg versão $installedVersion é inferior à requerida ($minVersion)."
            $versionIssues++
            if (-not $DryRun) {
                Write-Log "📦 Atualizando $pkg..."
                pip install "$pkg>=$minVersion"
                if ($LASTEXITCODE -eq 0) {
                    Write-Log "✅ $pkg atualizado para versão mínima."
                    $fixedCount++
                } else {
                    Write-Log "❌ Falha ao atualizar $pkg."
                }
            } else {
                Write-Log "🧪 Dry-run: atualização de $pkg simulada."
            }
        } else {
            Write-Log "✅ $pkg versão $installedVersion atende ao requisito."
            $installedCount++
        }
    } else {
        Write-Log "❌ $pkg ausente."
        $missingCount++
        if (-not $DryRun) {
            Write-Log "📦 Instalando $pkg..."
            pip install "$pkg>=$minVersion"
            if ($LASTEXITCODE -eq 0) {
                Write-Log "✅ Instalação de $pkg concluída."
                $fixedCount++
            } else {
                Write-Log "❌ Falha ao instalar $pkg."
            }
        } else {
            Write-Log "🧪 Dry-run: instalação de $pkg simulada."
        }
    }

    # Registro JSON
    $results += [PSCustomObject]@{
        package         = $pkg
        requiredVersion = "$minVersion"
        status          = if ($pkgInfo) {
            if ($installedVersion -lt $minVersion) { "versão insuficiente" } else { "ok" }
        } else { "ausente" }
        installedVersion = if ($pkgInfo) { "$installedVersion" } else { "n/a" }
    }
}

# Exporta JSON
$results | ConvertTo-Json -Depth 3 | Set-Content -Path $jsonPath

# Resumo final
Write-Host "`n📊 Resumo:" -ForegroundColor Yellow
Write-Host "Total de pacotes críticos: $($requiredPackages.Count)"
Write-Host "✅ Válidos: $installedCount"
Write-Host "⚠️ Versão insuficiente: $versionIssues"
Write-Host "❌ Ausentes: $missingCount"
Write-Host "➕ Corrigidos: $fixedCount"
Write-Host "📄 Log salvo em: $logPath"
Write-Host "📦 Status JSON: $jsonPath"
