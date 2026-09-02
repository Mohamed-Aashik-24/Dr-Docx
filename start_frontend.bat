@echo off
title ML DOCX Formatting - Frontend Dev Server
echo ============================================================
echo   Starting Frontend Dev Server on http://localhost:3000
echo   (API proxy -> http://localhost:5000)
echo ============================================================
echo.

cd /d "%~dp0Frontend"

:: Install node modules if needed
if not exist "node_modules" (
    echo Installing dependencies...
    npm install
)

echo Starting Vite dev server...
npm run dev
pause
