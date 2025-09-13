#!/usr/bin/env pwsh

<#
.SYNOPSIS
    Fixes the migration order in Alembic migration files to respect foreign key constraints.
.DESCRIPTION
    This script analyzes the database schema and updates the migration files to ensure
    tables are dropped in the correct order to avoid foreign key constraint violations.
.PARAMETER MigrationFile
    Path to the Alembic migration file to fix.
.PARAMETER DbName
    Name of the database to analyze.
.PARAMETER User
    Database username.
.PARAMETER Password
    Database password.

.PARAMETER WhatIf
    Shows what would happen if the script runs without making any changes.
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$MigrationFile,
    
    [string]$Database = "sila_db",
    [string]$DbHost = "localhost",
    [int]$Port = 5432,
    [string]$User = "postgres",
    [string]$Password = "postgres",
    [switch]$WhatIf
)

# Load helper functions
. $PSScriptRoot\db-utils.ps1

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
                    Write-Warning "Ciclo de dependência detectado: $cycle"
                }
            }
        }
    }
    catch {
        Write-Error "Erro ao analisar dependências da tabela $TableName : $_"
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
    
    # Initialize graph and in-degree
    foreach ($table in $Tables) {
        $dependencies = Get-TableDependencies -TableName $table -DbName $DbName
        $dependencyGraph[$table] = $dependencies
        $inDegree[$table] = 0
    }
    
    # Calculate in-degree for each node
    foreach ($table in $Tables) {
        foreach ($dep in $dependencyGraph[$table]) {
            if ($inDegree.ContainsKey($dep)) {
                $inDegree[$dep]++
            }
        }
    }
    
    # Add nodes with zero in-degree to the queue
    foreach ($table in $Tables) {
        if ($inDegree[$table] -eq 0) {
            $queue.Enqueue($table)
        }
    }
    
    # Topological sort
    while ($queue.Count -gt 0) {
        $table = $queue.Dequeue()
        $result += $table
        
        foreach ($dep in $dependencyGraph[$table]) {
            if ($inDegree.ContainsKey($dep)) {
                $inDegree[$dep]--
                if ($inDegree[$dep] -eq 0) {
                    $queue.Enqueue($dep)
                }
            }
        }
    }
    
    if ($result.Count -ne $Tables.Count) {
        Write-Warning "Ciclo detectado no grafo de dependências. A ordem de remoção pode não ser segura."
    }
    
    return $result
}

function Get-TableDependencies {
    param(
        [string]$Database,
        [string]$DbHost,
        [int]$Port,
        [string]$User,
        [string]$Password
    )
    
    $connectionString = "host=$DbHost port=$Port dbname=$Database user=$User password=$Password"
    
    try {
        $conn = New-Object Npgsql.NpgsqlConnection($connectionString)
        $conn.Open()
        
        $command = $conn.CreateCommand()
        $command.CommandText = @"
            SELECT
                tc.table_name,
                ccu.table_name AS referenced_table_name
            FROM
                information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name
                    AND tc.table_schema = kcu.table_schema
                JOIN information_schema.constraint_column_usage AS ccu
                    ON ccu.constraint_name = tc.constraint_name
                    AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY';
"@
        
        $adapter = New-Object Npgsql.NpgsqlDataAdapter($command)
        $dataSet = New-Object System.Data.DataSet
        $adapter.Fill($dataSet) | Out-Null
        
        $dependencies = @{}
        
        foreach ($row in $dataSet.Tables[0].Rows) {
            $table = $row[0]
            $referencedTable = $row[1]
            
            if (-not $dependencies.ContainsKey($table)) {
                $dependencies[$table] = @()
            }
            
            $dependencies[$table] += $referencedTable
        }
        
        return $dependencies
    }
    finally {
        if ($conn -ne $null) {
            $conn.Close()
        }
    }
}

