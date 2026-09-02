@echo off
cd /d "%~dp0"
echo ===================================================
echo   Formatting Sample Manuscript with ML System...
echo ===================================================
python run.py sample_manuscript.docx formatted_book.docx
echo.
echo Output saved to formatted_book.docx
echo.
pause
