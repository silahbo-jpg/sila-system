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

param(
    [string]$ProjectRoot = $PWD,
    [switch]$RestoreEssentials = $true,
    [switch]$DryRun = $true
)

# Função para exibir mensagens formatadas
function Write-Status {
    param([string]$Message, [string]$Status = "INFO")
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
    "backend/scripts/README.md",
    "backend/scripts/requirements-db.txt",
    "backend/scripts/setup_database.py",
    "backend/scripts/test_db_connection.py"
)

# 2. Criar backup dos itens essenciais
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = Join-Path $env:TEMP "sila_clean_reset_$timestamp"

Write-Status "Criando backup dos itens essenciais em: $backupDir" -Status "INFO"
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null

$essentials | ForEach-Object {
    $sourcePath = Join-Path $ProjectRoot $_
    if (Test-Path $sourcePath) {
        $targetPath = Join-Path $backupDir ($_ -replace '[\/]', '\')
        $targetDir = Split-Path -Parent $targetPath
        
        if (-not (Test-Path $targetDir)) {
            New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
        }
        
        Copy-Item -Path $sourcePath -Destination $targetPath -Recurse -Force
        Write-Status "  ✓ Backup: $_" -Status "SUCCESS"
    } else {
        Write-Status "  ⚠️ Não encontrado: $_" -Status "WARNING"
    }
}

# 3. Limpeza Segura
Write-Status "Iniciando limpeza da estrutura antiga..." -Status "ACTION"

$targets = @(
    "$ProjectRoot\scripts",
    "$ProjectRoot\backend\scripts"
)

$filesToDelete = Get-ChildItem -Path $targets -Recurse -ErrorAction SilentlyContinue | 
    Where-Object { $_.FullName -notmatch "\\backup\\|\\archived\\|\\docs\\|\\migrations\\" }

if ($DryRun) {
    Write-Status "MODO SIMULAÇÃO (DryRun) - Nenhum arquivo será removido" -Status "WARNING"
    $filesToDelete | ForEach-Object {
        Write-Status "  📄 Seria removido: $($_.FullName.Substring($ProjectRoot.Length))" -Status "INFO"
    }
} else {
    $filesToDelete | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    Write-Status "Limpeza concluída. Itens removidos: $($filesToDelete.Count)" -Status "SUCCESS"
}

# 4. Criar Nova Estrutura
Write-Status "Criando nova estrutura de diretórios..." -Status "ACTION"

$newCoreStructure = @(
    "scripts/deployment",
    "scripts/database",
    "scripts/testing",
    "scripts/maintenance",
    "scripts/docs"
)

$newCoreStructure | ForEach-Object {
    $fullPath = Join-Path $ProjectRoot $_
    if (-not (Test-Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        Write-Status "  ✓ Criado: $_" -Status "SUCCESS"
    }
}

# 5. Restaurar Itens Essenciais
if ($RestoreEssentials -and (Test-Path $backupDir)) {
    Write-Status "Restaurando itens essenciais..." -Status "ACTION"
    
    Get-ChildItem -Path $backupDir -Recurse | ForEach-Object {
        $relativePath = $_.FullName.Substring($backupDir.Length).TrimStart('\\')
        $targetPath = Join-Path $ProjectRoot $relativePath
        
        if ($_.PSIsContainer) {
            if (-not (Test-Path $targetPath)) {
                New-Item -ItemType Directory -Path $targetPath -Force | Out-Null
                Write-Status "  ✓ Criado diretório: $relativePath" -Status "SUCCESS"
            }
        } else {
            Copy-Item -Path $_.FullName -Destination $targetPath -Force
            Write-Status "  ✓ Restaurado: $relativePath" -Status "SUCCESS"
        }
    }
}

# 6. Criar Arquivos Básicos
Write-Status "Criando arquivos básicos..." -Status "ACTION"

# Arquivo de deploy
$deployScript = @"
param(
    [string]`$Environment = "production"
)

Write-Host "🚀 Iniciando deploy no ambiente: `$Environment"
# Adicione aqui os comandos de deploy
"@

$deployPath = Join-Path $ProjectRoot "scripts\deployment\deploy.ps1"
if (-not (Test-Path $deployPath)) {
    $deployScript | Out-File -FilePath $deployPath -Encoding UTF8
    Write-Status "  ✓ Criado: scripts/deployment/deploy.ps1" -Status "SUCCESS"
}

# README
$readmeContent = @"
# Estrutura de Scripts

- `/deployment`   → CI/CD e automação de deploy
- `/database`     → Migrações e scripts do banco de dados
- `/testing`      → Automação de testes
- `/maintenance`  → Limpeza, backups e utilitários
- `/docs`         → Documentação técnica

## Uso

- Para limpar e reconstruir a estrutura:
  ```powershell
  .\scripts\init_project.ps1 -DryRun:`$false
  ```
"@

$readmePath = Join-Path $ProjectRoot "scripts\README.md"
if (-not (Test-Path $readmePath)) {
    $readmeContent | Out-File -FilePath $readmePath -Encoding UTF8
    Write-Status "  ✓ Criado: scripts/README.md" -Status "SUCCESS"
}

Write-Status "Processo concluído com sucesso!" -Status "SUCCESS"

if ($DryRun) {
    Write-Host "\n⚠️  MODO SIMULAÇÃO ATIVADO. Para executar as alterações, use: " -ForegroundColor Yellow -NoNewline
    Write-Host ".\scripts\init_project.ps1 -DryRun:`$false" -ForegroundColor White -BackgroundColor DarkGray
}
