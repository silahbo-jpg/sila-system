# Script PowerShell para sincronizar endpoints entre frontend e backend
# Este script garante que os endpoints do frontend e backend estejam atualizados e documentados

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

# Função para extrair endpoints do backend
function Extract-BackendEndpoints {
    $backendModulesPath = Join-Path -Path (Get-Location) -ChildPath "backend\app\modules"
    $endpoints = @{}
    
    if (-not (Test-Path -Path $backendModulesPath)) {
        Write-Warning "Diretório de módulos backend não encontrado em $backendModulesPath"
        return $endpoints
    }
    
    $modules = Get-ChildItem -Path $backendModulesPath -Directory
    
    foreach ($module in $modules) {
        $moduleName = $module.Name
        $endpointsFile = Join-Path -Path $module.FullName -ChildPath "endpoints.py"
        
        if (Test-Path -Path $endpointsFile) {
            Write-Info "Analisando endpoints do módulo $moduleName..."
            
            $content = Get-Content -Path $endpointsFile -Raw
            
            # Extrair rotas usando expressões regulares
            $routePattern = '@router\.(get|post|put|delete|patch)\(["\''](.*?)["\']'
            $matches = [regex]::Matches($content, $routePattern)
            
            $moduleEndpoints = @()
            foreach ($match in $matches) {
                $method = $match.Groups[1].Value.ToUpper()
                $route = $match.Groups[2].Value
                
                # Extrair nome da função associada
                $functionPattern = "def ([\w_]+).*?:\s*#?.*?$route"
                $functionMatch = [regex]::Match($content, $functionPattern)
                $functionName = ""
                
                if ($functionMatch.Success) {
                    $functionName = $functionMatch.Groups[1].Value
                }
                
                $moduleEndpoints += @{
                    "method" = $method
                    "route" = $route
                    "function" = $functionName
                }
            }
            
            $endpoints[$moduleName] = $moduleEndpoints
        }
    }
    
    return $endpoints
}

# Função para extrair endpoints do frontend
function Extract-FrontendEndpoints {
    $frontendServicesPath = Join-Path -Path (Get-Location) -ChildPath "frontend\webapp\src\services"
    $endpoints = @{}
    
    if (-not (Test-Path -Path $frontendServicesPath)) {
        Write-Warning "Diretório de serviços frontend não encontrado em $frontendServicesPath"
        return $endpoints
    }
    
    $serviceFiles = Get-ChildItem -Path $frontendServicesPath -Filter "*.ts" -Recurse
    
    foreach ($file in $serviceFiles) {
        $serviceName = $file.BaseName
        $content = Get-Content -Path $file.FullName -Raw
        
        # Extrair chamadas de API usando expressões regulares
        $apiCallPattern = '(get|post|put|delete|patch)\(["\''](.*?)["\']'
        $matches = [regex]::Matches($content, $apiCallPattern)
        
        $serviceEndpoints = @()
        foreach ($match in $matches) {
            $method = $match.Groups[1].Value.ToUpper()
            $route = $match.Groups[2].Value
            
            # Filtrar apenas rotas que parecem ser endpoints de API
            if ($route -match "/api/" -or $route -match "^/" -or $route -match "http") {
                $serviceEndpoints += @{
                    "method" = $method
                    "route" = $route
                }
            }
        }
        
        if ($serviceEndpoints.Count -gt 0) {
            $endpoints[$serviceName] = $serviceEndpoints
        }
    }
    
    return $endpoints
}

# Função para comparar endpoints e identificar inconsistências
function Compare-Endpoints {
    param(
        [hashtable]$BackendEndpoints,
        [hashtable]$FrontendEndpoints
    )
    
    $inconsistencies = @()
    $backendRoutes = @{}
    
    # Criar um mapa de todas as rotas do backend
    foreach ($module in $BackendEndpoints.Keys) {
        foreach ($endpoint in $BackendEndpoints[$module]) {
            $key = "$($endpoint.method):$($endpoint.route)"
            $backendRoutes[$key] = @{
                "module" = $module
                "function" = $endpoint.function
            }
        }
    }
    
    # Verificar se as rotas do frontend existem no backend
    foreach ($service in $FrontendEndpoints.Keys) {
        foreach ($endpoint in $FrontendEndpoints[$service]) {
            $key = "$($endpoint.method):$($endpoint.route)"
            
            # Normalizar rota para comparação (remover prefixos de API, etc.)
            $normalizedRoute = $endpoint.route -replace "^/api", ""
            $normalizedKey = "$($endpoint.method):$normalizedRoute"
            
            if (-not $backendRoutes.ContainsKey($key) -and -not $backendRoutes.ContainsKey($normalizedKey)) {
                $inconsistencies += @{
                    "type" = "missing_backend"
                    "service" = $service
                    "method" = $endpoint.method
                    "route" = $endpoint.route
                }
            }
        }
    }
    
    # Criar um mapa de todas as rotas do frontend
    $frontendRoutes = @{}
    foreach ($service in $FrontendEndpoints.Keys) {
        foreach ($endpoint in $FrontendEndpoints[$service]) {
            $key = "$($endpoint.method):$($endpoint.route)"
            $frontendRoutes[$key] = $service
            
            # Adicionar versão normalizada também
            $normalizedRoute = $endpoint.route -replace "^/api", ""
            $normalizedKey = "$($endpoint.method):$normalizedRoute"
            $frontendRoutes[$normalizedKey] = $service
        }
    }
    
    # Verificar se as rotas do backend são usadas no frontend
    foreach ($module in $BackendEndpoints.Keys) {
        foreach ($endpoint in $BackendEndpoints[$module]) {
            $key = "$($endpoint.method):$($endpoint.route)"
            
            if (-not $frontendRoutes.ContainsKey($key)) {
                $inconsistencies += @{
                    "type" = "missing_frontend"
                    "module" = $module
                    "method" = $endpoint.method
                    "route" = $endpoint.route
                    "function" = $endpoint.function
                }
            }
        }
    }
    
    return $inconsistencies
}

