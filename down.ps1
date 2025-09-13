<#
.SYNOPSIS
Script para parar containers do projeto Sila.
.PARAMETER Mode
Modo de execução: 'dev' ou 'prod'. Default: dev
#>

param(
    [ValidateSet("dev", "prod")]
    [string]$Mode = "dev"
)

function Resolve-ComposeCmd {
    try {
        $null = & docker compose version 2>$null
        if ($LASTEXITCODE -eq 0) { return @("docker","compose") }
    } catch {}
    if (Get-Command docker-compose -ErrorAction SilentlyContinue) { return @("docker-compose") }
    throw "Docker Compose não encontrado."
}

$PROJECT_ROOT = "C:\Users\User5\Music\MEGA1\sila\sila-system"
if (-not (Test-Path $PROJECT_ROOT)) {
    Write-Host "❌ Diretório do projeto não encontrado: $PROJECT_ROOT" -ForegroundColor Red
    exit 1
}
Set-Location $PROJECT_ROOT

try {
    $composeCmd = Resolve-ComposeCmd
    Write-Host "🛑 Parando containers ($Mode)..." -ForegroundColor Yellow
    & $composeCmd down
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Containers parados com sucesso." -ForegroundColor Green
    } else {
        throw "Falha ao parar containers."
    }
}
catch {
    Write-Host "❌ Erro: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}