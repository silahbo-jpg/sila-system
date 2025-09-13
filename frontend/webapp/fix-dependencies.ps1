param(
    [Parameter(Mandatory=$false)]
    [ValidateSet('dev', 'homolog', 'prod')]
    [string]$Ambiente = "dev",
    
    [Parameter(Mandatory=$false)]
    [switch]$DryRun,
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipAudit,
    
    [Parameter(Mandatory=$false)]
    [string]$LogDirectory = (Join-Path $PSScriptRoot "..\..\logs")
)

#region Inicialização e Configuração
$ErrorActionPreference = 'Stop'
$executionStart = Get-Date
$timestamp = $executionStart.ToString("yyyyMMdd-HHmmss")

# Configuração de Logs
$logFile = Join-Path $LogDirectory "deps_${Ambiente}_${timestamp}.log"
$csvFile = Join-Path $LogDirectory "deps_${Ambiente}_${timestamp}.csv"
$dependencyLogs = [System.Collections.Generic.List[PSObject]]::new()

# Criar diretório de logs se não existir
if (-not (Test-Path $LogDirectory)) {
    New-Item -ItemType Directory -Path $LogDirectory -Force | Out-Null
}
#endregion

#region Funções de Log
function Write-Log {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$Message,
        
        [Parameter(Mandatory=$false)]
        [ValidateSet('INFO', 'WARNING', 'ERROR', 'SUCCESS', 'DEBUG')]
        [string]$Level = 'INFO',
        
        [Parameter(Mandatory=$false)]
        [switch]$NoConsole
    )
    
    $logMessage = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss.fff')] [$Level] $Message"
    
    # Adicionar ao log estruturado
    $logEntry = [PSCustomObject]@{
        Timestamp   = Get-Date -Format 'yyyy-MM-dd HH:mm:ss.fff'
        Level       = $Level
        Message     = $Message
        Environment = $Ambiente
        DryRun      = $DryRun
    }
    
    $script:dependencyLogs.Add($logEntry)
    
    # Saída para console (a menos que suprimido)
    if (-not $NoConsole) {
        $colorMap = @{
            'ERROR'   = 'Red'
            'WARNING' = 'Yellow'
            'SUCCESS' = 'Green'
            'DEBUG'   = 'Gray'
            'INFO'    = 'White'
        }
        
        $color = $colorMap[$Level]
        Write-Host $logMessage -ForegroundColor $color
    }
    
    # Escrever no arquivo de log
    Add-Content -Path $logFile -Value $logMessage -Encoding UTF8 -Force
}

function Register-Dependency {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$Name,
        
        [Parameter(Mandatory=$true)]
        [string]$Type,
        
        [Parameter(Mandatory=$true)]
        [ValidateSet('SUCCESS', 'ERROR', 'WARNING', 'SKIPPED')]
        [string]$Status,
        
        [Parameter(Mandatory=$false)]
        [string]$Version = '',
        
        [Parameter(Mandatory=$false)]
        [string]$Message = ''
    )
    
    $entry = [PSCustomObject]@{
        Timestamp   = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss.fff")
        Dependencia = $Name
        Tipo        = $Type
        Status      = $Status
        Versao      = $Version
        Mensagem    = $Message
        Ambiente    = $script:Ambiente
        DryRun      = $script:DryRun
    }
    
    $script:dependencyLogs.Add($entry)
    Write-Log "$($Status.PadRight(7)) - $($Type.PadRight(15)): $Name $Version $Message" -Level $Status
}
#endregion

#region Validação de Ambiente
try {
    Write-Log "Iniciando execução do script" -Level 'INFO'
    Write-Log "Ambiente: $Ambiente" -Level 'INFO'
    Write-Log "Modo DryRun: $($DryRun.IsPresent)" -Level 'INFO'
    
    # Verificar Node.js e npm
    if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
        throw "Node.js não está instalado"
    }
    
    if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
        throw "npm não está disponível"
    }
    
    # Verificar diretório do projeto
    $packagePath = Join-Path $PSScriptRoot "package.json"
    if (-not (Test-Path $packagePath)) {
        throw "Arquivo package.json não encontrado em $PSScriptRoot"
    }
    
    Write-Log "Pré-validações concluídas com sucesso" -Level 'SUCCESS'
    
} catch {
    Write-Log "Falha na validação inicial: $_" -Level 'ERROR'
    exit 1
}
#endregion

