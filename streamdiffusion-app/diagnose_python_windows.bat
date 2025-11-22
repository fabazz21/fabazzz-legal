@echo off
echo ==========================================
echo Diagnostic Python pour Windows
echo ==========================================
echo.

REM Test 1: Python dans le PATH
echo [Test 1] Python est-il dans le PATH?
echo.
where python
if %errorlevel% equ 0 (
    echo [OK] Python trouve dans le PATH
    python --version
) else (
    echo [ERREUR] Python NON trouve dans le PATH
)

echo.
echo ==========================================
echo.

REM Test 2: Python3
echo [Test 2] Python3?
echo.
where python3
if %errorlevel% equ 0 (
    echo [OK] Python3 trouve
    python3 --version
) else (
    echo [ERREUR] Python3 non trouve
)

echo.
echo ==========================================
echo.

REM Test 3: py launcher
echo [Test 3] Lanceur py?
echo.
where py
if %errorlevel% equ 0 (
    echo [OK] Lanceur py trouve
    py --version
) else (
    echo [ERREUR] Lanceur py non trouve
)

echo.
echo ==========================================
echo.

REM Test 4: Recherche dans les emplacements communs
echo [Test 4] Recherche Python dans les emplacements standards...
echo.

set FOUND=0

if exist "C:\Python311\python.exe" (
    echo [TROUVE] C:\Python311\python.exe
    C:\Python311\python.exe --version
    set FOUND=1
)

if exist "C:\Python310\python.exe" (
    echo [TROUVE] C:\Python310\python.exe
    C:\Python310\python.exe --version
    set FOUND=1
)

if exist "C:\Python312\python.exe" (
    echo [TROUVE] C:\Python312\python.exe
    C:\Python312\python.exe --version
    set FOUND=1
)

if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    echo [TROUVE] %LOCALAPPDATA%\Programs\Python\Python311\python.exe
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" --version
    set FOUND=1
)

if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" (
    echo [TROUVE] %LOCALAPPDATA%\Programs\Python\Python310\python.exe
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" --version
    set FOUND=1
)

if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    echo [TROUVE] %LOCALAPPDATA%\Programs\Python\Python312\python.exe
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" --version
    set FOUND=1
)

if %FOUND% equ 0 (
    echo [AUCUN] Python non trouve dans les emplacements standards
)

echo.
echo ==========================================
echo.

REM Test 5: PATH actuel
echo [Test 5] Contenu du PATH:
echo.
echo %PATH%

echo.
echo ==========================================
echo RESUME
echo ==========================================
echo.
echo Si Python est trouve mais pas dans le PATH:
echo   1. Notez le chemin complet affiche ci-dessus
echo   2. Executez: fix_python_path.bat [chemin]
echo.
echo Si Python n'est PAS trouve:
echo   1. Reinstallez Python depuis python.org
echo   2. COCHEZ "Add Python to PATH"
echo   3. Redemarrez votre ordinateur
echo.
pause
