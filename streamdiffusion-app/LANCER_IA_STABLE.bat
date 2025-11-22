@echo off
REM Script de lancement version IA (SANS StreamDiffusion)
REM Plus compatible, moins de bugs

echo ======================================
echo Lancement IA Drawing-to-Image
echo Version Stable Diffusion (sans StreamDiffusion)
echo ======================================
echo.

cd /d "%~dp0"

echo Activation de l'environnement virtuel...
call venv_sd\Scripts\activate.bat

echo.
echo Vérification des dépendances...

python -c "import diffusers" 2>nul
if errorlevel 1 (
    echo Installation des dépendances...
    pip install diffusers transformers accelerate flask flask-cors pillow numpy opencv-python --quiet
)

echo.
echo Vérification de PyTorch et CUDA...
python -c "import torch; print('PyTorch:', torch.__version__); print('CUDA:', torch.cuda.is_available())"

echo.
echo ======================================
echo Lancement du serveur IA
echo ======================================
echo.
echo ATTENTION - Première fois:
echo - Téléchargement modèle SD-Turbo (~2 GB)
echo - Peut prendre 10-15 minutes
echo.
echo Ensuite:
echo 1. Ouvrez http://localhost:5002
echo 2. Dessinez sur le canvas
echo 3. Tapez un prompt IA
echo    Exemples:
echo    - anime character, detailed
echo    - photorealistic portrait
echo    - watercolor painting
echo 4. Cliquez 'Apply Style'
echo 5. Regardez la magie!
echo.
echo Note: Génération = 5-10 FPS (plus lent mais ça marche!)
echo.
echo Appuyez sur Ctrl+C pour arrêter
echo.
echo ======================================

cd backend
python server_draw2img_ai.py
