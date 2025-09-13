@echo off
echo Running SILA System Initialization...
powershell -NoProfile -ExecutionPolicy Bypass -Command "& { .\simple_init.ps1 }"
pause
