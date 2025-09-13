# Script para saneamento do projeto SILA
# Baseado nas recomendações do arquivo truman_try.txt

function log_info($msg) {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$ts] [INFO] $msg" -ForegroundColor Cyan
}
function log_success($msg) {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$ts] [SUCCESS] $msg" -ForegroundColor Green
}
function log_error($msg) {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$ts] [ERROR] $msg" -ForegroundColor Red
}

$etapas = @()
function registrar_etapa($desc, $status) {
    $etapas += "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [$status] $desc"
}

log_info "Iniciando saneamento do projeto SILA..."

# 1. Remover arquivos desnecessários
log_info "Removendo arquivos desnecessários..."

$arquivosParaRemover = @(
    ".cascade_tmp",
    "backend\.cascade_tmp",
    "tests\.cascade_tmp",
    "backend\app\main.py.bak",
    "backend\package.json.backup",
    "frontend\webapp\npx",
    "nano generate_tree_json.py"
)

foreach ($arquivo in $arquivosParaRemover) {
    if (Test-Path $arquivo) {
        Remove-Item $arquivo -Force
        log_success "Removido: $arquivo"
        registrar_etapa "Arquivo removido: $arquivo" "OK"
    } else {
        log_info "Não encontrado: $arquivo"
        registrar_etapa "Arquivo não encontrado: $arquivo" "INFO"
    }
}

# 2. Verificar arquivo tgres
log_info "Verificando arquivo tgres..."
if (Test-Path "tgres") {
    $tamanhoTgres = (Get-Item "tgres").Length
    log_info "Arquivo 'tgres' encontrado ($tamanhoTgres bytes)."
    log_info "Este parece ser um arquivo de saída do PostgreSQL. Movendo para pasta de documentação..."
    # Criar diretório de documentação se não existir
    if (-not (Test-Path "docs")) {
        New-Item -Path "docs" -ItemType Directory -Force | Out-Null
    }
    # Mover o arquivo para a pasta de documentação
    Move-Item "tgres" -Destination "docs\tgres.txt" -Force
    log_success "Arquivo 'tgres' movido para 'docs\tgres.txt'"
    registrar_etapa "Arquivo 'tgres' movido para documentação" "OK"
} else {
    registrar_etapa "Arquivo 'tgres' não encontrado" "INFO"
}

# 3. Padronizar scripts de setup
log_info "Padronizando scripts de setup..."

$scriptsSetup = @(
    "backend\setup_backend.ps1",
    "backend\setup_backend_new.ps1",
    "backend\setup_backend_simple.ps1"
)

$scriptsEncontrados = $scriptsSetup | Where-Object { Test-Path $_ }

if ($scriptsEncontrados.Count -gt 1) {
    log_info "Encontrados múltiplos scripts de setup:"
    foreach ($script in $scriptsEncontrados) {
        log_info "  - $script"
    }
    
    # Criar diretório de backup se não existir
    if (-not (Test-Path "backend\setup_backup")) {
        New-Item -Path "backend\setup_backup" -ItemType Directory -Force | Out-Null
        log_success "Criado diretório de backup: backend\setup_backup"
    }
    
    # Manter apenas setup_backend_simple.ps1 e criar backup dos outros
    if (Test-Path "backend\setup_backend.ps1") {
        # Verificar se não é o mesmo arquivo que queremos manter
        $pathSimple = Resolve-Path "backend\setup_backend_simple.ps1" -ErrorAction SilentlyContinue
        $pathRegular = Resolve-Path "backend\setup_backend.ps1" -ErrorAction SilentlyContinue
        
        if ($pathSimple -ne $pathRegular) {
            Copy-Item "backend\setup_backend.ps1" -Destination "backend\setup_backup\setup_backend.ps1.bak" -Force
            Remove-Item "backend\setup_backend.ps1" -Force
            log_success "Removido: backend\setup_backend.ps1 (backup criado)"
        }
    }
    
    if (Test-Path "backend\setup_backend_new.ps1") {
        Copy-Item "backend\setup_backend_new.ps1" -Destination "backend\setup_backup\setup_backend_new.ps1.bak" -Force
        Remove-Item "backend\setup_backend_new.ps1" -Force
        log_success "Removido: backend\setup_backend_new.ps1 (backup criado)"
    }
    
    # Renomear setup_backend_simple.ps1 para setup_backend.ps1 se necessário
    if ((Test-Path "backend\setup_backend_simple.ps1") -and (-not (Test-Path "backend\setup_backend.ps1"))) {
        Copy-Item "backend\setup_backend_simple.ps1" -Destination "backend\setup_backend.ps1" -Force
        Remove-Item "backend\setup_backend_simple.ps1" -Force
        log_success "Renomeado: setup_backend_simple.ps1 -> setup_backend.ps1"
    }
    
    log_success "Scripts de setup padronizados."
}

