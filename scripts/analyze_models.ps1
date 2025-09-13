# Script para analisar modelos do backend
# Saída salva em: reports/models_analysis_<timestamp>.md

# Configurações iniciais
$basePath = (Get-Item -Path "$PSScriptRoot\..").FullName
$modulesPath = Join-Path $basePath "backend\app\modules"
$outputDir = Join-Path $basePath "reports"

# Garante que o diretório de saída existe
if (-not (Test-Path -Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$outputFile = Join-Path $outputDir "models_analysis_${timestamp}.md"

# Inicializa o relatório como array de linhas
$reportLines = @()
$reportLines += "# Análise dos Modelos do Backend"
$reportLines += ""
$reportLines += "Data da Análise: $(Get-Date -Format "dd/MM/yyyy HH:mm:ss")"
$reportLines += "Diretório Base: $modulesPath"
$reportLines += ""

# Verifica se o diretório de módulos existe
if (-not (Test-Path -Path $modulesPath)) {
    $errorMsg = "ERRO: O diretório de módulos não foi encontrado em: $modulesPath"
    $reportLines += "## ❌ Erro na Análise"
    $reportLines += ""
    $reportLines += $errorMsg
    $reportLines += ""
    $reportLines | Out-File -FilePath $outputFile -Encoding UTF8
    Write-Host $errorMsg -ForegroundColor Red
    exit 1
}

Write-Host "🔍 Iniciando análise de modelos em: $modulesPath" -ForegroundColor Cyan
Write-Host "📂 Diretório de saída: $outputDir" -ForegroundColor Cyan
Write-Host "📄 Arquivo de saída: $outputFile" -ForegroundColor Cyan

# Função para analisar um arquivo de modelo
function Analyze-ModelFile {
    param (
        [string]$filePath
    )
    
    $analysis = @{
        FileName = [System.IO.Path]::GetFileName($filePath)
        FilePath = $filePath
        Module = ""
        Classes = @()
        LineCount = 0
        SizeKB = [math]::Round((Get-Item $filePath).Length / 1KB, 2)
        Issues = @()
    }
    
    # Extrai o nome do módulo do caminho
    $moduleMatch = [regex]::Match($filePath, 'modules\\([^\\]+)\\models')
    if ($moduleMatch.Success) {
        $analysis.Module = $moduleMatch.Groups[1].Value
    }
    
    $content = Get-Content -Path $filePath -Raw -ErrorAction SilentlyContinue
    if (-not $content) {
        $analysis.Issues += "Falha ao ler o arquivo"
        return $analysis
    }
    
    $analysis.LineCount = ($content -split "`r`n" | Measure-Object).Count
    
    # Extrai classes
    $classMatches = [regex]::Matches($content, '^class\s+(\w+)(?:\s*\(([^)]*)\))?', [System.Text.RegularExpressions.RegexOptions]::Multiline)
    foreach ($match in $classMatches) {
        $className = $match.Groups[1].Value
        $baseClass = $match.Groups[2].Value
        
        # Extrai o nome da tabela
        $tableName = ""
        $tableLine = ($content -split "`n" | Where-Object { $_ -match "__tablename__" } | Select-Object -First 1)
        if ($tableLine) {
            $tableParts = $tableLine -split "='"
            if ($tableParts.Count -gt 1) {
                $tableName = ($tableParts[1] -split "'")[0]
            } else {
                $tableParts = $tableLine -split '="'
                if ($tableParts.Count -gt 1) {
                    $tableName = ($tableParts[1] -split '"')[0]
                }
            }
        }
        
        $analysis.Classes += @{
            Name = $className
            BaseClass = $baseClass
            TableName = $tableName
            Columns = @()
        }
    }
    
    # Verifica problemas comuns
    if ($analysis.LineCount -gt 1000) {
        $analysis.Issues += "Arquivo muito grande ($($analysis.LineCount) linhas). Considere dividir em módulos menores."
    }
    
    if ($analysis.Classes.Count -eq 0) {
        $analysis.Issues += "Nenhuma classe de modelo encontrada no arquivo."
    }
    
    return $analysis
}

Write-Host "🔍 Procurando arquivos de modelo..." -ForegroundColor Cyan

# Encontra todos os arquivos Python nos diretórios de modelos
Write-Host "🔍 Procurando arquivos de modelo em: $modulesPath" -ForegroundColor Cyan
$modelFiles = @()

try {
    Write-Host "🔍 Buscando arquivos .py em subdiretórios..." -ForegroundColor Cyan
    $allPythonFiles = Get-ChildItem -Path $modulesPath -Recurse -Filter "*.py" -ErrorAction Stop
    Write-Host "✅ Encontrados $($allPythonFiles.Count) arquivos .py" -ForegroundColor Green
    
    $modelFiles = $allPythonFiles |
                 Where-Object { $_.FullName -match '\\models(?:\\|$)' -and $_.Name -ne "__init__.py" } |
                 Sort-Object FullName
                 
    Write-Host "✅ Encontrados $($modelFiles.Count) arquivos de modelo" -ForegroundColor Green
} catch {
    $errorMsg = "ERRO ao buscar arquivos de modelo: $_"
    $reportLines += "## ❌ Erro na Análise"
    $reportLines += ""
    $reportLines += $errorMsg
    $reportLines += ""
    $reportLines | Out-File -FilePath $outputFile -Encoding UTF8
    Write-Host $errorMsg -ForegroundColor Red
    exit 1
}

if ($modelFiles.Count -eq 0) {
    $warningMsg = "AVISO: Nenhum arquivo de modelo encontrado no diretório: $modulesPath"
    $reportLines += "## ⚠️ Aviso"
    $reportLines += ""
    $reportLines += $warningMsg
    $reportLines += ""
    $reportLines | Out-File -FilePath $outputFile -Encoding UTF8
    Write-Host $warningMsg -ForegroundColor Yellow
    exit 0
}

Write-Host "✅ Encontrados $($modelFiles.Count) arquivos de modelo para análise" -ForegroundColor Green

$totalFiles = $modelFiles.Count
$totalClasses = 0
$totalLines = 0
$totalSizeKB = 0
$allIssues = @()

$reportLines += "## Resumo da Análise"
$reportLines += "- Total de arquivos de modelo: $totalFiles"
$reportLines += ""

# Agrupa por módulo
$modules = @{}
foreach ($file in $modelFiles) {
    $moduleMatch = [regex]::Match($file.FullName, 'modules\\([^\\]+)\\models')
    $moduleName = if ($moduleMatch.Success) { $moduleMatch.Groups[1].Value } else { "Outros" }
    
    if (-not $modules.ContainsKey($moduleName)) {
        $modules[$moduleName] = @()
    }
    
    $analysis = Analyze-ModelFile -filePath $file.FullName
    $modules[$moduleName] += $analysis
    
    $totalClasses += $analysis.Classes.Count
    $totalLines += $analysis.LineCount
    $totalSizeKB += $analysis.SizeKB
    
    if ($analysis.Issues.Count -gt 0) {
        $allIssues += @{
            File = $file.FullName
            Issues = $analysis.Issues
        }
    }
}

# Adiciona estatísticas ao relatório
$avgLines = if ($totalFiles -gt 0) { [math]::Round($totalLines / $totalFiles, 2) } else { 0 }
$avgClasses = if ($totalFiles -gt 0) { [math]::Round($totalClasses / $totalFiles, 2) } else { 0 }
$avgSizeKB = if ($totalFiles -gt 0) { [math]::Round($totalSizeKB / $totalFiles, 2) } else { 0 }

$reportLines += "- Total de classes de modelo: $totalClasses"
$reportLines += "- Média de classes por arquivo: $avgClasses"
$reportLines += "- Total de linhas de código: $totalLines"
$reportLines += "- Média de linhas por arquivo: $avgLines"
$reportLines += "- Tamanho total dos arquivos: $totalSizeKB KB"
$reportLines += "- Tamanho médio dos arquivos: $avgSizeKB KB"
$reportLines += ""

# Adiciona seção de problemas encontrados
if ($allIssues.Count -gt 0) {
    $reportLines += "## PROBLEMAS ENCONTRADOS"
    $reportLines += ""
    foreach ($issue in $allIssues) {
        $shortPath = $issue.File.Replace($basePath, '...')
        $reportLines += "### $shortPath"
        foreach ($item in $issue.Issues) {
            $reportLines += "- [ ] $item"
        }
        $reportLines += ""
    }
} else {
    $reportLines += "## NENHUM PROBLEMA CRITICO ENCONTRADO"
    $reportLines += ""
}

# Adiciona análise detalhada por módulo
$reportLines += "## ANALISE POR MODULO"
$reportLines += ""

foreach ($moduleName in ($modules.Keys | Sort-Object)) {
    $moduleFiles = $modules[$moduleName]
    $moduleClasses = ($moduleFiles | ForEach-Object { $_.Classes } | Measure-Object).Count
    $moduleLines = ($moduleFiles | Measure-Object -Property LineCount -Sum).Sum
    $moduleSizeKB = [math]::Round(($moduleFiles | Measure-Object -Property SizeKB -Sum).Sum, 2)
    
    $reportLines += "### Módulo: $moduleName"
    $reportLines += "- **Arquivos:** $($moduleFiles.Count)"
    $reportLines += "- **Classes:** $moduleClasses"
    $reportLines += "- **Linhas de código:** $moduleLines"
    $reportLines += "- **Tamanho total:** $moduleSizeKB KB"
    $reportLines += ""
    
    $reportLines += "#### Classes do Módulo"
    $reportLines += ""
    
    foreach ($file in $moduleFiles) {
        $reportLines += "📄 **$($file.FileName)**"
        
        foreach ($class in $file.Classes) {
            $classLine = "- **$($class.Name)**"
            if ($class.BaseClass) { $classLine += " (herda de $($class.BaseClass))" }
            if ($class.TableName) { $classLine += " → Tabela: `$($class.TableName)`" }
            $reportLines += $classLine
        }
        
        # Adiciona problemas, se houver
        foreach ($issue in $file.Issues) {
            $line = "  - ATENCAO: $issue"
            $reportLines += $line
        }
        
        $reportLines += ""
    }
    
    $reportLines += "---"
    $reportLines += ""
}

# Adiciona seção de recomendações
$reportLines += "## RECOMENDACOES"
$reportLines += ""
$reportLines += "1. **Padronização de Modelos**"
$reportLines += "   - Verificar se todos os modelos seguem o mesmo padrão de nomenclatura"
$reportLines += "   - Garantir que todos os modelos tenham docstrings adequadas"
$reportLines += "   - Verificar se todos os campos obrigatórios estão com as restrições corretas (nullable, unique, etc.)"
$reportLines += ""
$reportLines += "2. **Documentação**"
$reportLines += "   - Atualizar a documentação dos modelos para refletir a estrutura atual"
$reportLines += "   - Adicionar exemplos de uso para modelos complexos"
$reportLines += ""
$reportLines += "3. **Validação**"
$reportLines += "   - Implementar validação de dados nos modelos quando aplicável"
$reportLines += "   - Verificar se há campos que poderiam ser enums"
$reportLines += ""
$reportLines += "4. **Indexação**"
$reportLines += "   - Avaliar a necessidade de adicionar índices para campos frequentemente consultados"
$reportLines += "   - Verificar se há consultas que poderiam se beneficiar de índices compostos"
$reportLines += ""
$reportLines += "5. **Relacionamentos**"
$reportLines += "   - Revisar os relacionamentos entre os modelos"
$reportLines += "   - Verificar se há necessidade de adicionar restrições de chave estrangeira"
$reportLines += ""
$reportLines += "6. **Migrações**"
$reportLines += "   - Revisar as migrações existentes para garantir que refletem o estado atual dos modelos"
$reportLines += "   - Considerar criar migrações de dados para corrigir inconsistências"
$reportLines += ""

# Salva o relatório
try {
    # Mostra o caminho completo do arquivo de saída
    $fullOutputPath = (Resolve-Path $outputFile -ErrorAction SilentlyContinue).Path
    if (-not $fullOutputPath) {
        $fullOutputPath = $outputFile
    }
    
    # Garante que o diretório de saída existe
    $outputDir = [System.IO.Path]::GetDirectoryName($outputFile)
    if (-not (Test-Path -Path $outputDir)) {
        New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
        Write-Host "📂 Criado diretório de saída: $outputDir" -ForegroundColor Yellow
    }
    
    # Converte as linhas do relatório para uma única string
    $reportContent = $reportLines -join "`r`n"
    
    # Salva o relatório
    $reportContent | Out-File -FilePath $outputFile -Encoding UTF8 -Force
    
    # Verifica se o arquivo foi criado
    if (Test-Path -Path $outputFile) {
        $fileInfo = Get-Item -Path $outputFile
        Write-Host "`n✅ ANÁLISE DE MODELOS CONCLUÍDA COM SUCESSO" -ForegroundColor Green
        Write-Host "📄 Relatório salvo em: $($fileInfo.FullName)" -ForegroundColor Cyan
        Write-Host "📊 Tamanho do relatório: $($fileInfo.Length) bytes" -ForegroundColor Cyan
        Write-Host "📊 Estatísticas:" -ForegroundColor Cyan
        Write-Host "   - Módulos analisados: $($modules.Count)"
        Write-Host "   - Arquivos de modelo: $totalFiles"
        Write-Host "   - Classes de modelo: $totalClasses"
        Write-Host "   - Problemas encontrados: $($allIssues.Count)"
    } else {
        Write-Host "❌ ERRO: Não foi possível salvar o relatório em: $outputFile" -ForegroundColor Red
        Write-Host "Conteúdo do relatório que não pôde ser salvo:"
        Write-Host "----------------------------------------"
        $report | Out-String
        Write-Host "----------------------------------------"
        exit 1
    }
    
} catch {
    Write-Host "ERRO ao salvar o relatório: $_" -ForegroundColor Red
    exit 1
}