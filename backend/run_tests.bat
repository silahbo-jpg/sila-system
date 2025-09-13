@echo off
REM Script para execução de testes no Windows

echo ===============================================
echo  Executando Testes Automatizados - SILA System
echo ===============================================

:: Verifica se o Python está instalado
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Erro: Python não encontrado no PATH.
    echo Por favor, instale o Python ou adicione-o ao PATH.
    pause
    exit /b 1
)

echo.
echo [1/4] Instalando dependências...
python -m pip install --upgrade pip
if %ERRORLEVEL% neq 0 (
    echo Erro ao atualizar o pip.
    pause
    exit /b 1
)

pip install -r requirements-test.txt
if %ERRORLEVEL% neq 0 (
    echo Erro ao instalar dependências.
    pause
    exit /b 1
)

echo.
echo [2/4] Executando testes com cobertura...
python -m pytest -v --cov=app --cov-report=term-missing --cov-report=html:htmlcov
if %ERRORLEVEL% neq 0 (
    echo.
    echo AVISO: Alguns testes falharam. Verifique os logs acima.
    echo.
)

echo.
echo [3/4] Verificando cobertura mínima...
python -m coverage report --fail-under=80
if %ERRORLEVEL% neq 0 (
    echo.
    echo AVISO: Cobertura de código abaixo de 80%%.
    echo.
)

echo.
echo [4/4] Abrindo relatório de cobertura...
start "" "htmlcov\index.html" 2>nul || (
    echo Não foi possível abrir o relatório automaticamente.
    echo Por favor, abra manualmente o arquivo htmlcov\index.html
)

echo.
echo ===============================================
echo  Processo de teste concluído!
echo ===============================================

pause

