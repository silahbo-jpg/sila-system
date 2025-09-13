# fix_database_urls.ps1
# Corrige URLs de conexão do banco de dados em arquivos do projeto

$sila_dev-system = "C:\Users\User5\Music\MEGA1\sila_dev\sila_dev-system"

# URLs corretas
$correctDevURL  = "sila_dev-systemql://sila_dev-system:Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*@localhost:5432/sila_dev_dev?schema=public"
$correctTestURL = "sila_dev-systemql://sila_dev-system:Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*@localhost:5432/sila_dev_test?schema=public"

# Procurar arquivos relevantes
Get-ChildItem -Path $sila_dev-system -Recurse -Include *.env,*.py,*.ts,*.js,*.yml | ForEach-Object {
    $file = $_.FullName

    # Ler conteúdo e substituir URLs incorretas
    $newContent = Get-Content $file | ForEach-Object {
        $_ -replace "sila_dev-systemql://[^'""\s]+", {
            if ($_ -match "sila_dev_test") { 
                $correctTestURL 
            } else { 
                $correctDevURL 
            }
        }
    }

    # Salvar alterações
    $newContent | Set-Content -Encoding UTF8 $file

    # Feedback
    Write-Host "✅ Corrigido: $file" -ForegroundColor Green
}