# 4. Corrigir arquivos __init__.py corrompidos
log_info "Verificando e corrigindo arquivos __init__.py corrompidos..."
if (Test-Path "fix_init_files.py") {
    try {
        python fix_init_files.py
        log_success "Arquivos __init__.py verificados e corrigidos."
        registrar_etapa "Arquivos __init__.py corrigidos" "OK"
    } catch {
        log_error "Falha ao corrigir arquivos __init__.py: $_"
        registrar_etapa "Falha ao corrigir arquivos __init__.py" "ERRO"
    }
} else {
    log_info "Script fix_init_files.py não encontrado. Pulando correção."
    registrar_etapa "Script fix_init_files.py não encontrado" "INFO"
}

# 5. Gerar árvore atualizada do projeto
log_info "Gerando árvore atualizada do projeto..."

$estruturaPath = "estrutura_atualizada.txt"

Get-ChildItem -Recurse -Depth 3 | Where-Object {
    $_.Name -ne "node_modules" -and
    $_.Name -ne "__pycache__" -and
    $_.Name -ne ".git" -and
    $_.Name -ne "dist" -and
    $_.Name -ne "logs" -and
    $_.Name -ne "backups" -and
    $_.Name -ne "db_backups" -and
    $_.Name -notlike "*.log" -and
    $_.Name -notlike "*.db*" -and
    $_.Name -notlike "*.backup*"
} | Sort-Object FullName | ForEach-Object {
    $relativePath = $_.FullName.Replace((Get-Location).Path + "\", "")
    $depth = ($relativePath.Split("\").Length - 1)
    $indent = "  " * $depth
    
    if ($_.PSIsContainer) {
        "$indent[D] $($_.Name)"
    } else {
        "$indent[F] $($_.Name)"
    }
} | Out-File -Encoding UTF8 $estruturaPath

log_success "Árvore do projeto gerada em: $estruturaPath"
registrar_etapa "Árvore do projeto gerada em: $estruturaPath" "OK"

# 5. Remover fsevents do node_modules (Windows)
if ($env:OS -eq "Windows_NT") {
    $fseventsPath = "frontend\webapp\node_modules\fsevents"
    if (Test-Path $fseventsPath) {
        Remove-Item $fseventsPath -Recurse -Force
        log_success "Pacote opcional 'fsevents' removido do node_modules."
        registrar_etapa "fsevents removido do node_modules" "OK"
    }
}

# 5. Validação do backend antes do build do frontend
log_info "[Checkpoint] Validando backend antes do build do frontend..."

# Validação .env backend
if (Test-Path "backend\.env") {
    log_success ".env do backend encontrado."
    registrar_etapa ".env do backend encontrado" "OK"
} else {
    log_error ".env do backend NÃO encontrado. Abortando."
    registrar_etapa ".env do backend NÃO encontrado" "ERRO"
    exit 1
}

# Validação .env frontend
if (Test-Path "frontend\webapp\.env") {
    log_success ".env do frontend encontrado."
    registrar_etapa ".env do frontend encontrado" "OK"
} else {
    log_error ".env do frontend NÃO encontrado. Abortando."
    registrar_etapa ".env do frontend NÃO encontrado" "ERRO"
    exit 1
}

# Validação versão do Node.js
try {
    $nodeVersion = node --version
    if ($nodeVersion -match "v(1[6-9]|[2-9][0-9])") {
        log_success "Node.js versão $nodeVersion OK."
        registrar_etapa "Node.js versão $nodeVersion OK" "OK"
    } else {
        log_error "Node.js versão $nodeVersion insuficiente. Requerido >=16. Abortando."
        registrar_etapa "Node.js versão $nodeVersion insuficiente" "ERRO"
        exit 1
    }
} catch {
    log_error "Node.js não encontrado. Abortando."
    registrar_etapa "Node.js não encontrado" "ERRO"
    exit 1
}

# Testar conectividade backend
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/docs" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        log_success "Backend está respondendo em http://localhost:8000/docs."
        registrar_etapa "Backend está respondendo em /docs" "OK"
    } else {
        log_error "Backend não respondeu corretamente. Abortando."
        registrar_etapa "Backend não respondeu corretamente" "ERRO"
        exit 1
    }
} catch {
    log_error "Não foi possível conectar ao backend em http://localhost:8000/docs. Abortando."
    registrar_etapa "Conectividade backend falhou" "ERRO"
    exit 1
}

# Atualizar pip antes de instalar dependências do backend
log_info "Atualizando pip..."
try {
    python -m pip install --upgrade pip
    log_success "pip atualizado com sucesso."
    registrar_etapa "pip atualizado" "OK"
} catch {
    log_error "Falha ao atualizar pip: $_"
    registrar_etapa "Falha ao atualizar pip" "ERRO"
}

# Executar setup do backend e capturar saída/erros
$backendSetupScript = "backend\setup_backend.ps1"
if (Test-Path $backendSetupScript) {
    log_info "Executando setup do backend..."
    try {
        & $backendSetupScript
        if ($LASTEXITCODE -ne 0) {
            log_error "Setup do backend falhou. Interrompendo saneamento."
            registrar_etapa "Setup do backend falhou" "ERRO"
            exit 1
        }
        log_success "Backend validado com sucesso."
        registrar_etapa "Backend validado com sucesso" "OK"
    } catch {
        log_error "Falha ao executar setup do backend: $_"
        registrar_etapa "Falha ao executar setup do backend" "ERRO"
        exit 1
    }
} else {
    log_error "Script de setup do backend não encontrado!"
    registrar_etapa "Script de setup do backend não encontrado" "ERRO"
    exit 1
}

# Rodar testes automatizados do backend
$backendTestScript = "backend\run_tests.ps1"
if (Test-Path $backendTestScript) {
    log_info "Executando testes automatizados do backend..."
    try {
        & $backendTestScript
        if ($LASTEXITCODE -ne 0) {
            log_error "Testes do backend falharam. Interrompendo saneamento."
            registrar_etapa "Testes do backend falharam" "ERRO"
            exit 1
        }
        log_success "Testes do backend passaram com sucesso."
        registrar_etapa "Testes do backend passaram com sucesso" "OK"
    } catch {
        log_error "Falha ao executar testes do backend: $_"
        registrar_etapa "Falha ao executar testes do backend" "ERRO"
        exit 1
    }
} else {
    log_info "Script de testes do backend não encontrado. Prosseguindo..."
    registrar_etapa "Script de testes do backend não encontrado" "INFO"
}

# 6. Build do frontend (executado apenas se backend OK)
log_info "[Checkpoint] Iniciando build do frontend..."
$frontendBuildScript = "frontend\build_frontend.ps1"
if (Test-Path $frontendBuildScript) {
    try {
        & $frontendBuildScript
        if ($LASTEXITCODE -ne 0) {
            log_error "Build do frontend falhou."
            registrar_etapa "Build do frontend falhou" "ERRO"
            exit 1
        }
        log_success "Build do frontend concluído com sucesso."
        registrar_etapa "Build do frontend concluído com sucesso" "OK"
    } catch {
        log_error "Falha ao executar build do frontend: $_"
        registrar_etapa "Falha ao executar build do frontend" "ERRO"
        exit 1
    }
} else {
    log_info "Script de build do frontend não encontrado. Prosseguindo apenas com saneamento."
    registrar_etapa "Script de build do frontend não encontrado" "INFO"
}

# 7. Iniciar backend com Uvicorn robusto (Windows reload exclude)
$uvicornCmd = "uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --reload-exclude='*/node_modules/*' --reload-exclude='*/static/*' --reload-exclude='*/.git/*'"
if ($env:OS -eq "Windows_NT") {
    log_info "Iniciando backend com Uvicorn e reload-exclude para node_modules/static/.git (Windows)..."
    try {
        Start-Process powershell -ArgumentList "-NoProfile", "-Command", $uvicornCmd -WindowStyle Hidden
        log_success "Servidor backend iniciado com exclusão de node_modules/static/.git."
        registrar_etapa "Servidor backend iniciado com reload-exclude" "OK"
    } catch {
        log_error "Falha ao iniciar Uvicorn com reload-exclude: $_"
        registrar_etapa "Falha ao iniciar Uvicorn com reload-exclude" "ERRO"
    }
}

# 8. Resumo final
log_success "Saneamento concluído!"
log_info "Gerando relatório final de saneamento..."
$relatorioPath = "relatorio_saneamento.txt"
$etapas | Out-File -Encoding UTF8 $relatorioPath
log_success "Relatório final salvo em: $relatorioPath"
log_info "Recomendações adicionais:"
log_info "  1. Atualize o README.md com instruções claras de setup"
log_info "  2. Considere usar .gitattributes ou .dockerignore para arquivos temporários"
Write-Host "  3. Revise os scripts de setup e mantenha apenas um por função" -ForegroundColor White
