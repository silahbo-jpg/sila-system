#!/usr/bin/env pwsh
# nuke-legacy-and-trash.ps1
# Limpeza radical do SILA-System: remove lixo, caches, backups, reports e pastas problematicas.
# Nenhum backup sera criado. Nada sera movido para legacy/. Tudo sera EXCLUÍDO.

$ErrorActionPreference = 'SilentlyContinue'
$StartTime = Get-Date

# === 0) Guardas de seguranca basicas ===
# Raiz do projeto assumida como: pastas "backend\app" e "scripts" presentes
$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot '..')
$BackendApp  = Join-Path $ProjectRoot 'backend\app'
$ScriptsDir  = Join-Path $ProjectRoot 'scripts'

if (-not (Test-Path $BackendApp)) {
    Write-Host 'ERRO: Nao encontrei "backend\app" relativo a este script. Abortando.' -ForegroundColor Red
    exit 1
}
if (-not (Test-Path $ScriptsDir)) {
    Write-Host 'ERRO: Nao encontrei a pasta "scripts" (onde este arquivo deveria estar). Abortando.' -ForegroundColor Red
    exit 1
}

# Nunca apagar .git (historico). Nao tocamos em .git
$GitDir = Join-Path $ProjectRoot '.git'
if (-not (Test-Path $GitDir)) {
    Write-Host 'ATENCAO: Nao encontrei .git na raiz. Continuarei mesmo assim, mas certifique-se de estar na raiz do repo.' -ForegroundColor Yellow
}

# === 1) Padroes de diretorios a DELETAR (radical) ===
$DirsToNuke = @(
    # caches/artefatos comuns
    '**\__pycache__',
    '**\.pytest_cache',
    '**\.mypy_cache',
    '**\.ruff_cache',
    '**\.cache',
    '**\.tox',
    '**\.venv',
    '**\dist',
    '**\build',
    '**\site',
    '**\htmlcov',
    '**\coverage',
    '**\.coverage',
    '**\.hypothesis',
    '**\.vite',
    '**\.parcel-cache',
    '**\cypress\videos',
    '**\cypress\screenshots',
    '**\storybook-static',
    '**\tmp',
    '**\temp',
    '**\logs',
    '**\log',

    # node / front
    '**\node_modules',

    # backups locais e refugios
    '**\backup',
    '**\backups',
    '**\legacy',
    '**\*.backup',
    '**\*.bkp',
    '**\*.bk',
    '**\*.old',
    '**\*.orig',
    '**\*.save',

    # reports do projeto (remoção total)
    'reports'
)

# === 2) Padroes de ARQUIVOS a DELETAR (radical) ===
$FilesToNuke = @(
    # Python bytecode / cache
    '**\*.pyc',
    '**\*.pyo',
    '**\*.pyd',

    # artefatos diversos
    '**\*.log',
    '**\*.tmp',
    '**\*.temp',
    '**\*.lock',
    '**\*.swp',
    '**\*.swo',
    '**\Thumbs.db',
    '**\.DS_Store',

    # bundles comuns
    '**\*.zip',
    '**\*.tar',
    '**\*.tar.gz',
    '**\*.tgz',
    '**\*.7z',
    '**\*.whl',

    # binarios
    '**\*.exe',
    '**\*.dll',
    '**\*.so',
    '**\*.dylib',

    # cobertura / testes
    '**\.coverage*',
    '**\coverage.xml',
    '**\junit*.xml'
)

# === 3) Pastas problemáticas dentro de backend/app a REMOVER (radical) ===
# Se existir e for legado/duplicado/desnecessario no teu plano, some.
$AppDirsToRemove = @(
    'api',
    'crud',
    'routes',
    'routers',
    'i18n',
    'static'
) | ForEach-Object { Join-Path $BackendApp $_ }

# === 4) Arquivos sensiveis e configs locais a REMOVER (radical) ===
$SensitiveToNuke = @(
    '**\.env',
    '**\.env.*',
    '**\*.env',
    '**\secrets.json',
    '**\config-local.json',
    '**\*.pem',
    '**\*.key',
    '**\*.crt'
)

# === 5) Funcoes utilitarias ===
function Remove-DirPattern {
    param([string]$Base, [string]$Pattern)
    $items = Get-ChildItem -Path $Base -Directory -Recurse -Force -ErrorAction SilentlyContinue | Where-Object {
        $_.FullName -like (Join-Path $Base $Pattern)
    }
    foreach ($d in $items) {
        if ($d.FullName -like '*\.git*') { continue } # nunca apagar .git
        try {
            Remove-Item -Path $d.FullName -Recurse -Force -ErrorAction SilentlyContinue
            Write-Host ('[DIR] REMOVIDO: ' + $d.FullName) -ForegroundColor DarkYellow
        } catch {}
    }
}

