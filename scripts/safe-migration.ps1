#!/usr/bin/env pwsh

# safe-migration.ps1
# Gerencia migrações de banco de dados de forma segura, respeitando constraints de chave estrangeira
# Uso: .\safe-migration.ps1 [--action=migrate|rollback|reset|analyze] [--revision=revision_id] [--tables=table1,table2]

# Carrega funções auxiliares
. $PSScriptRoot\db-utils.ps1

param(
    [ValidateSet('migrate', 'rollback', 'reset', 'analyze')]
    [string]$Action = "migrate",
    [string]$Revision = "head",
    [string]$DbName = "sila_db",
    [string]$User = "postgres",
    [string]$Password = "postgres",
    [string]$Host = "localhost",
    [int]$Port = 5432,
    [string]$Tables = ""
)

$BasePath = $PSScriptRoot | Split-Path -Parent
$LogPath = Join-Path $BasePath "reports\setup\migration-$(Get-Date -Format 'yyyyMMdd-HHmmss').log"

# Criar diretório de logs se não existir
New-Item -ItemType Directory -Path (Split-Path $LogPath -Parent) -Force | Out-Null

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "[$timestamp] [$Level] $Message" | Tee-Object -FilePath $LogPath -Append
}

function Get-TableDependencies {
    param(
        [string]$TableName,
        [string]$DbName,
        [hashtable]$Visited = @{},
        [array]$Path = @()
    )
    
    if ($Visited.ContainsKey($TableName)) {
        return @()
    }
    
    $Visited[$TableName] = $true
    $Path += $TableName
    
    $query = @"
    SELECT 
        tc.table_name AS dependent_table,
        kcu.column_name AS dependent_column,
        ccu.table_name AS referenced_table,
        ccu.column_name AS referenced_column
    FROM 
        information_schema.table_constraints AS tc 
        JOIN information_schema.key_column_usage AS kcu
          ON tc.constraint_name = kcu.constraint_name
          AND tc.table_schema = kcu.table_schema
        JOIN information_schema.constraint_column_usage AS ccu
          ON ccu.constraint_name = tc.constraint_name
          AND ccu.table_schema = tc.table_schema
    WHERE 
        tc.constraint_type = 'FOREIGN KEY' 
        AND ccu.table_name = '$TableName';
"@
    
    $dependencies = @()
    
    try {
        $results = psql -d $DbName -c $query -t
        
        foreach ($line in $results -split "`r`n" | Where-Object { $_.Trim() -ne "" }) {
            $parts = $line -split '\|' | ForEach-Object { $_.Trim() }
            if ($parts.Count -ge 2) {
                $dependentTable = $parts[0]
                if (-not $Visited.ContainsKey($dependentTable)) {
                    $dependencies += $dependentTable
                    $dependencies += Get-TableDependencies -TableName $dependentTable -DbName $DbName -Visited $Visited -Path $Path
                } elseif ($Path -contains $dependentTable) {
                    $cycle = ($Path + $dependentTable) -join ' -> '
                    Write-Log "⚠️ Ciclo de dependência detectado: $cycle" -Level "WARNING"
                }
            }
        }
    }
    catch {
        Write-Log "❌ Erro ao analisar dependências da tabela $TableName : $_" -Level "ERROR"
    }
    
    return $dependencies | Select-Object -Unique
}

function Get-SafeDropOrder {
    param(
        [string[]]$Tables,
        [string]$DbName
    )
    
    $dependencyGraph = @{}
    $inDegree = @{}
    $queue = [System.Collections.Queue]::new()
    $result = @()
    
    # Inicializa o grafo e o grau de entrada
    foreach ($table in $Tables) {
        $dependencies = Get-TableDependencies -TableName $table -DbName $DbName
        $dependencyGraph[$table] = $dependencies
        $inDegree[$table] = 0
    }
    
    # Calcula o grau de entrada de cada nó
    foreach ($table in $Tables) {
        foreach ($dep in $dependencyGraph[$table]) {
            $inDegree[$dep]++
        }
    }
    
    # Adiciona nós com grau de entrada zero à fila
    foreach ($table in $Tables) {
        if ($inDegree[$table] -eq 0) {
            $queue.Enqueue($table)
        }
    }
    
    # Ordenação topológica
    while ($queue.Count -gt 0) {
        $table = $queue.Dequeue()
        $result += $table
        
        foreach ($dep in $dependencyGraph[$table]) {
            $inDegree[$dep]--
            if ($inDegree[$dep] -eq 0) {
                $queue.Enqueue($dep)
            }
        }
    }
    
    if ($result.Count -ne $Tables.Count) {
        Write-Log "⚠️ Ciclo detectado no grafo de dependências. A ordem de remoção pode não ser segura." -Level "WARNING"
    }
    
    return $result
}

