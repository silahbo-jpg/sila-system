# scripts/validate-module-integrity.ps1
# Script PowerShell para validar a integridade dos módulos do sistema sila_dev

$ErrorActionPreference = "Stop"
$startTime = Get-Date

Write-Host "Iniciando validação de integridade de módulos..." -ForegroundColor Cyan

# Função para verificar se o Python está instalado
function Check-Python {
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Python não encontrado. Por favor, instale o Python 3.8 ou superior."
            return $false
        }
        
        Write-Host "Python encontrado: $pythonVersion" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Error "Erro ao verificar Python: $_"
        return $false
    }
}

# Função para verificar padrões proibidos
function Check-ForbiddenPatterns {
    param(
        [string]$Path
    )
    
    $badPatterns = @("from sqlalchemy", "import sqlalchemy", "SessionLocal", "Base.metadata", "create_engine", "declarative_base")
    $results = @()
    
    foreach ($pattern in $badPatterns) {
        $found = Select-String -Path "$Path/**/*.py" -Pattern $pattern -List
        if ($found) {
            Write-Warning "Padrão proibido encontrado: $pattern"
            foreach ($item in $found) {
                Write-Host "   $($item.Path):$($item.LineNumber)" -ForegroundColor Yellow
            }
            $results += $found
        }
    }
    
    return $results
}

# Função para verificar arquivos __init__.py
function Check-InitFiles {
    $modulesExpectingInit = @(
        "backend/app/core",
        "backend/app/db",
        "backend/app/api/routes",
        "backend/app/middleware",
        "backend/app/services",
        "backend/app/schemas",
        "backend/app/modules"
    )
    
    $missingInit = @()
    
    foreach ($modulePath in $modulesExpectingInit) {
        $fullPath = Join-Path -Path $PSScriptsila_dev-system -ChildPath "../$modulePath"
        $initFile = Join-Path -Path $fullPath -ChildPath "__init__.py"
        
        if (Test-Path -Path $fullPath -PathType Container) {
            if (-not (Test-Path -Path $initFile -PathType Leaf)) {
                $missingInit += $modulePath
            }
        }
    }
    
    # Verificar também todos os subdiretórios em app/modules
    $modulesDir = Join-Path -Path $PSScriptsila_dev-system -ChildPath "../backend/app/modules"
    if (Test-Path -Path $modulesDir -PathType Container) {
        $modulesDirs = Get-ChildItem -Path $modulesDir -Directory | Where-Object { $_.Name -notlike "__*" }
        
        foreach ($moduleDir in $modulesDirs) {
            $initFile = Join-Path -Path $moduleDir.FullName -ChildPath "__init__.py"
            if (-not (Test-Path -Path $initFile -PathType Leaf)) {
                $missingInit += "backend/app/modules/$($moduleDir.Name)"
            }
        }
    }
    
    return $missingInit
}

# Função para verificar a estrutura dos módulos
function Check-ModuleStructure {
    $modulesDir = Join-Path -Path $PSScriptsila_dev-system -ChildPath "../backend/app/modules"
    $requiredFiles = @("__init__.py", "models.py", "schemas.py", "crud.py", "services.py", "endpoints.py")
    
    $results = @{}
    
    if (-not (Test-Path -Path $modulesDir -PathType Container)) {
        Write-Error "Diretório de módulos não encontrado: $modulesDir"
        return $results
    }
    
    $modulesDirs = Get-ChildItem -Path $modulesDir -Directory | Where-Object { $_.Name -notlike "__*" }
    
    foreach ($moduleDir in $modulesDirs) {
        $moduleName = $moduleDir.Name
        $moduleResult = @{
            "Name" = $moduleName
            "Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed" = $true
            "MissingFiles" = @()
        }
        
        foreach ($file in $requiredFiles) {
            $filePath = Join-Path -Path $moduleDir.FullName -ChildPath $file
            if (-not (Test-Path -Path $filePath -PathType Leaf)) {
                $moduleResult.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed = $false
                $moduleResult.MissingFiles += $file
            }
        }
        
        $results[$moduleName] = $moduleResult
    }
    
    return $results
}

