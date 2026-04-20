@echo off
REM Topic Tracker Complete Setup - Runs tracker and generates dashboard
REM Windows Batch Script

cd /d "%~dp0"

echo.
echo ============================================
echo Topic Tracking System - Calcolo Numerico
echo ============================================
echo.

REM Check if C:\Users\ricca\AppData\Local\Python\pythoncore-3.14-64\python.exe is available
C:\Users\ricca\AppData\Local\Python\pythoncore-3.14-64\python.exe --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: C:\Users\ricca\AppData\Local\Python\pythoncore-3.14-64\python.exe not found!
    echo.
    echo Your system doesn't have C:\Users\ricca\AppData\Local\Python\pythoncore-3.14-64\python.exe installed or it's not in PATH.
    echo.
    echo QUICK FIX:
    echo 1. Run: check_C:\Users\ricca\AppData\Local\Python\pythoncore-3.14-64\python.exe.bat (in this folder)
    echo 2. Follow the installation instructions
    echo 3. Come back and run this file again
    echo.
    echo OR visit: https://www.C:\Users\ricca\AppData\Local\Python\pythoncore-3.14-64\python.exe.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [1/3] Running topic tracker...
C:\Users\ricca\AppData\Local\Python\pythoncore-3.14-64\python.exe topic_tracker.py
if errorlevel 1 (
    echo.
    echo ERROR: Topic tracker failed!
    echo.
    echo Try running: C:\Users\ricca\AppData\Local\Python\pythoncore-3.14-64\python.exe topic_tracker.py
    echo This will show more detailed error information.
    echo.
    pause
    exit /b 1
)

echo.
echo [2/3] Generating HTML dashboard...
C:\Users\ricca\AppData\Local\Python\pythoncore-3.14-64\python.exe generate_dashboard.py dashboard.html
if errorlevel 1 (
    echo.
    echo ERROR: Dashboard generation failed!
    echo.
    echo But topic_status.json was created successfully.
    echo You can still view it with a text editor.
    echo.
    pause
    exit /b 1
)

echo.
echo [3/3] Opening dashboard in browser...
start dashboard.html

echo.
echo ============================================
echo ✓ Complete! Dashboard opened in your browser
echo ============================================
echo.
echo Files generated:
echo   - topic_status.json (data export)
echo   - dashboard.html (visual dashboard)
echo.
pause
