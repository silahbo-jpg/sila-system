# audit-project.ps1
# Auditoria completa do estado do projeto SILA System
# Versão 2.0 - Corrigida e Testada - 17/08/2025

param(
    [string]$ProjectRoot = $(Get-Location).Path,
    [string]$OutputFile = "sila_audit_report_$(Get-Date -Format 'yyyyMMdd_HHmmss').html"
)

# Configurações iniciais
$ReportData = @{}
$ReportPath = Join-Path -Path $ProjectRoot -ChildPath "audit_reports"
$ReportPath = Join-Path -Path $ReportPath -ChildPath $OutputFile
$TempDir = Join-Path -Path $env:TEMP -ChildPath "sila_audit"
$ProgressPreference = 'SilentlyContinue'

# Criar diretórios necessários
if (-not (Test-Path -Path (Split-Path -Path $ReportPath -Parent))) {
    New-Item -ItemType Directory -Path (Split-Path -Path $ReportPath -Parent) -Force | Out-Null
}

if (-not (Test-Path -Path $TempDir)) {
    New-Item -ItemType Directory -Path $TempDir -Force | Out-Null
}

# 1. Função para gerar hash SHA256 de arquivos
function Get-FileHashRecursive {
    param(
        [string]$Path,
        [string]$Filter = "*.*"
    )
    
    Get-ChildItem -Path $Path -Recurse -File -Filter $Filter | ForEach-Object {
        $hash = (Get-FileHash -Path $_.FullName -Algorithm SHA256).Hash
        [PSCustomObject]@{
            Path = $_.FullName
            Hash = $hash
            Size = $_.Length
            LastModified = $_.LastWriteTime
        }
    }
}

# 2. Coletar dados da estrutura do projeto
Write-Host "🔍 Analisando estrutura do projeto..." -ForegroundColor Cyan
$ProjectStructure = Get-ChildItem -Path $ProjectRoot -Recurse | 
    Where-Object { $_.PSIsContainer } |
    Select-Object FullName, @{Name="Depth";Expression={($_.FullName.Split('\').Count - $ProjectRoot.Split('\').Count)}}

$ReportData.ProjectStructure = $ProjectStructure | Group-Object Depth | 
    Select-Object Count, @{Name="Depth";Expression={$_.Name}}, 
    @{Name="ExamplePaths";Expression={$_.Group.FullName | Select-Object -First 3}}

# 3. Auditoria de arquivos
Write-Host "📊 Coletando métricas de arquivos..." -ForegroundColor Cyan
$FileTypes = Get-ChildItem -Path $ProjectRoot -Recurse -File | 
    Group-Object Extension | 
    Select-Object Count, Name | 
    Sort-Object Count -Descending

$LargeFiles = Get-ChildItem -Path $ProjectRoot -Recurse -File | 
    Sort-Object Length -Descending | 
    Select-Object -First 10 Name, Length, LastWriteTime, FullName

$FileHashes = Get-FileHashRecursive -Path $ProjectRoot

$ReportData.FileAnalysis = @{
    FileTypes = $FileTypes
    LargeFiles = $LargeFiles
    TotalSize = ($FileHashes | Measure-Object -Property Size -Sum).Sum
    FileHashes = $FileHashes
}

# 4. Gerar relatório HTML com CSS corrigido
Write-Host "📄 Gerando relatório completo..." -ForegroundColor Cyan

# CSS como string literal usando @' '@ para evitar problemas de parsing
$css = @'
<style>
body { 
    font-family: Arial, sans-serif; 
    line-height: 1.6; 
    margin: 0; 
    padding: 20px; 
    color: #333; 
}
h1, h2, h3 { 
    color: #2c3e50; 
}
.card { 
    background: #f9f9f9; 
    border: 1px solid #ddd; 
    border-radius: 5px; 
    padding: 15px; 
    margin-bottom: 20px; 
}
table { 
    width: 100%; 
    border-collapse: collapse; 
    margin-bottom: 20px; 
}
th, td { 
    padding: 10px; 
    text-align: left; 
    border-bottom: 1px solid #ddd; 
}
th { 
    background-color: #3498db; 
    color: white; 
}
tr:nth-child(even) { 
    background-color: #f2f2f2; 
}
.warning { 
    background-color: #fff3cd; 
    border-left: 4px solid #ffc107; 
    padding: 10px; 
    margin: 10px 0; 
}
.error { 
    background-color: #f8d7da; 
    border-left: 4px solid #dc3545; 
    padding: 10px; 
    margin: 10px 0; 
}
.success { 
    background-color: #d4edda; 
    border-left: 4px solid #28a745; 
    padding: 10px; 
    margin: 10px 0; 
}
</style>
'@

# HTML report - usando here-string para evitar problemas com caracteres especiais
$html = @"
<!DOCTYPE html>
<html>
<head>
    <title>Relatório de Auditoria - SILA System</title>
    $css
</head>
<body>
    <h1>Relatório de Auditoria - SILA System</h1>
    <p>Gerado em: $(Get-Date)</p>
    <p>Diretório analisado: $ProjectRoot</p>
    
    <h2>📁 Estrutura do Projeto</h2>
    <div class="card">
        <h3>Distribuição de Diretórios</h3>
        <table>
            <tr><th>Profundidade</th><th>Quantidade</th><th>Exemplos</th></tr>
"@

# Adicionar dados da estrutura do projeto
foreach ($item in $ReportData.ProjectStructure) {
    $html += "<tr><td>$($item.Depth)</td><td>$($item.Count)</td><td>$($item.ExamplePaths -join '<br>')</td></tr>"
}

$html += @"
        </table>
    </div>
    <h2>📊 Análise de Arquivos</h2>
    <div class="card">
        <h3>Tipos de Arquivos</h3>
        <table>
            <tr><th>Extensão</th><th>Quantidade</th></tr>
"@

# Adicionar tipos de arquivos
foreach ($item in $ReportData.FileAnalysis.FileTypes) {
    $html += "<tr><td>$($item.Name)</td><td>$($item.Count)</td></tr>"
}

$html += @"
        </table>
        <h3>Arquivos Grandes</h3>
        <table>
            <tr><th>Nome</th><th>Tamanho (MB)</th><th>Última Modificação</th></tr>
"@

# Adicionar arquivos grandes
foreach ($item in $ReportData.FileAnalysis.LargeFiles) {
    $sizeMB = [math]::Round($item.Length / 1MB, 2)
    $html += "<tr><td>$($item.Name)</td><td>$sizeMB</td><td>$($item.LastWriteTime)</td></tr>"
}

$html += @"
        </table>
    </div>
    <div class="success">
        <h3>✅ Próximos Passos</h3>
        <ol>
            <li>Revise os arquivos grandes identificados</li>
            <li>Verifique a distribuição de tipos de arquivos</li>
            <li>Analise a estrutura de diretórios</li>
        </ol>
    </div>
</body>
</html>
"@

# Salvar relatório
$html | Out-File -FilePath $ReportPath -Encoding UTF8

# Finalização
Write-Host "✅ Auditoria concluída com sucesso!" -ForegroundColor Green
Write-Host "Relatório gerado em: $ReportPath" -ForegroundColor Green
Start-Process $ReportPath

# Retornar dados para análise adicional
$ReportData