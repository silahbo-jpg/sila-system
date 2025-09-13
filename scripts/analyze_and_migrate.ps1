# Script to analyze and migrate existing backend files to the new structure
param(
    [string]$BackendRoot = (Join-Path (Get-Location).Parent.FullName "backend"),
    [switch]$DryRun = $true
)

# Import the organization script to ensure the target structure exists
. (Join-Path $PSScriptRoot "organize_backend.ps1") -BackendRoot $BackendRoot

# Define file patterns and their target directories
$filePatterns = @{
    # API Routes
    "*controller*.py" = "app/api/routes"
    "*router*.py" = "app/api/routes"
    "*api*.py" = "app/api/routes"
    
    # Models
    "*model*.py" = "app/models"
    "*schema*.py" = "app/schemas"
    "*dto*.py" = "app/schemas"
    
    # Services
    "*service*.py" = "app/services"
    "*manager*.py" = "app/services"
    "*business*.py" = "app/services"
    
    # Utils
    "*util*.py" = "app/utils"
    "*helper*.py" = "app/utils"
    "*common*.py" = "app/utils"
    
    # Core
    "*config*.py" = "app/core/config"
    "*auth*.py" = "app/core/security"
    "*middleware*.py" = "app/core/middleware"
    "*database*.py" = "app/core"
}

# Find all Python files in the backend directory
$pythonFiles = Get-ChildItem -Path $BackendRoot -Filter "*.py" -Recurse -File |
    Where-Object { $_.FullName -notlike "*\venv\*" -and $_.FullName -notlike "*\scripts\*" }

Write-Host "Found $($pythonFiles.Count) Python files to analyze" -ForegroundColor Cyan

# Track files and their proposed locations
$fileMapping = @()

foreach ($file in $pythonFiles) {
    $relativePath = $file.FullName.Substring($BackendRoot.Length).TrimStart('\')
    $targetDir = $null
    
    # Check if file matches any pattern
    foreach ($pattern in $filePatterns.Keys) {
        if ($file.Name -like $pattern) {
            $targetDir = $filePatterns[$pattern]
            break
        }
    }
    
    # If no pattern matched, put in the root of the app directory
    if (-not $targetDir) {
        $targetDir = "app"
    }
    
    # Skip if already in the target directory
    if ($relativePath.StartsWith($targetDir)) {
        continue
    }
    
    $targetPath = Join-Path $BackendRoot $targetDir $file.Name
    
    $fileMapping += [PSCustomObject]@{
        Source = $relativePath
        Target = "$targetDir\$($file.Name)"
        Action = "Move"
    }
}

# Display the migration plan
Write-Host "`nMigration Plan:" -ForegroundColor Yellow
$fileMapping | Format-Table -AutoSize

# Execute the migration if not in dry run mode
if (-not $DryRun) {
    Write-Host "`nExecuting migration..." -ForegroundColor Cyan
    
    foreach ($mapping in $fileMapping) {
        $sourcePath = Join-Path $BackendRoot $mapping.Source
        $targetPath = Join-Path $BackendRoot $mapping.Target
        $targetDir = Split-Path -Parent $targetPath
        
        # Create target directory if it doesn't exist
        if (-not (Test-Path $targetDir)) {
            New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
        }
        
        # Move the file
        try {
            Move-Item -Path $sourcePath -Destination $targetPath -Force -ErrorAction Stop
            Write-Host "Moved: $($mapping.Source) -> $($mapping.Target)" -ForegroundColor Green
        } catch {
            Write-Host "Error moving $($mapping.Source): $_" -ForegroundColor Red
        }
    }
    
    Write-Host "`nMigration completed!" -ForegroundColor Green
} else {
    Write-Host "`nThis was a dry run. To execute the migration, run the script with -DryRun:$false" -ForegroundColor Yellow
    Write-Host "Example: .\analyze_and_migrate.ps1 -DryRun:`$false" -ForegroundColor Yellow
}

# Generate a report of the new structure
$newStructure = Get-ChildItem -Path (Join-Path $BackendRoot "app") -Recurse -Directory | 
    ForEach-Object {
        $dir = $_.FullName.Substring($BackendRoot.Length).TrimStart('\')
        $fileCount = (Get-ChildItem -Path $_.FullName -Filter "*.py" -File -Recurse -ErrorAction SilentlyContinue).Count
        [PSCustomObject]@{
            Directory = $dir
            PythonFiles = $fileCount
        }
    } | Sort-Object Directory

Write-Host "`nNew Backend Structure:" -ForegroundColor Cyan
$newStructure | Format-Table -AutoSize
