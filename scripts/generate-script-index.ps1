# Script para gerar o índice técnico de scripts Python do projeto sila_dev
# Autor: Equipe de Desenvolvimento sila_dev
# Data: 2025-08-11

# Definição de variáveis
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectsila_dev-system = Split-Path -Parent $scriptPath
$pythonScript = Join-Path $scriptPath "generate_script_index.py"
$outputFile = Join-Path $projectsila_dev-system "docs\INDICE_TECNICO.md"

# Verifica se o Python está instalado
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Erro: Python não encontrado. Por favor, instale o Python e tente novamente." -ForegroundColor Red
    exit 1
}

# Executa o script Python para gerar o índice técnico
Write-Host "Gerando índice técnico de scripts Python..." -ForegroundColor Cyan

try {
    # Executa o script Python
    python $pythonScript
    
    # Verifica se o arquivo de saída foi criado
    if (Test-Path $outputFile) {
        Write-Host "✅ Índice técnico gerado com sucesso em: $outputFile" -ForegroundColor Green
        
        # Exibe estatísticas básicas do arquivo gerado
        $content = Get-Content $outputFile
        $totalLines = $content.Count
        $scriptCount = ($content | Select-String -Pattern "Total de scripts Python: (\d+)" -AllMatches).Matches.Groups[1].Value
        
        Write-Host "📊 Estatísticas:" -ForegroundColor Yellow
        Write-Host "   - Total de scripts indexados: $scriptCount" -ForegroundColor Yellow
        Write-Host "   - Tamanho do índice: $totalLines linhas" -ForegroundColor Yellow
        
        # Pergunta se deseja abrir o arquivo
        $openFile = Read-Host "Deseja abrir o índice técnico agora? (S/N)"
        if ($openFile -eq "S" -or $openFile -eq "s") {
            Invoke-Item $outputFile
        }
    } else {
        Write-Host "❌ Erro: O arquivo de índice não foi gerado." -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Erro ao executar o script: $_" -ForegroundColor Red
    exit 1
}

