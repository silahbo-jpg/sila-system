<#
.SYNOPSIS
Script unificado para subir ambiente Dev ou Prod do projeto Sila.

.PARAMETER Mode
Modo de execução: 'dev' (hot-reload) ou 'prod' (build + nginx). Default: dev
#>

param(
    [ValidateSet("dev", "prod")]
    [string]$Mode = "dev"
)

# === Utilitários ===
function Resolve-ComposeCmd {
    try {
        $null = & docker compose version 2>$null
        if ($LASTEXITCODE -eq 0) { return @("docker","compose") }
    } catch {}
    if (Get-Command docker-compose -ErrorAction SilentlyContinue) { return @("docker-compose") }
    throw "Docker Compose não encontrado (nem 'docker compose' nem 'docker-compose')."
}

function Run-Compose {
    param(
        [string[]]$BaseCmd,
        [string[]]$Args,
        [string]$OutLog,
        [string]$ErrLog
    )
    $output = & $BaseCmd @Args *>&1
    $output | Out-File -FilePath $OutLog -Encoding UTF8
    if ($LASTEXITCODE -ne 0) {
        $output | Out-File -FilePath $ErrLog -Encoding UTF8
        throw "Falha ao executar '$($BaseCmd -join ' ') $($Args -join ' ')'. Verifique os logs."
    }
}

function Get-ContainerInfo {
    $out = & docker ps -a --format "{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}" 2>$null
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($out)) { return "Nenhum container encontrado." }
    return $out -join "`n"
}

function Get-RunningContainersCount {
    $out = & docker ps -q 2>$null
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($out)) { return 0 }
    return ($out -split "`n").Count
}

function Try-Resolve-Port {
    param(
        [string[]]$ComposeCmd,
        [string]$Service,
        [int]$ContainerPort
    )
    $args = @("port", $Service, $ContainerPort)
    $out = & $ComposeCmd @args 2>$null
    if ($LASTEXITCODE -eq 0 -and -not [string]::IsNullOrWhiteSpace($out)) {
        $parts = $out.Trim() -split "[:]"
        if ($parts.Length -ge 2) { return $parts[-1] }
    }
    return $null
}

function Write-Log {
    param([string]$message, [string]$color = "White")
    Write-Host $message -ForegroundColor $color
    $script:logContent += "`n$message"
}

# === Pré-validações ===
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker não está disponível no sistema." -ForegroundColor Red
    exit 1
}

$PROJECT_ROOT = "C:\Users\User5\Music\MEGA1\sila\sila-system"
if (-not (Test-Path $PROJECT_ROOT)) {
    Write-Host "❌ Diretório do projeto não encontrado: $PROJECT_ROOT" -ForegroundColor Red
    exit 1
}
Set-Location $PROJECT_ROOT

$requiredFiles = @(
    "docker-compose.yml",
    "backend/Dockerfile",
    "frontend/webapp/Dockerfile"
)
foreach ($file in $requiredFiles) {
    if (-not (Test-Path "$PROJECT_ROOT\$file")) {
        Write-Host "❌ Arquivo obrigatório não encontrado: $file" -ForegroundColor Red
        exit 1
    }
}

