@echo off
REM Auto-detect Python and update batch scripts
REM This script finds Python.exe and configures track_all.bat to use it

setlocal enabledelayedexpansion
cd /d "%~dp0"

echo.
echo ============================================
echo Python Auto-Detector
echo ============================================
echo.
echo Looking for Python installation...
echo.

REM Try common Python installation locations
set "PYTHON_PATH="

REM Check AppData (Microsoft Store or local install)
if exist "%APPDATA%\Python\Python39\python.exe" (
    set "PYTHON_PATH=%APPDATA%\Python\Python39\python.exe"
    goto FOUND
)

if exist "%APPDATA%\Python\Python310\python.exe" (
    set "PYTHON_PATH=%APPDATA%\Python\Python310\python.exe"
    goto FOUND
)

if exist "%APPDATA%\Python\Python311\python.exe" (
    set "PYTHON_PATH=%APPDATA%\Python\Python311\python.exe"
    goto FOUND
)

REM Check Program Files
if exist "C:\Program Files\Python39\python.exe" (
    set "PYTHON_PATH=C:\Program Files\Python39\python.exe"
    goto FOUND
)

if exist "C:\Program Files\Python310\python.exe" (
    set "PYTHON_PATH=C:\Program Files\Python310\python.exe"
    goto FOUND
)

if exist "C:\Program Files\Python311\python.exe" (
    set "PYTHON_PATH=C:\Program Files\Python311\python.exe"
    goto FOUND
)

REM Check Program Files (x86)
if exist "C:\Program Files (x86)\Python39\python.exe" (
    set "PYTHON_PATH=C:\Program Files (x86)\Python39\python.exe"
    goto FOUND
)

if exist "C:\Program Files (x86)\Python310\python.exe" (
    set "PYTHON_PATH=C:\Program Files (x86)\Python310\python.exe"
    goto FOUND
)

if exist "C:\Program Files (x86)\Python311\python.exe" (
    set "PYTHON_PATH=C:\Program Files (x86)\Python311\python.exe"
    goto FOUND
)

REM Check Users directory
for /d %%A in (C:\Users\*) do (
    if exist "%%A\AppData\Local\Programs\Python\Python39\python.exe" (
        set "PYTHON_PATH=%%A\AppData\Local\Programs\Python\Python39\python.exe"
        goto FOUND
    )
    if exist "%%A\AppData\Local\Programs\Python\Python310\python.exe" (
        set "PYTHON_PATH=%%A\AppData\Local\Programs\Python\Python310\python.exe"
        goto FOUND
    )
    if exist "%%A\AppData\Local\Programs\Python\Python311\python.exe" (
        set "PYTHON_PATH=%%A\AppData\Local\Programs\Python\Python311\python.exe"
        goto FOUND
    )
)

goto NOTFOUND

:FOUND
echo ✓ FOUND Python at:
echo   !PYTHON_PATH!
echo.

REM Test it
"!PYTHON_PATH!" --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python found but doesn't work
    goto NOTFOUND
)

echo ✓ Python works!
echo.
echo Updating batch scripts...
echo.

REM Create updated track_all.bat with full path
(
echo @echo off
echo REM Topic Tracker Complete Setup - AUTO-DETECTED PYTHON
echo REM Windows Batch Script
echo.
echo cd /d "%%~dp0"
echo.
echo echo.
echo echo ============================================
echo echo Topic Tracking System - Calcolo Numerico
echo echo ============================================
echo echo.
echo.
echo echo [1/3] Running topic tracker...
echo "!PYTHON_PATH!" topic_tracker.py
echo if errorlevel 1 (
echo     echo ERROR: Topic tracker failed!
echo     pause
echo     exit /b 1
echo ^)
echo.
echo echo.
echo echo [2/3] Generating HTML dashboard...
echo "!PYTHON_PATH!" generate_dashboard.py dashboard.html
echo if errorlevel 1 (
echo     echo ERROR: Dashboard generation failed!
echo     pause
echo     exit /b 1
echo ^)
echo.
echo echo.
echo echo [3/3] Opening dashboard in browser...
echo start dashboard.html
echo.
echo echo.
echo echo ============================================
echo echo ✓ Complete! Dashboard opened in your browser
echo echo ============================================
echo echo.
echo echo Files generated:
echo echo   - topic_status.json (data export^)
echo echo   - dashboard.html (visual dashboard^)
echo echo.
echo pause
) > track_all_auto.bat

echo ✓ Created: track_all_auto.bat
echo.
echo READY! Try now:
echo   Double-click: track_all_auto.bat
echo.
pause
exit /b 0

:NOTFOUND
echo ✗ Python not found in common locations
echo.
echo TRY THIS:
echo 1. Search your computer for "python.exe"
echo 2. Copy the FULL PATH to python.exe
echo 3. Edit this script and add the path below
echo 4. Or add Python to Windows PATH settings
echo.
echo For help, read: FIX_PYTHON_ERROR.txt
echo.
pause
exit /b 1
