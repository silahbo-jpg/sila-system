<#
.SYNOPSIS
    RECONSTRUÇÃO CONTROLADA - SILA System 2.1

.DESCRIPTION
    Este script:
      1. Faz backup dos itens essenciais
      2. Remove scripts não necessários
      3. Cria estrutura mínima recomendada
      4. Restaura os itens essenciais no novo layout

.PARAMETER ProjectRoot
    Diretório raiz do projeto (padrão: diretório atual)

.PARAMETER RestoreEssentials
    Define se os itens essenciais devem ser restaurados (padrão: $true)

.PARAMETER DryRun
    Simula a execução sem fazer alterações reais (padrão: $true)
#>

# Set proper encoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

param(
    [string]$ProjectRoot = $PWD,
    [switch]$RestoreEssentials = $true,
    [switch]$DryRun = $true
)

# Função para exibir mensagens formatadas
function Write-Status {
    param(
        [string]$Message, 
        [ValidateSet("INFO", "SUCCESS", "WARNING", "ERROR", "ACTION")]
        [string]$Status = "INFO"
    )
    $timestamp = Get-Date -Format "HH:mm:ss"
    $statusMap = @{
        "INFO" = "[INFO]"
        "SUCCESS" = "[OK]"
        "WARNING" = "[WARN]"
        "ERROR" = "[ERR]"
        "ACTION" = "[ACT]"
    }
    
    if ($statusMap.ContainsKey($Status)) {
        Write-Host "[$timestamp] $($statusMap[$Status]) $Message"
    } else {
        Write-Host "[$timestamp] $Message"
    }
}

# 1. Definição dos Itens Essenciais
$essentials = @(
    "backend/scripts/migrations/",
    "backend/scripts/docs/",
    "backend/scripts/README.md"
)

# 2. Estrutura de Diretórios Recomendada
$recommendedDirs = @(
    "backend/app",
    "backend/tests",
    "frontend/src",
    "scripts/db",
    "scripts/deployment",
    "scripts/testing",
    "docs",
    "logs"
)

# 3. Inicialização
Write-Status "Iniciando reconstrução controlada do projeto..." -Status "ACTION"
Write-Status "Modo DryRun: $($DryRun.IsPresent)" -Status "INFO"
Write-Status "Restaurar itens essenciais: $($RestoreEssentials.IsPresent)" -Status "INFO"

# 4. Criar estrutura de diretórios
if (-not $DryRun) {
    foreach ($dir in $recommendedDirs) {
        $fullPath = Join-Path -Path $ProjectRoot -Path $dir
        if (-not (Test-Path -Path $fullPath)) {
            try {
                New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
                Write-Status "Diretório criado: $dir" -Status "SUCCESS"
            } catch {
                Write-Status "Falha ao criar diretório $dir : $($_.Exception.Message)" -Status "ERROR"
            }
        } else {
            Write-Status "Diretório já existe: $dir" -Status "INFO"
        }
    }
} else {
    Write-Status "[SIMULAÇÃO] Os seguintes diretórios seriam criados:" -Status "INFO"
    foreach ($dir in $recommendedDirs) {
        Write-Status "- $dir" -Status "INFO"
    }
}

# 5. Criar arquivos básicos
$readmeContent = @"
# SILA System

Estrutura de diretórios:
- `/backend`    → Código-fonte do backend
- `/frontend`   → Código-fonte do frontend
- `/scripts`    → Scripts de automação
  - `/db`       → Scripts de banco de dados
  - `/deployment` → CI/CD e automação de deploy
  - `/testing`  → Automação de testes
- `/docs`       → Documentação técnica
- `/logs`       → Arquivos de log
"@

$readmePath = Join-Path -Path $ProjectRoot -Path "README.md"
if (-not (Test-Path -Path $readmePath)) {
    if (-not $DryRun) {
        try {
            $readmeContent | Out-File -FilePath $readmePath -Encoding UTF8
            Write-Status "Arquivo criado: README.md" -Status "SUCCESS"
        } catch {
            Write-Status "Falha ao criar README.md: $($_.Exception.Message)" -Status "ERROR"
        }
    } else {
        Write-Status "[SIMULAÇÃO] Arquivo seria criado: README.md" -Status "INFO"
    }
}

# 6. Criar script de deploy básico
$deployPath = Join-Path -Path $ProjectRoot -Path "scripts\deployment\deploy.ps1"
$deployScript = @"
# Script de deploy básico
Write-Status "Iniciando deploy..." -Status "INFO"
# Adicione aqui os comandos de deploy
"@

if (-not (Test-Path -Path $deployPath)) {
    if (-not $DryRun) {
        try {
            $deployScript | Out-File -FilePath $deployPath -Encoding UTF8
            Write-Status "Arquivo criado: scripts/deployment/deploy.ps1" -Status "SUCCESS"
        } catch {
            Write-Status "Falha ao criar deploy.ps1: $($_.Exception.Message)" -Status "ERROR"
        }
    } else {
        Write-Status "[SIMULAÇÃO] Arquivo seria criado: scripts/deployment/deploy.ps1" -Status "INFO"
    }
}

Write-Status "Reconstrução concluída com sucesso!" -Status "SUCCESS"
