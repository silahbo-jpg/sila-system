param(
    [string]$OutputFile = "requirements.txt"
)

Write-Host "🔍 Gerando arquivo de requisitos..." -ForegroundColor Cyan

# Cria um ambiente virtual temporário para identificar dependências
$venvPath = ".temp_venv"
$requirements = @()

# Verifica se o pip está instalado
if (-not (Get-Command pip -ErrorAction SilentlyContinue)) {
    Write-Host "❌ O pip não foi encontrado. Certifique-se de que o Python está instalado corretamente." -ForegroundColor Red
    exit 1
}

# Cria ambiente virtual temporário
Write-Host "Criando ambiente virtual temporário..." -ForegroundColor Cyan
python -m venv $venvPath

# Ativa o ambiente virtual e instala o projeto em modo desenvolvimento
& "$venvPath\Scripts\Activate.ps1"
pip install -e .

# Gera o requirements.txt
Write-Host "Gerando requirements.txt..." -ForegroundColor Cyan
pip freeze | Out-File -FilePath $OutputFile -Encoding utf8

# Remove o ambiente virtual temporário
Write-Host "Limpando ambiente temporário..." -ForegroundColor Cyan
Deactivate
Remove-Item -Path $venvPath -Recurse -Force -ErrorAction SilentlyContinue

# Remove pacotes de desenvolvimento desnecessários
$devPackages = @("pytest", "pytest-cov", "mypy", "black", "flake8", "isort")
$content = Get-Content -Path $OutputFile -Raw
$newContent = $content -split "`n" | Where-Object {
    $line = $_.Trim()
    $keep = $true
    foreach ($pkg in $devPackages) {
        if ($line -match "^$pkg[=<>]") {
            $keep = $false
            break
        }
    }
    $keep -and ($line -ne "")
}

# Adiciona uma seção de dependências de desenvolvimento
$devSection = @"

# Dependências de desenvolvimento
# Instale com: pip install -r requirements-dev.txt
"@

Set-Content -Path $OutputFile -Value ($newContent -join "`n") -Encoding utf8

# Cria um arquivo de requisitos de desenvolvimento separado
$devContent = @"
# Dependências de desenvolvimento
# Instale com: pip install -r requirements-dev.txt

# Testes
pytest>=7.0.0
pytest-cov>=4.0.0

# Formatação e qualidade de código
black>=23.0.0
flake8>=6.0.0
isort>=5.12.0
mypy>=1.0.0

# Documentação
sphinx>=6.0.0
sphinx-rtd-theme>=1.2.0
"@

Set-Content -Path "requirements-dev.txt" -Value $devContent -Encoding utf8

Write-Host "✅ Arquivos gerados com sucesso!" -ForegroundColor Green
Write-Host "- $OutputFile (dependências principais)" -ForegroundColor Green
Write-Host "- requirements-dev.txt (dependências de desenvolvimento)" -ForegroundColor Green
