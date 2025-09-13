# Script para build automatizado do frontend SILA
# Executa build do React e retorna código de saída apropriado

Write-Host "Iniciando build automatizado do frontend..." -ForegroundColor Cyan

$frontendPath = ".\frontend\webapp"

if (Test-Path $frontendPath) {
    Push-Location $frontendPath
    try {
        if (Test-Path "package.json") {
            Write-Host "Instalando dependências do frontend..." -ForegroundColor Yellow
            npm install
            if ($LASTEXITCODE -ne 0) {
                Write-Host "[ERRO] Falha ao instalar dependências do frontend." -ForegroundColor Red
                Pop-Location
                exit 1
            }
            Write-Host "Executando build do frontend..." -ForegroundColor Yellow
            npm run build
            if ($LASTEXITCODE -ne 0) {
                Write-Host "[ERRO] Build do frontend falhou." -ForegroundColor Red
                Pop-Location
                exit 1
            }
            Write-Host "Build do frontend concluído com sucesso." -ForegroundColor Green
            Pop-Location
            exit 0
        } else {
            Write-Host "[ERRO] package.json não encontrado no diretório do frontend." -ForegroundColor Red
            Pop-Location
            exit 1
        }
    } catch {
        Write-Host "[ERRO] Falha ao executar build do frontend: $_" -ForegroundColor Red
        Pop-Location
        exit 1
    }
} else {
    Write-Host "[ERRO] Diretório do frontend não encontrado: $frontendPath" -ForegroundColor Red
    exit 1
}

