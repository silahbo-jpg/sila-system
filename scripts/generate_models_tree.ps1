# Caminho base para os modelos
$basePath = "backend/app"

# Inicializa a saida
$treeOutput = @()
$reportContent = @()

# Cores (para Write-Host, mas nao sao usadas no Markdown)
$colors = @{
    Package = "Yellow"
    Module = "Cyan"
    Directory = "Green"
    File = "Magenta"
}

# Funcao recursiva para construir arvore
function Build-Tree {
    param (
        [string]$path,
        [int]$level = 0
    )

    $indent = ' ' * ($level * 4)

    # Diretorios
    Get-ChildItem -Path $path -Directory | ForEach-Object {
        $treeOutput += $indent + '[DIR] ' + $_.Name
        Build-Tree -path $_.FullName -level ($level + 1)
    }

    # Arquivos .py
    Get-ChildItem -Path $path -File -Filter '*.py' | ForEach-Object {
        $treeOutput += $indent + '[FILE] ' + $_.Name
    }
}

# Processar cada modulo dentro de backend/app/
Get-ChildItem -Path $basePath -Directory | ForEach-Object {
    $moduleName = $_.Name

    $treeOutput += ''
    $treeOutput += '[PACOTE] Modulo: ' + $moduleName
    $treeOutput += ('-' * 80)

    # Arvore do modulo
    Build-Tree -path $_.FullName -level 1

    # Estatisticas
    $pyFiles = Get-ChildItem -Path $_.FullName -Recurse -File -Filter '*.py'
    $lineCount = 0
    foreach ($file in $pyFiles) {
        $lineCount += (Get-Content $file.FullName | Measure-Object -Line).Lines
    }

    $treeOutput += 'Estatisticas:'
    $treeOutput += '    Numero de arquivos .py: ' + $pyFiles.Count
    $treeOutput += '    Total de linhas de codigo: ' + $lineCount
    $treeOutput += ('=' * 80)

    # Relatorio detalhado
    $reportContent += '## Modulo: ' + $moduleName
    $reportContent += ''
    $reportContent += '### Estrutura de Diretorios'
    $reportContent += '```'
    Build-Tree -path $_.FullName -level 1
    $reportContent += '```'
    $reportContent += ''
    $reportContent += '### Estatisticas'
    $reportContent += '- Numero de arquivos .py: ' + $pyFiles.Count
    $reportContent += '- Total de linhas de codigo: ' + $lineCount
    $reportContent += ''
    $reportContent += '---'
    $reportContent += ''
}

# Garantir que pasta reports/directory_trees/specific existe
if (-not (Test-Path -Path "reports/directory_trees/specific")) {
    New-Item -ItemType Directory -Path "reports/directory_trees/specific" | Out-Null
}

# Salvar arvore
$treeFile = "reports/directory_trees/specific/models_tree.txt"
$treeOutput | Out-File -FilePath $treeFile -Encoding UTF8

# Salvar relatorio
$reportFile = "reports/directory_trees/specific/models_report.md"
$reportContent | Out-File -FilePath $reportFile -Encoding UTF8

# Exibir resultado
Write-Host ''
Write-Host 'Arquivos gerados com sucesso:' -ForegroundColor Green
Write-Host ' - ' $treeFile -ForegroundColor Cyan
Write-Host ' - ' $reportFile -ForegroundColor Cyan
