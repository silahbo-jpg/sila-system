@echo off
echo Running SILA System Initialization...
powershell -NoProfile -ExecutionPolicy Bypass -Command "& {Start-Process powershell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File ""%~dp0init_project.ps1""' -Verb RunAs}
pause