# Função para verificar a sintaxe Python
function Check-PythonSyntax {
    param(
        [string]$Path
    )
    
    $pythonFiles = Get-ChildItem -Path $Path -Filter "*.py" -Recurse -File
    $results = @{}
    
    foreach ($file in $pythonFiles) {
        $output = python -c "import py_compile; py_compile.compile('$($file.FullName)')" 2>&1
        $results[$file.FullName] = @{
            "Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed" = ($LASTEXITCODE -eq 0)
            "Error" = if ($LASTEXITCODE -ne 0) { $output } else { "" }
        }
    }
    
    return $results
}

# Função para gerar relatório em Markdown
function Generate-MarkdownReport {
    param(
        [hashtable]$ModuleResults,
        [array]$MissingInit,
        [hashtable]$SyntaxResults,
        [array]$ForbiddenPatterns,
        [string]$OutputPath
    )
    
    $report = @()
    $report += "# Relatório de Validação de Integridade de Módulos"
    $report += ""
    $report += "Data: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    $report += ""
    
    # Resumo
    $totalModules = $ModuleResults.Count
    $Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*edModules = ($ModuleResults.Values | Where-Object { $_.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed -eq $true }).Count
    $failedModules = $totalModules - $Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*edModules
    
    $report += "## Resumo"
    $report += "- Total de módulos: $totalModules"
    $report += "- Módulos válidos: $Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*edModules"
    $report += "- Módulos com problemas: $failedModules"
    $report += "- Diretórios sem __init__.py: $($MissingInit.Count)"
    $report += "- Arquivos com padrões proibidos: $($ForbiddenPatterns.Count)"
    
    # Verificação de __init__.py
    $report += ""
    $report += "## Verificação de arquivos __init__.py"
    if ($MissingInit.Count -gt 0) {
        $report += ""
        $report += "❌ **Diretórios sem __init__.py:**"
        foreach ($path in $MissingInit) {
            $report += "- `$path`"
        }
        $report += ""
        $report += "**Sugestão:** Crie os arquivos __init__.py nos diretórios listados acima."
    } else {
        $report += ""
        $report += "✅ Todos os diretórios necessários possuem arquivos __init__.py."
    }
    
    # Verificação de padrões proibidos
    $report += ""
    $report += "## Verificação de padrões proibidos"
    if ($ForbiddenPatterns.Count -gt 0) {
        $report += ""
        $report += "❌ **Arquivos com padrões proibidos:**"
        $uniqueFiles = $ForbiddenPatterns | Select-Object -Property Path -Unique
        foreach ($file in $uniqueFiles) {
            $patterns = $ForbiddenPatterns | Where-Object { $_.Path -eq $file.Path } | Select-Object -ExpandProperty Pattern
            $report += "- `$($file.Path)`: $($patterns -join ', ')"
        }
        $report += ""
        $report += "**Sugestão:** Execute `scripts/fix-sqlalchemy-refs.py` para corrigir automaticamente."
    } else {
        $report += ""
        $report += "✅ Nenhum padrão proibido encontrado."
    }
    
    # Detalhes por módulo
    $report += ""
    $report += "## Detalhes por Módulo"
    
    foreach ($moduleName in ($ModuleResults.Keys | Sort-Object)) {
        $moduleResult = $ModuleResults[$moduleName]
        $status = if ($moduleResult.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed) { "✅" } else { "❌" }
        
        $report += ""
        $report += "### $status Módulo: $moduleName"
        
        if (-not $moduleResult.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed) {
            $report += ""
            $report += "#### Arquivos Ausentes"
            foreach ($file in $moduleResult.MissingFiles) {
                $report += "- ❌ $file"
            }
            $report += ""
            $report += "**Sugestão:** Crie os arquivos ausentes para completar a estrutura do módulo."
        } else {
            $report += ""
            $report += "✅ Todos os arquivos obrigatórios estão presentes."
        }
        
        # Verificação de sintaxe para este módulo
        $modulePath = "backend/app/modules/$moduleName"
        $moduleSyntaxResults = $SyntaxResults.GetEnumerator() | Where-Object { $_.Key -like "*$modulePath*" }
        
        if ($moduleSyntaxResults.Count -gt 0) {
            $report += ""
            $report += "#### Sintaxe Python"
            
            $failedSyntax = $moduleSyntaxResults | Where-Object { $_.Value.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed -eq $false }
            if ($failedSyntax.Count -gt 0) {
                foreach ($result in $failedSyntax) {
                    $fileName = Split-Path -Path $result.Key -Leaf
                    $report += "- ❌ Erro de sintaxe em $fileName"
                    $report += "  - *Erro:* $($result.Value.Error)"
                }
            } else {
                $report += "- ✅ Todos os arquivos têm sintaxe válida"
            }
        }
    }
    
    # Próximos Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*os
    $report += ""
    $report += "## Próximos Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*os"
    
    if ($failedModules -eq 0 -and $MissingInit.Count -eq 0 -and $ForbiddenPatterns.Count -eq 0) {
        $report += ""
        $report += "✅ **Todos os módulos Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*aram na validação!**"
        $report += ""
        $report += "O sistema está pronto para execução."
    } else {
        $report += ""
        $report += "1. **Corrija os problemas identificados:**"
        if ($MissingInit.Count -gt 0) {
            $report += "   - Crie os arquivos __init__.py nos diretórios listados"
        }
        
        if ($ForbiddenPatterns.Count -gt 0) {
            $report += "   - Execute `scripts/fix-sqlalchemy-refs.py` para corrigir padrões proibidos"
        }
        
        $failedModuleNames = $ModuleResults.GetEnumerator() | Where-Object { $_.Value.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed -eq $false } | Select-Object -ExpandProperty Key
        if ($failedModuleNames.Count -gt 0) {
            $report += "   - Resolva os problemas nos seguintes módulos: $($failedModuleNames -join ', ')"
        }
        
        $report += ""
        $report += "2. **Execute novamente este validador para confirmar as correções.**"
        $report += ""
        $report += "3. **Após todas as correções, o sistema estará pronto para execução.**"
    }
    
    # Salvar relatório
    $report -join "`n" | Out-File -FilePath $OutputPath -Encoding utf8
    
    return $OutputPath
}

