# Script to analyze project structure and provide a summary

param(
    [string]$ProjectRoot = (Get-Location).Path
)

function Get-DirectorySize {
    param([string]$path)
    if (Test-Path $path) {
        $size = (Get-ChildItem $path -Recurse -File | Measure-Object -Property Length -Sum).Sum
        if ($null -eq $size) { $size = 0 }
        return [math]::Round($size / 1MB, 2)
    }
    return 0
}

Write-Host "📊 Project Analysis Report" -ForegroundColor Cyan
Write-Host "==========================" -ForegroundColor Cyan

# 1. Basic project info
$projectName = Split-Path -Path $ProjectRoot -Leaf
Write-Host "Project: $projectName" -ForegroundColor Yellow
Write-Host "Location: $ProjectRoot" -ForegroundColor Yellow

# 2. Directory structure
Write-Host "`n📁 Directory Structure:" -ForegroundColor Green
$dirs = Get-ChildItem -Path $ProjectRoot -Directory | Where-Object { 
    $_.Name -notin @('__pycache__', '.git', '.venv', 'venv', 'node_modules', '.idea', '.vscode') 
}

foreach ($dir in $dirs) {
    $pyFiles = Get-ChildItem -Path $dir.FullName -Filter "*.py" -Recurse -File -ErrorAction SilentlyContinue
    $sizeMB = Get-DirectorySize -path $dir.FullName
    Write-Host "- $($dir.Name)/ ($($pyFiles.Count) Python files, $sizeMB MB)" -ForegroundColor White
    
    # Show first level subdirectories
    $subDirs = Get-ChildItem -Path $dir.FullName -Directory -ErrorAction SilentlyContinue | 
               Where-Object { $_.Name -notin @('__pycache__', 'venv', '.venv') }
    
    foreach ($subDir in $subDirs) {
        $subPyFiles = Get-ChildItem -Path $subDir.FullName -Filter "*.py" -Recurse -File -ErrorAction SilentlyContinue
        $subSizeMB = Get-DirectorySize -path $subDir.FullName
        Write-Host "  ├── $($subDir.Name)/ ($($subPyFiles.Count) Python files, $subSizeMB MB)" -ForegroundColor Gray
    }
}

# 3. Python files summary
$allPyFiles = Get-ChildItem -Path $ProjectRoot -Filter "*.py" -Recurse -File -ErrorAction SilentlyContinue
Write-Host "`n🐍 Python Files Summary:" -ForegroundColor Green
Write-Host "Total Python files: $($allPyFiles.Count)" -ForegroundColor White

# 4. Requirements and dependencies
$requirementsFiles = @("requirements.txt", "setup.py", "pyproject.toml") | 
    Where-Object { Test-Path (Join-Path $ProjectRoot $_) }

if ($requirementsFiles.Count -gt 0) {
    Write-Host "`n📦 Dependencies:" -ForegroundColor Green
    foreach ($reqFile in $requirementsFiles) {
        $reqPath = Join-Path $ProjectRoot $reqFile
        Write-Host "- $reqFile" -ForegroundColor White
        if ($reqFile -eq "requirements.txt") {
            $topDeps = Get-Content $reqPath -ErrorAction SilentlyContinue | 
                      Where-Object { $_ -notmatch '^\s*$|^\s*#' } | 
                      Select-Object -First 5
            $topDeps | ForEach-Object { Write-Host "  ├── $_" -ForegroundColor Gray }
            if ((Get-Content $reqPath -ErrorAction SilentlyContinue | Measure-Object -Line).Lines -gt 5) {
                Write-Host "  └── ... and more" -ForegroundColor Gray
            }
        }
    }
}

# 5. Git status (if available)
if (Test-Path (Join-Path $ProjectRoot ".git")) {
    Write-Host "`n🔄 Git Status:" -ForegroundColor Green
    $branch = git -C $ProjectRoot rev-parse --abbrev-ref HEAD 2>$null
    $changes = git -C $ProjectRoot status --porcelain 2>$null
    
    if ($branch) {
        Write-Host "Current branch: $branch" -ForegroundColor White
        if ($changes) {
            $changesCount = ($changes -split "`n").Count
            Write-Host "Uncommitted changes: $changesCount files" -ForegroundColor Yellow
        } else {
            Write-Host "No uncommitted changes" -ForegroundColor Green
        }
    }
}

# 6. Recommendations
Write-Host "`n🔍 Recommendations:" -ForegroundColor Green
$recommendations = @()

# Check for virtual environment
if (-not (Test-Path (Join-Path $ProjectRoot ".venv")) -and -not (Test-Path (Join-Path $ProjectRoot "venv"))) {
    $recommendations += "- Create a virtual environment (python -m venv .venv)"
}

# Check for requirements.txt
if (-not (Test-Path (Join-Path $ProjectRoot "requirements.txt"))) {
    $recommendations += "- Create a requirements.txt file with project dependencies"
}

# Check for README
if (-not (Test-Path (Join-Path $ProjectRoot "README.md"))) {
    $recommendations += "- Create a README.md with project documentation"
}

if ($recommendations.Count -eq 0) {
    Write-Host "- Project structure looks good! No critical issues found." -ForegroundColor Green
} else {
    $recommendations | ForEach-Object { Write-Host $_ -ForegroundColor Yellow }
}

Write-Host "`n✅ Analysis complete!" -ForegroundColor Green
