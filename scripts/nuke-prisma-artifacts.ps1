<# nuke-prisma-artifacts.ps1
Remove artefatos legados do Prisma
Use -DryRun para apenas listar
#>

param([switch]$DryRun)

$patterns = @(
    "schema.prisma", "prisma/", "app/db/prisma*", "app/db/prisma_client.py",
    "scripts/prisma-migrate-core.py", "master-migration.ps1", "generate-migration-report.py",
    "setup_prisma_backend.ps1", "setup_dev.ps1",
    "test_notification_service_*.py", "test_password_reset_flow.py", "test_user_registration.py",
    "test_refresh_tokens.py", "test_health.py", "test_config.py", "test_isolated.py",
    "001_initial_auth_schema.py", "conftest.py"
)

$foundFiles = @()
foreach ($pattern in $patterns) {
    $foundFiles += Get-ChildItem -Path "..\" -Recurse -Include $pattern -ErrorAction SilentlyContinue
}

if ($foundFiles.Count -eq 0) {
    Write-Host "✅ Nenhum artefato do Prisma encontrado."
    exit 0
}

Write-Host "📂 Arquivos encontrados:" -ForegroundColor Cyan
$foundFiles | ForEach-Object { Write-Host "  - $($_.FullName)" }

if ($DryRun) {
    Write-Warning "[DRY RUN] Nenhum arquivo será removido."
} else {
    $foundFiles | Remove-Item -Force -Recurse
    Write-Host "✅ Limpeza concluída. $($foundFiles.Count) arquivos removidos." -ForegroundColor Green
}
