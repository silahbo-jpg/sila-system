param($ProjectRoot = $(Get-Location).Path)

# 1. Limpar arquivos temporários
Get-ChildItem -Path $ProjectRoot -Recurse -Include "*.pyc","__pycache__" | Remove-Item -Recurse -Force

# 2. Organizar estrutura
$dirs = @{
    "certificados" = "*.pem"
    "binarios" = "*.exe,*.bat"
    "logs" = "*.log"
    "docs" = "*.md"
}

$dirs.GetEnumerator() | ForEach-Object {
    New-Item -Path "$ProjectRoot\$($_.Key)" -ItemType Directory -Force
    Get-ChildItem -Path $ProjectRoot -Include $_.Value.Split(",") -Recurse | 
        Where-Object { $_.Directory -ne "$ProjectRoot\$($_.Key)" } |
        Move-Item -Destination "$ProjectRoot\$($_.Key)" -Force
}

# 3. Atualizar .gitignore
$gitignore = @"
*.pyc
__pycache__/
*.pem
*.exe
*.log
.DS_Store
.venv/
"@

Set-Content -Path "$ProjectRoot\.gitignore" -Value $gitignore

# 4. Verificação final
Write-Host "✅ Projeto organizado com sucesso!" -ForegroundColor Green
Get-ChildItem -Path $ProjectRoot -Recurse | 
    Group-Object Extension | 
    Sort-Object Count -Descending | 
    Select-Object Count, Name | 
    Format-Table -AutoSize