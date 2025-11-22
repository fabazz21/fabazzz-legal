@echo off
echo ==========================================
echo Test Simple - Version Windows
echo ==========================================
echo.

REM Vérifier si Python existe
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas dans le PATH
    echo.
    echo Essayez avec le lanceur py:
    where py >nul 2>&1
    if %errorlevel% equ 0 (
        echo [OK] Lanceur py trouve - utilisation de py au lieu de python
        set PYTHON_CMD=py
    ) else (
        echo [ERREUR] Ni python ni py ne sont trouves
        echo.
        echo SOLUTIONS:
        echo 1. Redemarrez votre terminal
        echo 2. Redemarrez votre ordinateur
        echo 3. Executez: diagnose_python_windows.bat
        echo 4. Lisez: INSTALLER_PYTHON_WINDOWS_FR.md
        pause
        exit /b 1
    )
) else (
    set PYTHON_CMD=python
)

echo Python trouve: %PYTHON_CMD%
%PYTHON_CMD% --version
echo.

REM Installer les dépendances minimales
echo Installation des dependances minimales...
%PYTHON_CMD% -m pip install flask flask-cors pillow numpy --quiet
if %errorlevel% neq 0 (
    echo [ERREUR] Installation des dependances echouee
    pause
    exit /b 1
)

echo.
echo Demarrage du serveur simple (SANS IA)...
echo.
echo Ouvrez http://localhost:5002 dans votre navigateur
echo.
echo Appuyez sur Ctrl+C pour arreter
echo.

cd backend
%PYTHON_CMD% server_draw2img_simple.py
