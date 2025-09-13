@echo off
REM finalize_project_cleanup.bat
REM Windows batch file to run the SILA System final project cleanup

TITLE SILA System Final Project Cleanup

echo ============================================================
echo 🧼 SILA SYSTEM FINAL PROJECT CLEANUP
echo ============================================================
echo This will perform a comprehensive cleanup of the project.
echo.

REM Check if we're in the right directory
if not exist "scripts" (
    echo ❌ Error: 'scripts' directory not found.
    echo Please run this script from the project root directory.
    echo.
    pause
    exit /b 1
)

if not exist "backend" (
    echo ❌ Error: 'backend' directory not found.
    echo Please run this script from the project root directory.
    echo.
    pause
    exit /b 1
)

echo ✅ Project directory structure verified.
echo.

REM Ask for confirmation
echo This process will:
echo   • Remove obsolete SQLAlchemy/SQLite references
echo   • Audit tests and migration scripts
echo   • Execute correction and structure scripts
echo   • Review dependencies
echo   • Perform final restructuring
echo   • Validate and close the project
echo.
echo Reports will be generated in the 'reports' directory.
echo.

choice /C YN /M "Do you want to continue with the cleanup"
if errorlevel 2 (
    echo Cleanup cancelled by user.
    pause
    exit /b 0
)

echo.
echo 🚀 Starting cleanup process...
echo.

REM Run the PowerShell cleanup script
powershell -ExecutionPolicy Bypass -File "scripts\finalize_project_cleanup.ps1" -SkipConfirmation

if %errorlevel% equ 0 (
    echo.
    echo 🎉 Cleanup process completed successfully!
    echo.
    echo The project is now clean, stable, and ready for delivery or archiving.
) else (
    echo.
    echo ⚠️  Cleanup process completed with issues.
    echo.
    echo Please review the output above and check the reports directory.
)

echo.
echo Press any key to exit...
pause >nul
exit /b %errorlevel%