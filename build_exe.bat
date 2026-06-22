@echo off
title Building Advance Key Generator EXE
cd /d "%~dp0"
echo ============================================
echo    Building EXE with PyInstaller
echo ============================================
echo.

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Building EXE (this may take a few minutes)...
pyinstaller ^
    --onefile ^
    --windowed ^
    --name "AdvanceKeyGen" ^
    --icon NONE ^
    --add-data "hardware.py;." ^
    --add-data "keygen.py;." ^
    --add-data "sms.py;." ^
    --add-data "ui.py;." ^
    --hidden-import wmi ^
    --hidden-import customtkinter ^
    --hidden-import pyperclip ^
    --hidden-import requests ^
    main.py

echo.
if exist "dist\AdvanceKeyGen.exe" (
    echo ============================================
    echo    SUCCESS! EXE created at:
    echo    dist\AdvanceKeyGen.exe
    echo ============================================
    echo.
    echo File size:
    dir "dist\AdvanceKeyGen.exe"
) else (
    echo [ERROR] Build failed. Check errors above.
)

pause
