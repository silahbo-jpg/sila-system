<#
.SYNOPSIS
    Inicializa estrutura limpa do projeto SILA System
.DESCRIPTION
    Cria diretÃ³rios essenciais e arquivos padrÃ£o para organizaÃ§Ã£o inicial.
    Inclui validaÃ§Ã£o de permissÃµes, restauraÃ§Ã£o opcional de backup e logs detalhados.
.NOTES
    VersÃ£o: 3.5 (2025-08-17)
    Autor: SILA Team
#>

# ConfiguraÃ§Ã£o robusta de encoding UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

param(
    # Caminho raiz do projeto
    [Parameter(Mandatory=$false)]
    [string]$ProjectRoot,
    
    # Modo de simulaÃ§Ã£o (nÃ£o executa alteraÃ§Ãµes)
    [switch]$DryRun,
    
    # Tenta restaurar arquivos essenciais de backup
    [switch]$RestoreEssentials = $true,
    
    # Sobrescreve arquivos existentes
    [switch]$Force
)

# Determina o diretÃ³rio raiz padrÃ£o se nÃ£o especificado
if (-not $ProjectRoot) {
    $ProjectRoot = if ($PSScriptRoot) { 
        $PSScriptRoot 
    } else { 
        $MyInvocation.MyCommand.Path | Split-Path -Parent 
    }
}

# === FunÃ§Ã£o de log aprimorada ===
function Write-ProjectLog {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )

    $logEntry = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] [$Level] $Message"
    
    # Cria diretÃ³rio de logs se nÃ£o existir
    $logDir = Join-Path -Path $ProjectRoot -ChildPath "logs"
    if (-not (Test-Path -Path $logDir)) {
        try {
            New-Item -ItemType Directory -Path $logDir -Force | Out-Null
        } catch {
            Write-Host "[ERRO CRÃTICO] Falha ao criar diretÃ³rio de logs: $($_.Exception.Message)" -ForegroundColor Red
            exit 1
        }
    }
    
    # Adiciona ao arquivo de log
    $logFile = Join-Path -Path $logDir -ChildPath "project_init_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
    try {
        Add-Content -Path $logFile -Value $logEntry -Encoding UTF8
    } catch {
        Write-Host "[ERRO] Falha ao escrever no log: $($_.Exception.Message)" -ForegroundColor Yellow
    }
    
    # Exibe no console com cores
    switch ($Level) {
        "ERROR" { Write-Host $logEntry -ForegroundColor Red }
        "WARN"  { Write-Host $logEntry -ForegroundColor Yellow }
        default { Write-Host $logEntry -ForegroundColor Green }
    }
}

# === ValidaÃ§Ã£o do ambiente ===
Write-ProjectLog -Message "Iniciando inicializaÃ§Ã£o do projeto"
Write-ProjectLog -Message "Modo DryRun: $($DryRun.IsPresent)"
Write-ProjectLog -Message "DiretÃ³rio raiz: $ProjectRoot"

# ValidaÃ§Ã£o do diretÃ³rio base
if (-not (Test-Path -Path $ProjectRoot -PathType Container)) {
    Write-ProjectLog -Message "Caminho especificado nÃ£o existe ou nÃ£o Ã© um diretÃ³rio vÃ¡lido" -Level "ERROR"
    exit 1
}

# ValidaÃ§Ã£o de permissÃµes de escrita
try {
    $testFile = Join-Path -Path $ProjectRoot -ChildPath ".__write_test_$(Get-Random).tmp"
    Set-Content -Path $testFile -Value "test" -ErrorAction Stop
    Remove-Item -Path $testFile -Force -ErrorAction Stop
} catch {
    Write-ProjectLog -Message "Falha na verificaÃ§Ã£o de permissÃµes: $($_.Exception.Message)" -Level "ERROR"
    exit 1
}

# === Estrutura de diretÃ³rios ===
$directories = @(
    "app/models",
    "app/services",
    "app/core",
    "app/api/v1",
    "app/utils",
    "app/tests",
    "scripts/db",
    "scripts/deploy",
    "scripts/utils",
    "docs",
    "logs"
)

Write-ProjectLog -Message "Criando estrutura de diretÃ³rios..."

