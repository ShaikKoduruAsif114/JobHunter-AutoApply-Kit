@echo off
title JobHunter AutoApply - One-Click Installer
echo ============================================================
echo 🚀 JOBHUNTER AUTOAPPLY - ONE-CLICK INSTALLER
echo ============================================================
echo.

:: Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please download and install Python 3.10+ from https://www.python.org/
    echo (Make sure to check "Add Python to PATH" during installation)
    echo.
    pause
    exit /b 1
)

echo [1/3] Python detected!
python --version
echo.

echo [2/3] Installing required Python packages...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install requirements.
    pause
    exit /b 1
)
echo.

echo [3/3] Installing Playwright Chromium browser binary...
python -m playwright install chromium
if %errorlevel% neq 0 (
    echo [WARNING] Playwright browser install had a notice, but continuing...
)

echo.
echo ============================================================
echo 🎉 INSTALLATION COMPLETE!
echo ============================================================
echo Next step:
echo 1. Put your resume PDF in the 'resumes/' folder.
echo 2. Double-click 'start.bat' to configure your profile and start applying!
echo ============================================================
echo.
pause
