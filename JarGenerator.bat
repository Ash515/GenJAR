@echo off
REM Navigate to the directory of this batch file
cd /d "%~dp0"

REM Run app.py using the system's Python (must be in PATH)
python app.py

pause
