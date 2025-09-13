# fix-corrupted-filenames.ps1
$sila_dev-system = "$PSScriptsila_dev-system\.."

Write-Host "Corrigindo nomes de arquivos..." -ForegroundColor Yellow

Get-ChildItem -Path $sila_dev-system -Recurse -Include *.py, *.pyw, *.txt, *.md, *.sh, *.ps1 | ForEach-Object {
    $oldName = $_.Name
    $newName = $oldName `
        -replace 'otifier', 'notifier' `
        -replace 'otifications', 'notifications' `
        -replace 'otificacoes', 'notificacoes' `
        -replace 'otifica', 'notifica' `
        -replace 'otificacoes', 'notificacoes' `
        -replace 'otificar', 'notificar' `
        -replace 'otificacao', 'notificacao'

    if ($newName -ne $oldName) {
        $newPath = Join-Path $_.DirectoryName $newName
        Rename-Item -Path $_.FullName -NewName $newName
        Write-Host "$($oldName) -> $($newName)" -ForegroundColor Green
    }
}

Write-Host "Correcao de nomes de arquivos concluida" -ForegroundColor Green

