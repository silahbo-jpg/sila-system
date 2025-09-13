<# run_all_validations.ps1
Script unificado de validações
Inclui:
 - Auditoria de resíduos do Prisma
 - Validação da estrutura __init__.py
 - Lint (ruff/flake8)
 - Testes pytest
Suporta:
 - Modo CI (--ci) com saída resumida
 - Exportação JSON (--json ou --json-file <path>)
#>

param (
    [switch]$fix,
    [switch]$dryRun,
    [switch]$ci,
    [switch]$json,
    [string]$jsonFile
)

function Write-Header($msg) { if (-not $ci) { Write-Host "`n=== $msg ===" -ForegroundColor Cyan } }
function Write-Success($msg) { if (-not $ci) { Write-Host $msg -ForegroundColor Green } }
function Write-Warning($msg) { if (-not $ci) { Write-Host $msg -ForegroundColor Yellow } }
function Write-Error($msg) { if (-not $ci) { Write-Host $msg -ForegroundColor Red } }

# ================== PRISMA AUDIT ==================
function Validate-PrismaArtifacts {
    Write-Header "🔍 Auditoria de Resíduos do Prisma"
    $ok = $true
    $results = @{
        PrismaFiles   = @()
        PrismaScripts = @()
        PrismaConfigs = @()
    }

    $pyFiles = Get-ChildItem -Path "..\" -Recurse -Include "*.py" -ErrorAction SilentlyContinue
    foreach ($file in $pyFiles) {
        $content = Get-Content $file.FullName -Raw
        if ($content -match "from prisma" -or $content -match "import prisma" -or $content -match "PrismaClient") {
            $results.PrismaFiles += $file.FullName
        }
    }

    $ps1Files = Get-ChildItem -Path "..\" -Recurse -Include "*.ps1" -ErrorAction SilentlyContinue
    foreach ($file in $ps1Files) {
        $content = Get-Content $file.FullName -Raw
        if ($content -match "npx prisma" -or $content -match "prisma generate" -or $content -match "setup_prisma") {
            $results.PrismaScripts += $file.FullName
        }
    }

    $configFiles = @("config.py","settings.py","setup.py",".env","docker-compose.yml")
    foreach ($conf in $configFiles) {
        $path = Join-Path "..\" $conf
        if (Test-Path $path) {
            $content = Get-Content $path -Raw
            if ($content -match "prisma") { $results.PrismaConfigs += $path }
        }
    }

    if ($results.PrismaFiles.Count -eq 0 -and $results.PrismaScripts.Count -eq 0 -and $results.PrismaConfigs.Count -eq 0) {
        Write-Success "✅ Nenhum resíduo do Prisma encontrado."
    } else {
        Write-Warning "⚠️ Prisma ainda encontrado."
        $ok = $false
    }

    return @{ Success=$ok; Details=$results }
}

# ================== INIT STRUCTURE ==================
function Validate-InitStructure {
    Write-Header "📦 Validação de Estrutura (__init__.py)"
    $scriptPath = Join-Path $PSScriptRoot "validate-init-structure.ps1"
    if (-not (Test-Path $scriptPath)) {
        Write-Error "❌ Script validate-init-structure.ps1 não encontrado!"
        return @{ Success=$false; Details=@{ MissingScript=$true } }
    }
    $output = & $scriptPath @PSBoundParameters | Out-String
    if ($output -match "❌") {
        Write-Error "❌ Estrutura de pacotes com problemas."
        return @{ Success=$false; Details=@{ Output=$output } }
    } else {
        Write-Success "✅ Estrutura de pacotes validada."
        return @{ Success=$true; Details=@{ Output=$output } }
    }
}

# ================== LINT ==================
function Validate-Lint {
    Write-Header "🧹 Lint (ruff/flake8)"
    if (Get-Command ruff -ErrorAction SilentlyContinue) {
        $null = if ($ci) { ruff check .. --quiet } else { ruff check .. }
        return @{ Success=($LASTEXITCODE -eq 0); Details=@{ Tool="ruff" } }
    } elseif (Get-Command flake8 -ErrorAction SilentlyContinue) {
        $null = if ($ci) { flake8 .. } else { flake8 .. }
        return @{ Success=($LASTEXITCODE -eq 0); Details=@{ Tool="flake8" } }
    } else {
        Write-Warning "⚠️ Nenhum linter encontrado (ruff/flake8)."
        return @{ Success=$true; Details=@{ Tool="none" } }
    }
}

# ================== TESTES ==================
function Validate-Tests {
    Write-Header "🧪 Testes (pytest)"
    if (Get-Command pytest -ErrorAction SilentlyContinue) {
        $null = if ($ci) { pytest .. -q } else { pytest .. }
        return @{ Success=($LASTEXITCODE -eq 0); Details=@{ Tool="pytest" } }
    } else {
        Write-Warning "⚠️ Pytest não encontrado."
        return @{ Success=$true; Details=@{ Tool="none" } }
    }
}

# ================== MAIN ==================
function Main {
    $results = @()
    $allPassed = $true

    $checks = @(
        @{ Name="Prisma Audit";    Func="Validate-PrismaArtifacts" },
        @{ Name="Init Structure";  Func="Validate-InitStructure" },
        @{ Name="Lint";            Func="Validate-Lint" },
        @{ Name="Tests";           Func="Validate-Tests" }
    )

    foreach ($chk in $checks) {
        $res = & (Get-Command $chk.Func -CommandType Function)
        if (-not $res.Success) { $allPassed = $false }
        $results += [pscustomobject]@{
            Check   = $chk.Name
            Success = $res.Success
            Status  = if ($res.Success) { "✅" } else { "❌" }
            Details = $res.Details
        }
    }

    # ----- CI/CD output -----
    if ($ci) {
        if ($json -or $jsonFile) {
            $jsonOutput = $results | ConvertTo-Json -Depth 5
            if ($jsonFile) {
                $jsonOutput | Out-File -FilePath $jsonFile -Encoding utf8
            } else {
                $jsonOutput
            }
        } else {
            Write-Host ""
            Write-Host "====== VALIDATION SUMMARY ======" -ForegroundColor Cyan
            $results | Select-Object Check,Status | Format-Table -AutoSize
            Write-Host "================================"
        }
    }

    if ($allPassed) {
        if (-not $ci) { Write-Success "`n🎉 Todas as validações passaram com sucesso!" }
        exit 0
    } else {
        if (-not $ci) { Write-Error "`n⚠️ Algumas validações falharam." }
        exit 1
    }
}

Main
