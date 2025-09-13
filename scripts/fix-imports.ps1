param(
    [string]$ProjectRoot = (Get-Location).Path
)

Write-Host "🔍 Analisando e corrigindo imports em $ProjectRoot" -ForegroundColor Cyan

# Mapeamento de padrões de import para pastas
$importMappings = @{
    "from sila_" = "from ..sila_"
    "from core" = "from ..core"
    "from utils" = "from ..utils"
    "from services" = "from ..services"
    "from api" = "from ..api"
    "from models" = "from ..models"
}

# Processa cada arquivo Python
Get-ChildItem -Path $ProjectRoot -Recurse -Filter "*.py" | ForEach-Object {
    $filePath = $_.FullName
    $relativePath = $filePath.Substring($ProjectRoot.Length).TrimStart('\')
    
    # Pula arquivos em pastas de ambiente virtual
    if ($relativePath -match '(\\|^)(venv|env|.venv)\\') {
        return
    }
    
    $content = Get-Content -Path $filePath -Raw -ErrorAction SilentlyContinue
    if (-not $content) { return }
    
    $modified = $false
    $newContent = $content
    
    # Aplica as correções de import
    foreach ($mapping in $importMappings.GetEnumerator()) {
        if ($newContent -match $mapping.Key) {
            $newContent = $newContent -replace $mapping.Key, $mapping.Value
            $modified = $true
        }
    }
    
    # Se houve modificações, salva o arquivo
    if ($modified) {
        Set-Content -Path $filePath -Value $newContent -Force
        Write-Host "✅ Atualizado: $relativePath" -ForegroundColor Green
    }
}

Write-Host "✅ Correção de imports concluída!" -ForegroundColor Green
