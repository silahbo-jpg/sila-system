Write-Host "Verificando FastAPI..."
python -c "import fastapi; print(f'FastAPI OK: {fastapi.__version__}')"

Write-Host "Verificando Prisma..."
python -c "import prisma; print(f'Prisma OK: {prisma.__version__}')"

Write-Host "Verificando Pytest..."
pytest --version

