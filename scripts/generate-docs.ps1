# Script PowerShell para gerar documentação técnica dos módulos e APIs
# Este script extrai e atualiza a documentação técnica do projeto sila_dev

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

# Função para verificar dependências
function Check-Dependencies {
    # Verificar se o Python está instalado
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Python não encontrado. Por favor, instale o Python 3.8 ou superior."
            return $false
        }
        
        Write-Info "Python encontrado: $pythonVersion"
        
        # Verificar se o módulo pdoc está instalado
        $pdocInstalled = python -c "import pdoc" 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Warning "Módulo pdoc não encontrado. Tentando instalar..."
            python -m pip install pdoc3 2>&1
            
            if ($LASTEXITCODE -ne 0) {
                Write-Error "Falha ao instalar pdoc. Por favor, instale manualmente com: pip install pdoc3"
                return $false
            }
        }
        
        Write-Success "Todas as dependências estão instaladas."
        return $true
    }
    catch {
        Write-Error "Erro ao verificar dependências: $_"
        return $false
    }
}

# Função para gerar documentação de código Python
function Generate-PythonDocs {
    $backendPath = Join-Path -Path (Get-Location) -ChildPath "backend\app"
    $docsOutputPath = Join-Path -Path (Get-Location) -ChildPath "docs\python"
    
    # Criar diretório de saída se não existir
    if (-not (Test-Path -Path $docsOutputPath)) {
        New-Item -Path $docsOutputPath -ItemType Directory | Out-Null
    }
    
    Write-Info "Gerando documentação Python para $backendPath..."
    
    try {
        # Usar pdoc para gerar documentação HTML
        $result = python -m pdoc --html --output-dir $docsOutputPath $backendPath 2>&1
        
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Falha ao gerar documentação Python: $result"
            return $false
        }
        
        Write-Success "Documentação Python gerada com sucesso em: $docsOutputPath"
        return $true
    }
    catch {
        Write-Error "Erro ao gerar documentação Python: $_"
        return $false
    }
}

