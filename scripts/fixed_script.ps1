<#
.SYNOPSIS
    Inicializa estrutura limpa do projeto SILA System
.DESCRIPTION
    Cria diretórios essenciais e arquivos padrão para organização inicial.
    Inclui validação de permissões, restauração opcional de backup e logs detalhados.
.NOTES
    Versão: 3.5 (2025-08-17)
    Autor: SILA Team
#>

# Configuração robusta de encoding UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

param(
    # Caminho raiz do projeto
    [Parameter(Mandatory=$false)]
    [string]$ProjectRoot,
    
    # Modo de simulação (não executa alterações)
    [switch]$DryRun,
    
    # Tenta restaurar arquivos essenciais de backup
    [switch]$RestoreEssentials = $true,
    
    # Sobrescreve arquivos existentes
    [switch]$Force
)

# Determina o diretório raiz padrão se não especificado
if (-not $ProjectRoot) {
    $ProjectRoot = if ($PSScriptRoot) { 
        $PSScriptRoot 
    } else { 
        $MyInvocation.MyCommand.Path | Split-Path -Parent 
    }
}

# === Função de log aprimorada ===
function Write-ProjectLog {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )

    $logEntry = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] [$Level] $Message"
    
    # Cria diretório de logs se não existir
    $logDir = Join-Path -Path $ProjectRoot -ChildPath "logs"
    if (-not (Test-Path -Path $logDir)) {
        try {
            New-Item -ItemType Directory -Path $logDir -Force | Out-Null
        } catch {
            Write-Host "[ERRO CRÍTICO] Falha ao criar diretório de logs: $($_.Exception.Message)" -ForegroundColor Red
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

# === Validação do ambiente ===
Write-ProjectLog -Message "Iniciando inicialização do projeto"
Write-ProjectLog -Message "Modo DryRun: $($DryRun.IsPresent)"
Write-ProjectLog -Message "Diretório raiz: $ProjectRoot"

# Validação do diretório base
if (-not (Test-Path -Path $ProjectRoot -PathType Container)) {
    Write-ProjectLog -Message "Caminho especificado não existe ou não é um diretório válido" -Level "ERROR"
    exit 1
}

# Validação de permissões de escrita
try {
    $testFile = Join-Path -Path $ProjectRoot -ChildPath ".__write_test_$(Get-Random).tmp"
    Set-Content -Path $testFile -Value "test" -ErrorAction Stop
    Remove-Item -Path $testFile -Force -ErrorAction Stop
} catch {
    Write-ProjectLog -Message "Falha na verificação de permissões: $($_.Exception.Message)" -Level "ERROR"
    exit 1
}

# === Estrutura de diretórios ===
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

Write-ProjectLog -Message "Criando estrutura de diretórios..."

foreach ($dir in $directories) {
    $fullPath = Join-Path -Path $ProjectRoot -ChildPath $dir
    
    if (Test-Path -Path $fullPath) {
        Write-ProjectLog -Message "Diretório já existe: $dir" -Level "WARN"
        continue
    }
    
    if ($DryRun) {
        Write-ProjectLog -Message "[SIMULAÇÃO] Criaria diretório: $fullPath"
        continue
    }
    
    try {
        New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        Write-ProjectLog -Message "Diretório criado com sucesso: $dir"
    } catch {
        Write-ProjectLog -Message ("Falha ao criar diretório {0}: {1}" -f $dir, $_.Exception.Message) -Level "ERROR"
    }
}

# === Arquivos padrão ===
$defaultFiles = @{
    "README.md" = @"
# $(Split-Path -Path $ProjectRoot -Leaf)

## Descrição
Projeto criado automaticamente em $(Get-Date -Format "dd/MM/yyyy").

## Estrutura
- `/app`: Código-fonte principal
- `/scripts`: Scripts de automação
- `/docs`: Documentação técnica

## Configuração Inicial
1. Criar ambiente virtual: `python -m venv venv`
2. Ativar ambiente:
   - Windows: `.\venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
3. Instalar dependências: `pip install -r requirements.txt`
"@

    "requirements.txt" = @"
# Lista de dependências Python
# Exemplo:
# fastapi==0.95.2
# sqlalchemy==2.0.15
# uvicorn==0.21.1
"@

    "config.yml" = @"
# Configurações básicas do projeto
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

Write-ProjectLog -Message "Criando arquivos padrão..."

foreach ($file in $defaultFiles.Keys) {
    $filePath = Join-Path -Path $ProjectRoot -ChildPath $file
    
    if ((Test-Path -Path $filePath) -and (-not $Force)) {
        Write-ProjectLog -Message "Arquivo já existe (use -Force para sobrescrever): $file" -Level "WARN"
        continue
    }
    
    if ($DryRun) {
        Write-ProjectLog -Message "[SIMULAÇÃO] Criaria arquivo: $filePath"
        continue
    }
    
    try {
        Set-Content -Path $filePath -Value $defaultFiles[$file] -Encoding UTF8 -Force
        Write-ProjectLog -Message "Arquivo criado com sucesso: $file"
    } catch {
        Write-ProjectLog -Message ("Falha ao criar arquivo {0}: {1}" -f $file, $_.Exception.Message) -Level "ERROR"
    }
}

# === Restauração de backup ===
if ($RestoreEssentials -and (-not $DryRun)) {
    Write-ProjectLog -Message "Verificando backups disponíveis..."
    
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
        Write-ProjectLog -Message "Diretório de backups não encontrado" -Level "WARN"
    }
}

# === Conclusão ===
Write-ProjectLog -Message "Inicialização do projeto concluída com sucesso!"
Write-ProjectLog -Message "Log completo disponível em: $(Join-Path -Path $ProjectRoot -ChildPath "logs")"