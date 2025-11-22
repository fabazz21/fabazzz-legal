@echo off
echo ======================================
echo Installation StreamDiffusion avec IA
echo ======================================
echo.

REM Aller dans le dossier du script
cd /d "%~dp0"

echo [1/8] Verification de l'environnement virtuel...

REM Verifier si venv_sd existe
if not exist "venv_sd" (
    echo Creation de l'environnement virtuel...
    python -m venv venv_sd
    if errorlevel 1 (
        echo ERREUR: Impossible de creer l'environnement virtuel
        pause
        exit /b 1
    )
) else (
    echo Environnement virtuel existe deja
)

echo.
echo [2/8] Activation de l'environnement virtuel...

REM Activer l'environnement virtuel
call venv_sd\Scripts\activate.bat

if errorlevel 1 (
    echo ERREUR: Impossible d'activer l'environnement virtuel
    pause
    exit /b 1
)

echo Environnement virtuel active

echo.
echo [3/8] Mise a jour de pip...
python -m pip install --upgrade pip --quiet

echo.
echo [4/8] Verification de PyTorch...

REM Verifier si PyTorch est installe
python -c "import torch" 2>nul
if errorlevel 1 (
    echo Installation de PyTorch avec CUDA (10 minutes)...
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
    if errorlevel 1 (
        echo ERREUR: Installation de PyTorch echouee
        pause
        exit /b 1
    )
) else (
    echo PyTorch deja installe
)

echo.
echo [5/8] Verification de CUDA...
python -c "import torch; print('CUDA:', torch.cuda.is_available())"

echo.
echo [6/8] Installation de StreamDiffusion...

python -c "import streamdiffusion" 2>nul
if errorlevel 1 (
    echo Installation de StreamDiffusion...
    pip install streamdiffusion --quiet
    if errorlevel 1 (
        echo ERREUR: Installation de StreamDiffusion echouee
        pause
        exit /b 1
    )
) else (
    echo StreamDiffusion deja installe
)

echo.
echo [7/8] Installation de Flask et utilitaires...
pip install flask flask-cors pillow numpy opencv-python --quiet

if errorlevel 1 (
    echo ERREUR: Installation des dependances echouee
    pause
    exit /b 1
)

echo.
echo [8/8] Lancement du serveur...
echo.
echo ======================================
echo Installation terminee avec succes!
echo ======================================
echo.
echo Demarrage du serveur StreamDiffusion...
echo.
echo ATTENTION:
echo - Premiere utilisation = Telechargement modeles IA (2-3 GB)
echo - Cela peut prendre 10-20 minutes
echo - Attendez "Running on http://0.0.0.0:5002"
echo.
echo Ensuite, ouvrez http://localhost:5002
echo.
echo Appuyez sur Ctrl+C pour arreter
echo.
echo ======================================

REM Aller dans backend
cd backend

REM Lancer le serveur
python server_draw2img.py
