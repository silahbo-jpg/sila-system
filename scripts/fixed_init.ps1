<#
.SYNOPSIS
Creates a new project directory structure with default files.

.DESCRIPTION
This script initializes a project by creating directories and placeholder files.
Supports dry-run mode and force overwrite.

.PARAMETER ProjectRoot
Root directory for the project (default: current directory)

.PARAMETER DryRun
Show planned actions without making changes

.PARAMETER Force
Overwrite existing files

.EXAMPLE
.\init_project.ps1 -DryRun
Shows what would be created

.EXAMPLE
.\init_project.ps1 -Force
Creates structure and overwrites existing files
#>

[CmdletBinding(SupportsShouldProcess=$true)]
param(
    [Parameter(Mandatory=$false, 
               HelpMessage="Project root directory (default: current location)")]
    [ValidateNotNullOrEmpty()]
    [string]$ProjectRoot = $PWD.Path,
    
    [Parameter(Mandatory=$false)]
    [switch]$DryRun,
    
    [Parameter(Mandatory=$false)]
    [switch]$Force
)

# Configure logging
$logDir = Join-Path $ProjectRoot "logs"
$logFile = Join-Path $logDir "project_init_$(Get-Date -Format 'yyyyMMdd-HHmmss').log"

# Initialize log system
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] [$Level] $Message"
    
    if (-not $DryRun) {
        if (-not (Test-Path $logDir)) { New-Item $logDir -ItemType Directory | Out-Null }
        $logEntry | Out-File $logFile -Append -Encoding UTF8
    }
    
    # Color coding for console
    $color = switch ($Level) {
        "INFO"  { "White" }
        "WARN"  { "Yellow" }
        "ERROR" { "Red" }
        default { "Gray" }
    }
    
    Write-Host $logEntry -ForegroundColor $color
}

# Show startup information
Write-Log "Starting project initialization"
Write-Log "Project root: $ProjectRoot"
Write-Log "DryRun mode: $($DryRun.IsPresent)"
Write-Log "Force mode: $($Force.IsPresent)"

# Define directory structure
$directories = @(
    "app/models",
    "app/services",
    "app/core",
    "app/api/v1",
    "app/utils",
    "app/tests",
    "scripts/db",
    "scripts/deploy",
    "scripts/utils",
    "docs",
    "logs"
)

# Define files to create
$files = @{
    "README.md" = "# Project Documentation"
    "config.yml" = "# Configuration settings"
    ".gitignore" = "# Ignore files`n__pycache__/`n.env`n*.log"
    "app/__init__.py" = "# Package initialization"
    "scripts/__init__.py" = "# Scripts package"
}

try {
    # Create directory structure
    Write-Log "Creating directory structure..."
    foreach ($dir in $directories) {
        $fullPath = Join-Path $ProjectRoot $dir
        
        if (Test-Path $fullPath) {
            Write-Log "Directory already exists: $dir" -Level "WARN"
        }
        else {
            if ($DryRun) {
                Write-Log "[DRY RUN] Would create directory: $dir" -Level "INFO"
            }
            else {
                New-Item -Path $fullPath -ItemType Directory -Force | Out-Null
                Write-Log "Created directory: $dir" -Level "INFO"
            }
        }
    }

    # Create files
    Write-Log "Creating standard files..."
    foreach ($file in $files.GetEnumerator()) {
        $filePath = Join-Path $ProjectRoot $file.Key
        $fileDir = Split-Path $filePath -Parent
        
        # Create parent directory if needed
        if (-not (Test-Path $fileDir) -and -not $DryRun) {
            New-Item -Path $fileDir -ItemType Directory -Force | Out-Null
        }

        if (Test-Path $filePath) {
            if ($Force) {
                if ($DryRun) {
                    Write-Log "[DRY RUN] Would overwrite file: $($file.Key)" -Level "INFO"
                }
                else {
                    $file.Value | Out-File $filePath -Encoding UTF8
                    Write-Log "Overwrote file: $($file.Key)" -Level "INFO"
                }
            }
            else {
                Write-Log "File already exists (use -Force to overwrite): $($file.Key)" -Level "WARN"
            }
        }
        else {
            if ($DryRun) {
                Write-Log "[DRY RUN] Would create file: $($file.Key)" -Level "INFO"
            }
            else {
                $file.Value | Out-File $filePath -Encoding UTF8
                Write-Log "Created file: $($file.Key)" -Level "INFO"
            }
        }
    }

    Write-Log "Project initialization completed successfully"
}
catch {
    Write-Log "Error during initialization: $_" -Level "ERROR"
    Write-Log "Stack trace: $($_.ScriptStackTrace)" -Level "ERROR"
    exit 1
}

# Final log location
if (-not $DryRun) {
    Write-Log "Full log available at: $logFile"
}