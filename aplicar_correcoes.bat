@echo off
echo ===================================================
echo    SILA - Assistente de Correcao Automatica
echo ===================================================
echo.

echo Iniciando processo de correcao...
echo.

cd scripts

echo Executando scripts de correcao...
powershell -ExecutionPolicy Bypass -File .\fix-all.ps1

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Ocorreram erros durante a execucao. Tentando recuperacao avancada...
    python recreate-critical-files.py
    echo.
    echo Por favor, verifique os erros acima e tente novamente.
    pause
    exit /b 1
)

echo.
echo Verificando arquivos criticos...
python recreate-critical-files.py

echo.
echo ===================================================
echo    Correcao concluida com sucesso!
echo ===================================================
echo.
echo Proximos passos:
echo 1. Recrie o ambiente virtual:
echo    cd backend
echo    python -m venv .venv
echo    .venv\Scripts\activate
echo    pip install -r requirements.txt
echo    python -m prisma generate
echo 2. Rode o servidor:
echo    uvicorn app.main:app --reload
echo.

pause
