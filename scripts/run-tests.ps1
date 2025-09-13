# ==============================
# 🚀 SILA System Test Runner
# Arquivo: scripts\run-tests.ps1
# ==============================

$ErrorActionPreference = "Stop"

Write-Host "`n🚀 SILA System Test Runner"
Write-Host "============================="

# Caminho da raiz do projeto (subindo uma pasta a partir de /scripts)
$projectRoot = Split-Path $PSScriptRoot -Parent

# Caminho do ambiente virtual
$venvPath = Join-Path $projectRoot "backend\.venv\Scripts\Activate.ps1"

# Verifica se o ambiente virtual existe
if (-Not (Test-Path $venvPath)) {
    Write-Host "❌ Error: Activation script not found at: $venvPath" -ForegroundColor Red
    Write-Host "💡 Dica: crie o ambiente com:" -ForegroundColor Yellow
    Write-Host "    python -m venv backend\.venv" -ForegroundColor Yellow
    exit 1
}

# Ativa o ambiente virtual
Write-Host "`n🔧 Activating virtual environment..."
& $venvPath

# Configura PYTHONPATH (pasta backend)
$env:PYTHONPATH = Join-Path $projectRoot "backend"
Write-Host "`n📂 PYTHONPATH definido para $env:PYTHONPATH" -ForegroundColor Green

# Executa os testes com pytest
Write-Host "`n🚀 Executando testes..." -ForegroundColor Cyan
pytest backend/tests --tb=short -v -s

# Mensagem final
if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Todos os testes passaram com sucesso!" -ForegroundColor Green
} else {
    Write-Host "`n❌ Alguns testes falharam. Verifique os logs acima." -ForegroundColor Red
}