function Remove-FilePattern {
    param([string]$Base, [string]$Pattern)
    $items = Get-ChildItem -Path $Base -File -Recurse -Force -ErrorAction SilentlyContinue | Where-Object {
        $_.FullName -like (Join-Path $Base $Pattern)
    }
    foreach ($f in $items) {
        try {
            Remove-Item -Path $f.FullName -Force -ErrorAction SilentlyContinue
            Write-Host ('[ARQ] REMOVIDO: ' + $f.FullName) -ForegroundColor DarkCyan
        } catch {}
    }
}

function Safe-RemovePath {
    param([string]$Path)
    if (Test-Path $Path) {
        if ($Path -like '*\.git*') { return } # nunca apagar .git
        try {
            Remove-Item -Path $Path -Recurse -Force -ErrorAction SilentlyContinue
            Write-Host ('[NUKE] ' + $Path) -ForegroundColor Red
        } catch {}
    }
}

# === 6) Execucao: Nuke total ===
Write-Host '--- SANITIZACAO NUCLEAR: INICIO ---' -ForegroundColor Green

# 6.1 Nuke diretorios por padrao
foreach ($p in $DirsToNuke) { Remove-DirPattern -Base $ProjectRoot -Pattern $p }

# 6.2 Nuke arquivos por padrao
foreach ($p in $FilesToNuke) { Remove-FilePattern -Base $ProjectRoot -Pattern $p }

# 6.3 Nuke pastas especificas do backend/app (api, crud, routes, routers, i18n, static)
foreach ($p in $AppDirsToRemove) { Safe-RemovePath -Path $p }

# 6.4 Nuke arquivos sensiveis/config locais
foreach ($p in $SensitiveToNuke) { Remove-FilePattern -Base $ProjectRoot -Pattern $p }

# 6.5 Limpar diretorios vazios remanescentes (sem tocar .git)
# Repetimos algumas vezes para garantir cascata
for ($i=0; $i -lt 3; $i++) {
    Get-ChildItem -Path $ProjectRoot -Directory -Recurse -Force -ErrorAction SilentlyContinue | ForEach-Object {
        if ($_.FullName -like '*\.git*') { return }
        $hasChildren = (Get-ChildItem -Path $_.FullName -Force -ErrorAction SilentlyContinue | Measure-Object).Count -gt 0
        if (-not $hasChildren) {
            try {
                Remove-Item -Path $_.FullName -Force -ErrorAction SilentlyContinue
                Write-Host ('[VAZIO] REMOVIDO: ' + $_.FullName) -ForegroundColor DarkGray
            } catch {}
        }
    }
}

# === 7) Recriar .gitignore forte (na raiz) ===
$GitIgnore = Join-Path $ProjectRoot '.gitignore'
$StrongRules = @(
    '# === NUCLEAR IGNORE (SILA-System) ===',
    '',
    '# caches e bytecode',
    '__pycache__/',
    '*.py[cod]',
    '*.pyo',
    '.pytest_cache/',
    '.mypy_cache/',
    '.ruff_cache/',
    '.cache/',
    '.tox/',
    '.hypothesis/',
    '',
    '# node/front',
    'node_modules/',
    '.vite/',
    'storybook-static/',
    '',
    '# artefatos de build e cobertura',
    'dist/',
    'build/',
    'site/',
    'htmlcov/',
    'coverage/',
    '.coverage*',
    'coverage.xml',
    '',
    '# lixos SO/editores',
    '.DS_Store',
    'Thumbs.db',
    '*.swp',
    '*.swo',
    '.idea/',
    '.vscode/',
    '',
    '# backups locais',
    'backup/',
    'backups/',
    'legacy/',
    '*.backup',
    '*.bkp',
    '*.bk',
    '*.old',
    '*.orig',
    '*.save',
    '',
    '# temporarios',
    'tmp/',
    'temp/',
    'logs/',
    'log/',
    '',
    '# sensiveis',
    '.env',
    '.env.*',
    '*.env',
    '*.pem',
    '*.key',
    '*.crt',
    'secrets.json',
    'config-local.json',
    '',
    '# relatorios (serao recriados quando necessario)',
    'reports/',
    '',
    '# cypress',
    'cypress/videos/',
    'cypress/screenshots/'
)
$StrongRules | Out-File -FilePath $GitIgnore -Encoding UTF8 -Force
Write-Host ('[OK] .gitignore recriado: ' + $GitIgnore) -ForegroundColor Green

# === 8) Fim ===
$EndTime = Get-Date
$Duration = $EndTime - $StartTime
Write-Host ('--- SANITIZACAO NUCLEAR: FIM ( ' + [int]$Duration.TotalSeconds + 's ) ---') -ForegroundColor Green
