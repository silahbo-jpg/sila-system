# fix-migration-order-simple.ps1
# A simplified version that handles basic table drop reordering

param(
    [Parameter(Mandatory=$true)]
    [string]$MigrationFile
)

# Define known table dependencies
$dependencies = @{
    "PaymentNotification" = @("Payment")
    "Notification" = @("Payment")
    # Add more dependencies as needed
}

# Read the migration file
$content = Get-Content -Path $MigrationFile -Raw

# Find all drop_table statements
$dropStatements = @()
$lines = $content -split "`n"

foreach ($line in $lines) {
    $trimmed = $line.Trim()
    if ($trimmed -like '*op.drop_table(*') {
        # Extract table name
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
    Write-Host "No drop_table statements found in the migration file."
    exit 0
}

# Sort tables based on dependencies
$sortedTables = @()
$remaining = $dropStatements | ForEach-Object { $_.Table } | Sort-Object -Unique

while ($remaining.Count -gt 0) {
    $added = $false
    foreach ($table in @($remaining)) {
        $deps = if ($dependencies.ContainsKey($table)) { $dependencies[$table] } else { @() }
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

# Create backup
$backupFile = "$MigrationFile.bak"
Copy-Item -Path $MigrationFile -Destination $backupFile -Force

# Rebuild the file with reordered drop statements
$newContent = $content

# Remove all existing drop_table statements
foreach ($stmt in $dropStatements) {
    $escaped = [regex]::Escape($stmt.Line.Trim())
    $newContent = $newContent -replace "$escaped\s*\r?\n?", ""
}

# Find the upgrade function
$upgradeStart = $newContent.IndexOf('def upgrade() -> None:')
$upgradeEnd = $newContent.IndexOf('def downgrade() -> None:', $upgradeStart)
$upgradeContent = $newContent.Substring($upgradeStart, $upgradeEnd - $upgradeStart)

# Find the first non-comment line after the upgrade function start
$insertPos = $upgradeContent.IndexOf('    #') + 1
if ($insertPos -eq 0) { $insertPos = $upgradeContent.IndexOf("`n") + 1 }

# Add the drop statements in the correct order
$dropCode = "    # Tables dropped in dependency order (auto-generated)`n"
$dropCode += $sortedTables | ForEach-Object { "    op.drop_table('$_')" } | Join-String -Separator "`n"

# Insert the new drop statements
$newUpgradeContent = $upgradeContent.Insert($insertPos, "`n$dropCode`n")
$newContent = $newContent.Replace($upgradeContent, $newUpgradeContent)

# Save the updated file
$newContent | Set-Content -Path $MigrationFile -NoNewline

Write-Host "✅ Migration file has been updated with safe drop order."
Write-Host "  Original file backed up to: $backupFile"
Write-Host "  Modified file: $MigrationFile"
Write-Host "`nDrop order:"
$sortedTables | ForEach-Object { Write-Host "  - $_" }
