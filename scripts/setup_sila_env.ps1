# Caminho absoluto do diretório atual (scripts)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Caminho raiz do projeto (um nível acima de scripts)
$projectRoot = Join-Path $scriptDir ".." | Resolve-Path
$venvPath = Join-Path $projectRoot ".venv"
$requirementsFile = Join-Path $projectRoot "backend\requirements.txt"

# 1. Cria ambiente virtual se não existir
if (-Not (Test-Path "$venvPath\Scripts\Activate.ps1")) {
    Write-Host "🔧 Criando ambiente virtual em $venvPath..."
    python -m venv $venvPath
}

# 2. Ativa o ambiente virtual
Write-Host "✅ Ativando ambiente virtual..."
& "$venvPath\Scripts\Activate.ps1"

# 3. Instala dependências
if (Test-Path $requirementsFile) {
    Write-Host "📦 Instalando dependências de backend..."
    pip install -r $requirementsFile
} else {
    Write-Host "⚠️ Arquivo de requisitos não encontrado: $requirementsFile"
}

# 4. Lista pacotes instalados
Write-Host "`n📋 Pacotes instalados:"
pip list

# 5. Detecta ambientes duplicados
$duplicateEnvs = @(
    Join-Path $projectRoot "venv",
    Join-Path $projectRoot "backend\venv",
    Join-Path $projectRoot "backend\test_venv"
)
foreach ($env in $duplicateEnvs) {
    if (Test-Path $env) {
        Write-Host "⚠️ Ambiente duplicado detectado: $env"
        Write-Host "👉 Para remover: Remove-Item -Recurse -Force '$env'"
    }
}

Write-Host "`n✅ Ambiente pronto. Para rodar o backend:"
Write-Host "   cd $($projectRoot)\backend"
Write-Host "   uvicorn main:app --reload"
