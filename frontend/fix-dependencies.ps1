param(
    [switch]$InstallOnly
)

$webappDir = "frontend\webapp"

Write-Host "Verificando dependências do frontend..." -ForegroundColor Cyan

# Verificar se package.json existe
if (-not (Test-Path "$webappDir\package.json")) {
    Write-Host "ERRO: Arquivo package.json não encontrado!" -ForegroundColor Red
    exit 1
}

# Instalar dependências essenciais
$dependencies = @(
    "axios",
    "formik",
    "react-icons",
    "react-query",
    "react-router-dom@6",
    "yup"
)

$devDependencies = @(
    "@compodoc/compodoc",
    "cypress",
    "detect-secrets",
    "@types/node",
    "npm-audit-ci"
)

Write-Host "Instalando dependências..." -ForegroundColor Yellow
Set-Location $webappDir

foreach ($dep in $dependencies) {
    Write-Host "Instalando: $dep" -ForegroundColor DarkGray
    npm install $dep
}

foreach ($dep in $devDependencies) {
    Write-Host "Instalando (dev): $dep" -ForegroundColor DarkGray
    npm install --save-dev $dep
}

# Atualizar scripts no package.json
$packageJson = Get-Content -Raw -Path package.json | ConvertFrom-Json

$packageJson.scripts = @{
    "start"         = "react-scripts start";
    "build"         = "react-scripts build";
    "test"          = "react-scripts test";
    "eject"         = "react-scripts eject";
    "compodoc"      = "compodoc -p tsconfig.json -d ../docs/frontend";
    "cy:run"        = "cypress run";
    "test:ci"       = "react-scripts test --ci --coverage";
    "security-scan" = "detect-secrets scan --update .secrets.baseline"
}

# Salvar alterações
$packageJson | ConvertTo-Json -Depth 100 | Set-Content package.json

Write-Host "Dependências instaladas e package.json atualizado com sucesso!" -ForegroundColor Green

if (-not $InstallOnly) {
    Write-Host "Executando auditoria de segurança..." -ForegroundColor Yellow
    npm audit --omit=dev

    Write-Host "Verificando dependências faltantes..." -ForegroundColor Yellow
    npx npm-audit-ci
}

Set-Location ../..
