# Run-Tests-Direct.ps1 - Direct test runner

# Set console encoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Change to backend directory
Set-Location "$PSScriptRoot\backend"

# Activate virtual environment
. "venv\Scripts\Activate.ps1"

# Run tests with coverage
python -m pytest --cov=app --cov-report=term-missing --cov-report=html -v

