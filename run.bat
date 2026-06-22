@echo off
title Advance Key Generator v2.0
cd /d "%~dp0"
echo ============================================
echo    Advance Key Generator v2.0
echo    Starting application...
echo ============================================
echo.
python main.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to start. Check Python installation.
    echo Make sure dependencies are installed: pip install -r requirements.txt
    echo.
    pause
)
