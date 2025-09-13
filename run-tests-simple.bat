@echo off
chcp 65001 > nul
echo Starting SILA test runner...

cd /d "%~dp0"
cd backend

if not exist "venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found in backend\venv
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Running tests...
python -m pytest --cov=app --cov-report=term-missing -v

if %ERRORLEVEL% neq 0 (
    echo.
    echo Tests failed with error code %ERRORLEVEL%
) else (
    echo.
    echo All tests passed successfully!
)

pause