# Função para gerar documentação de API
function Generate-ApiDocumentation {
    param(
        [hashtable]$BackendEndpoints
    )
    
    $docsPath = Join-Path -Path (Get-Location) -ChildPath "docs\api"
    
    # Criar diretório de documentação se não existir
    if (-not (Test-Path -Path $docsPath)) {
        New-Item -Path $docsPath -ItemType Directory | Out-Null
    }
    
    # Gerar arquivo README.md principal
    $readmePath = Join-Path -Path $docsPath -ChildPath "README.md"
    $readmeContent = @"
# Documentação da API do sila_dev

Este diretório contém a documentação dos endpoints da API do sistema sila_dev.

## Módulos

"@
    
    foreach ($module in $BackendEndpoints.Keys | Sort-Object) {
        $readmeContent += "- [$module](./$module.md)\n"
    }
    
    $readmeContent | Out-File -FilePath $readmePath -Encoding utf8
    
    # Gerar documentação para cada módulo
    foreach ($module in $BackendEndpoints.Keys | Sort-Object) {
        $moduleDocPath = Join-Path -Path $docsPath -ChildPath "$module.md"
        $moduleDocContent = @"
# API do Módulo $module

Esta documentação descreve os endpoints disponíveis no módulo $module.

## Endpoints

"@
        
        foreach ($endpoint in $BackendEndpoints[$module] | Sort-Object -Property route) {
            $moduleDocContent += "### `$($endpoint.method) $($endpoint.route)`\n\n"
            $moduleDocContent += "**Função:** `$($endpoint.function)`\n\n"
            $moduleDocContent += "**Descrição:** *(Adicionar descrição)*\n\n"
            $moduleDocContent += "**Parâmetros:**\n\n*(Adicionar parâmetros)*\n\n"
            $moduleDocContent += "**Resposta:**\n\n*(Adicionar formato de resposta)*\n\n"
            $moduleDocContent += "---\n\n"
        }
        
        $moduleDocContent | Out-File -FilePath $moduleDocPath -Encoding utf8
    }
    
    return $docsPath
}

# Função para atualizar arquivos de serviço do frontend
function Update-FrontendServices {
    param(
        [array]$Inconsistencies
    )
    
    $missingFrontend = $Inconsistencies | Where-Object { $_.type -eq "missing_frontend" }
    
    if ($missingFrontend.Count -eq 0) {
        Write-Success "Não há endpoints do backend ausentes no frontend."
        return $true
    }
    
    Write-Info "Encontrados $($missingFrontend.Count) endpoints do backend ausentes no frontend."
    
    # Agrupar por módulo
    $moduleGroups = $missingFrontend | Group-Object -Property module
    
    foreach ($group in $moduleGroups) {
        $moduleName = $group.Name
        $serviceFilePath = Join-Path -Path (Get-Location) -ChildPath "frontend\webapp\src\services\${moduleName}Service.ts"
        
        # Verificar se o arquivo de serviço já existe
        $serviceExists = Test-Path -Path $serviceFilePath
        
        if (-not $serviceExists) {
            # Criar novo arquivo de serviço
            Write-Info "Criando novo arquivo de serviço para o módulo $moduleName..."
            
            $serviceContent = @"
// ${moduleName}Service.ts - Gerado automaticamente por sync-endpoints.ps1
import axios from 'axios';
import { API_BASE_URL } from '../config';

const ${moduleName}Service = {
"@
            
            foreach ($endpoint in $group.Group) {
                $functionName = $endpoint.function
                $method = $endpoint.method.ToLower()
                $route = $endpoint.route
                
                $serviceContent += @"

  // $functionName
  ${functionName}: async (params = {}) => {
    try {
      const response = await axios.${method}(`${API_BASE_URL}${route}`, params);
      return response.data;
    } catch (error) {
      console.error(`Erro ao chamar ${functionName}:`, error);
      throw error;
    }
  },
"@
            }
            
            $serviceContent += @"

};

export default ${moduleName}Service;
"@
            
            $serviceContent | Out-File -FilePath $serviceFilePath -Encoding utf8
            Write-Success "Arquivo de serviço criado: $serviceFilePath"
        }
        else {
            # Atualizar arquivo de serviço existente
            Write-Info "Atualizando arquivo de serviço existente para o módulo $moduleName..."
            
            $content = Get-Content -Path $serviceFilePath -Raw
            $updatedContent = $content
            
            foreach ($endpoint in $group.Group) {
                $functionName = $endpoint.function
                $method = $endpoint.method.ToLower()
                $route = $endpoint.route
                
                # Verificar se a função já existe no arquivo
                if ($content -notmatch "\b$functionName\s*:") {
                    $newFunction = @"

  // $functionName
  ${functionName}: async (params = {}) => {
    try {
      const response = await axios.${method}(`${API_BASE_URL}${route}`, params);
      return response.data;
    } catch (error) {
      console.error(`Erro ao chamar ${functionName}:`, error);
      throw error;
    }
  },
"@
                    
                    # Inserir antes do fechamento do objeto de serviço
                    $updatedContent = $updatedContent -replace "(\n\};\s*\n*export default)", "$newFunction$1"
                }
            }
            
            if ($updatedContent -ne $content) {
                $updatedContent | Out-File -FilePath $serviceFilePath -Encoding utf8
                Write-Success "Arquivo de serviço atualizado: $serviceFilePath"
            }
            else {
                Write-Info "Nenhuma atualização necessária para $serviceFilePath"
            }
        }
    }
    
    return $true
}