foreach ($dir in $directories) {
    $fullPath = Join-Path -Path $ProjectRoot -ChildPath $dir
    
    if (Test-Path -Path $fullPath) {
        Write-ProjectLog -Message "DiretÃ³rio jÃ¡ existe: $dir" -Level "WARN"
        continue
    }
    
    if ($DryRun) {
        Write-ProjectLog -Message "[SIMULAÃ‡ÃƒO] Criaria diretÃ³rio: $fullPath"
        continue
    }
    
    try {
        New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        Write-ProjectLog -Message "DiretÃ³rio criado com sucesso: $dir"
    } catch {
        Write-ProjectLog -Message ("Falha ao criar diretÃ³rio {0}: {1}" -f $dir, $_.Exception.Message) -Level "ERROR"
    }
}

# === Arquivos padrÃ£o ===
$defaultFiles = @{
    "README.md" = @"
# $(Split-Path -Path $ProjectRoot -Leaf)

## DescriÃ§Ã£o
Projeto criado automaticamente em $(Get-Date -Format "dd/MM/yyyy").

## Estrutura
- `/app`: CÃ³digo-fonte principal
- `/scripts`: Scripts de automaÃ§Ã£o
- `/docs`: DocumentaÃ§Ã£o tÃ©cnica

## ConfiguraÃ§Ã£o Inicial
1. Criar ambiente virtual: `python -m venv venv`
2. Ativar ambiente:
   - Windows: `.\venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
3. Instalar dependÃªncias: `pip install -r requirements.txt`
"@

    "requirements.txt" = @"
# Lista de dependÃªncias Python
# Exemplo:
# fastapi==0.95.2
# sqlalchemy==2.0.15
# uvicorn==0.21.1
"@

    "config.yml" = @"
# ConfiguraÃ§Ãµes bÃ¡sicas do projeto
app:
  name: "SILA System"
  version: "1.0.0"
  debug: false

database:
  host: "localhost"
  port: 5432
  username: "sila_user"
  password: "change_me"
"@

    ".gitignore" = @"
# Arquivos ignorados pelo Git
venv/
__pycache__/
*.py[cod]
*.log
.env
.DS_Store
.idea/
.vscode/
"@
}

Write-ProjectLog -Message "Criando arquivos padrÃ£o..."

foreach ($file in $defaultFiles.Keys) {
    $filePath = Join-Path -Path $ProjectRoot -ChildPath $file
    
    if ((Test-Path -Path $filePath) -and (-not $Force)) {
        Write-ProjectLog -Message "Arquivo jÃ¡ existe (use -Force para sobrescrever): $file" -Level "WARN"
        continue
    }
    
    if ($DryRun) {
        Write-ProjectLog -Message "[SIMULAÃ‡ÃƒO] Criaria arquivo: $filePath"
        continue
    }
    
    try {
        Set-Content -Path $filePath -Value $defaultFiles[$file] -Encoding UTF8 -Force
        Write-ProjectLog -Message "Arquivo criado com sucesso: $file"
    } catch {
        Write-ProjectLog -Message ("Falha ao criar arquivo {0}: {1}" -f $file, $_.Exception.Message) -Level "ERROR"
    }
}

# === RestauraÃ§Ã£o de backup ===
if ($RestoreEssentials -and (-not $DryRun)) {
    Write-ProjectLog -Message "Verificando backups disponÃ­veis..."
    
    $backupDir = Join-Path -Path $env:TEMP -ChildPath "sila_backups"
    if (Test-Path -Path $backupDir) {
        $latestBackup = Get-ChildItem -Path $backupDir | Sort-Object LastWriteTime -Descending | Select-Object -First 1
        
        if ($latestBackup) {
            try {
                Write-ProjectLog -Message "Restaurando backup: $($latestBackup.Name)"
                Copy-Item -Path "$($latestBackup.FullName)\*" -Destination $ProjectRoot -Recurse -Force
                Write-ProjectLog -Message "Backup restaurado com sucesso"
            } catch {
                Write-ProjectLog -Message "Falha ao restaurar backup: $($_.Exception.Message)" -Level "ERROR"
            }
        } else {
            Write-ProjectLog -Message "Nenhum backup encontrado para restaurar" -Level "WARN"
        }
    } else {
        Write-ProjectLog -Message "DiretÃ³rio de backups nÃ£o encontrado" -Level "WARN"
    }
}

# === ConclusÃ£o ===
Write-ProjectLog -Message "InicializaÃ§Ã£o do projeto concluÃ­da com sucesso!"
Write-ProjectLog -Message "Log completo disponÃ­vel em: $(Join-Path -Path $ProjectRoot -ChildPath "logs")"
