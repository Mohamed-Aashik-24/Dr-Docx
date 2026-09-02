@echo off
cd /d "%~dp0"
echo ===================================================
echo   Intelligent ML-Based Offline Book Formatter GUI
echo ===================================================
python -m src.gui
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo An error occurred while launching GUI.
    pause
)
