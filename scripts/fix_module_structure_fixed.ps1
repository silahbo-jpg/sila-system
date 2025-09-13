# Script PowerShell para verificar e corrigir a estrutura dos modulos
# Este script identifica e corrige problemas estruturais nos modulos do projeto

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
    Write-Header "Verificando estrutura dos modulos"
    
    $backendModulesPath = Join-Path -Path (Get-Location) -ChildPath "backend\app\modules"
    if (-not (Test-Path -Path $backendModulesPath)) {
        Write-Warning "Diretorio de modulos nao encontrado em $backendModulesPath"
        return
    }
    
    $modules = Get-ChildItem -Path $backendModulesPath -Directory
    Write-Info "Encontrados $($modules.Count) modulos no backend."
    
    # Nota: A verificação de duplicidade saude/health foi removida pois o módulo saude foi consolidado com health
    $healthExists = Test-Path -Path (Join-Path -Path $backendModulesPath -ChildPath "health")
    
    if (-not $healthExists) {
        Write-Warning "Módulo 'health' não encontrado. Verifique a estrutura do projeto."
    } else {
        Write-Info "Módulo 'health' encontrado e consolidado (antiga duplicidade com 'saude' foi resolvida)."
    }
    
    # Verificar estrutura interna dos modulos
    foreach ($module in $modules) {
        $modulePath = $module.FullName
        $moduleName = $module.Name
        
        # Verificar se tem a estrutura basica esperada
        $expectedDirs = @("models", "routes", "services", "tests")
        $missingDirs = @()
        
        foreach ($dir in $expectedDirs) {
            $dirPath = Join-Path -Path $modulePath -ChildPath $dir
            if (-not (Test-Path -Path $dirPath)) {
                $missingDirs += $dir
            }
        }
        
        if ($missingDirs.Count -gt 0) {
            Write-Warning "Modulo '$moduleName' esta incompleto. Diretorios ausentes: $($missingDirs -join ', ')"
            
            # Perguntar ao usuario se deseja criar os diretorios ausentes
            $choice = Read-Host "Deseja criar os diretorios ausentes para o modulo '$moduleName'? (S/N)"
            
            if ($choice -eq "S" -or $choice -eq "s") {
                foreach ($dir in $missingDirs) {
                    $dirPath = Join-Path -Path $modulePath -ChildPath $dir
                    New-Item -Path $dirPath -ItemType Directory | Out-Null
                    
                    # Criar arquivo __init__.py para cada diretorio
                    $initPath = Join-Path -Path $dirPath -ChildPath "__init__.py"
                    """# $moduleName $dir module
# Este arquivo foi gerado automaticamente pelo script fix_module_structure.ps1
""" | Out-File -FilePath $initPath -Encoding utf8
                    
                    Write-Success "Criado diretorio e __init__.py: $dirPath"
                }
            }
        } else {
            Write-Success "Modulo '$moduleName' tem estrutura completa."
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
        Write-Warning "Um dos modulos nao existe. Nao e possivel mesclar."
        return
    }
    
    Write-Info "Mesclando modulo '$SourceModule' em '$TargetModule'..."
    
    # Criar backup do modulo de origem
    $backupDir = Join-Path -Path (Get-Location) -ChildPath "backups\modules"
    if (-not (Test-Path -Path $backupDir)) {
        New-Item -Path $backupDir -ItemType Directory | Out-Null
    }
    
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backupPath = Join-Path -Path $backupDir -ChildPath "${SourceModule}_${timestamp}"
    
    Copy-Item -Path $sourcePath -Destination $backupPath -Recurse
    Write-Info "Backup do modulo '$SourceModule' criado em: $backupPath"
    
    # Copiar arquivos do modulo de origem para o destino
    $sourceItems = Get-ChildItem -Path $sourcePath -Recurse
    
    foreach ($item in $sourceItems) {
        $relativePath = $item.FullName.Substring($sourcePath.Length)
        $targetItemPath = Join-Path -Path $targetPath -ChildPath $relativePath
        
        if ($item.PSIsContainer) {
            # E um diretorio
            if (-not (Test-Path -Path $targetItemPath)) {
                New-Item -Path $targetItemPath -ItemType Directory | Out-Null
                Write-Info "Criado diretorio: $targetItemPath"
            }
        } else {
            # E um arquivo
            $targetItemDir = Split-Path -Path $targetItemPath -Parent
            if (-not (Test-Path -Path $targetItemDir)) {
                New-Item -Path $targetItemDir -ItemType Directory | Out-Null
            }
            
            # Verificar se o arquivo ja existe no destino
            if (Test-Path -Path $targetItemPath) {
                $fileName = Split-Path -Path $targetItemPath -Leaf
                $newFileName = "${fileName}.${SourceModule}"
                $newTargetPath = Join-Path -Path (Split-Path -Path $targetItemPath -Parent) -ChildPath $newFileName
                
                Copy-Item -Path $item.FullName -Destination $newTargetPath
                Write-Info "Arquivo ja existe no destino. Copiado como: $newTargetPath"
            } else {
                Copy-Item -Path $item.FullName -Destination $targetItemPath
                Write-Info "Copiado: $targetItemPath"
            }
        }
    }
    
    Write-Success "Mesclagem concluida. O modulo '$SourceModule' foi mesclado em '$TargetModule'."
    Write-Warning "O modulo original '$SourceModule' ainda existe. Voce pode remove-lo manualmente apos verificar se tudo esta funcionando corretamente."
}

