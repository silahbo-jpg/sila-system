<#
.SYNOPSIS
    Auditoria institucional de segredos com detect-secrets.

.DESCRIPTION
    - Executa varredura com exclusões padronizadas
    - Suporte a simulação segura (-DryRun)
    - Exporta para JSON, CSV e Markdown
    - Pode ser integrado ao pre-commit ou CI

.PARAMETER DryRun
    Executa simulação sem gerar arquivos reais

.PARAMETER OutputPath
    Diretório de saída para os relatórios (padrão: ./logs)

.PARAMETER ExcludeDirs
    Diretórios adicionais para exclusão (além dos padrões)

.PARAMETER FailOnSecrets
    Falha ao encontrar segredos

.PARAMETER ShortTimestamp
    Usa timestamp curto (HHmm) em vez do padrão (yyyyMMdd_HHmmss)
#>

param (
    [switch]$DryRun,
    [string]$OutputPath = ".\logs",
    [string[]]$ExcludeDirs = @(),
    [switch]$FailOnSecrets,
    [switch]$ShortTimestamp
)

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    switch ($Level) {
        "WARNING" { Write-Warning $logMessage }
        "ERROR"   { Write-Error $logMessage }
        default   { Write-Host $logMessage }
    }
}

function Ensure-DirectoryExists {
    param([string]$Path)
    if (-not (Test-Path -Path $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
        Write-Log "Created directory: $Path"
    }
}

try {
    if (-not $env:VIRTUAL_ENV) {
        Write-Log "Virtual environment not active. Please activate it first." -Level "ERROR"
        exit 1
    }

    $binPath = Join-Path $env:VIRTUAL_ENV "Scripts\detect-secrets.exe"
    if (-not (Test-Path $binPath)) {
        Write-Log "detect-secrets binary not found at $binPath" -Level "ERROR"
        exit 1
    }

    foreach ($dir in $ExcludeDirs) {
        if (-not (Test-Path $dir)) {
            Write-Log "Excluded directory not found: $dir" -Level "WARNING"
        }
    }

    Ensure-DirectoryExists -Path $OutputPath
    $timestamp = if ($ShortTimestamp) { Get-Date -Format "HHmm" } else { Get-Date -Format "yyyyMMdd_HHmmss" }
    $reportJson = Join-Path $OutputPath "secrets_${timestamp}.json"
    $reportCsv  = Join-Path $OutputPath "secrets_${timestamp}.csv"
    $reportMd   = Join-Path $OutputPath "secrets_${timestamp}.md"

    $excludeParams = @(
        "--exclude-files", "logs/",
        "--exclude-files", "node_modules/",
        "--exclude-files", "venv/",
        "--exclude-files", ".venv/"
    )

    $ExcludeDirs | ForEach-Object {
        $excludeParams += "--exclude-files"
        $excludeParams += $_
    }

    if ($DryRun) {
        Write-Log "DRY RUN: No files will be created"
        Write-Log "Command: $binPath scan $($excludeParams -join ' ')"
        exit 0
    }

    Write-Log "Starting secrets scan..."
    & $binPath scan @excludeParams | Out-File -FilePath $reportJson -Encoding utf8
    $secrets = Get-Content $reportJson -Raw | ConvertFrom-Json

    Write-Log "Exporting results to CSV..."
    "LineNumber,Type,Filename,Secret" | Out-File -Encoding UTF8 $reportCsv -Force
    $secrets.results | ForEach-Object {
        "{0},{1},{2},{3}" -f $_.lineNumber, $_.type, $_.filename, ($_.secret | ConvertTo-Json -Compress) |
        Add-Content -Encoding UTF8 $reportCsv
    }

    Write-Log "Generating Markdown report..."
    $mdContent = @"
# Relatório de Segredos - $timestamp

## Sumário
- Data: $(Get-Date -Format 'dd/MM/yyyy HH:mm')
- Total de segredos: $($secrets.results.Count)
- Diretórios excluídos: $($ExcludeDirs -join ', ')

## Detalhes
Linha | Tipo | Arquivo
----- | ---- | -------
"@

    $secrets.results | ForEach-Object {
        $mdContent += "`n{0} | {1} | {2}" -f $_.lineNumber, $_.type, $_.filename
    }

    [System.IO.File]::WriteAllText($reportMd, $mdContent, [System.Text.Encoding]::UTF8)

    if ($secrets.results.Count -gt 0) {
        Write-Log "Found $($secrets.results.Count) potential secrets. Review the reports in $OutputPath" -Level "WARNING"
        if ($FailOnSecrets) {
            Write-Log "Failing due to detected secrets (FailOnSecrets=$true)" -Level "ERROR"
            exit 1
        }
    } else {
        Write-Log "No secrets found. Security check passed." -Level "INFO"
    }

} catch {
    Write-Log "Error during execution: $_" -Level "ERROR"
    Write-Log $_.ScriptStackTrace -Level "ERROR"
    exit 1
}
