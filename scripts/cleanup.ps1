param(
    [string]$ProjectRoot = (Get-Location).Path
)

Write-Host "🧹 Iniciando limpeza do projeto..." -ForegroundColor Cyan

# Lista de diretórios e arquivos para remover
$itemsToRemove = @(
    # Python cache and build artifacts
    "__pycache__",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    ".Python",
    "build/",
    "develop-eggs/",
    "dist/",
    "downloads/",
    "eggs/",
    ".eggs/",
    "lib/",
    "lib64/",
    "parts/",
    "sdist/",
    "var/",
    "wheels/",
    "*.egg-info/",
    ".installed.cfg",
    "*.egg",
    
    # Environment and IDE
    ".venv",
    "env/",
    "venv/",
    ".vs/",
    ".vscode/",
    ".idea/",
    ".pytest_cache/",
    ".mypy_cache/",
    
    # Logs and databases
    "*.log",
    "*.db",
    
    # OS specific
    ".DS_Store",
    "Thumbs.db"
)

# Função para remover itens
function Remove-ItemsSafe {
    param (
        [string]$path,
        [string]$filter
    )
    
    try {
        if (Test-Path $path) {
            if ($filter.EndsWith("/") -or $filter.EndsWith("\\")) {
                # É um diretório
                $dirFilter = $filter.TrimEnd("/\")
                Get-ChildItem -Path $path -Directory -Recurse -Filter $dirFilter -ErrorAction SilentlyContinue | 
                    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
            } else {
                # É um arquivo
                Get-ChildItem -Path $path -File -Recurse -Filter $filter -ErrorAction SilentlyContinue | 
                    Remove-Item -Force -ErrorAction SilentlyContinue
            }
        }
    } catch {
        Write-Host "⚠️ Erro ao processar $filter : $_" -ForegroundColor Yellow
    }
}

# Processa cada item a ser removido
foreach ($item in $itemsToRemove) {
    Write-Host "Removendo $item..." -NoNewline
    Remove-ItemsSafe -path $ProjectRoot -filter $item
    Write-Host " ✅" -ForegroundColor Green
}

# Limpar pastas vazias
Write-Host "Removendo pastas vazias..." -NoNewline
Get-ChildItem -Path $ProjectRoot -Directory -Recurse -Force | Where-Object { 
    $_.GetFiles().Count -eq 0 -and $_.GetDirectories().Count -eq 0 
} | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue
Write-Host " ✅" -ForegroundColor Green

Write-Host "✅ Limpeza concluída!" -ForegroundColor Green
