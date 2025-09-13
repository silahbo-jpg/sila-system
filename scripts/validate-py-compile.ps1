# scripts/validate-py-compile.ps1
# Script para validar todos os arquivos Python do projeto usando py_compile

$ErrorActionPreference = "Stop"
$startTime = Get-Date

Write-Host "Iniciando validação completa de arquivos Python com py_compile..." -ForegroundColor Cyan

# Verifica se foram Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ados argumentos específicos
if ($args.Count -gt 0) {
    # Executa o script Python de validação com os argumentos fornecidos
    $argString = $args -join " "
    Write-Host "Validando arquivos específicos: $argString" -ForegroundColor Yellow
    python "$PSScriptsila_dev-system\validate_py_compile.py" $args
} else {
    # Executa o script Python de validação para todo o projeto
    Write-Host "Validando todos os arquivos do projeto..." -ForegroundColor Yellow
    python "$PSScriptsila_dev-system\validate_py_compile.py" --ignore-dirs archived venv .venv __pycache__ node_modules .git
}

# Verifica o resultado
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Validação falhou! Existem arquivos com erros de sintaxe." -ForegroundColor Red
    exit 1
} else {
    $endTime = Get-Date
    $duration = ($endTime - $startTime).TotalSeconds
    
    Write-Host "✅ Validação concluída com sucesso! Todos os arquivos estão com sintaxe válida." -ForegroundColor Green
    Write-Host "Tempo de execução: $([math]::Round($duration, 2)) segundos" -ForegroundColor Gray
    exit 0
}

