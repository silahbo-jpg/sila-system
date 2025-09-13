# Backend-Tests.ps1 - SILA Backend Test Runner
# Executes backend tests with database setup, coverage, and logging

# ─── Encoding & Error Preferences ─────────────────────────────────────────────
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['*:Encoding'] = 'utf8'
$ErrorActionPreference = "Stop"

# ─── Configuration ────────────────────────────────────────────────────────────
$config = @{
    TestDatabase  = "sila_test"
    TestUser      = "postgres"
    TestPassword  = "Truman1*"
    TestHost      = "localhost"
    TestPort      = "5432"
}

# ─── Environment Variables ────────────────────────────────────────────────────
$env:ENV                          = 'test'
$env:ENVIRONMENT                  = 'test'
$env:DATABASE_URL                = "postgresql://$($config.TestUser):$($config.TestPassword)@$($config.TestHost):$($config.TestPort)/$($config.TestDatabase)"
$env:SECRET_KEY                  = 'test_secret_key_that_is_at_least_32_chars'
$env:FIRST_SUPERUSER_EMAIL      = 'admin@example.com'
$env:FIRST_SUPERUSER_PASSWORD   = 'admin123'
$env:ACCESS_TOKEN_EXPIRE_MINUTES = '30'

# ─── Helper Function ──────────────────────────────────────────────────────────
function Invoke-TestCommand {
    param (
        [string]$Command,
        [string[]]$Arguments,
        [string]$WorkingDir = $PSScriptRoot
    )

    $stdout = "output_$([Guid]::NewGuid().ToString()).txt"
    $stderr = "error_$([Guid]::NewGuid().ToString()).txt"

    $processInfo = @{
        FilePath              = $Command
        ArgumentList          = $Arguments
        WorkingDirectory      = $WorkingDir
        NoNewWindow           = $true
        PassThru              = $true
        RedirectStandardOutput = $stdout
        RedirectStandardError  = $stderr
    }

    try {
        $process = Start-Process @processInfo
        $process.WaitForExit()

        if (Test-Path $stdout) {
            Get-Content $stdout | ForEach-Object { Write-Verbose $_ -Verbose }
            Remove-Item $stdout -Force -ErrorAction SilentlyContinue
        }

        if (Test-Path $stderr) {
            Get-Content $stderr | ForEach-Object { Write-Warning $_ }
            Remove-Item $stderr -Force -ErrorAction SilentlyContinue
        }

        if ($process.ExitCode -ne 0) {
            throw "Command failed with exit code $($process.ExitCode)"
        }

        return $process.ExitCode
    }
    catch {
        Write-Error "❌ Error executing command: $_"
        throw
    }
}

# ─── Execution ────────────────────────────────────────────────────────────────
try {
    Set-Location $PSScriptRoot

    Write-Host "`n🛠️  Generating Prisma client..." -ForegroundColor Cyan
    Invoke-TestCommand -Command "npx" -Arguments @("prisma", "generate")

    Write-Host "🔄 Running database migrations..." -ForegroundColor Cyan
    Invoke-TestCommand -Command "npx" -Arguments @("prisma", "migrate", "deploy", "--schema=prisma/schema.prisma")

    Write-Host "🧪 Running tests with coverage..." -ForegroundColor Cyan
    $testArgs = @(
        "-m", "pytest",
        "--cov=app",
        "--cov-report=term-missing",
        "--cov-report=html",
        "--cov-fail-under=10",
        "-v"
    )

    $testExitCode = Invoke-TestCommand -Command "python" -Arguments $testArgs

    if ($testExitCode -eq 0) {
        $coveragePath = Join-Path $PSScriptRoot "htmlcov/index.html"
        if (Test-Path $coveragePath) {
            Write-Host "`n📊 Coverage report generated at: $coveragePath" -ForegroundColor Green
            Start-Process $coveragePath
        }
    }

    exit $testExitCode
}
catch {
    Write-Host "`n❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.ScriptStackTrace) {
        Write-Host "`n📌 Stack Trace:" -ForegroundColor DarkGray
        Write-Host $_.ScriptStackTrace -ForegroundColor DarkGray
    }
    exit 1
}
finally {
    Set-Location $PSScriptRoot
}

