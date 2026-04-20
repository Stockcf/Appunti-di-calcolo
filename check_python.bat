@echo off
REM Check Python installation
REM This script helps diagnose Python issues

echo ============================================
echo Python Installation Diagnostic
echo ============================================
echo.

echo Checking for Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python not found in PATH
    echo.
    echo SOLUTIONS:
    echo.
    echo Solution 1: Install Python (EASIEST)
    echo ────────────────────────────────────
    echo 1. Go to: https://www.python.org/downloads/
    echo 2. Download Python 3.8 or newer
    echo 3. During installation, CHECK the box:
    echo    "Add Python to PATH"
    echo 4. Click Install
    echo 5. After install, restart Command Prompt
    echo 6. Try running track_all.bat again
    echo.
    echo Solution 2: Use Microsoft Store (Alternative)
    echo ───────────────────────────────────────────
    echo 1. Open: Windows Settings
    echo 2. Go to: Apps ^> Apps and Features
    echo 3. Scroll down and search for Python
    echo 4. Click Install from Microsoft Store
    echo 5. After install, restart Command Prompt
    echo 6. Try running track_all.bat again
    echo.
    echo Solution 3: Find Existing Python
    echo ─────────────────────────────────
    echo If Python is installed but not in PATH:
    echo 1. Find python.exe on your computer
    echo 2. Copy full path (e.g., C:\Python39\python.exe)
    echo 3. Edit track_all.bat and replace "python" with full path
    echo.
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('python --version') do set VERSION=%%i
    echo ✓ Python found: !VERSION!
    echo.
    echo You can now run: track_all.bat
    echo.
    pause
    exit /b 0
)
