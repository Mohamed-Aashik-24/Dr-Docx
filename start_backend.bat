@echo off
title ML DOCX Formatting - Backend API Server
echo ============================================================
echo   Starting Backend API Server on http://localhost:5000
echo ============================================================
echo.

cd /d "%~dp0Backend"

:: Install dependencies if needed
pip install flask flask-cors python-docx scikit-learn numpy scipy joblib Pillow >nul 2>&1

echo Starting Flask server...
python api.py
pause
