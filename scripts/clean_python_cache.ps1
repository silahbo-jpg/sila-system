# Script PowerShell para limpar arquivos de cache Python
# Este script implementa as recomendações de limpeza para resolver problemas de portabilidade
# entre WSL2 (Linux) e Windows 10

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

function Clean-PythonCache {
    Write-Header "Limpando arquivos de cache Python"
    
    # Contadores para estatísticas
    $pycCount = 0
    $pycacheCount = 0
    
    # Remover arquivos .pyc
    Get-ChildItem -Path . -Include *.pyc -Recurse | ForEach-Object {
        try {
            Remove-Item $_.FullName -Force
            $pycCount++
            Write-Info "Removido: $($_.FullName)"
        } catch {
            Write-Warning "Não foi possível remover $($_.FullName): $_"
        }
    }
    
    # Remover diretórios __pycache__
    Get-ChildItem -Path . -Include __pycache__ -Directory -Recurse | ForEach-Object {
        try {
            Remove-Item $_.FullName -Recurse -Force
            $pycacheCount++
            Write-Info "Removido: $($_.FullName)"
        } catch {
            Write-Warning "Não foi possível remover $($_.FullName): $_"
        }
    }
    
    Write-Success "Limpeza concluída: $pycCount arquivos .pyc e $pycacheCount diretórios __pycache__ removidos."
}

function Clean-CompiledLibraries {
    Write-Header "Limpando bibliotecas compiladas específicas do Linux"
    
    # Contadores para estatísticas
    $soCount = 0
    
    # Remover arquivos .so (bibliotecas compartilhadas Linux)
    Get-ChildItem -Path . -Include *.so, *.so.* -Recurse | ForEach-Object {
        try {
            Remove-Item $_.FullName -Force
            $soCount++
            Write-Info "Removido: $($_.FullName)"
        } catch {
            Write-Warning "Não foi possível remover $($_.FullName): $_"
        }
    }
    
    Write-Success "Limpeza concluída: $soCount bibliotecas Linux removidas."
}

function Move-DatabaseFiles {
    Write-Header "Organizando arquivos de banco de dados"
    
    # Garantir que o diretório de backups existe
    $backupDir = Join-Path -Path (Get-Location) -ChildPath "backups"
    if (-not (Test-Path -Path $backupDir)) {
        New-Item -Path $backupDir -ItemType Directory | Out-Null
        Write-Info "Diretório de backups criado: $backupDir"
    }
    
    # Contadores para estatísticas
    $dbCount = 0
    $sqlCount = 0
    
    # Mover arquivos .db da raiz para backups
    Get-ChildItem -Path . -Filter *.db | Where-Object { $_.FullName -notlike "*\prisma\dev.db" } | ForEach-Object {
        try {
            $destination = Join-Path -Path $backupDir -ChildPath $_.Name
            Move-Item -Path $_.FullName -Destination $destination -Force
            $dbCount++
            Write-Info "Movido para backups: $($_.FullName)"
        } catch {
            Write-Warning "Não foi possível mover $($_.FullName): $_"
        }
    }
    
    # Mover arquivos .sql da raiz para backups
    Get-ChildItem -Path . -Filter *.sql | ForEach-Object {
        try {
            $destination = Join-Path -Path $backupDir -ChildPath $_.Name
            Move-Item -Path $_.FullName -Destination $destination -Force
            $sqlCount++
            Write-Info "Movido para backups: $($_.FullName)"
        } catch {
            Write-Warning "Não foi possível mover $($_.FullName): $_"
        }
    }
    
    Write-Success "Organização concluída: $dbCount arquivos .db e $sqlCount arquivos .sql movidos para $backupDir"
}

