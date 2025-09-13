# Simple script to list the project structure
$root = Get-Item .
Write-Host "`nProject Structure for: $($root.FullName)" -ForegroundColor Cyan
Write-Host ("-" * 80)

# Function to get directory size
function Get-DirSize {
    param($path)
    $size = (Get-ChildItem $path -Recurse -File -ErrorAction SilentlyContinue | 
             Measure-Object -Property Length -Sum).Sum
    if ($null -eq $size) { return "0 MB" }
    if ($size -gt 1GB) { return "{0:N2} GB" -f ($size / 1GB) }
    return "{0:N2} MB" -f ($size / 1MB)
}

# List top-level directories
Get-ChildItem -Directory | ForEach-Object {
    $pyFiles = Get-ChildItem -Path $_.FullName -Filter "*.py" -Recurse -File -ErrorAction SilentlyContinue
    $size = Get-DirSize -path $_.FullName
    Write-Host ("{0,-30} {1,10} files {2,10}" -f $_.Name, $pyFiles.Count, $size) -ForegroundColor White
    
    # List first 3 Python files if any
    if ($pyFiles.Count -gt 0) {
        $pyFiles | Select-Object -First 3 | ForEach-Object {
            Write-Host ("  - {0}" -f $_.Name) -ForegroundColor Gray
        }
        if ($pyFiles.Count -gt 3) {
            Write-Host ("  ... and {0} more" -f ($pyFiles.Count - 3)) -ForegroundColor DarkGray
        }
    }
    Write-Host ("-" * 80)
}

# List top-level Python files if any
$topPyFiles = Get-ChildItem -Filter "*.py" -File
if ($topPyFiles.Count -gt 0) {
    Write-Host "`nTop-level Python files:" -ForegroundColor Yellow
    $topPyFiles | ForEach-Object {
        Write-Host ("- {0,-30} {1,10:N0} KB" -f $_.Name, ($_.Length/1KB)) -ForegroundColor White
    }
}
