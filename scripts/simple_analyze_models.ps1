# Script simplificado para análise de modelos
# Gera um relatório básico dos modelos encontrados no projeto

# Configuração
$basePath = (Get-Item -Path "$PSScriptRoot\..").FullName
$modulesPath = Join-Path $basePath "backend\app\modules"
$outputDir = Join-Path $basePath "reports"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$outputFile = Join-Path $outputDir "simple_models_analysis_${timestamp}.txt"

# Garante que o diretório de saída existe
Write-Host "Verificando diretório de saída: $outputDir" -ForegroundColor Cyan
if (-not (Test-Path -Path $outputDir)) {
    Write-Host "Criando diretório de saída..." -ForegroundColor Yellow
    try {
        $null = New-Item -ItemType Directory -Path $outputDir -Force -ErrorAction Stop
        Write-Host "✅ Diretório criado com sucesso" -ForegroundColor Green
    } catch {
        Write-Host "❌ ERRO ao criar diretório: $_" -ForegroundColor Red
        Write-Host "Tentando criar diretório em outra localização..." -ForegroundColor Yellow
        
        # Tenta criar o diretório no diretório temporário
        $outputDir = Join-Path $env:TEMP "sila_analysis"
        $outputFile = Join-Path $outputDir "simple_models_analysis_${timestamp}.txt"
        
        try {
            $null = New-Item -ItemType Directory -Path $outputDir -Force -ErrorAction Stop
            Write-Host "✅ Diretório temporário criado com sucesso: $outputDir" -ForegroundColor Green
        } catch {
            Write-Host "❌ ERRO crítico: Não foi possível criar diretório em nenhuma localização" -ForegroundColor Red
            exit 1
        }
    }
} else {
    Write-Host "✅ Diretório de saída já existe" -ForegroundColor Green
}

Write-Host "🔍 Iniciando análise de modelos em: $modulesPath" -ForegroundColor Cyan
Write-Host "📄 Arquivo de saída: $outputFile" -ForegroundColor Cyan

# Inicializa o relatório
$report = @()
$report += "# Análise Básica dos Modelos do Backend"
$report += ""
$report += "Data da Análise: $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')"
$report += "Diretório Base: $modulesPath"
$report += ""

# Verifica se o diretório de módulos existe
if (-not (Test-Path -Path $modulesPath)) {
    $errorMsg = "ERRO: O diretório de módulos não foi encontrado em: $modulesPath"
    $report += "## ERRO NA ANALISE"
    $report += $errorMsg
    $report | Out-File -FilePath $outputFile -Encoding UTF8
    Write-Host $errorMsg -ForegroundColor Red
    exit 1
}

# Encontra todos os arquivos Python nos diretórios de modelos
Write-Host "🔍 Procurando arquivos de modelo..." -ForegroundColor Cyan
$modelFiles = @()

try {
    $allPythonFiles = Get-ChildItem -Path $modulesPath -Recurse -Filter "*.py" -ErrorAction Stop
    Write-Host "✅ Encontrados $($allPythonFiles.Count) arquivos .py" -ForegroundColor Green
    
    $modelFiles = $allPythonFiles |
                 Where-Object { $_.FullName -match '\\models(?:\\|$)' -and $_.Name -ne "__init__.py" } |
                 Sort-Object FullName
                 
    Write-Host "✅ Encontrados $($modelFiles.Count) arquivos de modelo" -ForegroundColor Green
} catch {
    $errorMsg = "ERRO ao buscar arquivos de modelo: $_"
    $report += "## ERRO NA ANALISE"
    $report += $errorMsg
    $report | Out-File -FilePath $outputFile -Encoding UTF8
    Write-Host $errorMsg -ForegroundColor Red
    exit 1
}

if ($modelFiles.Count -eq 0) {
    $warningMsg = "AVISO: Nenhum arquivo de modelo encontrado no diretório: $modulesPath"
    $report += "## AVISO"
    $report += $warningMsg
    $report | Out-File -FilePath $outputFile -Encoding UTF8
    Write-Host $warningMsg -ForegroundColor Yellow
    exit 0
}

# Processa os arquivos de modelo
$report += "## RESUMO DA ANALISE"
$report += "- Total de arquivos de modelo: $($modelFiles.Count)"
$report += ""

# Agrupa por módulo
$modules = @{}
foreach ($file in $modelFiles) {
    $moduleName = if ($file.DirectoryName -match '\\([^\\]+)\\models') { $matches[1] } else { "Outros" }
    if (-not $modules.ContainsKey($moduleName)) {
        $modules[$moduleName] = @()
    }
    $modules[$moduleName] += $file
}

# Adiciona análise por módulo
$report += "## ANALISE POR MODULO"
$report += ""

foreach ($moduleName in ($modules.Keys | Sort-Object)) {
    $moduleFiles = $modules[$moduleName]
    $report += "### Modulo: $moduleName"
    $report += "- Arquivos: $($moduleFiles.Count)"
    $report += ""
    
    foreach ($file in $moduleFiles) {
        $report += "Arquivo: $($file.Name)"
        $report += "Caminho: $($file.FullName)"
        
        # Conta linhas de código
        $lineCount = (Get-Content $file.FullName | Measure-Object -Line).Lines
        $report += "Linhas de código: $lineCount"
        
        # Lê o conteúdo do arquivo para análise básica
        $content = Get-Content $file.FullName -Raw
        
        # Conta classes
        $classCount = ([regex]::Matches($content, 'class\s+\w+')).Count
        $report += "Classes encontradas: $classCount"
        
        # Verifica se tem docstring
        $hasDocstring = $content -match '"""[\s\S]*?"""'
        $report += "Possui documentacao: $(if ($hasDocstring) { 'Sim' } else { 'Nao' })"
        
        $report += ""
    }
    
    $report += "---"
    $report += ""
}

# Adiciona recomendações
$report += "## RECOMENDACOES"
$report += ""
$report += "1. Verificar se todos os modelos tem documentacao adequada"
$report += "2. Padronizar a estrutura dos modelos"
$report += "3. Verificar relacoes entre modelos"
$report += ""

# Salva o relatório
Write-Host "`n📝 Salvando relatório em: $outputFile" -ForegroundColor Cyan
try {
    # Mostra as primeiras 5 linhas do relatório para debug
    Write-Host "`n📋 Preview do relatório (primeiras 5 linhas):" -ForegroundColor Cyan
    $report | Select-Object -First 5 | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
    
    # Tenta salvar o relatório
    Write-Host "`n💾 Salvando arquivo..." -ForegroundColor Cyan
    $report | Out-File -FilePath $outputFile -Encoding UTF8 -Force -ErrorAction Stop
    
    if (Test-Path -Path $outputFile) {
        $fileInfo = Get-Item -Path $outputFile
        Write-Host "`n✅ ANALISE CONCLUIDA COM SUCESSO" -ForegroundColor Green
        Write-Host "📄 Relatorio salvo em: $($fileInfo.FullName)" -ForegroundColor Cyan
        Write-Host "📊 Tamanho do relatorio: $($fileInfo.Length) bytes" -ForegroundColor Cyan
    } else {
        Write-Host "❌ ERRO: Nao foi possivel salvar o relatorio em: $outputFile" -ForegroundColor Red
    }
} catch {
    Write-Host "ERRO ao salvar o relatorio: $_" -ForegroundColor Red
    exit 1
}
