# scripts/generate-scripts-index.ps1
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$files = Get-ChildItem -Path $root -Recurse -Include *.ps1, *.py, *.sh

$index = foreach ($f in $files) {
    [PSCustomObject]@{
        Nome = $f.Name
        Caminho = $f.FullName
        Extensao = $f.Extension
        UltimaModificacao = $f.LastWriteTime
        PrimeiraLinha = (Get-Content $f.FullName -First 1)
    }
}

$csvPath = Join-Path $root "scripts_index.csv"
$index | Export-Csv -Path $csvPath -NoTypeInformation -Encoding UTF8

Write-Host "Inventário salvo em $csvPath"
