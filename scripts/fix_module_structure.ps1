# Script PowerShell para verificar e corrigir a estrutura dos módulos
# Este script identifica e corrige problemas estruturais nos módulos do projeto

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

function Check-ModuleStructure {
    Write-Header "Verificando estrutura dos módulos"
    
    $backendModulesPath = Join-Path -Path (Get-Location) -ChildPath "backend\app\modules"
    if (-not (Test-Path -Path $backendModulesPath)) {
        Write-Warning "Diretório de módulos não encontrado em $backendModulesPath"
        return
    }
    
    $modules = Get-ChildItem -Path $backendModulesPath -Directory
    Write-Info "Encontrados $($modules.Count) módulos no backend."
    
    # Verificar duplicidade saude/health
    $saudeExists = Test-Path -Path (Join-Path -Path $backendModulesPath -ChildPath "saude")
    $healthExists = Test-Path -Path (Join-Path -Path $backendModulesPath -ChildPath "health")
    
    if ($saudeExists -and $healthExists) {
        Write-Warning "Módulos duplicados detectados: 'saude' e 'health' existem simultaneamente."
        Write-Info "Recomendação: Padronize usando apenas um dos módulos e migre o conteúdo."
        
        # Perguntar ao usuário se deseja mesclar os módulos
        $choice = Read-Host "Deseja mesclar os módulos 'saude' e 'health'? (S/N)"
        
        if ($choice -eq "S" -or $choice -eq "s") {
            Write-Info "Qual módulo deseja manter? (1 - saude, 2 - health)"
            $moduleChoice = Read-Host "Escolha (1/2)"
            
            if ($moduleChoice -eq "1") {
                # Manter 'saude' e mesclar conteúdo de 'health'
                Merge-Modules -SourceModule "health" -TargetModule "saude"
            } elseif ($moduleChoice -eq "2") {
                # Manter 'health' e mesclar conteúdo de 'saude'
                Merge-Modules -SourceModule "saude" -TargetModule "health"
            } else {
                Write-Warning "Escolha inválida. Nenhuma ação será tomada."
            }
        }
    }
    
    # Verificar estrutura interna dos módulos
    foreach ($module in $modules) {
        $modulePath = $module.FullName
        $moduleName = $module.Name
        
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
            Write-Warning "Módulo '$moduleName' está incompleto. Diretórios ausentes: $($missingDirs -join ', ')"
            
            # Perguntar ao usuário se deseja criar os diretórios ausentes
            $choice = Read-Host "Deseja criar os diretórios ausentes para o módulo '$moduleName'? (S/N)"
            
            if ($choice -eq "S" -or $choice -eq "s") {
                foreach ($dir in $missingDirs) {
                    $dirPath = Join-Path -Path $modulePath -ChildPath $dir
                    New-Item -Path $dirPath -ItemType Directory | Out-Null
                    
                    # Criar arquivo __init__.py para cada diretório
                    $initPath = Join-Path -Path $dirPath -ChildPath "__init__.py"
                    """# $moduleName $dir module
# Este arquivo foi gerado automaticamente pelo script fix_module_structure.ps1
""" | Out-File -FilePath $initPath -Encoding utf8
                    
                    Write-Success "Criado diretório e __init__.py: $dirPath"
                }
            }
        } else {
            Write-Success "Módulo '$moduleName' tem estrutura completa."
        }
    }
}

function Merge-Modules {
    param(
        [string]$SourceModule,
        [string]$TargetModule
    )
    
    $backendModulesPath = Join-Path -Path (Get-Location) -ChildPath "backend\app\modules"
    $sourcePath = Join-Path -Path $backendModulesPath -ChildPath $SourceModule
    $targetPath = Join-Path -Path $backendModulesPath -ChildPath $TargetModule
    
    if (-not (Test-Path -Path $sourcePath) -or -not (Test-Path -Path $targetPath)) {
        Write-Warning "Um dos módulos não existe. Não é possível mesclar."
        return
    }
    
    Write-Info "Mesclando módulo '$SourceModule' em '$TargetModule'..."
    
    # Criar backup do módulo de origem
    $backupDir = Join-Path -Path (Get-Location) -ChildPath "backups\modules"
    if (-not (Test-Path -Path $backupDir)) {
        New-Item -Path $backupDir -ItemType Directory | Out-Null
    }
    
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backupPath = Join-Path -Path $backupDir -ChildPath "${SourceModule}_${timestamp}"
    
    Copy-Item -Path $sourcePath -Destination $backupPath -Recurse
    Write-Info "Backup do módulo '$SourceModule' criado em: $backupPath"
    
    # Copiar arquivos do módulo de origem para o destino
    $sourceItems = Get-ChildItem -Path $sourcePath -Recurse
    
    foreach ($item in $sourceItems) {
        $relativePath = $item.FullName.Substring($sourcePath.Length)
        $targetItemPath = Join-Path -Path $targetPath -ChildPath $relativePath
        
        if ($item.PSIsContainer) {
            # É um diretório
            if (-not (Test-Path -Path $targetItemPath)) {
                New-Item -Path $targetItemPath -ItemType Directory | Out-Null
                Write-Info "Criado diretório: $targetItemPath"
            }
        } else {
            # É um arquivo
            $targetItemDir = Split-Path -Path $targetItemPath -Parent
            if (-not (Test-Path -Path $targetItemDir)) {
                New-Item -Path $targetItemDir -ItemType Directory | Out-Null
            }
            
            # Verificar se o arquivo já existe no destino
            if (Test-Path -Path $targetItemPath) {
                $fileName = Split-Path -Path $targetItemPath -Leaf
                $newFileName = "${fileName}.${SourceModule}"
                $newTargetPath = Join-Path -Path (Split-Path -Path $targetItemPath -Parent) -ChildPath $newFileName
                
                Copy-Item -Path $item.FullName -Destination $newTargetPath
                Write-Info "Arquivo já existe no destino. Copiado como: $newTargetPath"
            } else {
                Copy-Item -Path $item.FullName -Destination $targetItemPath
                Write-Info "Copiado: $targetItemPath"
            }
        }
    }
    
    Write-Success "Mesclagem concluída. O módulo '$SourceModule' foi mesclado em '$TargetModule'."
    Write-Warning "O módulo original '$SourceModule' ainda existe. Você pode removê-lo manualmente após verificar se tudo está funcionando corretamente."
}

