@echo off
REM SILA Service Testing Automation Pipeline
REM ========================================
REM Batch file version for reliable cross-Windows compatibility

echo.
echo 🚀 SILA Service Testing Pipeline Starting...
echo ============================================================

REM Check if we're in the right directory
if not exist "app\main.py" (
    echo ❌ Error: Not in backend directory. Please run from SILA backend root.
    echo Expected: backend\app\main.py should exist
    pause
    exit /b 1
)

REM Check Python availability
echo.
echo 📋 Checking Environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python not found. Please install Python and add to PATH.
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('python --version') do echo ✅ Python found: %%i
)

REM Check required directories
if not exist "scripts\" (
    echo ❌ Error: Scripts directory not found
    pause
    exit /b 1
)

if not exist "app\modules\" (
    echo ❌ Error: Modules directory not found
    pause
    exit /b 1
)

REM Step 1: Service Discovery
echo.
echo 📋 Step 1: Running Service Discovery...
if not exist "scripts\generate_services_map.py" (
    echo ❌ Error: Service discovery script not found
    pause
    exit /b 1
)

python scripts\generate_services_map.py
if errorlevel 1 (
    echo ❌ Error: Service discovery failed
    pause
    exit /b 1
)

echo ✅ Service discovery completed successfully

REM Step 2: Check for generated files
echo.
echo 📋 Step 2: Validating Generated Files...

if exist "modules_services.json" (
    echo ✅ Service configuration generated: modules_services.json
) else (
    echo ⚠️  Warning: Service configuration file not found
)

if exist "reports\" (
    echo ✅ Reports directory ready
) else (
    echo ⚠️  Warning: Reports directory not found
)

REM Step 3: Service Testing (with server check)
echo.
echo 📋 Step 3: Running Service Tests...

REM Check if server is running (basic check)
curl -s http://localhost:8000/ping >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Server not detected. The test script will handle server verification.
    echo 💡 If tests fail, start server with: python -m uvicorn app.main:app --reload
) else (
    echo ✅ Server appears to be running
)

if not exist "scripts\test_all_services.py" (
    echo ❌ Error: Service testing script not found
    pause
    exit /b 1
)

python scripts\test_all_services.py
set TEST_EXIT_CODE=%errorlevel%

REM Step 4: Results Summary
echo.
echo 📋 Step 4: Processing Results...

if %TEST_EXIT_CODE% equ 0 (
    echo ✅ Service testing completed successfully!
    
    if exist "services_test_report.html" (
        for %%A in ("services_test_report.html") do (
            set /a "size_kb=%%~zA/1024"
        )
        echo 📄 HTML report generated: services_test_report.html
        
        REM Ask if user wants to open the report
        echo.
        set /p "open_report=🌐 Open HTML report in browser? (y/n): "
        if /i "%open_report%"=="y" (
            start "" "services_test_report.html"
            echo ✅ Report opened in default browser
        )
    ) else (
        echo ⚠️  Warning: HTML report not generated
    )
    
    if exist "reports\" (
        dir /b "reports\*.*" 2>nul | find /c /v "" >temp_count.txt
        set /p report_count=<temp_count.txt
        del temp_count.txt 2>nul
        if not "%report_count%"=="0" (
            echo 📊 Additional reports: %report_count% files in reports/
        )
    )
    
) else (
    echo ❌ Service testing failed or incomplete
    echo    Check the output above for error details
)

REM Final Summary
echo.
echo ============================================================
if %TEST_EXIT_CODE% equ 0 (
    echo ✅ SILA Service Testing Pipeline Complete!
) else (
    echo ⚠️  Pipeline completed with issues
)

echo.
echo 💡 Next Steps:
echo    1. Review the generated HTML report for detailed results
echo    2. Update modules_services.json with frontend mappings  
echo    3. Address any failed endpoint tests
echo    4. Integrate working endpoints into frontend applications

echo.
echo 📁 Generated Files:
if exist "modules_services.json" echo    • modules_services.json - Service configuration
if exist "services_test_report.html" echo    • services_test_report.html - Test report
if exist "reports\" echo    • reports/ - Additional analysis files

echo.
echo Pipeline execution completed.
pause