# Função para extrair informações dos modelos de dados
function Extract-DataModels {
    $backendModulesPath = Join-Path -Path (Get-Location) -ChildPath "backend\app\modules"
    $modelsOutputPath = Join-Path -Path (Get-Location) -ChildPath "docs\models"
    
    # Criar diretório de saída se não existir
    if (-not (Test-Path -Path $modelsOutputPath)) {
        New-Item -Path $modelsOutputPath -ItemType Directory | Out-Null
    }
    
    if (-not (Test-Path -Path $backendModulesPath)) {
        Write-Warning "Diretório de módulos não encontrado em $backendModulesPath"
        return $false
    }
    
    $modules = Get-ChildItem -Path $backendModulesPath -Directory
    
    # Gerar arquivo README.md principal
    $readmePath = Join-Path -Path $modelsOutputPath -ChildPath "README.md"
    $readmeContent = @"
# Modelos de Dados do sila_dev

Este diretório contém a documentação dos modelos de dados do sistema sila_dev.

## Módulos

"@
    
    foreach ($module in $modules) {
        $moduleName = $module.Name
        $readmeContent += "- [$moduleName](./$moduleName.md)\n"
    }
    
    $readmeContent | Out-File -FilePath $readmePath -Encoding utf8
    
    # Processar cada módulo
    foreach ($module in $modules) {
        $moduleName = $module.Name
        $modelsFile = Join-Path -Path $module.FullName -ChildPath "models.py"
        
        if (Test-Path -Path $modelsFile) {
            Write-Info "Extraindo modelos do módulo $moduleName..."
            
            $content = Get-Content -Path $modelsFile -Raw
            
            # Extrair classes de modelo usando expressões regulares
            $classPattern = "class\s+([\w]+)\s*\(.*?\):\s*"
            $matches = [regex]::Matches($content, $classPattern)
            
            $moduleDocPath = Join-Path -Path $modelsOutputPath -ChildPath "$moduleName.md"
            $moduleDocContent = @"
# Modelos de Dados: $moduleName

Esta documentação descreve os modelos de dados disponíveis no módulo $moduleName.

"@
            
            if ($matches.Count -eq 0) {
                $moduleDocContent += "*Nenhum modelo de dados encontrado neste módulo.*\n"
            }
            else {
                foreach ($match in $matches) {
                    $className = $match.Groups[1].Value
                    
                    # Extrair docstring da classe
                    $docstringPattern = "class\s+$className.*?:\s*\"\"\"(.*?)\"\"\""  # Padrão para docstring de várias linhas
                    $docstringMatch = [regex]::Match($content, $docstringPattern, [System.Text.RegularExpressions.RegexOptions]::Singleline)
                    
                    $docstring = ""
                    if ($docstringMatch.Success) {
                        $docstring = $docstringMatch.Groups[1].Value.Trim()
                    }
                    
                    # Extrair atributos da classe
                    $attributePattern = "$className.*?:\s*.*?(?:\"\"\".*?\"\"\")?\s*(.+?)(?=\s*class|\s*$)"
                    $attributeMatch = [regex]::Match($content, $attributePattern, [System.Text.RegularExpressions.RegexOptions]::Singleline)
                    
                    $attributes = @()
                    if ($attributeMatch.Success) {
                        $attributeText = $attributeMatch.Groups[1].Value
                        $attributeLines = $attributeText -split "`n" | Where-Object { $_ -match "\s*([\w_]+)\s*=" }
                        
                        foreach ($line in $attributeLines) {
                            if ($line -match "\s*([\w_]+)\s*=\s*(.*)$") {
                                $attrName = $matches[1]
                                $attrValue = $matches[2].Trim()
                                
                                $attributes += @{
                                    "name" = $attrName
                                    "value" = $attrValue
                                }
                            }
                        }
                    }
                    
                    # Adicionar à documentação
                    $moduleDocContent += "## $className\n\n"
                    
                    if ($docstring) {
                        $moduleDocContent += "$docstring\n\n"
                    }
                    
                    if ($attributes.Count -gt 0) {
                        $moduleDocContent += "### Atributos\n\n"
                        $moduleDocContent += "| Nome | Tipo/Valor |\n|------|------------|\n"
                        
                        foreach ($attr in $attributes) {
                            $moduleDocContent += "| $($attr.name) | $($attr.value) |\n"
                        }
                        
                        $moduleDocContent += "\n"
                    }
                    
                    $moduleDocContent += "---\n\n"
                }
            }
            
            $moduleDocContent | Out-File -FilePath $moduleDocPath -Encoding utf8
        }
    }
    
    Write-Success "Documentação de modelos de dados gerada com sucesso em: $modelsOutputPath"
    return $true
}

