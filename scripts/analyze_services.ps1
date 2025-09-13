# Script para gerar análise detalhada do diretório de serviços
# Saída salva em: reports/analysis/services_analysis_<timestamp>.md

# Configuração
$basePath = (Get-Item -Path "$PSScriptRoot\..").FullName
$servicesPath = Join-Path $basePath "backend\app\services"
$outputDir = Join-Path $basePath "reports\analysis"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$outputFile = Join-Path $outputDir "services_analysis_${timestamp}.md"

# Garante que o diretório de saída existe
if (-not (Test-Path -Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

# Função para analisar um arquivo Python
function Analyze-PythonFile {
    param (
        [string]$filePath
    )
    
    $analysis = @{
        FileName = [System.IO.Path]::GetFileName($filePath)
        FilePath = $filePath
        Classes = @()
        Functions = @()
        Imports = @()
        Issues = @()
        LineCount = 0
        SizeKB = [math]::Round((Get-Item $filePath).Length / 1KB, 2)
    }
    
    $content = Get-Content -Path $filePath -Raw -ErrorAction SilentlyContinue
    if (-not $content) {
        $analysis.Issues += "Falha ao ler o arquivo"
        return $analysis
    }
    
    $analysis.LineCount = ($content -split "`r`n" | Measure-Object).Count
    
    # Extrai imports
    $importMatches = [regex]::Matches($content, '^\s*(?:from\s+(\S+)\s+import|import\s+([^#\n]+))', [System.Text.RegularExpressions.RegexOptions]::Multiline)
    foreach ($match in $importMatches) {
        $import = if ($match.Groups[1].Success) { $match.Groups[1].Value.Trim() } else { $match.Groups[2].Value.Trim() }
        if ($import -and -not $analysis.Imports.Contains($import)) {
            $analysis.Imports += $import
        }
    }
    
    # Extrai classes
    $classMatches = [regex]::Matches($content, '^class\s+(\w+)(?:\(([^)]*)\))?', [System.Text.RegularExpressions.RegexOptions]::Multiline)
    foreach ($match in $classMatches) {
        $className = $match.Groups[1].Value
        $baseClass = $match.Groups[2].Value
        $analysis.Classes += @{
            Name = $className
            BaseClass = $baseClass
            Methods = @()
        }
    }
    
    # Extrai funções (incluindo métodos de classe)
    $functionMatches = [regex]::Matches($content, '^\s*(?:async\s+)?def\s+(\w+)\s*\(', [System.Text.RegularExpressions.RegexOptions]::Multiline)
    foreach ($match in $functionMatches) {
        $functionName = $match.Groups[1].Value
        if ($functionName -ne "__init__") {
            $analysis.Functions += $functionName
        }
    }
    
    # Verifica problemas comuns
    if ($analysis.LineCount -gt 500) {
        $analysis.Issues += "Arquivo muito grande ($($analysis.LineCount) linhas). Considere dividir em módulos menores."
    }
    
    if ($analysis.Imports.Count -gt 15) {
        $analysis.Issues += "Muitas importações ($($analysis.Imports.Count)). Considere refatorar."
    }
    
    if (($analysis.Functions.Count + $analysis.Classes.Count) -eq 0) {
        $analysis.Issues += "Nenhuma função ou classe encontrada. Verificar se o arquivo está em uso."
    }
    
    return $analysis
}

# Cabeçalho do relatório
$report = @"
# Análise dos Serviços

**Data da Análise:** $(Get-Date -Format "dd/MM/yyyy HH:mm:ss")
**Diretório Analisado:** $servicesPath

"@

# Obtém todos os arquivos Python no diretório de serviços
$pythonFiles = Get-ChildItem -Path $servicesPath -Filter "*.py" -Recurse | 
              Where-Object { $_.Name -ne "__init__.py" } |
              Sort-Object Name

$totalFiles = $pythonFiles.Count
$totalLines = 0
$totalSizeKB = 0
$allIssues = @()

$report += "## Resumo da Análise\n"
$report += "- Total de arquivos Python: $totalFiles\n"

# Analisa cada arquivo
$fileAnalyses = @()
foreach ($file in $pythonFiles) {
    $analysis = Analyze-PythonFile -filePath $file.FullName
    $fileAnalyses += $analysis
    $totalLines += $analysis.LineCount
    $totalSizeKB += $analysis.SizeKB
    
    if ($analysis.Issues.Count -gt 0) {
        $allIssues += @{
            File = $analysis.FileName
            Issues = $analysis.Issues
        }
    }
}

# Adiciona estatísticas ao relatório
$avgLines = if ($totalFiles -gt 0) { [math]::Round($totalLines / $totalFiles, 2) } else { 0 }
$avgSizeKB = if ($totalFiles -gt 0) { [math]::Round($totalSizeKB / $totalFiles, 2) } else { 0 }

$report += "- Total de linhas de código: $totalLines\n"
$report += "- Média de linhas por arquivo: $avgLines\n"
$report += "- Tamanho total dos arquivos: $totalSizeKB KB\n"
$report += "- Tamanho médio dos arquivos: $avgSizeKB KB\n\n"

# Adiciona seção de problemas encontrados
if ($allIssues.Count -gt 0) {
    $report += "## 🚨 Problemas Encontrados\n\n"
    foreach ($issue in $allIssues) {
        $report += "### $($issue.File)\n"
        foreach ($item in $issue.Issues) {
            $report += "- [ ] $item\n"
        }
        $report += "\n"
    }
} else {
    $report += "## ✅ Nenhum problema crítico encontrado\n\n"
}

# Adiciona análise detalhada de cada arquivo
$report += "## 📁 Análise Detalhada por Arquivo\n\n"

foreach ($analysis in $fileAnalyses) {
    $report += "### 📄 $($analysis.FileName)\n"
    $report += "- **Tamanho:** $($analysis.SizeKB) KB\n"
    $report += "- **Linhas de código:** $($analysis.LineCount)\n"
    
    if ($analysis.Classes.Count -gt 0) {
        $report += "- **Classes:** $($analysis.Classes.Count\n"
        foreach ($class in $analysis.Classes) {
            $report += "  - $($class.Name)"
            if ($class.BaseClass) { $report += " (herda de $($class.BaseClass))" }
            $report += "\n"
        }
    }
    
    if ($analysis.Functions.Count -gt 0) {
        $report += "- **Funções/Métodos:** $($analysis.Functions.Count)\n"
        foreach ($func in $analysis.Functions | Select-Object -First 5) {
            $report += "  - $func\n"
        }
        if ($analysis.Functions.Count -gt 5) {
            $report += "  - ... e mais $($analysis.Functions.Count - 5) funções\n"
        }
    }
    
    if ($analysis.Imports.Count -gt 0) {
        $report += "- **Principais importações:**\n"
        foreach ($import in $analysis.Imports | Select-Object -First 5) {
            $report += "  - `$import\n"
        }
        if ($analysis.Imports.Count -gt 5) {
            $report += "  - ... e mais $($analysis.Imports.Count - 5) importações\n"
        }
    }
    
    if ($analysis.Issues.Count -gt 0) {
        $report += "- **Problemas encontrados:**\n"
        foreach ($issue in $analysis.Issues) {
            $report += "  - [ ] $issue\n"
        }
    }
    
    $report += "\n---\n\n"
}

# Salva o relatório
$report | Out-File -FilePath $outputFile -Encoding UTF8

# Exibe resumo
Write-Host "✅ ANÁLISE DE SERVIÇOS CONCLUÍDA" -ForegroundColor Green
Write-Host "📄 Relatório salvo em: $outputFile" -ForegroundColor Cyan
Write-Host "📊 Estatísticas:" -ForegroundColor Cyan
Write-Host "   - Arquivos analisados: $totalFiles"
Write-Host "   - Total de linhas: $totalLines"
Write-Host "   - Problemas encontrados: $($allIssues.Count)"
Write-Host "\n🔍 Dica: Abra o relatório em um visualizador de Markdown para melhor formatação" -ForegroundColor Yellow
