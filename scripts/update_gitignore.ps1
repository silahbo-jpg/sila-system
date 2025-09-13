$gitignorePath = "..\.gitignore"

$entries = @(
    "__pycache__/",
    "*.db",
    "node_modules/",
    "venv/",
    ".env"
)

if (!(Test-Path $gitignorePath)) {
    New-Item -Path $gitignorePath -ItemType File -Force
}

$existing = Get-Content $gitignorePath
$newEntries = $entries | Where-Object { $_ -notin $existing }

if ($newEntries.Count -gt 0) {
    Add-Content -Path $gitignorePath -Value $newEntries
    Write-Host "[OK] .gitignore atualizado com novas entradas."
} else {
    Write-Host "[INFO] Nenhuma nova entrada necessaria. .gitignore ja esta completo."
}