# Função para gerar documentação de API
function Generate-ApiDocs {
    $backendModulesPath = Join-Path -Path (Get-Location) -ChildPath "backend\app\modules"
    $apiDocsPath = Join-Path -Path (Get-Location) -ChildPath "docs\api"
    
    # Criar diretório de saída se não existir
    if (-not (Test-Path -Path $apiDocsPath)) {
        New-Item -Path $apiDocsPath -ItemType Directory | Out-Null
    }
    
    if (-not (Test-Path -Path $backendModulesPath)) {
        Write-Warning "Diretório de módulos não encontrado em $backendModulesPath"
        return $false
    }
    
    $modules = Get-ChildItem -Path $backendModulesPath -Directory
    
    # Gerar arquivo README.md principal
    $readmePath = Join-Path -Path $apiDocsPath -ChildPath "README.md"
    $readmeContent = @"
# Documentação da API do sila_dev

Este diretório contém a documentação dos endpoints da API do sistema sila_dev.

## Módulos

"@
    
    foreach ($module in $modules) {
        $moduleName = $module.Name
        $readmeContent += "- [$moduleName](./$moduleName.md)\n"
    }
    
    $readmeContent | Out-File -FilePath $readmePath -Encoding utf8
    
    # Processar cada módulo
    foreach ($module in $modules) {
        $moduleName = $module.Name
        $endpointsFile = Join-Path -Path $module.FullName -ChildPath "endpoints.py"
        
        if (Test-Path -Path $endpointsFile) {
            Write-Info "Extraindo endpoints do módulo $moduleName..."
            
            $content = Get-Content -Path $endpointsFile -Raw
            
            # Extrair rotas usando expressões regulares
            $routePattern = '@router\.(get|post|put|delete|patch)\(["\''](.*?)["\']'
            $matches = [regex]::Matches($content, $routePattern)
            
            $moduleDocPath = Join-Path -Path $apiDocsPath -ChildPath "$moduleName.md"
            $moduleDocContent = @"
# API do Módulo $moduleName

Esta documentação descreve os endpoints disponíveis no módulo $moduleName.

## Endpoints

"@
            
            if ($matches.Count -eq 0) {
                $moduleDocContent += "*Nenhum endpoint encontrado neste módulo.*\n"
            }
            else {
                foreach ($match in $matches) {
                    $method = $match.Groups[1].Value.ToUpper()
                    $route = $match.Groups[2].Value
                    
                    # Extrair função associada
                    $functionPattern = "def ([\w_]+).*?:\s*.*?$route"
                    $functionMatch = [regex]::Match($content, $functionPattern)
                    $functionName = ""
                    
                    if ($functionMatch.Success) {
                        $functionName = $functionMatch.Groups[1].Value
                    }
                    
                    # Extrair docstring da função
                    $docstringPattern = "def\s+$functionName.*?:\s*\"\"\"(.*?)\"\"\""  # Padrão para docstring de várias linhas
                    $docstringMatch = [regex]::Match($content, $docstringPattern, [System.Text.RegularExpressions.RegexOptions]::Singleline)
                    
                    $docstring = ""
                    if ($docstringMatch.Success) {
                        $docstring = $docstringMatch.Groups[1].Value.Trim()
                    }
                    
                    # Adicionar à documentação
                    $moduleDocContent += "### `$method $route`\n\n"
                    $moduleDocContent += "**Função:** `$functionName`\n\n"
                    
                    if ($docstring) {
                        $moduleDocContent += "**Descrição:**\n\n$docstring\n\n"
                    }
                    else {
                        $moduleDocContent += "**Descrição:** *(Adicionar descrição)*\n\n"
                    }
                    
                    $moduleDocContent += "**Parâmetros:**\n\n*(Adicionar parâmetros)*\n\n"
                    $moduleDocContent += "**Resposta:**\n\n*(Adicionar formato de resposta)*\n\n"
                    $moduleDocContent += "---\n\n"
                }
            }
            
            $moduleDocContent | Out-File -FilePath $moduleDocPath -Encoding utf8
        }
    }
    
    Write-Success "Documentação de API gerada com sucesso em: $apiDocsPath"
    return $true
}

