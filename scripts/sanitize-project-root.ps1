#!/usr/bin/env pwsh

# sanitize-project-root.ps1
# Sanitização radical da raiz do projeto SILA-System
# Remove vestígios, ambientes, caches, dependências embutidas e lixo
# Compatível com pwsh 7+

$StartTime = Get-Date
$BasePath = $PSScriptRoot | Split-Path -Parent
$LogPath = Join-Path $BasePath "reports" "cleanup" "project-sanitization-root.log"

# Criar pasta de logs
$LogDir = Split-Path $LogPath -Parent
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir -Force | Out-Null }

# Função de log
function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "HH:mm:ss"
    "[$timestamp] $Message" | Tee-Object -FilePath $LogPath -Append
}

Write-Log "🚀 Iniciando sanitização da raiz do projeto: $BasePath"

# === 1. Pastas que NUNCA devem estar versionadas (remover recursivamente) ===
$NeverVersioned = @(
    "__pycache__",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".cache",
    ".vscode",
    ".nodeenv",
    ".npm",
    ".config",
    "npm-debug.log*",
    "yarn-error.log*",
    "yarn-debug.log*",
    "*.log",
    "logs/",
    "reports/coverage_*.html",
    "z_*.html",
    "coverage.xml",
    ".coverage*",
    "htmlcov/",
    "dist/",
    "build/",
    "develop-eggs/",
    "eggs/",
    "lib/",
    "lib64/",
    "parts/",
    "sdist/",
    "var/",
    "*.egg-info",
    "*.egg",
    "WHEEL",
    "METADATA",
    "RECORD",
    "REQUESTED",
    "INSTALLER",
    "top_level.txt",
    "pip-selfcheck.json",
    "*.pot",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    "*.so",
    "*.dll",
    "*.dylib",
    "*.exe",
    "*.whl"
)

foreach ($pattern in $NeverVersioned) {
    try {
        $items = Get-ChildItem -Path $BasePath -Include $pattern -Recurse -ErrorAction SilentlyContinue
        if ($items) {
            $items | Remove-Item -Recurse -Force
            Write-Log "🗑️ Removido: $pattern ($($items.Count) itens)"
        }
    } catch {
        Write-Log "⚠️ Falha ao remover $pattern`: $($_.Exception.Message)"
    }
}

# === 2. Ambientes virtuais (Python e Node) ===
$VenvPatterns = @(
    "venv",
    ".venv",
    ".nodeenv",
    "test_venv",
    "migration_reports",
    "i18n",
    "node_modules"
)

foreach ($folder in $VenvPatterns) {
    $path = Join-Path $BasePath $folder
    if (Test-Path $path) {
        try {
            Remove-Item -Path $path -Recurse -Force
            Write-Log "🐍🗑️ Removido: ambiente virtual ou node_modules '$folder'"
        } catch {
            Write-Log "⚠️ Falha ao remover ambiente '$folder`: $($_.Exception.Message)"
        }
    }
}

# === 3. Pastas de dependências embutidas (BIBLIOTECAS PYTHON) ===
$PythonLibs = @(
    "astroid", "bcrypt", "certifi", "cffi", "charset_normalizer", "colorama", "click", "distlib",
    "greenlet", "idna", "importlib_metadata", "itsdangerous", "Jinja2", "loguru", "lxml", "Mako",
    "MarkupSafe", "packaging", "passlib", "pkg_resources", "platformdirs", "pluggy", "psycopg2",
    "pydantic", "pydantic_core", "PyJWT", "python_dotenv", "python_multipart", "pytz", "requests",
    "six", "sniffio", "SQLAlchemy", "starlette", "typing_extensions", "urllib3", "uvicorn", "watchfiles",
    "websockets", "Werkzeug", "zipp", "annotated_types", "anyio", "colorama", "distlib",
    "filelock", "importlib_metadata", "iniconfig", "Jinja2", "MarkupSafe", "packaging", "pluggy",
    "py", "pyparsing", "pytest", "pytest_asyncio", "pytest_cov", "python_dateutil", "regex",
    "rich", "sniffio", "SQLAlchemy-utils", "starlette", "typing_extensions", "uritemplate", "wcwidth",
    "fastapi", "pydantic", "sqlalchemy", "alembic", "passlib", "python-jose", "python-multipart",
    "python-dotenv", "requests", "cryptography", "pyjwt", "qrcode", "pillow", "python-levenshtein",
    "python-json-logger", "prometheus-client", "psutil", "redis", "python-socketio", "engineio"
)

