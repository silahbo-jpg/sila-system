param (
    [string]$ProjectRoot = "..",
    [ValidateSet("quick","full")]
    [string]$Mode = "quick",
    [int]$MaxDepth = 3
)

function Write-Header($text) {
    Write-Host "`n=== $text ===" -ForegroundColor Cyan
}

# Pastas a ignorar (pesadas e irrelevantes)
$excludeDirs = @("node_modules", ".git", ".venv", "venv", "__pycache__", "dist", "build")

# Caminho do relatório
$reportPath = Join-Path $ProjectRoot "project_structure_report.txt"

# Inicia relatório
"Relatório de Estrutura do Projeto" | Out-File $reportPath -Encoding utf8
"Gerado em: $(Get-Date)" | Out-File $reportPath -Append -Encoding utf8
"Raiz analisada: $(Resolve-Path $ProjectRoot)" | Out-File $reportPath -Append -Encoding utf8
"Modo: $Mode" | Out-File $reportPath -Append -Encoding utf8

# ----------------------
# 1. Estrutura de diretórios
# ----------------------
Write-Header "1. ESTRUTURA DE DIRETÓRIOS"
$dirs = Get-ChildItem -Path $ProjectRoot -Directory -Recurse -ErrorAction SilentlyContinue |
    Where-Object { $excludeDirs -notcontains $_.Name } |
    Where-Object { ($_.FullName -split '[\\/]').Count -le ($MaxDepth + ($ProjectRoot -split '[\\/]').Count) }

$dirs | ForEach-Object { Write-Host $_.FullName }
$dirs | Select-Object FullName | Out-File $reportPath -Append -Encoding utf8

# ----------------------
# 2. Arquivos principais
# ----------------------
Write-Header "2. ARQUIVOS PRINCIPAIS"
$mainFiles = Get-ChildItem -Path $ProjectRoot -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -in @("package.json","requirements.txt","pyproject.toml","docker-compose.yml","Dockerfile") }

if ($mainFiles) {
    $mainFiles | ForEach-Object { Write-Host $_.FullName }
    $mainFiles | Select-Object FullName | Out-File $reportPath -Append -Encoding utf8
} else {
    Write-Host "Nenhum arquivo principal encontrado."
    "Nenhum arquivo principal encontrado." | Out-File $reportPath -Append -Encoding utf8
}

# ----------------------
# 3. Scripts
# ----------------------
Write-Header "3. SCRIPTS"
$scripts = Get-ChildItem -Path $ProjectRoot -Recurse -Include *.ps1, *.sh, *.py -File -ErrorAction SilentlyContinue |
    Where-Object { $excludeDirs -notcontains $_.Directory.Name }

if ($scripts) {
    $scripts | ForEach-Object { Write-Host $_.FullName }
    $scripts | Select-Object FullName | Out-File $reportPath -Append -Encoding utf8
} else {
    Write-Host "Nenhum script encontrado."
    "Nenhum script encontrado." | Out-File $reportPath -Append -Encoding utf8
}

# ----------------------
# 4. Dependências
# ----------------------
Write-Header "4. DEPENDÊNCIAS"
$depFiles = @("package.json", "requirements.txt", "pyproject.toml")
foreach ($file in $depFiles) {
    $path = Join-Path $ProjectRoot $file
    if (Test-Path $path) {
        Write-Host "`nConteúdo de ${file}:"
        Get-Content $path | ForEach-Object { Write-Host $_ }
        "`n=== ${file} ===" | Out-File $reportPath -Append -Encoding utf8
        Get-Content $path | Out-File $reportPath -Append -Encoding utf8
    }
}

# ----------------------
# 5. Banco de Dados
# ----------------------
Write-Header "5. BANCO DE DADOS"
$dbFiles = Get-ChildItem -Path $ProjectRoot -Recurse -Include '*.db','*.sqlite','schema.prisma' -File -ErrorAction SilentlyContinue |
    Where-Object { $excludeDirs -notcontains $_.Directory.Name }

if ($dbFiles) {
    $dbFiles | ForEach-Object {
        $sizeMB = [math]::Round($_.Length / 1MB, 2)
        $sizeInfo = "{0} MB" -f $sizeMB
        Write-Host "Arquivo de banco de dados: $($_.Name)"
        Write-Host "  Local: $($_.FullName)"
        Write-Host ("  Tamanho: {0}" -f $sizeInfo)
        ("Banco de Dados: {0} ({1})" -f $_.Name, $sizeInfo) | Out-File $reportPath -Append -Encoding utf8
    }
} else {
    $msg = "Nenhum arquivo de banco de dados local encontrado."
    Write-Host $msg
    $msg | Out-File $reportPath -Append -Encoding utf8
}

# ----------------------
# 6. README
# ----------------------
Write-Header "6. README"
if (Test-Path (Join-Path $ProjectRoot 'README.md')) {
    $msg = "README.md encontrado."
    Write-Host $msg
    $msg | Out-File $reportPath -Append -Encoding utf8
} else {
    $msg = "README.md não encontrado."
    Write-Host $msg
    $msg | Out-File $reportPath -Append -Encoding utf8
}

# ----------------------
# Finalização
# ----------------------
Write-Host "`n[INFO] Relatório salvo em: $reportPath" -ForegroundColor Green