function Create-StandardModule {
    param(
        [string]$ModuleName
    )
    
    Write-Header "Criando novo módulo padronizado: $ModuleName"
    
    $backendModulesPath = Join-Path -Path (Get-Location) -ChildPath "backend\app\modules"
    if (-not (Test-Path -Path $backendModulesPath)) {
        Write-Warning "Diretório de módulos não encontrado em $backendModulesPath"
        return
    }
    
    $modulePath = Join-Path -Path $backendModulesPath -ChildPath $ModuleName
    
    if (Test-Path -Path $modulePath) {
        Write-Warning "O módulo '$ModuleName' já existe."
        return
    }
    
    # Criar diretório do módulo
    New-Item -Path $modulePath -ItemType Directory | Out-Null
    
    # Criar estrutura padrão
    $standardDirs = @("models", "routes", "services", "tests", "schemas", "utils")
    
    foreach ($dir in $standardDirs) {
        $dirPath = Join-Path -Path $modulePath -ChildPath $dir
        New-Item -Path $dirPath -ItemType Directory | Out-Null
        
        # Criar arquivo __init__.py para cada diretório
        $initPath = Join-Path -Path $dirPath -ChildPath "__init__.py"
        """# $ModuleName $dir module
# Este arquivo foi gerado automaticamente pelo script fix_module_structure.ps1
""" | Out-File -FilePath $initPath -Encoding utf8
    }
    
    # Criar arquivo __init__.py principal do módulo
    $mainInitPath = Join-Path -Path $modulePath -ChildPath "__init__.py"
    """# $ModuleName module
# Este módulo foi gerado automaticamente pelo script fix_module_structure.ps1

""" | Out-File -FilePath $mainInitPath -Encoding utf8
    
    # Criar arquivo README.md com documentação básica
    $readmePath = Join-Path -Path $modulePath -ChildPath "README.md"
    """# Módulo $ModuleName

## Descrição
Este módulo gerencia funcionalidades relacionadas a $ModuleName.

## Estrutura
- `models/`: Modelos de dados
- `routes/`: Rotas da API
- `services/`: Lógica de negócios
- `tests/`: Testes unitários e de integração
- `schemas/`: Esquemas de validação
- `utils/`: Utilitários específicos do módulo

## Como usar

```python
from backend.app.modules.$ModuleName import services

# Exemplo de uso
```
""" | Out-File -FilePath $readmePath -Encoding utf8
    
    Write-Success "Módulo '$ModuleName' criado com estrutura padronizada."
}

function Main {
    Write-Header "CORREÇÃO DE ESTRUTURA DE MÓDULOS DO PROJETO sila_dev"
    Write-Host "Este script verifica e corrige problemas estruturais nos módulos do projeto."
    Write-Host ""
    
    # Verificar se estamos no diretório raiz do projeto
    if (-not ((Test-Path -Path "backend") -and (Test-Path -Path "frontend"))) {
        Write-Warning "Este script deve ser executado no diretório raiz do projeto sila_dev."
        Write-Info "Diretório atual: $(Get-Location)"
        return
    }
    
    $option = 0
    while ($option -ne 4) {
        Write-Host ""
        Write-Host "Escolha uma opção:"
        Write-Host "1. Verificar estrutura dos módulos existentes"
        Write-Host "2. Criar novo módulo padronizado"
        Write-Host "3. Mesclar módulos duplicados (saude/health)"
        Write-Host "4. Sair"
        
        $option = Read-Host "Opção"
        
        switch ($option) {
            1 {
                Check-ModuleStructure
            }
            2 {
                $moduleName = Read-Host "Digite o nome do novo módulo"
                Create-StandardModule -ModuleName $moduleName
            }
            3 {
                $sourceModule = Read-Host "Digite o nome do módulo de origem (que será mesclado)"
                $targetModule = Read-Host "Digite o nome do módulo de destino (que receberá o conteúdo)"
                Merge-Modules -SourceModule $sourceModule -TargetModule $targetModule
            }
            4 {
                Write-Host "Saindo..."
            }
            default {
                Write-Warning "Opção inválida."
            }
        }
    }
}

# Executar a função principal
Main