function Create-StandardModule {
    param(
        [string]$ModuleName
    )
    
    Write-Header "Criando novo modulo padronizado: $ModuleName"
    
    $backendModulesPath = Join-Path -Path (Get-Location) -ChildPath "backend\app\modules"
    if (-not (Test-Path -Path $backendModulesPath)) {
        Write-Warning "Diretorio de modulos nao encontrado em $backendModulesPath"
        return
    }
    
    $modulePath = Join-Path -Path $backendModulesPath -ChildPath $ModuleName
    
    if (Test-Path -Path $modulePath) {
        Write-Warning "O modulo '$ModuleName' ja existe."
        return
    }
    
    # Criar diretorio do modulo
    New-Item -Path $modulePath -ItemType Directory | Out-Null
    
    # Criar estrutura padrao
    $standardDirs = @("models", "routes", "services", "tests", "schemas", "utils")
    
    foreach ($dir in $standardDirs) {
        $dirPath = Join-Path -Path $modulePath -ChildPath $dir
        New-Item -Path $dirPath -ItemType Directory | Out-Null
        
        # Criar arquivo __init__.py para cada diretorio
        $initPath = Join-Path -Path $dirPath -ChildPath "__init__.py"
        """# $ModuleName $dir module
# Este arquivo foi gerado automaticamente pelo script fix_module_structure.ps1
""" | Out-File -FilePath $initPath -Encoding utf8
    }
    
    # Criar arquivo __init__.py principal do modulo
    $mainInitPath = Join-Path -Path $modulePath -ChildPath "__init__.py"
    """# $ModuleName module
# Este modulo foi gerado automaticamente pelo script fix_module_structure.ps1

""" | Out-File -FilePath $mainInitPath -Encoding utf8
    
    # Criar arquivo README.md com documentacao basica
    $readmePath = Join-Path -Path $modulePath -ChildPath "README.md"
    """# Modulo $ModuleName

## Descricao
Este modulo gerencia funcionalidades relacionadas a $ModuleName.

## Estrutura
- `models/`: Modelos de dados
- `routes/`: Rotas da API
- `services/`: Logica de negocios
- `tests/`: Testes unitarios e de integracao
- `schemas/`: Esquemas de validacao
- `utils/`: Utilitarios especificos do modulo

## Como usar

```python
from backend.app.modules.$ModuleName import services

# Exemplo de uso
```
""" | Out-File -FilePath $readmePath -Encoding utf8
    
    Write-Success "Modulo '$ModuleName' criado com estrutura padronizada."
}

function Main {
    Write-Header "CORRECAO DE ESTRUTURA DE MODULOS DO PROJETO sila_dev"
    Write-Host "Este script verifica e corrige problemas estruturais nos modulos do projeto."
    Write-Host ""
    
    # Verificar se estamos no diretorio raiz do projeto
    if (-not ((Test-Path -Path "backend") -and (Test-Path -Path "frontend"))) {
        Write-Warning "Este script deve ser executado no diretorio raiz do projeto sila_dev."
        Write-Info "Diretorio atual: $(Get-Location)"
        return
    }
    
    $option = 0
    while ($option -ne 4) {
        Write-Host ""
        Write-Host "Escolha uma opcao:"
        Write-Host "1. Verificar estrutura dos modulos existentes"
        Write-Host "2. Criar novo modulo padronizado"
        Write-Host "3. Mesclar modulos duplicados (saude/health)"
        Write-Host "4. Sair"
        
        $option = Read-Host "Opcao"
        
        switch ($option) {
            1 {
                Check-ModuleStructure
            }
            2 {
                $moduleName = Read-Host "Digite o nome do novo modulo"
                Create-StandardModule -ModuleName $moduleName
            }
            3 {
                $sourceModule = Read-Host "Digite o nome do modulo de origem (que sera mesclado)"
                $targetModule = Read-Host "Digite o nome do modulo de destino (que recebera o conteudo)"
                Merge-Modules -SourceModule $sourceModule -TargetModule $targetModule
            }
            4 {
                Write-Host "Saindo..."
            }
            default {
                Write-Warning "Opcao invalida."
            }
        }
    }
}

# Executar a funcao principal
Main

