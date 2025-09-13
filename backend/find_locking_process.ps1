# Script para encontrar processos que estão travando o arquivo sila.db
$filePath = "sila.db"
$filePath = Resolve-Path $filePath -ErrorAction SilentlyContinue

if (-not $filePath) {
    Write-Host "Arquivo $filePath não encontrado."
    exit 1
}

Write-Host "Procurando processos que estão travando o arquivo: $filePath"

# Tentar obter processos que estão travando o arquivo
$lockingProcesses = Get-Process | Where-Object {
    $_.Modules | Where-Object { $_.FileName -eq $filePath.Path }
}

if ($lockingProcesses) {
    Write-Host "Processos travando o arquivo $filePath :"
    $lockingProcesses | Format-Table Id, ProcessName, Path -AutoSize
    
    $killProcesses = Read-Host "Deseja encerrar estes processos? (S/N)"
    if ($killProcesses -eq 'S') {
        $lockingProcesses | Stop-Process -Force
        Write-Host "Processos encerrados com sucesso."
    }
} else {
    Write-Host "Nenhum processo encontrado travando o arquivo $filePath"
    Write-Host "O bloqueio pode ser causado por um processo do WSL. Tente reiniciar o WSL com o comando:"
    Write-Host "wsl --shutdown"
}

