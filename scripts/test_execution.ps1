param(
    [string]$TestParam = "default value"
)

Write-Host "=== Test Script ==="
Write-Host "Current directory: $(Get-Location)"
Write-Host "Test parameter: $TestParam"
Write-Host "Script is running!"
