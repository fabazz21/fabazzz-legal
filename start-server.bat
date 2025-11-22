@echo off
echo ========================================
echo    AI Drawing to Art Server
echo ========================================
echo.
echo Starting local web server on port 8000
echo Open your browser to: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Try Python 3 first
where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Using Python...
    python -m http.server 8000
    goto :end
)

REM Try Python 2
where python2 >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Using Python 2...
    python2 -m SimpleHTTPServer 8000
    goto :end
)

REM Try PHP
where php >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Using PHP...
    php -S localhost:8000
    goto :end
)

REM Try Node.js
where npx >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Using Node.js...
    npx http-server -p 8000
    goto :end
)

REM No server found
echo ERROR: No suitable server found!
echo.
echo Please install one of the following:
echo   - Python: https://www.python.org/downloads/
echo   - Node.js: https://nodejs.org/
echo   - PHP: https://www.php.net/downloads
echo.
pause
exit /b 1

:end
