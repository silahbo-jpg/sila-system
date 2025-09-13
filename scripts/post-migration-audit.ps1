# scripts/post-migration-audit.ps1
Write-Host "Iniciando auditoria pos-migracao..." -ForegroundColor Cyan

$backend = "$PSScriptsila_dev-system/../backend"

# 1. Verifica se ainda há SQLAlchemy
$bad_patterns = @("from sqlalchemy", "SessionLocal", "Base.metadata", "db.add")
$results = @()
foreach ($pattern in $bad_patterns) {
    $found = Select-String -Path "$backend/**/*.py" -Pattern $pattern -List
    if ($found) {
        Write-Warning "Padrao proibido encontrado: $pattern"
        foreach ($item in $found) {
            Write-Host "   $($item.Path):$($item.LineNumber)"
        }
        $results += $found
    }
}

# 2. Verifica se prisma.generate foi feito
$client = "$backend/app/prisma/client.py"
$client_exists = Test-Path $client
if ($client_exists) {
    Write-Host "Cliente Prisma gerado" -ForegroundColor Green
} else {
    Write-Warning "Cliente Prisma nao encontrado. Execute 'python -m prisma generate'"
}

# 3. Verifica se há erros de sintaxe em arquivos Python
Write-Host "Verificando erros de sintaxe em arquivos Python..." -ForegroundColor Yellow
$syntax_errors = @()
foreach ($file in Get-ChildItem -Path "$backend/app" -Filter "*.py" -Recurse) {
    $output = python -c "import py_compile; py_compile.compile('$($file.FullName)')" 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "Erro de sintaxe em $($file.FullName)"
        $syntax_errors += $file
    }
}

# 4. Resumo
Write-Host ""
Write-Host "Resumo da Auditoria Pos-Migracao" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

# Calcular total de problemas
$results_count = 0
if ($results) { $results_count = $results.Count }

$client_issue = 0
if (-not $client_exists) { $client_issue = 1 }

$total_issues = $results_count + $syntax_errors.Count + $client_issue

if ($total_issues -eq 0) {
    Write-Host "Migracao concluida com sucesso! Nenhum problema encontrado." -ForegroundColor Green
} else {
    Write-Warning "Migracao concluida com $total_issues problemas que precisam ser corrigidos."
}