#region Instalação de Dependências
try {
    Push-Location $PSScriptRoot
    
    # Dependências de produção
    $dependencies = @(
        @{ Name = "axios"; Version = "^1.6.2" },
        @{ Name = "formik"; Version = "^2.4.5" },
        @{ Name = "react-icons"; Version = "^4.12.0" },
        @{ Name = "react-query"; Version = "^3.39.3" },
        @{ Name = "react-router-dom"; Version = "^6.21.1" },
        @{ Name = "yup"; Version = "^1.3.3" }
    )
    
    # Dependências de desenvolvimento
    $devDependencies = @(
        @{ Name = "@compodoc/compodoc"; Version = "^1.1.26" },
        @{ Name = "cypress"; Version = "^13.6.0" },
        @{ Name = "detect-secrets"; Version = "^1.4.0" },
        @{ Name = "@types/node"; Version = "^20.10.5" },
        @{ Name = "npm-audit-ci"; Version = "^5.0.0" }
    )
    
    # Função para instalar dependências
    function Install-Dependencies {
        param(
            [array]$Dependencies,
            [switch]$Dev
        )
        
        foreach ($dep in $Dependencies) {
            $name = $dep.Name
            $version = $dep.Version
            $fullName = "${name}@${version}"
            
            try {
                if ($DryRun) {
                    Register-Dependency -Name $name -Type "Dependência" -Status "SKIPPED" -Version $version -Message "[DRY RUN]"
                    continue
                }
                
                $installCmd = if ($Dev) { "npm install --save-dev $fullName" } else { "npm install $fullName" }
                Write-Log "Executando: $installCmd" -Level 'DEBUG'
                
                $output = & { if ($Dev) { npm install --save-dev $fullName } else { npm install $fullName } } 2>&1
                $installedVersion = (npm list $name --depth=0 --json 2>$null | ConvertFrom-Json).dependencies.$name.version
                
                Register-Dependency -Name $name -Type "Dependência" -Status "SUCCESS" -Version $installedVersion
                
            } catch {
                Register-Dependency -Name $name -Type "Dependência" -Status "ERROR" -Version $version -Message $_.Exception.Message
            }
        }
    }
    
    # Instalar dependências
    Write-Log "Iniciando instalação de dependências..." -Level 'INFO'
    Install-Dependencies -Dependencies $dependencies
    Install-Dependencies -Dependencies $devDependencies -Dev
    
    # Atualizar package.json
    if (-not $DryRun) {
        try {
            $packageJson = Get-Content -Raw -Path "package.json" | ConvertFrom-Json
            
            $packageJson.scripts = @{
                "start"         = "react-scripts start"
                "build"         = "react-scripts build"
                "test"          = "react-scripts test"
                "eject"         = "react-scripts eject"
                "compodoc"      = "compodoc -p tsconfig.json -d ../docs/frontend"
                "cy:run"        = "cypress run"
                "test:ci"       = "react-scripts test --ci --coverage"
                "security-scan" = "detect-secrets scan --update .secrets.baseline"
            }
            
            $packageJson | ConvertTo-Json -Depth 10 | Set-Content "package.json" -Encoding UTF8
            Write-Log "package.json atualizado com sucesso" -Level 'SUCCESS'
            
        } catch {
            Write-Log "Erro ao atualizar package.json: $_" -Level 'ERROR'
        }
    }
    
    # Executar auditoria de segurança
    if (-not $SkipAudit -and -not $DryRun) {
        try {
            Write-Log "Executando auditoria de segurança..." -Level 'INFO'
            $audit = npm audit --json 2>$null | ConvertFrom-Json
            
            if ($audit.metadata.vulnerabilities) {
                foreach ($severity in $audit.metadata.vulnerabilities.PSObject.Properties) {
                    if ($severity.Value -gt 0) {
                        Write-Log "$($severity.Name): $($severity.Value) vulnerabilidades encontradas" -Level 'WARNING'
                    }
                }
            }
            
            # Verificar pacotes desatualizados
            $outdated = npm outdated --json 2>$null | ConvertFrom-Json
            if ($outdated) {
                foreach ($pkg in $outdated.PSObject.Properties) {
                    Write-Log "Atualização disponível: $($pkg.Name) (atual: $($pkg.Value.current), mais recente: $($pkg.Value.latest))" -Level 'WARNING'
                }
            }
            
        } catch {
            Write-Log "Erro durante auditoria: $_" -Level 'ERROR'
        }
    }
    
} catch {
    Write-Log "Erro durante a instalação: $_" -Level 'ERROR'
    Write-Log $_.ScriptStackTrace -Level 'DEBUG' -NoConsole
    
} finally {
    # Exportar relatório CSV
    try {
        $csvData = $dependencyLogs | Where-Object { $_ -is [System.Management.Automation.PSCustomObject] } | 
            Select-Object Timestamp, Dependencia, Tipo, Status, Versao, Mensagem, Ambiente, DryRun
            
        $csvData | Export-Csv -Path $csvFile -NoTypeInformation -Encoding UTF8 -Delimiter ';' -Force
        
    } catch {
        Write-Log "Erro ao exportar relatório CSV: $_" -Level 'ERROR'
    }
    
    # Resumo da execução
    $endTime = Get-Date
    $duration = New-TimeSpan -Start $executionStart -End $endTime
    
    $summary = @"

=== RESUMO DA EXECUÇÃO ===
Início:       $($executionStart.ToString('yyyy-MM-dd HH:mm:ss'))
Término:      $($endTime.ToString('yyyy-MM-dd HH:mm:ss'))
Duração:      $($duration.ToString('hh\:mm\:ss'))
Ambiente:     $Ambiente
Modo DryRun:  $($DryRun.IsPresent)

ESTATÍSTICAS:
Total:        $($dependencyLogs.Count)
Sucesso:      $(($dependencyLogs | Where-Object { $_.Status -eq 'SUCCESS' }).Count)
Avisos:       $(($dependencyLogs | Where-Object { $_.Status -eq 'WARNING' }).Count)
Erros:        $(($dependencyLogs | Where-Object { $_.Status -eq 'ERROR' }).Count)
Pulados:      $(($dependencyLogs | Where-Object { $_.Status -eq 'SKIPPED' }).Count)

LOGS:
- Detalhado:  $logFile
- Estruturado: $csvFile
"@
    
    Write-Host $summary -ForegroundColor Cyan
    Add-Content -Path $logFile -Value $summary -Encoding UTF8
    
    Pop-Location | Out-Null
}