# === Logs ===
$logDir = "$PROJECT_ROOT\logs\$Mode"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$logFile = "$logDir\start-log-$timestamp.md"
if (-not (Test-Path -Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }

$startTime = Get-Date
$logContent = @"
# Log de Inicialização - $Mode
**Data/Hora**: $($startTime.ToString("dd/MM/yyyy HH:mm:ss"))
**Modo**: $Mode
**Usuário**: $env:USERNAME
**Máquina**: $env:COMPUTERNAME

## Comando Executado

$($MyInvocation.Line.Trim())

## Containers (antes)

$(Get-ContainerInfo)

## Ações Realizadas
"@

# === Execução ===
try {
    $composeCmd = Resolve-ComposeCmd

    if ($Mode -eq "dev") {
        Write-Log "🚀 Iniciando ambiente de DESENVOLVIMENTO..." "Cyan"

        Write-Log "===> Subindo containers com hot-reload (compose up --build -d)..." "Cyan"
        Run-Compose -BaseCmd $composeCmd `
            -Args @("up","--build","-d") `
            -OutLog "$logDir\docker-compose-output-$timestamp.log" `
            -ErrLog "$logDir\docker-compose-error-$timestamp.log"

        # Auditoria Node.js
        $webappPath = "$PROJECT_ROOT\frontend\webapp"
        if (Test-Path "$webappPath\package.json") {
            Write-Log "===> Rodando auditoria Node.js (npm install + npm audit)..." "Yellow"
            Push-Location $webappPath
            npm install *>> "$logDir\npm-install-$timestamp.log" 2>&1
            npm audit *>> "$logDir\npm-audit-$timestamp.log" 2>&1
            if ($LASTEXITCODE -ne 0) {
                Write-Log "⚠️ npm audit encontrou problemas. Veja: $logDir\npm-audit-$timestamp.log" "Yellow"
            }
            Pop-Location
        }

        # Auditoria Python
        if (Test-Path "$PROJECT_ROOT\backend\requirements.txt") {
            Write-Log "===> Rodando auditoria Python (pip-audit no host)..." "Yellow"
            try {
                pip install --disable-pip-version-check -q pip-audit *>> "$logDir\pip-audit-install-$timestamp.log" 2>&1
                pip-audit -r "$PROJECT_ROOT\backend\requirements.txt" *>> "$logDir\pip-audit-$timestamp.log" 2>&1
                if ($LASTEXITCODE -ne 0) {
                    Write-Log "⚠️ pip-audit encontrou problemas. Veja: $logDir\pip-audit-$timestamp.log" "Yellow"
                }
            } catch {
                Write-Log "⚠️ pip-audit não pôde ser executado: $($_.Exception.Message)" "Yellow"
            }
        }
    }
    else {
        Write-Log "🚀 Iniciando ambiente de PRODUÇÃO..." "Green"
        Write-Log "===> Subindo containers de produção (compose up --build -d)..." "Green"
        Run-Compose -BaseCmd $composeCmd `
            -Args @("up","--build","-d") `
            -OutLog "$logDir\docker-compose-prod-output-$timestamp.log" `
            -ErrLog "$logDir\docker-compose-prod-error-$timestamp.log"
    }

    # Aguarda containers
    $maxWait = 60
    $elapsed = 0
    while ((Get-RunningContainersCount) -eq 0 -and $elapsed -lt $maxWait) {
        Start-Sleep -Seconds 3
        $elapsed += 3
    }

    $running = Get-RunningContainersCount
    if ($running -eq 0) {
        throw "Nenhum container está em execução após o 'compose up'."
    }

    # Detecta portas
    $backendPortCandidates = @(8000, 8080, 5000)
    $frontendPortCandidates = @(5173, 3000, 8080)

    $backendPort = $null
    foreach ($p in $backendPortCandidates) {
        $backendPort = Try-Resolve-Port -ComposeCmd $composeCmd -Service "backend" -ContainerPort $p
        if ($backendPort) { break }
    }

    $frontendPort = $null
    foreach ($p in $frontendPortCandidates) {
        $frontendPort = Try-Resolve-Port -ComposeCmd $composeCmd -Service "frontend" -ContainerPort $p
        if ($frontendPort) { break }
    }

    $backendUrl  = $(if ($backendPort)  { "http://localhost:$backendPort" } else { "Porta não detectada (confira docker-compose.yml)" })
    $frontendUrl = $(if ($frontendPort) { "http://localhost:$frontendPort" } else { "Porta não detectada (confira docker-compose.yml)" })

    $logContent += @"

## Status Final

$(Get-ContainerInfo)

## URLs de Acesso
- Backend:  $backendUrl
- Frontend: $frontendUrl

## Arquivos de Log
- Log principal: $logFile
- Pasta de logs: $logDir\
"@

    Write-Host "✅ Ambiente $($Mode.ToUpper()) rodando com sucesso!" -ForegroundColor Green
}
catch {
    $errorMsg = $_.Exception.Message
    $logContent += @"

## ❌ Erro
Ocorreu um erro durante a inicialização:

$errorMsg

"@
    Write-Host "❌ Erro durante a inicialização: $errorMsg" -ForegroundColor Red
    exit 1
}
finally {
    $duration = [math]::Round(((Get-Date) - $startTime).TotalSeconds, 2)
    $logContent += "`n## Resultado`nConcluído em ${duration}s."
    $logContent | Out-File -FilePath $logFile -Encoding UTF8 -Force
    Write-Host "📝 Log salvo em: $logFile" -ForegroundColor Cyan
    Write-Host "`nPara parar os containers: .\down.ps1 -Mode $Mode" -ForegroundColor Magenta
}
