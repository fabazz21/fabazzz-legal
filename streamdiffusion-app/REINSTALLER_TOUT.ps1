# Script de RÉINSTALLATION COMPLÈTE StreamDiffusion
# Désinstalle tout et réinstalle proprement
# Exécuter en tant qu'administrateur

Write-Host "==========================================" -ForegroundColor Red
Write-Host "RÉINSTALLATION COMPLÈTE StreamDiffusion" -ForegroundColor Red
Write-Host "==========================================" -ForegroundColor Red
Write-Host ""
Write-Host "Ce script va:" -ForegroundColor Yellow
Write-Host "1. Supprimer l'ancien environnement virtuel" -ForegroundColor Yellow
Write-Host "2. Désinstaller les packages globaux conflictuels" -ForegroundColor Yellow
Write-Host "3. Créer un nouvel environnement propre" -ForegroundColor Yellow
Write-Host "4. Installer PyTorch + CUDA" -ForegroundColor Yellow
Write-Host "5. Installer StreamDiffusion" -ForegroundColor Yellow
Write-Host "6. Lancer l'application" -ForegroundColor Yellow
Write-Host ""

$confirmation = Read-Host "Continuer? (O/N)"
if ($confirmation -ne 'O' -and $confirmation -ne 'o') {
    Write-Host "Annulé par l'utilisateur" -ForegroundColor Red
    pause
    exit
}

# Obtenir le chemin du script
$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -Path $ScriptPath

Write-Host ""
Write-Host "[1/9] Suppression de l'ancien environnement virtuel..." -ForegroundColor Yellow

if (Test-Path "venv_sd") {
    Remove-Item -Path "venv_sd" -Recurse -Force
    Write-Host "Ancien venv_sd supprimé" -ForegroundColor Green
} else {
    Write-Host "Pas d'ancien venv_sd" -ForegroundColor Green
}

Write-Host ""
Write-Host "[2/9] Désinstallation des packages globaux conflictuels..." -ForegroundColor Yellow
Write-Host "Cela évite les conflits de versions..." -ForegroundColor Gray

# Désinstaller les packages globaux qui causent des problèmes
pip uninstall streamdiffusion diffusers transformers huggingface_hub accelerate -y 2>$null

Write-Host "Packages globaux désinstallés" -ForegroundColor Green

Write-Host ""
Write-Host "[3/9] Création du nouvel environnement virtuel..." -ForegroundColor Yellow

python -m venv venv_sd

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERREUR: Impossible de créer l'environnement virtuel" -ForegroundColor Red
    pause
    exit 1
}

Write-Host "Nouvel environnement créé" -ForegroundColor Green

Write-Host ""
Write-Host "[4/9] Activation de l'environnement virtuel..." -ForegroundColor Yellow

# Modifier la politique d'exécution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force

# Activer l'environnement virtuel
& ".\venv_sd\Scripts\Activate.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERREUR: Impossible d'activer l'environnement virtuel" -ForegroundColor Red
    pause
    exit 1
}

Write-Host "Environnement virtuel activé" -ForegroundColor Green

Write-Host ""
Write-Host "[5/9] Mise à jour de pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

Write-Host ""
Write-Host "[6/9] Installation de PyTorch avec CUDA..." -ForegroundColor Yellow
Write-Host "Téléchargement de ~2.5 GB - Patience (5-10 minutes)..." -ForegroundColor Gray

pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERREUR: Installation de PyTorch échouée" -ForegroundColor Red
    Write-Host "Essai avec CUDA 11.8..." -ForegroundColor Yellow
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERREUR: Installation de PyTorch échouée même avec CUDA 11.8" -ForegroundColor Red
        pause
        exit 1
    }
}

Write-Host "PyTorch installé" -ForegroundColor Green

Write-Host ""
Write-Host "[7/9] Vérification de CUDA..." -ForegroundColor Yellow

$cudaCheck = python -c "import torch; print('CUDA:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None')"
Write-Host $cudaCheck -ForegroundColor Cyan

$cudaAvailable = python -c "import torch; print(torch.cuda.is_available())" 2>$null

if ($cudaAvailable -eq "True") {
    Write-Host "CUDA fonctionne parfaitement!" -ForegroundColor Green
} else {
    Write-Host "ATTENTION: CUDA non disponible, utilisation du CPU (très lent)" -ForegroundColor Red
}

Write-Host ""
Write-Host "[8/9] Installation de StreamDiffusion et dépendances..." -ForegroundColor Yellow
Write-Host "Installation en cours (3-5 minutes)..." -ForegroundColor Gray

pip install streamdiffusion

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERREUR: Installation de StreamDiffusion échouée" -ForegroundColor Red
    Write-Host "Essai avec installation depuis GitHub..." -ForegroundColor Yellow
    pip install git+https://github.com/cumulo-autumn/StreamDiffusion.git

    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERREUR: Installation échouée même depuis GitHub" -ForegroundColor Red
        pause
        exit 1
    }
}

Write-Host "StreamDiffusion installé" -ForegroundColor Green

Write-Host ""
Write-Host "Installation de Flask et utilitaires..." -ForegroundColor Yellow
pip install flask flask-cors pillow numpy opencv-python --quiet

Write-Host ""
Write-Host "[9/9] Vérification finale..." -ForegroundColor Yellow

# Test d'import
$testSD = python -c "import streamdiffusion; print('OK')" 2>$null

if ($testSD -eq "OK") {
    Write-Host "StreamDiffusion importé avec succès!" -ForegroundColor Green
} else {
    Write-Host "ATTENTION: Problème d'import StreamDiffusion" -ForegroundColor Red
    python -c "import streamdiffusion"
    pause
    exit 1
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "INSTALLATION TERMINÉE AVEC SUCCÈS!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Résumé:" -ForegroundColor Cyan
Write-Host "✓ Environnement virtuel créé" -ForegroundColor Green
Write-Host "✓ PyTorch avec CUDA installé" -ForegroundColor Green
Write-Host "✓ StreamDiffusion installé" -ForegroundColor Green
Write-Host "✓ Toutes les dépendances installées" -ForegroundColor Green
Write-Host ""
Write-Host "Démarrage du serveur StreamDiffusion..." -ForegroundColor Cyan
Write-Host ""
Write-Host "ATTENTION - PREMIÈRE UTILISATION:" -ForegroundColor Yellow
Write-Host "- Va télécharger les modèles IA (2-3 GB)" -ForegroundColor Yellow
Write-Host "- Peut prendre 10-20 minutes" -ForegroundColor Yellow
Write-Host "- Attendez 'Running on http://0.0.0.0:5002'" -ForegroundColor Yellow
Write-Host ""
Write-Host "Ensuite:" -ForegroundColor Cyan
Write-Host "1. Ouvrez http://localhost:5002" -ForegroundColor White
Write-Host "2. Dessinez sur le canvas" -ForegroundColor White
Write-Host "3. Tapez un prompt IA (ex: 'anime character')" -ForegroundColor White
Write-Host "4. Regardez la magie opérer!" -ForegroundColor White
Write-Host ""
Write-Host "Appuyez sur Ctrl+C pour arrêter le serveur" -ForegroundColor Gray
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan

# Aller dans le dossier backend
Set-Location -Path "backend"

# Lancer le serveur
python server_draw2img.py