# Função principal
function Main {
    # Verificar se o Python está instalado
    if (-not (Check-Python)) {
        exit 1
    }
    
    # Definir caminhos
    $projectsila_dev-system = Split-Path -Path $PSScriptsila_dev-system -Parent
    $backendPath = Join-Path -Path $projectsila_dev-system -ChildPath "backend"
    $reportsDir = Join-Path -Path $projectsila_dev-system -ChildPath "reports"
    
    # Criar diretório de relatórios se não existir
    if (-not (Test-Path -Path $reportsDir -PathType Container)) {
        New-Item -Path $reportsDir -ItemType Directory | Out-Null
    }
    
    # Definir caminho do relatório
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $reportPath = Join-Path -Path $reportsDir -ChildPath "module_integrity_${timestamp}.md"
    
    Write-Host "Verificando arquivos __init__.py..." -ForegroundColor Cyan
    $missingInit = Check-InitFiles
    if ($missingInit.Count -gt 0) {
        Write-Warning "Encontrados $($missingInit.Count) diretórios sem __init__.py:"
        foreach ($path in $missingInit) {
            Write-Host "  - $path" -ForegroundColor Yellow
        }
    } else {
        Write-Host "✅ Todos os diretórios necessários possuem arquivos __init__.py." -ForegroundColor Green
    }
    
    Write-Host "Verificando padrões proibidos..." -ForegroundColor Cyan
    $forbiddenPatterns = Check-ForbiddenPatterns -Path $backendPath
    if ($forbiddenPatterns.Count -gt 0) {
        Write-Warning "Encontrados padrões proibidos em $($forbiddenPatterns.Count) arquivos."
    } else {
        Write-Host "✅ Nenhum padrão proibido encontrado." -ForegroundColor Green
    }
    
    Write-Host "Verificando estrutura dos módulos..." -ForegroundColor Cyan
    $moduleResults = Check-ModuleStructure
    $Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*edModules = ($moduleResults.Values | Where-Object { $_.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed -eq $true }).Count
    $failedModules = $moduleResults.Count - $Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*edModules
    
    if ($failedModules -gt 0) {
        Write-Warning "$failedModules módulos com problemas de estrutura:"
        foreach ($module in $moduleResults.GetEnumerator() | Where-Object { $_.Value.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed -eq $false }) {
            Write-Host "  - $($module.Key): Arquivos ausentes: $($module.Value.MissingFiles -join ', ')" -ForegroundColor Yellow
        }
    } else {
        Write-Host "✅ Todos os módulos têm a estrutura correta." -ForegroundColor Green
    }
    
    Write-Host "Verificando sintaxe Python..." -ForegroundColor Cyan
    $syntaxResults = Check-PythonSyntax -Path $backendPath
    $failedSyntax = $syntaxResults.GetEnumerator() | Where-Object { $_.Value.Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*ed -eq $false }
    
    if ($failedSyntax.Count -gt 0) {
        Write-Warning "$($failedSyntax.Count) arquivos com erros de sintaxe:"
        foreach ($result in $failedSyntax) {
            Write-Host "  - $($result.Key)" -ForegroundColor Yellow
            Write-Host "    Erro: $($result.Value.Error)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "✅ Todos os arquivos Python têm sintaxe válida." -ForegroundColor Green
    }
    
    # Gerar relatório
    Write-Host "Gerando relatório..." -ForegroundColor Cyan
    $reportFile = Generate-MarkdownReport -ModuleResults $moduleResults -MissingInit $missingInit -SyntaxResults $syntaxResults -ForbiddenPatterns $forbiddenPatterns -OutputPath $reportPath
    
    # Exibir resumo
    $endTime = Get-Date
    $duration = ($endTime - $startTime).TotalSeconds
    
    Write-Host ""
    Write-Host "="*80 -ForegroundColor Cyan
    Write-Host "RESUMO DA VALIDAÇÃO:" -ForegroundColor Cyan
    Write-Host "="*80 -ForegroundColor Cyan
    Write-Host "Total de módulos: $($moduleResults.Count)"
    Write-Host "Módulos válidos: $Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*edModules"
    Write-Host "Módulos com problemas: $failedModules"
    Write-Host "Diretórios sem __init__.py: $($missingInit.Count)"
    Write-Host "Arquivos com padrões proibidos: $($forbiddenPatterns.Count)"
    Write-Host "Arquivos com erros de sintaxe: $($failedSyntax.Count)"
    Write-Host "Tempo total de execução: $([math]::Round($duration, 2)) segundos"
    Write-Host "Relatório gerado em: $reportFile"
    
    # Determinar código de saída
    if ($failedModules -gt 0 -or $missingInit.Count -gt 0 -or $forbiddenPatterns.Count -gt 0 -or $failedSyntax.Count -gt 0) {
        Write-Host ""
        Write-Host "❌ Validação falhou! Existem problemas que precisam ser corrigidos." -ForegroundColor Red
        exit 1
    } else {
        Write-Host ""
        Write-Host "✅ Validação concluída com sucesso! Todos os módulos estão íntegros." -ForegroundColor Green
        exit 0
    }
}

# Executar função principal
Main

