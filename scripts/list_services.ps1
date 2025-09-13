# Script para listar serviços do backend
# Saída salva em: reports/services_list_<timestamp>.txt

# Configuração
$basePath = (Get-Item -Path "$PSScriptRoot\..").FullName
$servicesPath = Join-Path $basePath "backend\app\services"
$outputDir = Join-Path $basePath "reports"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$outputFile = Join-Path $outputDir "services_list_${timestamp}.txt"

# Garante que o diretório de saída existe
if (-not (Test-Path -Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

# Cabeçalho do relatório
$report = @"
============================================================
LISTA DE SERVIÇOS DO BACKEND
============================================================
Data: $(Get-Date -Format "dd/MM/yyyy HH:mm:ss")
Diretório: $servicesPath

"@

# Lista todos os arquivos Python no diretório de serviços
$pythonFiles = Get-ChildItem -Path $servicesPath -Filter "*.py" | 
              Where-Object { $_.Name -ne "__init__.py" } |
              Sort-Object Name

# Adiciona informações de cada arquivo
foreach ($file in $pythonFiles) {
    $content = Get-Content -Path $file.FullName -Raw -ErrorAction SilentlyContinue
    $lineCount = if ($content) { ($content -split "`r`n").Count } else { 0 }
    $sizeKB = [math]::Round($file.Length / 1KB, 2)
    
    $report += "`n=== $($file.Name) ===`n"
    $report += "- Tamanho: $sizeKB KB`n"
    $report += "- Linhas: $lineCount`n"
    
    # Extrai classes e funções de forma simples
    if ($content) {
        $classes = [regex]::Matches($content, '^class\s+(\w+)', [System.Text.RegularExpressions.RegexOptions]::Multiline)
        $functions = [regex]::Matches($content, '^\s*(?:async\s+)?def\s+(\w+)\s*\(', [System.Text.RegularExpressions.RegexOptions]::Multiline) | 
                    Where-Object { $_.Groups[1].Value -ne "__init__" }
        
        if ($classes.Count -gt 0) {
            $report += "- Classes: $($classes.Count)`n"
            foreach ($class in $classes) {
                $report += "  - $($class.Groups[1].Value)`n"
            }
        }
        
        if ($functions.Count -gt 0) {
            $report += "- Funções: $($functions.Count)`n"
            foreach ($func in $functions | Select-Object -First 5) {
                $report += "  - $($func.Groups[1].Value)`n"
            }
            if ($functions.Count -gt 5) {
                $report += "  - ... e mais $($functions.Count - 5) funções`n"
            }
        }
    }
    
    $report += "-" * 50 + "`n"
}

# Salva o relatório
$report | Out-File -FilePath $outputFile -Encoding UTF8

# Exibe resumo
Write-Host "✅ LISTAGEM DE SERVIÇOS CONCLUÍDA" -ForegroundColor Green
Write-Host "📄 Relatório salvo em: $outputFile" -ForegroundColor Cyan
Write-Host "📊 Arquivos listados: $($pythonFiles.Count)" -ForegroundColor Cyan
