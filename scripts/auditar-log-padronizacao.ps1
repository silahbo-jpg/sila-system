param (
    [string]$LogPath = "c:\Users\User5\Music\MEGA1\sila_dev\sila_dev-system\logs\normalization_20250817_022806.log",
    [string]$RelatorioPath = "c:\Users\User5\Music\MEGA1\sila_dev\sila_dev-system\relatorios\auditoria_ignorados_20250817.txt"
)

# Criar diretório de relatório se necessário
$relatorioDir = Split-Path $RelatorioPath
if (-not (Test-Path $relatorioDir)) {
    New-Item -ItemType Directory -Path $relatorioDir -Force | Out-Null
}

# Inicializar relatório
Set-Content -Path $RelatorioPath -Value @"
Relatório de Auditoria - Arquivos Ignorados ou com Erro
Data: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

Timestamp        | Tipo      | Arquivo                          | Motivo
-----------------|-----------|----------------------------------|------------------------------
"@

# Ler log e extrair linhas relevantes
$linhas = Get-Content $LogPath | Where-Object {
    $_ -match "

\[IGNORADO\]

" -or $_ -match "

\[ERRO\]

"
}

foreach ($linha in $linhas) {
    try {
        $timestamp = ($linha -split "\]

")[0] + "]"
        $tipo = if ($linha -match "

\[IGNORADO\]

") { "IGNORADO" } elseif ($linha -match "

\[ERRO\]

") { "ERRO" } else { "DESCONHECIDO" }
        $arquivo = ($linha -split ": ")[-1]
        $motivo = ($linha -split "\]

 ")[-1]

        Add-Content -Path $RelatorioPath -Value ("{0,-16} | {1,-9} | {2,-32} | {3}" -f $timestamp, $tipo, $arquivo, $motivo)
    } catch {
        Add-Content -Path $RelatorioPath -Value "⚠️ Linha malformada: $linha"
    }
}

Add-Content -Path $RelatorioPath -Value "`nTotal de ocorrências: $($linhas.Count)"
Write-Output "✅ Relatório gerado com sucesso em: $RelatorioPath"