function Invoke-SafeMigration {
    param(
        [string]$Action,
        [string]$Revision = "head",
        [string]$Tables = ""
    )

    $env:PGPASSWORD = $Password
    $env:PGUSER = $User
    $env:PGHOST = $Host
    $env:PGPORT = $Port
    $env:PGDATABASE = $DbName

    Write-Log "🚀 Iniciando migração segura" -Level "INFO"
    Write-Log "Ação: $Action" -Level "INFO"
    Write-Log "Revisão: $Revision" -Level "INFO"

    try {
        # Verificar se o banco de dados existe
        $dbExists = psql -lqt | Select-String -Pattern "\b$DbName\b"
        
        if (-not $dbExists) {
            Write-Log "⚠️ Banco de dados '$DbName' não encontrado. Criando..." -Level "WARNING"
            createdb -U $User -h $Host -p $Port $DbName
            Write-Log "✅ Banco de dados criado com sucesso" -Level "SUCCESS"
        }

        # Navegar para o diretório do backend para executar o Alembic
        Push-Location (Join-Path $BasePath "backend")

        # Verificar se o Alembic está configurado
        if (-not (Test-Path "alembic.ini")) {
            Write-Log "❌ Arquivo alembic.ini não encontrado" -Level "ERROR"
            Write-Log "💡 Execute 'alembic init alembic' para configurar o Alembic" -Level "INFO"
            return
        }

        # Executar a ação solicitada
        switch ($Action.ToLower()) {
            "migrate" {
                Write-Log "🔄 Aplicando migrações..." -Level "INFO"
                alembic upgrade $Revision
                Write-Log "✅ Migração concluída com sucesso" -Level "SUCCESS"
            }
            "rollback" {
                Write-Log "⏪ Revertendo para a revisão: $Revision" -Level "INFO"
                alembic downgrade $Revision
                Write-Log "✅ Rollback concluído com sucesso" -Level "SUCCESS"
            }
            "reset" {
                Write-Log "🔄 Resetando banco de dados..." -Level "WARNING"
                
                # Obter todas as migrações
                $revisions = alembic history -r "base:head" --verbose
                
                # Reverter todas as migrações
                if ($revisions) {
                    Write-Log "⏪ Revertendo todas as migrações..." -Level "INFO"
                    alembic downgrade base
                }
                
                # Aplicar todas as migrações
                Write-Log "🔄 Aplicando migrações mais recentes..." -Level "INFO"
                alembic upgrade head
                
                Write-Log "✅ Reset do banco de dados concluído com sucesso" -Level "SUCCESS"
            }
            "analyze" {
                if ([string]::IsNullOrEmpty($Tables)) {
                    Write-Log "ℹ️ Analisando todas as tabelas..." -Level "INFO"
                    $tablesQuery = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE'"
                    $tables = (psql -d $DbName -c $tablesQuery -t) | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
                } else {
                    $tables = $Tables -split ',' | ForEach-Object { $_.Trim() }
                }
                
                Write-Log "🔍 Analisando dependências para $($tables.Count) tabelas..." -Level "INFO"
                
                $dependencyGraph = @{}
                
                foreach ($table in $tables) {
                    $dependencies = Get-TableDependencies -TableName $table -DbName $DbName
                    $dependencyGraph[$table] = $dependencies
                    
                    if ($dependencies.Count -gt 0) {
                        Write-Log "📋 Tabela: $table" -Level "INFO"
                        $dependencies | ForEach-Object { 
                            Write-Log "   ↓ Depende de: $_" -Level "INFO"
                        }
                    } else {
                        Write-Log "📋 Tabela: $table (sem dependências)" -Level "INFO"
                    }
                }
                
                # Mostrar ordem segura para remoção
                $safeOrder = Get-SafeDropOrder -Tables $tables -DbName $DbName
                Write-Log "\n🔧 Ordem segura para remoção de tabelas:" -Level "INFO"
                for ($i = 0; $i -lt $safeOrder.Count; $i++) {
                    Write-Log "$($i + 1). $($safeOrder[$i])" -Level "INFO"
                }
                
                Write-Log "\n💡 Dica: Use esta ordem ao criar migrações que envolvam remoção de tabelas" -Level "INFO"
            }
            default {
                Write-Log "❌ Ação inválida: $Action" -Level "ERROR"
                Write-Log "💡 Ações disponíveis: migrate, rollback, reset" -Level "INFO"
            }
        }
    }
    catch {
        Write-Log "❌ Erro durante a migração: $_" -Level "ERROR"
        Write-Log "📄 Consulte o arquivo de log para mais detalhes: $LogPath" -Level "ERROR"
        throw $_.Exception
    }
    finally {
        # Limpar variáveis de ambiente
        Remove-Item Env:\PGPASSWORD -ErrorAction SilentlyContinue
        Remove-Item Env:\PGUSER -ErrorAction SilentlyContinue
        Remove-Item Env:\PGHOST -ErrorAction SilentlyContinue
        Remove-Item Env:\PGPORT -ErrorAction SilentlyContinue
        Remove-Item Env:\PGDATABASE -ErrorAction SilentlyContinue
        
        # Voltar para o diretório original
        Pop-Location
        
        Write-Log "🏁 Migração finalizada" -Level "INFO"
    }
}

# Executar a migração segura
try {
    Invoke-SafeMigration -Action $Action -Revision $Revision -Tables $Tables
}
catch {
    exit 1
}