# Função para gerar documentação de arquitetura
function Generate-ArchitectureDocs {
    $docsPath = Join-Path -Path (Get-Location) -ChildPath "docs\architecture"
    
    # Criar diretório de saída se não existir
    if (-not (Test-Path -Path $docsPath)) {
        New-Item -Path $docsPath -ItemType Directory | Out-Null
    }
    
    # Gerar arquivo README.md principal
    $readmePath = Join-Path -Path $docsPath -ChildPath "README.md"
    $readmeContent = @"
# Arquitetura do Sistema sila_dev

Este diretório contém a documentação da arquitetura do sistema sila_dev.

## Conteúdo

- [Visão Geral](./overview.md)
- [Módulos](./modules.md)
- [Fluxo de Dados](./data-flow.md)
- [Integração](./integration.md)
- [Segurança](./security.md)

"@
    
    $readmeContent | Out-File -FilePath $readmePath -Encoding utf8
    
    # Gerar documentação de visão geral
    $overviewPath = Join-Path -Path $docsPath -ChildPath "overview.md"
    $overviewContent = @"
# Visão Geral da Arquitetura

## Introdução

O Sistema Integrado de Licenciamento Angolano (sila_dev) é uma plataforma modular projetada para gerenciar processos de licenciamento e registro de cidadãos e empresas.

## Pilares Estratégicos

1. **Registro**: Gerenciamento de dados de cidadãos e empresas
2. **Governança**: Auditoria, permissões e conformidade
3. **Finanças**: Processamento de pagamentos e gestão financeira
4. **Integração**: Conexão com sistemas externos (BNA, SIMPLIFICA)
5. **Saúde**: Monitoramento e diagnóstico do sistema

## Arquitetura Técnica

### Backend

- **Linguagem**: Python
- **Framework**: FastAPI
- **Banco de Dados**: sila_dev-systemQL
- **Autenticação**: JWT

### Frontend

- **Framework**: React
- **UI**: Material-UI
- **Estado**: Redux
- **Comunicação**: Axios

### Infraestrutura

- **Containerização**: Docker
- **Orquestração**: Kubernetes
- **CI/CD**: GitHub Actions
- **Monitoramento**: Prometheus/Grafana

"@
    
    $overviewContent | Out-File -FilePath $overviewPath -Encoding utf8
    
    # Gerar documentação de módulos
    $modulesPath = Join-Path -Path $docsPath -ChildPath "modules.md"
    $modulesContent = @"
# Módulos do Sistema

## Estrutura Modular

O sila_dev é organizado em módulos independentes que se comunicam através de interfaces bem definidas.

## Módulos Principais

### Módulo de Registro

**Responsabilidade**: Gerenciamento de dados de cidadãos e empresas.

**Componentes**:
- Cadastro de cidadãos
- Cadastro de empresas
- Validação de documentos
- Histórico de alterações

### Módulo de Governança

**Responsabilidade**: Auditoria, permissões e conformidade.

**Componentes**:
- Logs de auditoria
- Gestão de permissões
- Relatórios de conformidade
- Monitoramento de atividades

### Módulo de Finanças

**Responsabilidade**: Processamento de pagamentos e gestão financeira.

**Componentes**:
- Processamento de pagamentos
- Emissão de recibos
- Relatórios financeiros
- Integração com BNA

### Módulo de Integração

**Responsabilidade**: Conexão com sistemas externos.

**Componentes**:
- Adaptadores para BNA
- Adaptadores para SIMPLIFICA
- API pública
- Webhooks

### Módulo de Saúde

**Responsabilidade**: Monitoramento e diagnóstico do sistema.

**Componentes**:
- Monitoramento de performance
- Alertas
- Diagnóstico de problemas
- Logs de sistema

"@
    
    $modulesContent | Out-File -FilePath $modulesPath -Encoding utf8
    
    # Gerar documentação de fluxo de dados
    $dataFlowPath = Join-Path -Path $docsPath -ChildPath "data-flow.md"
    $dataFlowContent = @"
# Fluxo de Dados

## Visão Geral

Este documento descreve como os dados fluem entre os diferentes módulos do sistema sila_dev.

## Fluxos Principais

### Registro de Cidadão

1. **Frontend** → Formulário de registro preenchido pelo usuário
2. **API** → Recebe os dados e valida formato
3. **Módulo de Registro** → Processa e armazena os dados
4. **Módulo de Integração** → Verifica dados com SIMPLIFICA (opcional)
5. **Módulo de Governança** → Registra a operação no log de auditoria
6. **Módulo de Registro** → Retorna confirmação
7. **API** → Envia resposta ao frontend

### Processamento de Pagamento

1. **Frontend** → Dados de pagamento enviados
2. **API** → Recebe os dados e valida formato
3. **Módulo de Finanças** → Processa o pagamento
4. **Módulo de Integração** → Comunica com BNA para autorização
5. **Módulo de Finanças** → Registra o resultado da transação
6. **Módulo de Governança** → Registra a operação no log de auditoria
7. **API** → Envia resposta ao frontend

## Diagrama de Sequência

```
┌─────────┐  ┌─────┐  ┌─────────┐  ┌───────────┐  ┌────────────┐
│ Frontend │  │ API │  │ Módulo  │  │ Integração │  │ Governança │
└────┬────┘  └──┬──┘  └────┬────┘  └─────┬─────┘  └──────┬─────┘
     │          │          │              │               │
     │ Request  │          │              │               │
     ├─────────>│          │              │               │
     │          │ Process  │              │               │
     │          ├─────────>│              │               │
     │          │          │ Validate     │               │
     │          │          ├─────────────>│               │
     │          │          │              │ Log          │
     │          │          │              ├──────────────>│
     │          │          │ Response     │               │
     │          │<─────────┤              │               │
     │ Response │          │              │               │
     │<─────────┤          │              │               │
     │          │          │              │               │
```

"@
    
    $dataFlowContent | Out-File -FilePath $dataFlowPath -Encoding utf8
    
    # Gerar documentação de integração
    $integrationPath = Join-Path -Path $docsPath -ChildPath "integration.md"
    $integrationContent = @"
# Integração

## Visão Geral

Este documento descreve as integrações do sistema sila_dev com sistemas externos.

## Sistemas Integrados

### BNA (Banco Nacional de Angola)

**Propósito**: Processamento de pagamentos e validação financeira.

**Métodos de Integração**:
- API REST
- Webhooks para notificações assíncronas

**Fluxos de Dados**:
- Autorização de pagamentos
- Verificação de transações
- Notificações de status

### SIMPLIFICA 2.0

**Propósito**: Validação de dados de cidadãos e empresas.

**Métodos de Integração**:
- API REST
- Troca de arquivos batch (opcional)

**Fluxos de Dados**:
- Validação de documentos
- Verificação de registros
- Sincronização de dados cadastrais

## Segurança da Integração

- Autenticação via OAuth 2.0
- Comunicação criptografada (TLS 1.3)
- Validação de certificados
- Logs de todas as chamadas de API
- Monitoramento de tempo de resposta e disponibilidade

## Estratégia de Resiliência

- Retry automático com backoff exponencial
- Circuit breaker para falhas persistentes
- Filas de mensagens para operações assíncronas
- Cache de dados frequentemente acessados
- Modo offline para operações críticas

"@
    
    $integrationContent | Out-File -FilePath $integrationPath -Encoding utf8
    
    # Gerar documentação de segurança
    $securityPath = Join-Path -Path $docsPath -ChildPath "security.md"
    $securityContent = @"
# Segurança

## Visão Geral

Este documento descreve a arquitetura de segurança do sistema sila_dev.

## Autenticação e Autorização

### Autenticação

- **JWT (JSON Web Tokens)** para autenticação stateless
- Rotação de tokens com refresh tokens
- Expiração configurável de tokens
- Autenticação multi-fator para usuários sila_dev-systemistrativos

### Autorização

- Sistema de permissões baseado em papéis (RBAC)
- Permissões granulares por módulo e operação
- Segregação de funções para operações sensíveis
- Validação de permissões em cada camada (API, serviço, dados)

## Proteção de Dados

- Criptografia de dados sensíveis em repouso
- TLS para todas as comunicações
- Mascaramento de dados sensíveis em logs
- Política de retenção de dados
- Backups criptografados

## Auditoria e Monitoramento

- Logs detalhados de todas as operações
- Alertas para atividades suspeitas
- Monitoramento de tentativas de acesso não autorizado
- Análise regular de logs
- Testes de penetração periódicos

## Conformidade

- Aderência às regulamentações angolanas de proteção de dados
- Processos documentados para resposta a incidentes
- Avaliações regulares de vulnerabilidades
- Treinamento de equipe em segurança

"@
    
    $securityContent | Out-File -FilePath $securityPath -Encoding utf8
    
    Write-Success "Documentação de arquitetura gerada com sucesso em: $docsPath"
    return $true
}

