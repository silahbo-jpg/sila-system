﻿# Script para mover scripts obsoletos para o diretório archived

Write-Host "Movendo scripts obsoletos para o diretório archived..." -ForegroundColor Cyan

$scriptsToMove = @(
    "fix_and_migrate.ps1",
    "fix_and_migrate.sh",
    "clean_project.py"
)

$sourceDir = "$PSScriptsila_dev-system"
$targetDir = "$PSScriptsila_dev-system\archived"

# Verificar se o diretório de destino existe
if (-not (Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    Write-Host "Diretório archived criado." -ForegroundColor Green
}

# Mover cada script para o diretório archived
foreach ($script in $scriptsToMove) {
    $sourcePath = Join-Path -Path $sourceDir -ChildPath $script
    $targetPath = Join-Path -Path $targetDir -ChildPath $script
    
    if (Test-Path $sourcePath) {
        Move-Item -Path $sourcePath -Destination $targetPath -Force
        Write-Host "Movido: $script para archived/" -ForegroundColor Green
    } else {
        Write-Host "Não encontrado: $script" -ForegroundColor Yellow
    }
}

# Atualizar ARQUITETURA.md com informações sobre os scripts arquivados
$arquiteturaPath = "$PSScriptsila_dev-system\..\ARQUITETURA.md"
$logEntry = "`n`n> [$(Get-Date -Format 'yyyy-MM-dd')] Scripts obsoletos movidos para archived/:"

foreach ($script in $scriptsToMove) {
    $targetPath = Join-Path -Path $targetDir -ChildPath $script
    if (Test-Path $targetPath) {
        $logEntry += "`n- scripts/$script"
    }
}

# Adicionar entrada ao ARQUITETURA.md
Add-Content -Path $arquiteturaPath -Value $logEntry
Write-Host "`nLog adicionado ao ARQUITETURA.md" -ForegroundColor Green

Write-Host "`nProcesso de arquivamento concluído." -ForegroundColor Cyan

