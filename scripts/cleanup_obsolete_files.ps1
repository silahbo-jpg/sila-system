# Caminho base do projeto
$basePath = "C:\Users\User5\Music\MEGA1\sila\sila-system"

Write-Host "🔍 Iniciando limpeza de arquivos obsoletos..."

$filesToDelete = @(
    "backend\test_fixes.py",
    "backend\scripts\test_sila_system.py",
    "backend\scripts\validate_implementation.py",
    "backend\scripts\generate_test_data.py"
)

foreach ($relativePath in $filesToDelete) {
    $fullPath = Join-Path $basePath $relativePath
    if (Test-Path $fullPath) {
        Remove-Item $fullPath -Force
        Write-Host "✅ Removido: $relativePath"
    } else {
        Write-Host "⚠️ Não encontrado: $relativePath"
    }
}

Write-Host "🧼 Limpeza concluída!"