foreach ($lib in $PythonLibs) {
    $path = Join-Path $BasePath $lib
    if (Test-Path $path) {
        try {
            Remove-Item -Path $path -Recurse -Force
            Write-Log "📦🗑️ Removido: biblioteca embutida '$lib'"
        } catch {
            Write-Log "⚠️ Falha ao remover biblioteca '$lib`: $($_.Exception.Message)"
        }
    }
}

# === 4. Pastas de build e cache do frontend ===
$FrontendTrash = @(
    "frontend/webapp/dist",
    "frontend/webapp/node_modules",
    "frontend/node_modules",
    "backend/.nodeenv",
    "backend/node_modules"
)

foreach ($path in $FrontendTrash) {
    $fullPath = Join-Path $BasePath $path
    if (Test-Path $fullPath) {
        Remove-Item -Path $fullPath -Recurse -Force
        Write-Log "🗑️ Removido: $path (frontend/backend build/cache)"
    }
}

# === 5. Arquivos de log e relatórios temporários ===
Get-ChildItem -Path $BasePath -Include "*.log", "secrets_report.json", "test_endpoints_snapshot.log" -Recurse -File | ForEach-Object {
    Remove-Item $_.FullName -Force
    Write-Log "📄🗑️ Removido: log ou relatório temporário '$($_.Name)'"
}

# === 6. Limpeza final: diretórios vazios ===
Write-Log "🧹 Removendo diretórios vazios..."
Get-ChildItem -Path $BasePath -Directory -Recurse -ErrorAction SilentlyContinue | Sort-Object FullName -Descending | ForEach-Object {
    if ((Get-ChildItem $_.FullName -Recurse -File -ErrorAction SilentlyContinue | Measure-Object).Count -eq 0) {
        try {
            Remove-Item $_.FullName -Force
            Write-Log "EmptyEntries] Diretório vazio removido: $($_.FullName)"
        } catch {
            Write-Log "⚠️ Falha ao remover diretório vazio '$($_.FullName)': $($_.Exception.Message)"
        }
    }
}

# === 7. Atualizar .gitignore (se não tiver regras essenciais) ===
$GitIgnore = Join-Path $BasePath ".gitignore"
$Rules = @(
    "# Python"
    "__pycache__/"
    "*.pyc"
    "*.pyo"
    "*.pyd"
    "*.pyc"
    "db.sqlite3"
    ".env"
    ".venv/"
    "venv/"
    "env/"
    "ENV/"
    "pip-log.txt"
    "pip-delete-this-directory.txt"
    ".python-version"
    "pip-selfcheck.json"
    ""
    "# Virtual Environment"
    "/backend/.venv/"
    "/backend/test_venv/"
    "/backend/.nodeenv/"
    ""
    "# Node"
    "node_modules/"
    "npm-debug.log*"
    "yarn-debug.log*"
    "yarn-error.log*"
    "pnpm-debug.log*"
    "package-lock.json"
    "npm-shrinkwrap.json"
    ""
    "# Build"
    "dist/"
    "build/"
    "develop-eggs/"
    "eggs/"
    "lib/"
    "lib64/"
    "parts/"
    "sdist/"
    "var/"
    "wheels/"
    "*.egg"
    "*.egg-info"
    "MANIFEST"
    ""
    "# Coverage"
    ".coverage"
    "coverage.xml"
    "htmlcov/"
    ".pytest_cache/"
    ".ruff_cache/"
    ".mypy_cache/"
    ""
    "# Logs"
    "*.log"
    "logs/"
    "reports/"
    ""
    "# IDE"
    ".vscode/"
    ".idea/"
    "*.swp"
    "*.swo"
    ""
    "# OS"
    ".DS_Store"
    "Thumbs.db"
)

if (Test-Path $GitIgnore) {
    $current = Get-Content $GitIgnore -Raw
    $missingRules = $Rules | Where-Object { $current -notlike "*$_*" }
    if ($missingRules) {
        $missingRules | Out-File -FilePath $GitIgnore -Encoding UTF8 -Append
        Write-Log "✅ Regras adicionadas ao .gitignore"
    }
} else {
    $Rules | Out-File -FilePath $GitIgnore -Encoding UTF8
    Write-Log "✅ .gitignore criado com regras padrão"
}

# === 8. Resumo final ===
$EndTime = Get-Date
$Duration = $EndTime - $StartTime

Write-Log "✅ SANITIZAÇÃO COMPLETA DA RAIZ DO PROJETO!"
Write-Log "⏱️ Duração: $($Duration.TotalSeconds) segundos"
Write-Log "🗑️ Itens removidos: bibliotecas embutidas, ambientes, caches, logs"
Write-Log "📄 Log salvo em: $LogPath"
Write-Log "💡 Próximo passo: Reinstale dependências com 'pip install -r requirements.txt' e 'npm install'"