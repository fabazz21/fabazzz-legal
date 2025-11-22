@echo off
REM Script de RÉINSTALLATION COMPLÈTE StreamDiffusion
REM Désinstalle tout et réinstalle proprement
REM Exécuter en tant qu'administrateur

echo ==========================================
echo RÉINSTALLATION COMPLÈTE StreamDiffusion
echo ==========================================
echo.
echo Ce script va:
echo 1. Supprimer l'ancien environnement virtuel
echo 2. Désinstaller les packages globaux conflictuels
echo 3. Créer un nouvel environnement propre
echo 4. Installer PyTorch + CUDA
echo 5. Installer StreamDiffusion
echo 6. Lancer l'application
echo.

set /p confirmation="Continuer? (O/N): "
if /i not "%confirmation%"=="O" (
    echo Annulé
    pause
    exit /b
)

REM Aller dans le dossier du script
cd /d "%~dp0"

echo.
echo [1/9] Suppression de l'ancien environnement virtuel...

if exist "venv_sd" (
    rmdir /s /q venv_sd
    echo Ancien venv_sd supprimé
) else (
    echo Pas d'ancien venv_sd
)

echo.
echo [2/9] Désinstallation des packages globaux conflictuels...
pip uninstall streamdiffusion diffusers transformers huggingface_hub accelerate -y 2>nul
echo Packages globaux désinstallés

echo.
echo [3/9] Création du nouvel environnement virtuel...
python -m venv venv_sd

if errorlevel 1 (
    echo ERREUR: Impossible de créer l'environnement virtuel
    pause
    exit /b 1
)

echo Nouvel environnement créé

echo.
echo [4/9] Activation de l'environnement virtuel...
call venv_sd\Scripts\activate.bat

if errorlevel 1 (
    echo ERREUR: Impossible d'activer l'environnement virtuel
    pause
    exit /b 1
)

echo Environnement virtuel activé

echo.
echo [5/9] Mise à jour de pip...
python -m pip install --upgrade pip --quiet

echo.
echo [6/9] Installation de PyTorch avec CUDA...
echo Téléchargement de ~2.5 GB - Patience (5-10 minutes)...

pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

if errorlevel 1 (
    echo Essai avec CUDA 11.8...
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

    if errorlevel 1 (
        echo ERREUR: Installation de PyTorch échouée
        pause
        exit /b 1
    )
)

echo PyTorch installé

echo.
echo [7/9] Vérification de CUDA...
python -c "import torch; print('CUDA:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None')"

echo.
echo [8/9] Installation de StreamDiffusion...
echo Installation en cours (3-5 minutes)...

pip install streamdiffusion

if errorlevel 1 (
    echo Essai depuis GitHub...
    pip install git+https://github.com/cumulo-autumn/StreamDiffusion.git

    if errorlevel 1 (
        echo ERREUR: Installation échouée
        pause
        exit /b 1
    )
)

echo StreamDiffusion installé

echo.
echo Installation de Flask et utilitaires...
pip install flask flask-cors pillow numpy opencv-python --quiet

echo.
echo [9/9] Vérification finale...
python -c "import streamdiffusion; print('OK')" 2>nul

if errorlevel 1 (
    echo ATTENTION: Problème d'import
    python -c "import streamdiffusion"
    pause
    exit /b 1
)

echo StreamDiffusion importé avec succès!

echo.
echo ==========================================
echo INSTALLATION TERMINÉE AVEC SUCCÈS!
echo ==========================================
echo.
echo Résumé:
echo [OK] Environnement virtuel créé
echo [OK] PyTorch avec CUDA installé
echo [OK] StreamDiffusion installé
echo [OK] Toutes les dépendances installées
echo.
echo Démarrage du serveur...
echo.
echo ATTENTION - PREMIÈRE UTILISATION:
echo - Va télécharger les modèles IA (2-3 GB)
echo - Peut prendre 10-20 minutes
echo - Attendez "Running on http://0.0.0.0:5002"
echo.
echo Ensuite:
echo 1. Ouvrez http://localhost:5002
echo 2. Dessinez sur le canvas
echo 3. Tapez un prompt IA
echo 4. Regardez la magie!
echo.
echo Appuyez sur Ctrl+C pour arrêter
echo.
echo ==========================================

REM Aller dans backend
cd backend

REM Lancer le serveur
python server_draw2img.py