# Função para gerar índice geral da documentação
function Generate-DocsIndex {
    $docsPath = Join-Path -Path (Get-Location) -ChildPath "docs"
    
    # Verificar se o diretório docs existe
    if (-not (Test-Path -Path $docsPath)) {
        Write-Warning "Diretório de documentação não encontrado em $docsPath"
        return $false
    }
    
    # Gerar arquivo README.md principal
    $readmePath = Join-Path -Path $docsPath -ChildPath "README.md"
    $readmeContent = @"
# Documentação do Sistema sila_dev

Bem-vindo à documentação do Sistema Integrado de Licenciamento Angolano (sila_dev).

## Conteúdo

"@
    
    # Adicionar links para as seções de documentação
    $sections = @(
        @{ "path" = "architecture"; "title" = "Arquitetura" },
        @{ "path" = "api"; "title" = "API" },
        @{ "path" = "models"; "title" = "Modelos de Dados" },
        @{ "path" = "python"; "title" = "Documentação Python" }
    )
    
    foreach ($section in $sections) {
        $sectionPath = Join-Path -Path $docsPath -ChildPath $section.path
        
        if (Test-Path -Path $sectionPath) {
            $readmeContent += "- [$($section.title)](./$($section.path)/)\n"
        }
    }
    
    # Adicionar informações sobre geração da documentação
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $readmeContent += @"

## Sobre esta Documentação

Esta documentação foi gerada automaticamente pelo script `generate-docs.ps1` em $timestamp.

Para atualizar a documentação, execute:

```powershell
.\scripts\generate-docs.ps1
```

"@
    
    $readmeContent | Out-File -FilePath $readmePath -Encoding utf8
    
    Write-Success "Índice geral da documentação gerado com sucesso em: $readmePath"
    return $true
}

