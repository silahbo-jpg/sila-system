# db-utils.ps1
# Funções auxiliares para gerenciamento de banco de dados

function ConvertTo-SecureStringParam {
    param(
        [string]$PlainText,
        [string]$ParameterName
    )
    
    $secureString = ConvertTo-SecureString $PlainText -AsPlainText -Force
    $credential = New-Object System.Management.Automation.PSCredential($ParameterName, $secureString)
    return $credential.GetNetworkCredential().Password
}

function Test-DatabaseConnection {
    param(
        [string]$DbName,
        [string]$User,
        [string]$Password,
        [string]$Server = "localhost",
        [int]$Port = 5432
    )
    
    try {
        $securePassword = ConvertTo-SecureString $Password -AsPlainText -Force
        $env:PGPASSWORD = $Password
        
        $query = "SELECT 1 AS test"
        $result = psql -h $Server -p $Port -U $User -d $DbName -c $query -t
        
        if ($LASTEXITCODE -eq 0) {
            return $true
        }
        return $false
    }
    catch {
        return $false
    }
    finally {
        Remove-Item Env:\PGPASSWORD -ErrorAction SilentlyContinue
    }
}

function Get-DatabaseSize {
    param(
        [string]$DbName,
        [string]$User,
        [string]$Password,
        [string]$Server = "localhost",
        [int]$Port = 5432
    )
    
    try {
        $env:PGPASSWORD = $Password
        $query = @"
        SELECT pg_size_pretty(pg_database_size('$DbName')) as size;
"@
        $result = (psql -h $Server -p $Port -U $User -d $DbName -c $query -t).Trim()
        return $result
    }
    catch {
        Write-Error "Erro ao obter tamanho do banco de dados: $_"
        return $null
    }
    finally {
        Remove-Item Env:\PGPASSWORD -ErrorAction SilentlyContinue
    }
}

function Backup-Database {
    param(
        [string]$DbName,
        [string]$User,
        [string]$Password,
        [string]$BackupPath,
        [string]$Server = "localhost",
        [int]$Port = 5432
    )
    
    try {
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $backupFile = Join-Path $BackupPath "${DbName}_${timestamp}.backup"
        
        Write-Log "💾 Criando backup do banco de dados $DbName..." -Level "INFO"
        
        $env:PGPASSWORD = $Password
        pg_dump -h $Server -p $Port -U $User -F c -b -v -f $backupFile $DbName
        
        if ($LASTEXITCODE -eq 0) {
            Write-Log "✅ Backup criado com sucesso: $backupFile" -Level "SUCCESS"
            return $backupFile
        } else {
            Write-Log "❌ Falha ao criar backup" -Level "ERROR"
            return $null
        }
    }
    catch {
        Write-Log "❌ Erro durante o backup: $_" -Level "ERROR"
        return $null
    }
    finally {
        Remove-Item Env:\PGPASSWORD -ErrorAction SilentlyContinue
    }
}

# Função para listar todas as tabelas do banco de dados
function Get-DatabaseTables {
    param(
        [string]$DbName,
        [string]$User,
        [string]$Password,
        [string]$Server = "localhost",
        [int]$Port = 5432
    )
    
    try {
        $env:PGPASSWORD = $Password
        $query = @"
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE';
"@
        $tables = (psql -h $Server -p $Port -U $User -d $DbName -c $query -t) | 
                 Where-Object { $_.Trim() -ne "" } | 
                 ForEach-Object { $_.Trim() }
        
        return $tables
    }
    catch {
        Write-Error "Erro ao listar tabelas: $_"
        return @()
    }
    finally {
        Remove-Item Env:\PGPASSWORD -ErrorAction SilentlyContinue
    }
}
