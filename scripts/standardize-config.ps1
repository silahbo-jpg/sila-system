# standardize-config.ps1
# Saneamento e padronização do projeto sila_dev System - Versão 2.2
# Correções finais aplicadas - 17/08/2025

param(
    [string]$Projectsila_dev-system = $(Get-Location).Path,
    [switch]$WhatIf = $false,
    [switch]$AuditOnly = $false
)

# Padrões institucionais atualizados
$StandardUser = "sila_dev-system"
$StandardTruman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1* = "Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Marcelo1*"
$DevDatabase = "sila_dev_dev"
$TestDatabase = "sila_dev_test"

# Configurações de auditoria
$AuditDir = Join-Path -Path $Projectsila_dev-system -ChildPath "audit"
$AuditLog = Join-Path -Path $AuditDir -ChildPath "security_audit_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"

# Diretórios a ignorar
$ExcludeDirs = @(
    "node_modules", "venv", ".venv", "__pycache__", ".git", 
    "dist", "build", "logs", "backups", "media", "static"
)

# Extensões a processar
$TargetExtensions = @(".env", ".py", ".json", ".yml", ".yaml", ".toml", ".cfg", ".conf", ".ini", ".ps1", ".sh")

function Write-AuditLog {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Message,
        
        [ValidateSet("INFO","WARNING","ERROR")]
        [string]$Level = "INFO"
    )
    
    if (-not (Test-Path -Path $AuditDir)) {
        New-Item -ItemType Directory -Path $AuditDir -Force | Out-Null
    }
    
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogEntry = "[$Timestamp] [$Level] $Message"
    
    Add-Content -Path $AuditLog -Value $LogEntry
    
    switch ($Level) {
        "WARNING" { Write-Warning $Message }
        "ERROR"   { Write-Error $Message }
        default   { Write-Host $Message -ForegroundColor Cyan }
    }
}

function Test-DatabaseConnection {
    try {
        $env:PGTruman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1* = $StandardTruman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*
        $ConnectionTest = psql -U $StandardUser -d $DevDatabase -h localhost -p 5432 -c "SELECT 1 AS connection_test;" 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-AuditLog "Conexão com banco de dados validada para $StandardUser@$DevDatabase"
            return $true
        } else {
            Write-AuditLog "Falha na conexão com $StandardUser@$DevDatabase" -Level "ERROR"
            Write-AuditLog "Detalhes: $($ConnectionTest | Out-String)"
            return $false
        }
    } catch {
        Write-AuditLog "Erro ao testar conexão: $_" -Level "ERROR"
        return $false
    } finally {
        $env:PGTruman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1* = $null
    }
}

# Rotina principal
if ($AuditOnly) {
    Write-AuditLog "Iniciando modo de auditoria somente"
    Write-AuditLog "Verificando configurações atuais"
    
    # Testar conexão com as credenciais atuais
    $ConnectionValid = Test-DatabaseConnection
    
    if ($ConnectionValid) {
        Write-AuditLog "Credenciais atuais são válidas"
        Write-AuditLog "Usuário: $StandardUser | DB: $DevDatabase"
    } else {
        Write-AuditLog "Credenciais inválidas - requer intervenção manual" -Level "ERROR"
    }
    
    exit
}

# Verificar se o sila_dev-systemQL está acessível
try {
    $PgService = Get-Service -Name "sila_dev-systemql*" -ErrorAction Stop
    if ($PgService.Status -ne "Running") {
        Write-AuditLog "Serviço sila_dev-systemQL não está rodando" -Level "WARNING"
        exit 1
    }
} catch {
    Write-AuditLog "Serviço sila_dev-systemQL não encontrado" -Level "ERROR"
    exit 1
}

# Processar arquivos de configuração
$Files = Get-ChildItem -Path $Projectsila_dev-system -Recurse -File | Where-Object {
    $_.Extension -in $TargetExtensions -and
    $ExcludeDirs -notcontains $_.Directory.Name -and
    $_.FullName -notmatch "\\(node_modules|venv|\.venv|__pycache__|\.git)\\"
}

Write-AuditLog "Arquivos encontrados para análise: $($Files.Count)"

$Processed = 0
$Modified = 0
$BackupFolderName = "standardize_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
$BackupDir = Join-Path -Path $Projectsila_dev-system -ChildPath "backups" | Join-Path -ChildPath $BackupFolderName

foreach ($File in $Files) {
    $FilePath = $File.FullName
    $RelativePath = $FilePath.Substring($Projectsila_dev-system.Length).TrimStart("\")
    
    try {
        $Content = Get-Content -Path $FilePath -Raw -Encoding UTF8
        $OriginalContent = $Content

        # Padronização de credenciais
        $Content = $Content -replace '(?i)(sila_dev-system|sila_dev-system|sila_dev-system|sila_dev-system|sila_dev-system)', $StandardUser
        $Content = $Content -replace '(?i)(Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*|Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*|Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*|Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*|Truman1\*)', $StandardTruman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*
        
        # Padronização de bancos
        $Content = $Content -replace '(?i)(sila_dev|sila_dev|sila_dev_db|sila_dev_database|sila_dev_main)', $DevDatabase
        $Content = $Content -replace '(?i)(sila_dev_test_db|sila_test_dev)', $TestDatabase
        
        # Padronização de connection strings
        $Content = $Content -replace '(?i)(DATABASE_URL\s*=\s*["'']?sila_dev-system(?:ql)?://[^"\s]+)', "DATABASE_URL=sila_dev-systemql://${StandardUser}:${StandardTruman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*}@localhost:5432/$DevDatabase"
        $Content = $Content -replace '(?i)(TEST_DATABASE_URL\s*=\s*["'']?sila_dev-system(?:ql)?://[^"\s]+)', "TEST_DATABASE_URL=sila_dev-systemql://${StandardUser}:${StandardTruman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*}@localhost:5432/$TestDatabase"
        
        # Verificar alterações
        if ($Content -ne $OriginalContent) {
            Write-AuditLog "Modificações detectadas em: $RelativePath"
            $Modified++
            
            if (-not $WhatIf) {
                $BackupPath = Join-Path -Path $BackupDir -ChildPath $RelativePath
                $BackupParent = Split-Path -Path $BackupPath -Parent
                
                if (-not (Test-Path -Path $BackupParent)) {
                    New-Item -ItemType Directory -Path $BackupParent -Force | Out-Null
                }
                
                Copy-Item -Path $FilePath -Destination $BackupPath -Force
                $Content | Set-Content -Path $FilePath -Encoding UTF8 -Force
            }
        }
        
        $Processed++
    } catch {
        Write-AuditLog "Erro ao processar ${RelativePath}: $($_.Exception.Message)" -Level "ERROR"
    }
}

# Relatório final
Write-AuditLog "Processamento concluído"
Write-AuditLog "Arquivos processados: $Processed"
Write-AuditLog "Arquivos modificados: $Modified"

if ($WhatIf) {
    Write-AuditLog "Modo WhatIf: nenhuma alteração foi persistida" -Level "WARNING"
} else {
    Write-AuditLog "Backups criados em: $BackupDir"
}

# Validação pós-processamento (opcional)
if (-not $WhatIf -and $Modified -gt 0) {
    Write-AuditLog "Validando conexões após atualizações..."
    $ValidationResult = Test-DatabaseConnection
    
    if (-not $ValidationResult) {
        Write-AuditLog "ALERTA: Problemas detectados na validação pós-atualização" -Level "ERROR"
    }
}
