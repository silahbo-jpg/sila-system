@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

cd /d "%~dp0"
cd backend
call venv\Scripts\activate.bat
python -m pytest --cov=app --cov-report=term-missing --cov-report=html -v
pause

