# Script PowerShell para validar a estrutura e implementação dos módulos do sila_dev
# Este script verifica se todos os módulos estão completos e padronizados

# Definição de funções de formatação
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

function Write-Error {
    param([string]$Message)
    
    Write-Host "[ERRO] $Message" -ForegroundColor Red
}

# Função para verificar a existência do Python e do módulo validator
function Check-PythonValidator {
    try {
        # Verificar se o Python está instalado
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Python não encontrado. Por favor, instale o Python 3.8 ou superior."
            return $false
        }
        
        Write-Info "Python encontrado: $pythonVersion"
        
        # Verificar se o arquivo module_validator.py existe
        $validatorPath = Join-Path -Path (Get-Location) -ChildPath "scripts\module_validator.py"
        if (-not (Test-Path -Path $validatorPath)) {
            Write-Error "Arquivo module_validator.py não encontrado em $validatorPath"
            return $false
        }
        
        Write-Success "Validador de módulos encontrado em $validatorPath"
        return $true
    }
    catch {
        Write-Error "Erro ao verificar dependências: $_"
        return $false
    }
}

# Função para executar o validador de módulos Python
function Run-ModuleValidator {
    param(
        [string]$OutputFormat = "markdown",
        [string]$ModuleName = "",
        [string]$OutputPath = ""
    )
    
    $validatorPath = Join-Path -Path (Get-Location) -ChildPath "scripts\module_validator.py"
    $projectPath = Get-Location
    
    $arguments = "$validatorPath --path `"$projectPath`" --format $OutputFormat"
    
    if ($ModuleName) {
        $arguments += " --module $ModuleName"
    }
    
    if ($OutputPath) {
        $arguments += " --output `"$OutputPath`""
    }
    
    Write-Info "Executando validador de módulos com os seguintes argumentos: $arguments"
    
    try {
        $result = python $arguments 2>&1
        
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Falha ao executar o validador de módulos: $result"
            return $false
        }
        
        if (-not $OutputPath) {
            # Se não estiver salvando em arquivo, exibir resultado no console
            Write-Host $result
        }
        
        return $true
    }
    catch {
        Write-Error "Erro ao executar o validador de módulos: $_"
        return $false
    }
}

# Função para verificar a estrutura básica dos módulos
function Check-ModuleStructure {
    $backendModulesPath = Join-Path -Path (Get-Location) -ChildPath "backend\app\modules"
    if (-not (Test-Path -Path $backendModulesPath)) {
        Write-Warning "Diretório de módulos não encontrado em $backendModulesPath"
        return $false
    }
    
    $modules = Get-ChildItem -Path $backendModulesPath -Directory
    $totalModules = $modules.Count
    $validModules = 0
    $problemModules = @()
    
    Write-Info "Encontrados $totalModules módulos no backend."
    
    foreach ($module in $modules) {
        $modulePath = $module.FullName
        $moduleName = $module.Name
        $hasProblems = $false
        
        # Verificar se tem a estrutura básica esperada
        $expectedFiles = @("__init__.py", "models.py", "schemas.py", "crud.py", "services.py", "endpoints.py")
        $missingFiles = @()
        
        foreach ($file in $expectedFiles) {
            $filePath = Join-Path -Path $modulePath -ChildPath $file
            if (-not (Test-Path -Path $filePath)) {
                $missingFiles += $file
                $hasProblems = $true
            }
        }
        
        if ($hasProblems) {
            $problemModules += @{"name" = $moduleName; "missing" = $missingFiles}
        } else {
            $validModules++
        }
    }
    
    # Exibir resumo
    Write-Header "Resumo da Verificação de Estrutura"
    Write-Info "Total de módulos: $totalModules"
    Write-Info "Módulos válidos: $validModules"
    Write-Info "Módulos com problemas: $($problemModules.Count)"
    
    if ($problemModules.Count -gt 0) {
        Write-Warning "Detalhes dos módulos com problemas:"
        foreach ($module in $problemModules) {
            Write-Warning "Módulo: $($module.name) - Arquivos ausentes: $($module.missing -join ', ')"
        }
        return $false
    } else {
        Write-Success "Todos os módulos possuem a estrutura básica esperada."
        return $true
    }
}

# Função para verificar a padronização de código
function Check-CodeStandards {
    # Verificar se o pylint está instalado
    try {
        $pylintVersion = python -c "import pylint; print(pylint.__version__)" 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Warning "Pylint não encontrado. A verificação de padrões de código não será executada."
            Write-Info "Instale o pylint com: pip install pylint"
            return $false
        }
        
        Write-Info "Pylint encontrado: $pylintVersion"
        
        # Executar pylint nos módulos
        $backendModulesPath = Join-Path -Path (Get-Location) -ChildPath "backend\app\modules"
        $result = python -m pylint $backendModulesPath --disable=C0111,C0103 --output-format=text 2>&1
        
        if ($LASTEXITCODE -gt 0) {
            Write-Warning "Problemas de padrão de código encontrados:"
            Write-Host $result
            return $false
        } else {
            Write-Success "Código está de acordo com os padrões definidos."
            return $true
        }
    }
    catch {
        Write-Warning "Erro ao verificar padrões de código: $_"
        return $false
    }
}

# Função principal
function Main {
    Write-Header "Validação de Módulos do sila_dev"
    
    $allChecksTruman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1* = $true
    
    # Verificar dependências
    if (-not (Check-PythonValidator)) {
        Write-Error "Falha na verificação de dependências. Abortando."
        exit 1
    }
    
    # Verificar estrutura dos módulos
    Write-Header "Verificando Estrutura dos Módulos"
    $structureOk = Check-ModuleStructure
    if (-not $structureOk) {
        Write-Warning "Problemas encontrados na estrutura dos módulos."
        $allChecksTruman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1* = $false
    }
    
    # Executar validador de módulos Python
    Write-Header "Executando Validador de Módulos Python"
    $outputPath = Join-Path -Path (Get-Location) -ChildPath "reports\module_validation_report.md"
    $validatorOk = Run-ModuleValidator -OutputFormat "markdown" -OutputPath $outputPath
    
    if (-not $validatorOk) {
        Write-Warning "Problemas encontrados pelo validador de módulos Python."
        $allChecksTruman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1* = $false
    } else {
        Write-Success "Relatório de validação gerado em: $outputPath"
    }
    
    # Verificar padrões de código
    Write-Header "Verificando Padrões de Código"
    $codeStandardsOk = Check-CodeStandards
    if (-not $codeStandardsOk) {
        Write-Warning "Problemas encontrados nos padrões de código."
        $allChecksTruman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1* = $false
    }
    
    # Resumo final
    Write-Header "Resumo da Validação"
    if ($allChecksTruman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*) {
        Write-Success "Todos os testes de validação foram concluídos com sucesso!"
        exit 0
    } else {
        Write-Warning "Foram encontrados problemas durante a validação. Verifique os detalhes acima."
        exit 1
    }
}

# Executar função principal
Main

