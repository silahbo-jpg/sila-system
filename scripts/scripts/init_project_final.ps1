<#
.SYNOPSIS
    Inicializa estrutura limpa do projeto SILA System
.DESCRIPTION
    Cria diretórios essenciais e arquivos padrão para organização inicial
    Inclui validação de permissões, restauração opcional de backup e logs.
.NOTES
    Versão: 2.2 (2025-08-17)
#>

param(
    [string]$ProjectRoot = $PWD,
    [switch]$DryRun,
    [switch]$RestoreEssentials = $true
)

# === Configuração de Encoding para suportar UTF-8 ===
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# === Função de log ===
function Write-ProjectLog {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )

    $prefix = switch ($Level) {
        "INFO"  { "✔️" }
        "WARN"  { "⚠️" }
        "ERROR" { "❌" }
        default { "ℹ️" }
    }

    if ($Level -eq "ERROR") {
        Write-Host "$prefix $Message" -ForegroundColor Red
    }
    elseif ($Level -eq "WARN") {
        Write-Host "$prefix $Message" -ForegroundColor Yellow
    }
    else {
        Write-Host "$prefix $Message" -ForegroundColor Green
    }
}

# === Validação do diretório base ===
if (-not (Test-Path -Path $ProjectRoot -PathType Container)) {
    Write-ProjectLog -Message "Caminho inválido ou não é um diretório: $ProjectRoot" -Level "ERROR"
    exit 1
}

# === Validação de permissões de escrita ===
try {
    $testFile = Join-Path $ProjectRoot ".__test_write.tmp"
    Set-Content -Path $testFile -Value "test" -ErrorAction Stop
    Remove-Item $testFile -Force
} catch {
    Write-ProjectLog -Message "Sem permissão de escrita em $ProjectRoot" -Level "ERROR"
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
    "docs"
)

foreach ($dir in $directories) {
    $path = Join-Path $ProjectRoot $dir
    if ($DryRun) {
        Write-ProjectLog -Message "[DRY-RUN] Criaria diretório: $path"
    } else {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
        Write-ProjectLog -Message "Diretório criado: $path"
    }
}

# === Arquivos padrão ===
$defaultFiles = @{
    "README.md" = @"
# $(Split-Path $ProjectRoot -Leaf)

## Descrição
Projeto criado automaticamente em $(Get-Date -Format "dd/MM/yyyy").

## Estrutura
- \`/app\`: Código-fonte principal.
- \`/scripts\`: Scripts de automação.
- \`/docs\`: Documentação.

## Próximos Passos
- Criar ambiente virtual (Python): \`python -m venv venv\`
- Ativar ambiente: 
  - Windows: \`.\venv\Scripts\activate\`
  - Linux/Mac: \`source venv/bin/activate\`
- Instalar dependências: \`pip install -r requirements.txt\`
"@

    "requirements.txt" = @"
# Dependências Python do projeto
# Exemplo:
# fastapi==0.115.0
# sqlalchemy==2.0.30
# uvicorn[standard]==0.30.0
"@

    "config.yml" = @"
# Configuração padrão do projeto SILA
app:
  name: SILA System
  version: 1.0.0

database:
  host: localhost
  port: 5432
  user: sila_user
  password: change_me
"@

    ".gitignore" = @"
# Arquivos e pastas ignorados
venv/
__pycache__/
*.log
.env
*.pyc
"@
}

foreach ($file in $defaultFiles.Keys) {
    $filePath = Join-Path $ProjectRoot $file
    if (-not (Test-Path -Path $filePath)) {
        if ($DryRun) {
            Write-ProjectLog -Message "[DRY-RUN] Criaria arquivo: $filePath"
        } else {
            Set-Content -Path $filePath -Value $defaultFiles[$file]
            Write-ProjectLog -Message "Arquivo padrão criado: $filePath"
        }
    } else {
        Write-ProjectLog -Message "Arquivo já existe, não sobrescrito: $file" -Level "WARN"
    }
}

# === Restauração opcional de backup ===
if ($RestoreEssentials -and -not $DryRun) {
    $backupSource = Get-ChildItem "$env:TEMP\sila_clean_reset_*" -ErrorAction SilentlyContinue | 
        Sort-Object LastWriteTime -Desc | Select-Object -First 1
    
    if ($backupSource) {
        Copy-Item -Path "$backupSource\*" -Destination $ProjectRoot -Recurse -Force
        Write-ProjectLog -Message "Itens essenciais restaurados de $backupSource"
    } else {
        Write-ProjectLog -Message "Nenhum backup encontrado para restaurar." -Level "WARN"
    }
}

Write-ProjectLog -Message "Inicialização concluída com sucesso!"
