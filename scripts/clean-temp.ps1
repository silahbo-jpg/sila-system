# scripts/clean-temp.ps1
Write-Host "Limpando arquivos temporarios..." -ForegroundColor Yellow

# Remove __pycache__
Get-ChildItem -Path "$PSScriptsila_dev-system\.." -Directory -Recurse -Include "__pycache__" | ForEach-Object {
    Remove-Item -Path $_.FullName -Recurse -Force
    Write-Host "Removido: $($_.FullName)" -ForegroundColor Gray
}

# Remove arquivos .pyc, .pyo, .pyd
Get-ChildItem -Path "$PSScriptsila_dev-system\.." -Recurse -Include *.pyc, *.pyo, *.pyd, *.log, *.bak | ForEach-Object {
    Remove-Item -Path $_.FullName -Force
    Write-Host "Removido: $($_.FullName)" -ForegroundColor Gray
}

Write-Host "Limpeza concluida" -ForegroundColor Green

