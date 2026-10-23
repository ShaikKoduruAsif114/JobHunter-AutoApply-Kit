@echo off
title JobHunter AutoApply Engine
cd /d "%~dp0"

echo ============================================================
echo 🚀 STARTING JOBHUNTER AUTOAPPLY PIPELINE
echo ============================================================
echo.

:: Check if profile.json exists
if not exist "config\profile.json" (
    echo Profile not configured yet. Launching setup wizard...
    echo.
    python setup_wizard.py
    if not exist "config\profile.json" (
        echo Setup was cancelled or failed. Exiting.
        pause
        exit /b 1
    )
)

echo Starting application runner...
echo.
python run_batch.py

echo.
echo ============================================================
echo Pipeline session ended. Check Job_Applications_Tracker.xlsx!
echo ============================================================
pause
