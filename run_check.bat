@echo off
echo Running SILA System Structure Check...
powershell -NoProfile -ExecutionPolicy Bypass -Command "& {Start-Process powershell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File ""%~dp0check_structure.ps1""' -Verb RunAs}
pause
