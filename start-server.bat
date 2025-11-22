@echo off
echo ========================================
echo    AI Drawing to Art Server
echo ========================================
echo.

REM Check if server.py exists
if not exist "server.py" (
    echo ERROR: server.py not found!
    echo Make sure you're running this from the app directory.
    echo.
    pause
    exit /b 1
)

REM Try Python
where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Starting server with Python...
    echo.
    python server.py
    goto :end
)

REM No Python found
echo ERROR: Python is not installed!
echo.
echo Please install Python from:
echo   https://www.python.org/downloads/
echo.
echo After installation, run this script again.
echo.
pause
exit /b 1

:end