# Função principal
function Main {
    Write-Header "Geração de Documentação do sila_dev"
    
    # Verificar dependências
    if (-not (Check-Dependencies)) {
        Write-Error "Falha na verificação de dependências. Abortando."
        exit 1
    }
    
    # Criar diretório docs se não existir
    $docsPath = Join-Path -Path (Get-Location) -ChildPath "docs"
    if (-not (Test-Path -Path $docsPath)) {
        New-Item -Path $docsPath -ItemType Directory | Out-Null
        Write-Info "Diretório de documentação criado: $docsPath"
    }
    
    # Gerar documentação Python
    Write-Header "Gerando Documentação Python"
    $pythonDocsOk = Generate-PythonDocs
    
    # Extrair modelos de dados
    Write-Header "Extraindo Modelos de Dados"
    $dataModelsOk = Extract-DataModels
    
    # Gerar documentação de API
    Write-Header "Gerando Documentação de API"
    $apiDocsOk = Generate-ApiDocs
    
    # Gerar documentação de arquitetura
    Write-Header "Gerando Documentação de Arquitetura"
    $architectureDocsOk = Generate-ArchitectureDocs
    
    # Gerar índice geral
    Write-Header "Gerando Índice Geral"
    $indexOk = Generate-DocsIndex
    
    # Resumo final
    Write-Header "Resumo da Geração de Documentação"
    
    $allOk = $pythonDocsOk -and $dataModelsOk -and $apiDocsOk -and $architectureDocsOk -and $indexOk
    
    if ($allOk) {
        Write-Success "Toda a documentação foi gerada com sucesso!"
        Write-Info "A documentação está disponível em: $docsPath"
        exit 0
    } else {
        Write-Warning "Houve problemas durante a geração da documentação. Verifique os detalhes acima."
        exit 1
    }
}

# Executar função principal
Main

