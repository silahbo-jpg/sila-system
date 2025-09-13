#!/usr/bin/env pwsh
# check-models.ps1
# Lista todas as tabelas detectadas pelo Alembic (via Base.metadata)

$ErrorActionPreference = "Stop"
$BasePath = $PSScriptRoot | Split-Path -Parent
$BackendPath = Join-Path $BasePath "backend"

Write-Host "🔍 Verificando tabelas detectadas pelo Alembic..." -ForegroundColor Cyan

# Verificar se Python está disponível
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python não encontrado no PATH." -ForegroundColor Red
    exit 1
}

# Verificar se Alembic está disponível
if (-not (Get-Command alembic -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Alembic não encontrado. Instale com: pip install alembic" -ForegroundColor Red
    exit 1
}

# Executar um script Python que lista as tabelas do Base.metadata
$PythonScript = @"
import os, sys
from dotenv import load_dotenv
load_dotenv()

# Adicionar backend ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

try:
    from app.db.base_class import Base
except Exception as e:
    print("❌ Erro ao importar Base:", e)
    sys.exit(1)

tables = list(Base.metadata.tables.keys())
if not tables:
    print("⚠️ Nenhuma tabela detectada pelo Alembic.")
    sys.exit(0)

print("✅ Tabelas detectadas pelo Alembic:")
for t in tables:
    print(" -", t)

print(f"📊 Total: {len(tables)} tabelas")
"@

$TmpFile = New-TemporaryFile
$PythonScript | Set-Content -Path $TmpFile -Encoding UTF8

# Executar script Python
python $TmpFile.FullName
Remove-Item $TmpFile -Force