# Função principal
function Main {
    Write-Header "Sincronização de Endpoints do sila_dev"
    
    # Extrair endpoints do backend
    Write-Info "Extraindo endpoints do backend..."
    $backendEndpoints = Extract-BackendEndpoints
    $totalBackendEndpoints = 0
    foreach ($module in $backendEndpoints.Keys) {
        $totalBackendEndpoints += $backendEndpoints[$module].Count
    }
    Write-Success "Encontrados $totalBackendEndpoints endpoints no backend em $($backendEndpoints.Keys.Count) módulos."
    
    # Extrair endpoints do frontend
    Write-Info "Extraindo endpoints do frontend..."
    $frontendEndpoints = Extract-FrontendEndpoints
    $totalFrontendEndpoints = 0
    foreach ($service in $frontendEndpoints.Keys) {
        $totalFrontendEndpoints += $frontendEndpoints[$service].Count
    }
    Write-Success "Encontrados $totalFrontendEndpoints endpoints no frontend em $($frontendEndpoints.Keys.Count) serviços."
    
    # Comparar endpoints
    Write-Info "Comparando endpoints..."
    $inconsistencies = Compare-Endpoints -BackendEndpoints $backendEndpoints -FrontendEndpoints $frontendEndpoints
    
    # Exibir inconsistências
    Write-Header "Resultados da Comparação"
    
    $missingBackend = $inconsistencies | Where-Object { $_.type -eq "missing_backend" }
    $missingFrontend = $inconsistencies | Where-Object { $_.type -eq "missing_frontend" }
    
    if ($missingBackend.Count -gt 0) {
        Write-Warning "Endpoints usados no frontend mas ausentes no backend: $($missingBackend.Count)"
        foreach ($item in $missingBackend) {
            Write-Warning "  $($item.method) $($item.route) (usado em $($item.service))"
        }
    } else {
        Write-Success "Todos os endpoints usados no frontend estão implementados no backend."
    }
    
    if ($missingFrontend.Count -gt 0) {
        Write-Warning "Endpoints implementados no backend mas não usados no frontend: $($missingFrontend.Count)"
        foreach ($item in $missingFrontend) {
            Write-Warning "  $($item.method) $($item.route) (implementado em $($item.module).$($item.function))"
        }
        
        # Perguntar se deseja gerar serviços para endpoints ausentes
        $choice = Read-Host "Deseja gerar/atualizar serviços no frontend para os endpoints ausentes? (S/N)"
        
        if ($choice -eq "S" -or $choice -eq "s") {
            Update-FrontendServices -Inconsistencies $inconsistencies
        }
    } else {
        Write-Success "Todos os endpoints do backend são utilizados no frontend."
    }
    
    # Gerar documentação
    Write-Info "Gerando documentação da API..."
    $docsPath = Generate-ApiDocumentation -BackendEndpoints $backendEndpoints
    Write-Success "Documentação da API gerada em: $docsPath"
    
    # Resumo final
    Write-Header "Resumo da Sincronização"
    Write-Info "Total de endpoints no backend: $totalBackendEndpoints"
    Write-Info "Total de endpoints no frontend: $totalFrontendEndpoints"
    Write-Info "Inconsistências encontradas: $($inconsistencies.Count)"
    
    if ($inconsistencies.Count -eq 0) {
        Write-Success "Frontend e backend estão completamente sincronizados!"
        exit 0
    } else {
        Write-Warning "Foram encontradas inconsistências entre frontend e backend. Verifique os detalhes acima."
        exit 1
    }
}

# Executar função principal
Main

