param(
    [string]$ProjectRoot = (Get-Location).Path,
    [switch]$DryRun = $false
)

Write-Host "[INFO] Organizando arquivos Python em $ProjectRoot" -ForegroundColor Cyan

# Mapeamento de padrões de arquivo para pastas de destino
$filePatterns = @{
    # Core modules
    "*core*.py" = "core"
    "*base*.py" = "core"
    
    # API
    "*api*.py" = "api"
    "*route*.py" = "api"
    "*endpoint*.py" = "api"
    
    # Services
    "*service*.py" = "services"
    "*business*.py" = "services"
    "*logic*.py" = "services"
    
    # Models
    "*model*.py" = "models"
    "*schema*.py" = "models"
    "*dto*.py" = "models"
    
    # Tests
    "*test*.py" = "tests"
    "*spec*.py" = "tests"
    
    # Utils
    "*util*.py" = "utils"
    "*helper*.py" = "utils"
    "*tool*.py" = "utils"
}

# Cria as pastas de destino se não existirem
$filePatterns.Values | Select-Object -Unique | ForEach-Object {
    $dir = Join-Path $ProjectRoot $_
    if (-not (Test-Path $dir)) {
        Write-Host "Criando diretório: $dir" -ForegroundColor Yellow
        if (-not $DryRun) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
        }
    }
}

# Processa os arquivos Python na raiz
Get-ChildItem -Path $ProjectRoot -File -Filter "*.py" | ForEach-Object {
    $file = $_
    $moved = $false
    
    foreach ($pattern in $filePatterns.Keys) {
        if ($file.Name -like $pattern) {
            $targetDir = Join-Path $ProjectRoot $filePatterns[$pattern]
            $targetPath = Join-Path $targetDir $file.Name
            
            Write-Host "Movendo $($file.Name) -> $($filePatterns[$pattern])/" -ForegroundColor Green
            
            if (-not $DryRun) {
                try {
                    Move-Item -Path $file.FullName -Destination $targetPath -Force -ErrorAction Stop
                    $moved = $true
                    break
                } catch {
                    Write-Host "Erro ao mover $($file.Name): $_" -ForegroundColor Red
                }
            } else {
                $moved = $true
                break
            }
        }
    }
    
    # Se não encontrou um padrão correspondente, move para a pasta raiz do módulo
    if (-not $moved -and $file.Directory.FullName -ne $ProjectRoot) {
        $targetPath = Join-Path $ProjectRoot $file.Name
        Write-Host "Movendo $($file.Name) para a raiz do módulo" -ForegroundColor Yellow
        
        if (-not $DryRun) {
            try {
                Move-Item -Path $file.FullName -Destination $targetPath -Force -ErrorAction Stop
            } catch {
                Write-Host "Erro ao mover $($file.Name) para a raiz: $_" -ForegroundColor Red
            }
        }
    }
}

Write-Host "[SUCESSO] Organizacao concluida!" -ForegroundColor Green

# Mostra um resumo
Write-Host "\n[RESUMO] Resumo da organizacao:" -ForegroundColor Cyan
Get-ChildItem -Path $ProjectRoot -Directory | 
    Where-Object { $_.Name -in @("core", "api", "services", "models", "tests", "utils") } | 
    ForEach-Object {
        $count = (Get-ChildItem -Path $_.FullName -Filter "*.py" -File -Recurse -ErrorAction SilentlyContinue).Count
        Write-Host "$($_.Name.PadRight(10)): $count arquivos"
    }
