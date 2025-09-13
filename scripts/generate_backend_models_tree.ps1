# Script to generate a directory tree of backend models
# Output will be saved to reports/directory_trees/specific/backend_models_tree.txt

$baseDir = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$outputDir = Join-Path $baseDir "reports\directory_trees\specific"
$outputFile = Join-Path $outputDir "backend_models_tree.txt"

# Create output directory if it doesn't exist
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

# Function to generate tree with proper indentation
function Get-Tree {
    param (
        [string]$path,
        [string]$indent = ""
    )
    
    $item = Get-Item $path -ErrorAction SilentlyContinue
    if (-not $item) { return "" }
    
    $result = $indent + $item.Name
    
    if (Test-Path -Path $path -PathType Container) {
        $result += "\"
        $children = Get-ChildItem -Path $path -ErrorAction SilentlyContinue | Sort-Object Name
        $count = $children.Count
        $i = 0
        
        foreach ($child in $children) {
            $i++
            $isLast = ($i -eq $count)
            $newIndent = $indent + ("    " * (($path.Split('\').Count - 1) - ($baseDir.Split('\').Count - 1)))
            
            if ($isLast) {
                $result += "`n" + (Get-Tree -path $child.FullName -indent "$newIndent└── ")
            }
            else {
                $result += "`n" + (Get-Tree -path $child.FullName -indent "$newIndent├── ")
            }
        }
    }
    
    return $result
}

# Find all model directories under backend
$modelDirs = @(
    (Join-Path $baseDir "backend\app\models"),
    (Join-Path $baseDir "backend\app\db\models"),
    (Get-ChildItem -Path (Join-Path $baseDir "backend\app\modules") -Recurse -Directory -Filter "models" -ErrorAction SilentlyContinue).FullName
)

# Generate tree for each models directory
$output = @()
$output += "BACKEND MODELS DIRECTORY TREE"
$output += "Generated on: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$output += "=" * 80
$output += ""

foreach ($dir in $modelDirs | Sort-Object) {
    if (Test-Path $dir) {
        $relativePath = $dir.Substring($baseDir.Length).TrimStart('\')
        $output += ""
        $output += $relativePath
        $output += ("-" * $relativePath.Length)
        $treeOutput = Get-Tree -path $dir
        if ($treeOutput) {
            $output += $treeOutput
        }
        $output += ""
    }
}

# Save to file
$output -join "`n" | Out-File -FilePath $outputFile -Encoding utf8

Write-Host "Backend models directory tree has been generated and saved to:"
Write-Host $outputFile -ForegroundColor Green
