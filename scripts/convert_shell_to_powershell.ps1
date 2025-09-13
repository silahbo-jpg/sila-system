# Script PowerShell para converter scripts shell (.sh) para PowerShell (.ps1)
# Este script identifica scripts shell e ajuda a convertê-los para PowerShell

function Write-Header {
    param([string]$Message)
    
    Write-Host ""
    Write-Host ("=" * 80)
    Write-Host (" $Message ".PadLeft(40 + $Message.Length/2).PadRight(80, "="))
    Write-Host ("=" * 80)
}

function Write-Info {
    param([string]$Message)
    
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Write-Warning {
    param([string]$Message)
    
    Write-Host "[AVISO] $Message" -ForegroundColor Yellow
}

function Write-Success {
    param([string]$Message)
    
    Write-Host "[SUCESSO] $Message" -ForegroundColor Green
}

function Find-ShellScripts {
    Write-Header "Identificando scripts shell (.sh) no projeto"
    
    $shellScripts = Get-ChildItem -Path . -Include *.sh -Recurse
    
    if ($shellScripts.Count -eq 0) {
        Write-Success "Nenhum script shell encontrado no projeto."
        return @()
    }
    
    Write-Info "Encontrados $($shellScripts.Count) scripts shell:"
    
    $scriptList = @()
    $index = 1
    
    foreach ($script in $shellScripts) {
        $relativePath = $script.FullName.Substring((Get-Location).Path.Length + 1)
        Write-Host "$index. $relativePath"
        $scriptList += $script
        $index++
    }
    
    return $scriptList
}

function Convert-ShellToPowerShell {
    param(
        [System.IO.FileInfo]$ShellScript
    )
    
    Write-Header "Convertendo: $($ShellScript.Name)"
    
    # Ler o conteúdo do script shell
    $shellContent = Get-Content -Path $ShellScript.FullName -Raw
    
    # Criar o nome do arquivo PowerShell
    $psScriptName = $ShellScript.Name -replace "\.sh$", ".ps1"
    $psScriptPath = Join-Path -Path $ShellScript.DirectoryName -ChildPath $psScriptName
    
    Write-Info "Analisando script shell: $($ShellScript.FullName)"
    Write-Info "Será convertido para: $psScriptPath"
    
    # Mostrar o conteúdo do script shell
    Write-Host ""
    Write-Host "Conteúdo do script shell:" -ForegroundColor Yellow
    Write-Host "------------------------------------------------------------------------------"
    Write-Host $shellContent
    Write-Host "------------------------------------------------------------------------------"
    
    # Iniciar a conversão básica
    $powershellContent = "# Convertido de $($ShellScript.Name) por convert_shell_to_powershell.ps1\n\n"
    
    # Adicionar cabeçalho com comentários sobre a conversão manual necessária
    $powershellContent += "<#\nEste script foi convertido automaticamente de um script shell (.sh) para PowerShell (.ps1).\nAlgumas conversões comuns foram aplicadas, mas é provável que seja necessário ajuste manual.\n\nConversões aplicadas automaticamente:\n- Comentários (# -> #)\n- Variáveis básicas ($VAR -> \$VAR)\n\nVerifique e ajuste manualmente:\n- Comandos específicos do Linux (ls, grep, etc.) para equivalentes do PowerShell\n- Redirecionamentos de saída (>, >>, |)\n- Estruturas de controle (if, for, while)\n- Execução de comandos em sequência (;, &&, ||)\n#>\n\n"
    
    # Converter comentários e variáveis básicas
    $lines = $shellContent -split "`n"
    foreach ($line in $lines) {
        # Ignorar shebang
        if ($line -match "^#!/") {
            $powershellContent += "# $line\n"
            continue
        }
        
        # Converter comandos comuns
        $convertedLine = $line
        
        # Converter echo para Write-Host
        if ($convertedLine -match "^\s*echo\s+(.*)$") {
            $echoContent = $Matches[1]
            $convertedLine = $convertedLine -replace "^\s*echo\s+(.*)", "Write-Host $echoContent"
        }
        
        # Converter mkdir para New-Item
        if ($convertedLine -match "^\s*mkdir\s+-p\s+(.*)$") {
            $dirPath = $Matches[1]
            $convertedLine = $convertedLine -replace "^\s*mkdir\s+-p\s+(.*)", "New-Item -Path $dirPath -ItemType Directory -Force | Out-Null"
        }
        
        # Converter cp para Copy-Item
        if ($convertedLine -match "^\s*cp\s+([^\s]+)\s+([^\s]+)$") {
            $source = $Matches[1]
            $dest = $Matches[2]
            $convertedLine = $convertedLine -replace "^\s*cp\s+([^\s]+)\s+([^\s]+)", "Copy-Item -Path $source -Destination $dest"
        }
        
        # Converter rm para Remove-Item
        if ($convertedLine -match "^\s*rm\s+-rf\s+(.*)$") {
            $rmPath = $Matches[1]
            $convertedLine = $convertedLine -replace "^\s*rm\s+-rf\s+(.*)", "Remove-Item -Path $rmPath -Recurse -Force"
        }
        
        # Adicionar comentário para comandos não convertidos automaticamente
        if ($convertedLine -match "^\s*(ls|grep|sed|awk|find|cat|chmod|chown|tar|curl|wget)") {
            $convertedLine = "# TODO: Converter comando Linux: $convertedLine"
        }
        
        # Adicionar a linha convertida ao conteúdo PowerShell
        $powershellContent += "$convertedLine\n"
    }
    
    # Adicionar nota final
    $powershellContent += "\n# Fim do script convertido\n"
    
    # Salvar o conteúdo convertido no arquivo PowerShell
    $powershellContent | Out-File -FilePath $psScriptPath -Encoding utf8
    
    Write-Success "Script PowerShell criado: $psScriptPath"
    Write-Warning "Revise o script PowerShell manualmente para garantir que funcione corretamente."
    
    return $psScriptPath
}

function Main {
    Write-Header "CONVERSOR DE SCRIPTS SHELL PARA POWERSHELL"
    Write-Host "Este script identifica scripts shell (.sh) no projeto e ajuda a convertê-los para PowerShell (.ps1)."
    Write-Host "A conversão é semi-automática e requer revisão manual após a conversão."
    Write-Host ""
    
    # Verificar se estamos no diretório raiz do projeto
    if (-not ((Test-Path -Path "backend") -and (Test-Path -Path "frontend"))) {
        Write-Warning "Este script deve ser executado no diretório raiz do projeto sila_dev."
        Write-Info "Diretório atual: $(Get-Location)"
        return
    }
    
    # Encontrar scripts shell
    $shellScripts = Find-ShellScripts
    
    if ($shellScripts.Count -eq 0) {
        return
    }
    
    Write-Host ""
    Write-Host "Escolha uma opção:"
    Write-Host "1. Converter um script específico"
    Write-Host "2. Converter todos os scripts"
    Write-Host "3. Sair"
    
    $option = Read-Host "Opção"
    
    switch ($option) {
        1 {
            Write-Host "Digite o número do script que deseja converter:"
            $scriptIndex = [int](Read-Host "Número")
            
            if ($scriptIndex -lt 1 -or $scriptIndex -gt $shellScripts.Count) {
                Write-Warning "Número inválido."
                return
            }
            
            $selectedScript = $shellScripts[$scriptIndex - 1]
            Convert-ShellToPowerShell -ShellScript $selectedScript
        }
        2 {
            Write-Warning "Isso irá converter todos os $($shellScripts.Count) scripts shell encontrados."
            $confirm = Read-Host "Tem certeza que deseja continuar? (S/N)"
            
            if ($confirm -eq "S" -or $confirm -eq "s") {
                foreach ($script in $shellScripts) {
                    Convert-ShellToPowerShell -ShellScript $script
                }
                
                Write-Success "Conversão em massa concluída. Revise todos os scripts PowerShell gerados."
            }
        }
        3 {
            Write-Host "Saindo..."
        }
        default {
            Write-Warning "Opção inválida."
        }
    }
}

# Executar a função principal
Main

