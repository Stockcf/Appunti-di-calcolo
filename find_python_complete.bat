@echo off
REM Find ALL Python installations on this computer
REM Questo script cerca TUTTI i file python.exe

setlocal enabledelayedexpansion
cd /d "%~dp0"

echo.
echo ============================================
echo Python Path Finder (Ricerca Completa)
echo ============================================
echo.
echo Cercando Python su C:\ ...
echo (questo potrebbe richiedere 30-60 secondi)
echo.

REM Search entire C: drive for python.exe
dir /s /b C:\python.exe 2>nul > python_locations.txt

if %errorlevel% equ 0 (
    echo.
    echo ✓ Trovati i seguenti percorsi Python:
    echo.
    type python_locations.txt
    echo.
    echo ════════════════════════════════════════
    echo.
    echo ISTRUZIONI:
    echo 1. Copia uno dei percorsi sopra (l'intero percorso)
    echo 2. Apri: track_all.bat con un editor di testo
    echo    (destro-click su track_all.bat → Edit)
    echo.
    echo 3. Trova la riga che dice: python topic_tracker.py
    echo.
    echo 4. Sostituisci "python" con il percorso completo
    echo.
    echo ESEMPIO:
    echo   Da: python topic_tracker.py
    echo   A:  C:\Users\ricca\AppData\Local\Programs\Python\Python39\python.exe topic_tracker.py
    echo.
    echo 5. Salva il file
    echo 6. Doppio-click: track_all.bat
    echo.
    echo I risultati sono stati salvati in: python_locations.txt
    echo.
) else (
    echo ✗ Python non trovato con ricerca completa
    echo.
    echo PROVA:
    echo 1. Apri Command Prompt
    echo 2. Digita: py --version
    echo 3. Se vedi un numero di versione, digita: py -c "import sys; print(sys.executable)"
    echo 4. Copia quel percorso e usalo nel track_all.bat
    echo.
)

pause
