# Create target directories if they don't exist
$targetDirs = @("core", "api", "services", "models", "tests", "utils")
foreach ($dir in $targetDirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
    }
}

# Move files based on patterns
$movedFiles = @()

# Core files
$coreFiles = Get-ChildItem -Path . -File -Filter "*core*.py" -Exclude "*test*"
foreach ($file in $coreFiles) {
    $target = Join-Path "core" $file.Name
    Move-Item -Path $file.FullName -Destination $target -Force
    $movedFiles += $file.Name
}

# API files
$apiFiles = Get-ChildItem -Path . -File -Filter "*api*.py" -Exclude "*test*"
foreach ($file in $apiFiles) {
    $target = Join-Path "api" $file.Name
    Move-Item -Path $file.FullName -Destination $target -Force
    $movedFiles += $file.Name
}

# Service files
$serviceFiles = Get-ChildItem -Path . -File -Filter "*service*.py" -Exclude "*test*"
foreach ($file in $serviceFiles) {
    $target = Join-Path "services" $file.Name
    Move-Item -Path $file.FullName -Destination $target -Force
    $movedFiles += $file.Name
}

# Model files
$modelFiles = Get-ChildItem -Path . -File -Filter "*model*.py" -Exclude "*test*"
foreach ($file in $modelFiles) {
    $target = Join-Path "models" $file.Name
    Move-Item -Path $file.FullName -Destination $target -Force
    $movedFiles += $file.Name
}

# Test files
$testFiles = Get-ChildItem -Path . -File -Filter "*test*.py"
foreach ($file in $testFiles) {
    $target = Join-Path "tests" $file.Name
    Move-Item -Path $file.FullName -Destination $target -Force
    $movedFiles += $file.Name
}

# Utils files
$utilFiles = Get-ChildItem -Path . -File -Filter "*util*.py" -Exclude "*test*"
foreach ($file in $utilFiles) {
    $target = Join-Path "utils" $file.Name
    Move-Item -Path $file.FullName -Destination $target -Force
    $movedFiles += $file.Name
}

# Show summary
Write-Host "Moved $($movedFiles.Count) files:"
$movedFiles | ForEach-Object { Write-Host "- $_" }

# Show remaining Python files
$remaining = Get-ChildItem -Path . -File -Filter "*.py" -Recurse | Where-Object { $_.DirectoryName -ne $PWD.Path }
Write-Host "`nRemaining Python files in root:"
$remaining | Select-Object Name | Format-Table -AutoSize
