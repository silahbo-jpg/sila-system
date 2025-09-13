$basePath = "backend"

# Lista de diretórios a serem ignorados globalmente
$ignoreDirs = @(
    ".*",                # diretórios ocultos (.venv, .pytest_cache, .github, etc.)
    "__pycache__",       # nunca deve ter __init__.py
    "alembic",           # ignorar fora de app\modules
    "integration",       # ignorar fora de app\modules
    "logs",
    "docs",
    "requirements",
    "reports",
    "scripts",
    "static",
    "test_venv",
    "venv"
)

# Diretórios válidos de código no backend/app
$validRoots = @(
    "app",
    "app\api",
    "app\api\v1",
    "app\api\v1\endpoints",
    "app\auth",
    "app\core",
    "app\core\auth",
    "app\core\config",
    "app\core\db",
    "app\core\i18n",
    "app\core\logging",
    "app\core\middleware",
    "app\db",
    "app\db\models",
    "app\db\repositories",
    "app\middleware",
    "app\models",
    "app\modules",
    "app\schemas",
    "app\services",
    "app\tests",
    "app\utils"
)

# Padrões de subpastas válidas dentro de app\modules
$moduleSubfolders = @("models", "routes", "schemas", "services", "tests", "utils")

# Lista para logging
$checked = @()
$created = @()
$skipped = @()

function Ensure-InitFile($dir) {
    $initFile = Join-Path $dir "__init__.py"
    if (-not (Test-Path $initFile)) {
        New-Item -ItemType File -Path $initFile | Out-Null
        Write-Host "➕ Criado: $initFile" -ForegroundColor Green
        $global:created += $initFile
    } else {
        Write-Host "✅ $initFile já existe."
    }
    $global:checked += $initFile
}

# 🔹 Processa apenas os diretórios válidos
foreach ($root in $validRoots) {
    $fullPath = Join-Path $basePath $root
    if (Test-Path $fullPath) {
        Ensure-InitFile $fullPath

        # Se for app\modules, processar submódulos e subpastas válidas
        if ($root -eq "app\modules") {
            Get-ChildItem -Path $fullPath -Directory | ForEach-Object {
                $modulePath = $_.FullName
                Ensure-InitFile $modulePath

                foreach ($sub in $moduleSubfolders) {
                    $subDir = Join-Path $modulePath $sub
                    if (Test-Path $subDir) {
                        Ensure-InitFile $subDir
                    }
                }
            }
        }
    } else {
        Write-Host "⚠️ Diretório não encontrado (ignorado): $fullPath" -ForegroundColor Yellow
        $global:skipped += $fullPath
    }
}

# 📊 Resumo final
Write-Host "`n📊 Resumo:"
Write-Host "Total verificados: $($checked.Count)"
Write-Host "Criados: $($created.Count)"
Write-Host "Ignorados: $($skipped.Count)"
