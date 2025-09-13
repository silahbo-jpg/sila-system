#!/usr/bin/env pwsh

# sanitize-frontend-webapp.ps1
# Sanitização específica do frontend/webapp
# Remove builds, caches, segredos, logs e node_modules
# Preserva apenas código-fonte, configuração e assets estáticos

$StartTime = Get-Date
$WebAppPath = Join-Path $PSScriptRoot "..\frontend\webapp"
$LogPath = Join-Path $PSScriptRoot "..\reports\cleanup\webapp-sanitization.log"
$BackupPath = Join-Path $PSScriptRoot "..\backup\webapp-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

# Validar caminho
if (-not (Test-Path $WebAppPath)) {
    Write-Host "❌ ERRO: Pasta 'webapp' não encontrada: $WebAppPath" -ForegroundColor Red
    exit 1
}

# Criar pastas
New-Item -ItemType Directory -Path (Split-Path $LogPath -Parent) -Force | Out-Null
New-Item -ItemType Directory -Path $BackupPath -Force | Out-Null

# Função de log
function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "HH:mm:ss"
    "[$timestamp] $Message" | Tee-Object -FilePath $LogPath -Append
}

Write-Log "🚀 Iniciando sanitização de: $WebAppPath"

# === 1. Backup opcional (descomente se quiser)
# Write-Log "📁 Criando backup..."
# Copy-Item -Path $WebAppPath -Destination $BackupPath -Recurse -Force
# Write-Log "✅ Backup concluído"

# === 2. Remover node_modules recursivamente ===
Write-Log "🧹 Removendo node_modules..."
$NodeModules = Get-ChildItem -Path $WebAppPath -Include "node_modules" -Recurse -Directory -ErrorAction SilentlyContinue
if ($NodeModules) {
    $NodeModules | ForEach-Object {
        Remove-Item $_.FullName -Recurse -Force
        Write-Log "🗑️ Removido: $($_.FullName)"
    }
} else {
    Write-Log "✅ Nenhum node_modules encontrado"
}

# === 3. Remover builds e artefatos ===
$BuildDirs = @("dist", ".vite", ".storybook", "coverage", "temp", "tmp", "build")
foreach ($dir in $BuildDirs) {
    $path = Join-Path $WebAppPath $dir
    if (Test-Path $path) {
        Remove-Item $path -Recurse -Force
        Write-Log "🗑️ Removido: $dir/"
    }
}

# === 4. Remover arquivos de log e relatórios ===
$TempFiles = @(
    "accessibility-report.txt",
    "broken-imports.log",
    "CONSOLE_WARNINGS.md",
    "*.log",
    "yarn-error.log",
    "npm-debug.log"
)
foreach ($file in $TempFiles) {
    Get-ChildItem -Path $WebAppPath -Include $file -Recurse -File | ForEach-Object {
        Remove-Item $_.FullName -Force
        Write-Log "📄🗑️ Removido: $($_.Name)"
    }
}

# === 5. Remover .env com segredos e gerar .env.example ===
$EnvFiles = @(".env", ".env.development", ".env.production")
foreach ($envFile in $EnvFiles) {
    $path = Join-Path $WebAppPath $envFile
    if (Test-Path $path) {
        $Content = Get-Content $path -Raw
        # Criar .env.example
        $Example = $Content -replace "=(.+)", "=VALUE"
        $ExamplePath = Join-Path $WebAppPath "${envFile}.example"
        $Example | Out-File -FilePath $ExamplePath -Encoding UTF8 -Force
        # Remover original
        Remove-Item $path -Force
        Write-Log "🔐 Removido: $envFile (sensível)"
    }
}

# === 6. Remover artefatos do Cypress e Storybook ===
$TestDirs = @("cypress/videos", "cypress/screenshots", ".storybook")
foreach ($dir in $TestDirs) {
    $path = Join-Path $WebAppPath $dir
    if (Test-Path $path) {
        Remove-Item $path -Recurse -Force
        Write-Log "🎥🗑️ Removido: $dir/"
    }
}

# === 7. Remover arquivos de build gerados (hash) ===
Get-ChildItem -Path $WebAppPath -Include "*.js", "*.css", "*.map" -Recurse -File | Where-Object {
    $_.Name -match "index-.*\.js" -or $_.Name -match "LoginPage-.*\.js" -or $_.Name -match "Dashboard-.*\.js"
} | ForEach-Object {
    Remove-Item $_.FullName -Force
    Write-Log "⚡ Removido: arquivo de build gerado: $($_.Name)"
}

# === 8. Atualizar .gitignore ===
$GitIgnore = Join-Path (Split-Path $WebAppPath -Parent) "..\.gitignore"
$Rules = @(
    "node_modules/"
    "dist/"
    "build/"
    ".vite/"
    ".env"
    ".env.local"
    "*.log"
    "coverage/"
    "cypress/videos/"
    "cypress/screenshots/"
    ".cache/"
    ".DS_Store"
)

if (Test-Path $GitIgnore) {
    $current = Get-Content $GitIgnore -Raw
    $newRules = $Rules | Where-Object { $current -notlike "*$_*" }
    if ($newRules) {
        $newRules | Out-File -FilePath $GitIgnore -Encoding UTF8 -Append
        Write-Log "✅ Regras adicionadas ao .gitignore"
    }
} else {
    $Rules | Out-File -FilePath $GitIgnore -Encoding UTF8
    Write-Log "✅ .gitignore criado"
}

# === 9. Limpeza final: diretórios vazios ===
Write-Log "🧹 Removendo diretórios vazios..."
Get-ChildItem -Path $WebAppPath -Directory -Recurse | Sort-Object FullName -Descending | ForEach-Object {
    if ((Get-ChildItem $_.FullName -Recurse -File | Measure-Object).Count -eq 0) {
        Remove-Item $_.FullName -Force
        Write-Log "EmptyEntries] Diretório vazio removido: $($_.FullName)"
    }
}

# === 10. Resumo final ===
$EndTime = Get-Date
$Duration = $EndTime - $StartTime
Write-Log "✅ Sanitização de 'frontend/webapp' concluída!"
Write-Log "⏱️ Duração: $($Duration.TotalSeconds) segundos"
Write-Log "📄 Log salvo em: $LogPath"
Write-Log "💡 Próximo passo: npm install && npm run build"