function Update-MigrationFile {
    param(
        [string]$FilePath,
        [hashtable]$Dependencies
    )
    
    Write-Host "🔍 Processing file: $FilePath"
    
    # Read the migration file
    Write-Host "📖 Reading file content..."
    $content = Get-Content -Path $FilePath -Raw
    if (-not $content) {
        Write-Error "Failed to read file content"
        return
    }
    Write-Host "✅ Successfully read file content (length: $($content.Length))"
    
    # Find all drop_table statements
    Write-Host "🔍 Searching for drop_table statements..."
    $dropStatements = @()
    $lines = $content -split "`n"
    Write-Host "  Found $($lines.Count) lines in the file"
    Write-Host "  First 5 lines of the file:"
    $lines[0..4] | ForEach-Object { Write-Host "    | $_" }

    foreach ($line in $lines) {
        $trimmed = $line.Trim()
        if ($trimmed -like '*op.drop_table*') {
            # Extract table name using string operations
            $start = $trimmed.IndexOf('(') + 1
            $end = $trimmed.IndexOf(')', $start)
            if ($start -gt 0 -and $end -gt $start) {
                $table = $trimmed.Substring($start, $end - $start).Trim(" ""'")
                if ($table) {
                    $dropStatements += @{
                        'Line' = $line
                        'Table' = $table
                    }
                }
            }
        }
    }
    
    if ($dropStatements.Count -eq 0) {
        Write-Host "❌ No drop_table statements found in the migration file."
        return
    }
    
    Write-Host "✅ Found $($dropStatements.Count) drop_table statements:"
    $dropStatements | ForEach-Object { Write-Host "  - $($_.Table)" }
    
    # Sort tables based on dependencies
    Write-Host "🔍 Sorting tables based on dependencies..."
    $sortedTables = @()
    $remaining = $dropStatements | ForEach-Object { $_.Table } | Sort-Object -Unique
    
    Write-Host "  Dependencies found:"
    $Dependencies.GetEnumerator() | ForEach-Object {
        Write-Host "    $($_.Key) -> $($_.Value -join ', ')"
    }
    
    while ($remaining.Count -gt 0) {
        $added = $false
        foreach ($table in @($remaining)) {
            $deps = if ($Dependencies.ContainsKey($table)) { $Dependencies[$table] } else { @() }
            $allDepsDropped = $true
            
            foreach ($dep in $deps) {
                if ($remaining -contains $dep) {
                    $allDepsDropped = $false
                    break
                }
            }
            
            if ($allDepsDropped) {
                $sortedTables += $table
                $remaining = $remaining | Where-Object { $_ -ne $table }
                $added = $true
            }
        }
        
        if (-not $added -and $remaining.Count -gt 0) {
            Write-Warning "Circular dependency detected. Remaining tables: $($remaining -join ', ')"
            $sortedTables += $remaining
            break
        }
    }
    
    if ($WhatIf) {
        Write-Host "[WhatIf] Would update $FilePath with the following drop order:"
        $sortedTables | ForEach-Object { Write-Host "  - $_" }
        return
    }
    
    # Create a backup of the original file
    $backupFile = "$FilePath.bak"
    Write-Host "📦 Creating backup at: $backupFile"
    try {
        Copy-Item -Path $FilePath -Destination $backupFile -Force -ErrorAction Stop
        Write-Host "✅ Backup created successfully"
    }
    catch {
        Write-Error "❌ Failed to create backup: $_"
        return
    }
    
    # Rebuild the file with reordered drop statements
    Write-Host "🔧 Rebuilding file with reordered drop statements..."
    $newContent = $content
    
    try {
        # Remove all existing drop_table statements
        Write-Host "  Removing existing drop_table statements..."
        foreach ($stmt in $dropStatements) {
            $escaped = [regex]::Escape($stmt.Line.Trim())
            $newContent = $newContent -replace "$escaped\s*\r?\n?", ""
        }
        
        # Find the upgrade function
        Write-Host "  Locating upgrade function..."
        $upgradeStart = $newContent.IndexOf('def upgrade() -> None:')
        if ($upgradeStart -eq -1) {
            $upgradeStart = $newContent.IndexOf('def upgrade():')
        }
        
        if ($upgradeStart -eq -1) {
            throw "Could not find upgrade function in the migration file."
        }
    
        # Find the end of the upgrade function
        Write-Host "  Locating end of upgrade function..."
        $upgradeEnd = $newContent.IndexOf('def downgrade() -> None:', $upgradeStart)
        if ($upgradeEnd -eq -1) {
            $upgradeEnd = $newContent.IndexOf('def downgrade():', $upgradeStart)
        }
        
        if ($upgradeEnd -eq -1) {
            throw "Could not find downgrade function in the migration file."
        }
        
        $upgradeContent = $newContent.Substring($upgradeStart, $upgradeEnd - $upgradeStart)
        
        # Find the first non-comment line after the upgrade function start
        Write-Host "  Finding insertion point for drop statements..."
        $insertPos = $upgradeContent.IndexOf('    #')
        if ($insertPos -eq -1) { 
            $insertPos = $upgradeContent.IndexOf("`n") 
            if ($insertPos -eq -1) {
                $insertPos = 0
            } else {
                $insertPos += 1  # Move past the newline
            }
        } else {
            # Find the end of the comment block
            $commentEnd = $upgradeContent.IndexOf("`n", $insertPos)
            while ($commentEnd -ne -1 -and $commentEnd -lt $upgradeContent.Length - 1) {
                $nextChar = $upgradeContent.Substring($commentEnd + 1).TrimStart()
                if (-not $nextChar.StartsWith('#')) {
                    break
                }
                $commentEnd = $upgradeContent.IndexOf("`n", $commentEnd + 1)
            }
            $insertPos = $commentEnd + 1
        }
        
        if ($insertPos -le 0) {
            $insertPos = $upgradeContent.IndexOf("`n") + 1
            if ($insertPos -le 0) {
                $insertPos = 0
            }
        }
    
        # Add the drop statements in the correct order
        Write-Host "  Generating drop statements..."
        $dropCode = "    # Tables dropped in dependency order (auto-generated)`n"
        $dropStatements = $sortedTables | ForEach-Object { "    op.drop_table('$_')" }
        $dropCode += $dropStatements -join "`n"
        
        Write-Host "  Inserting drop statements at position $insertPos..."
        $newUpgradeContent = $upgradeContent.Insert($insertPos, "`n$dropCode`n")
        $newContent = $newContent.Replace($upgradeContent, $newUpgradeContent)
        
        # Save the updated file
        Write-Host "  Saving updated file..."
        $newContent | Set-Content -Path $FilePath -NoNewline -Encoding UTF8
        
        Write-Host "✅ Successfully updated migration file with safe drop order."
        Write-Host "  Original file backed up to: $backupFile"
    }
    catch {
        Write-Error "Failed to update migration file: $_"
        Write-Error $_.ScriptStackTrace
        return
    }
    Write-Host "  Modified file: $FilePath"
    Write-Host "`nDrop order:"
    $sortedTables | ForEach-Object { Write-Host "  - $_" }
}

