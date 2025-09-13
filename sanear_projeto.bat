@echo off
setlocal enabledelayedexpansion

echo ===============================================================================
echo                         SANEAMENTO DO PROJETO SILA                            
echo ===============================================================================
echo.
echo Este script executa as acoes recomendadas para saneamento do projeto SILA,
echo com foco na resolucao de problemas de portabilidade entre WSL2 e Windows 10.
echo.
echo ATENCAO: Certifique-se de ter feito backup do projeto antes de continuar.
echo.

:menu
echo Escolha uma opcao:
echo 1. Limpar arquivos de cache Python e bibliotecas Linux
echo 2. Verificar e corrigir estrutura dos modulos
echo 3. Converter scripts shell para PowerShell
echo 4. Verificar pacotes binarios
echo 5. Ver recomendacoes de saneamento
echo 6. Sair
echo.

set /p opcao=Opcao: 

if "%opcao%"=="1" goto limpar_cache
if "%opcao%"=="2" goto corrigir_modulos
if "%opcao%"=="3" goto converter_scripts
if "%opcao%"=="4" goto verificar_binarios
if "%opcao%"=="5" goto ver_recomendacoes
if "%opcao%"=="6" goto sair

echo Opcao invalida!
goto menu

:limpar_cache
echo.
echo Executando script de limpeza de cache Python...
powershell -ExecutionPolicy Bypass -File .\scripts\clean_python_cache.ps1
echo.
echo Pressione qualquer tecla para voltar ao menu...
pause > nul
goto menu

:corrigir_modulos
echo.
echo Executando script de correcao de estrutura de modulos...
powershell -ExecutionPolicy Bypass -File .\scripts\fix_module_structure.ps1
echo.
echo Pressione qualquer tecla para voltar ao menu...
pause > nul
goto menu

:converter_scripts
echo.
echo Executando script de conversao de scripts shell para PowerShell...
powershell -ExecutionPolicy Bypass -File .\scripts\convert_shell_to_powershell.ps1
echo.
echo Pressione qualquer tecla para voltar ao menu...
pause > nul
goto menu

:verificar_binarios
echo.
echo Executando script de verificacao de pacotes binarios...
python .\scripts\check_binary_packages.py
echo.
echo Pressione qualquer tecla para voltar ao menu...
pause > nul
goto menu

:ver_recomendacoes
echo.
echo Abrindo documento de recomendacoes...
start "" ".\docs\recomendacoes_saneamento.md"
echo.
echo Pressione qualquer tecla para voltar ao menu...
pause > nul
goto menu

:sair
echo.
echo Obrigado por usar o script de saneamento do projeto SILA!
echo.
endlocal
exit /b 0