function Identify-ShellScripts {
    Write-Header "Identificando scripts shell incompatíveis com Windows"
    
    # Contador para estatísticas
    $shCount = 0
    
    # Encontrar todos os scripts .sh
    Get-ChildItem -Path . -Include *.sh -Recurse | ForEach-Object {
        $shCount++
        Write-Warning "Script shell encontrado: $($_.FullName)"
        Write-Info "Recomendação: Converta para PowerShell (.ps1) ou batch (.bat) para compatibilidade com Windows."
    }
    
    if ($shCount -eq 0) {
        Write-Success "Nenhum script shell incompatível encontrado."
    } else {
        Write-Warning "Total de $shCount scripts shell encontrados que precisam ser convertidos."
    }
}

function Check-ModuleConsistency {
    Write-Header "Verificando consistência dos módulos"
    
    # Verificar duplicidade de módulos (saude/health)
    $backendModulesPath = Join-Path -Path (Get-Location) -ChildPath "backend\app\modules"
    if (Test-Path -Path $backendModulesPath) {
        $modules = Get-ChildItem -Path $backendModulesPath -Directory
        
        # Nota: A verificação de duplicidade saude/health foi removida pois o módulo saude foi consolidado com health
        $healthExists = Test-Path -Path (Join-Path -Path $backendModulesPath -ChildPath "health")
        
        if (-not $healthExists) {
            Write-Warning "Módulo 'health' não encontrado. Verifique a estrutura do projeto."
        }
        
        # Verificar estrutura interna dos módulos
        foreach ($module in $modules) {
            $modulePath = $module.FullName
            
            # Verificar se tem a estrutura básica esperada
            $expectedDirs = @("models", "routes", "services", "tests")
            $missingDirs = @()
            
            foreach ($dir in $expectedDirs) {
                $dirPath = Join-Path -Path $modulePath -ChildPath $dir
                if (-not (Test-Path -Path $dirPath)) {
                    $missingDirs += $dir
                }
            }
            
            if ($missingDirs.Count -gt 0) {
                Write-Warning "Módulo '$($module.Name)' está incompleto. Diretórios ausentes: $($missingDirs -join ', ')"
            }
        }
    } else {
        Write-Warning "Diretório de módulos não encontrado em $backendModulesPath"
    }
}

# Função principal
function Main {
    Write-Header "SANEAMENTO DO PROJETO sila_dev"
    Write-Host "Este script implementa as recomendações para saneamento do projeto,"
    Write-Host "focando em problemas de portabilidade WSL2 → Windows e organização."
    Write-Host ""
    Write-Host "ATENÇÃO: Este script apenas identifica problemas e faz recomendações."
    Write-Host "Para executar as ações de limpeza, descomente as linhas no final do script."
    
    # Verificar se estamos no diretório raiz do projeto
    if (-not ((Test-Path -Path "backend") -and (Test-Path -Path "frontend"))) {
        Write-Warning "Este script deve ser executado no diretório raiz do projeto sila_dev."
        Write-Info "Diretório atual: $(Get-Location)"
        return
    }
    
    # Executar as funções de verificação
    Check-ModuleConsistency
    Identify-ShellScripts
    
    # Descomente as linhas abaixo para executar as ações de limpeza
    # Clean-PythonCache
    # Clean-CompiledLibraries
    # Move-DatabaseFiles
    
    Write-Header "RECOMENDAÇÕES FINAIS"
    Write-Host "1. Reinstale todas as dependências Python no ambiente Windows:"
    Write-Host "   pip install --force-reinstall -r requirements.txt"
    Write-Host ""
    Write-Host "2. Reinstale todas as dependências Node.js:"
    Write-Host "   npm ci"
    Write-Host ""
    Write-Host "3. Organize o projeto em subprojetos claros:"
    Write-Host "   - backend/: Django/FastAPI, Python"
    Write-Host "   - frontend/: React/Vue, Node.js"
    Write-Host "   - docs/: Documentação"
    Write-Host "   - scripts/: Scripts de utilidade"
    Write-Host ""
    Write-Host "4. Padronize a nomenclatura dos módulos (saude/health)"
    Write-Host ""
    Write-Host "5. Converta scripts .sh para PowerShell (.ps1) ou batch (.bat)"
}

# Executar a função principal
Main