# Main execution
try {
    # Load required assemblies
    $npgsqlPath = Join-Path $PSScriptRoot "..\lib\Npgsql.dll"
    if (Test-Path $npgsqlPath) {
        Add-Type -Path $npgsqlPath
    } else {
        Write-Warning "Npgsql.dll not found at $npgsqlPath. Using default dependencies."
    }
    
    Write-Host "🔍 Analyzing database schema..."
    
    # Get safe drop order
    $safeDropOrder = Get-SafeDropOrder -Tables $tables -DbName $DbName
    
    Write-Host "\n🔧 Safe drop order:"
    $safeDropOrder | ForEach-Object { Write-Host "  - $_" }
    
    # Update the migration file
    if (Test-Path $MigrationFile) {
        Write-Host "\n🔄 Updating migration file: $MigrationFile"
        Update-MigrationFile -FilePath $MigrationFile -SafeDropOrder $safeDropOrder
    } else {
        Write-Error "Migration file not found: $MigrationFile"
        exit 1
    }
    
    Write-Host "\n✅ Migration file has been updated with safe drop order."
    Write-Host "💡 Review the changes and run 'alembic upgrade head' to apply the migration."
}
catch {
    Write-Error "An error occurred: $_"
    exit 1
}
finally {
    # Clean up environment variables
    Remove-Item Env:\PGPASSWORD -ErrorAction SilentlyContinue
    Remove-Item Env:\PGUSER -ErrorAction SilentlyContinue
    Remove-Item Env:\PGHOST -ErrorAction SilentlyContinue
    Remove-Item Env:\PGPORT -ErrorAction SilentlyContinue
    Remove-Item Env:\PGDATABASE -ErrorAction SilentlyContinue
}
