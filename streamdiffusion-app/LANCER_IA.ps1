# Script d'installation et lancement StreamDiffusion
# Exécuter en tant qu'administrateur

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Installation StreamDiffusion avec IA" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Obtenir le chemin du script
$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path

# Aller dans le dossier streamdiffusion-app
Set-Location -Path $ScriptPath

Write-Host "[1/8] Vérification de l'environnement virtuel..." -ForegroundColor Yellow

# Vérifier si venv_sd existe
if (-not (Test-Path "venv_sd")) {
    Write-Host "Création de l'environnement virtuel..." -ForegroundColor Green
    python -m venv venv_sd
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERREUR: Impossible de créer l'environnement virtuel" -ForegroundColor Red
        pause
        exit 1
    }
} else {
    Write-Host "Environnement virtuel existe déjà" -ForegroundColor Green
}

Write-Host ""
Write-Host "[2/8] Activation de l'environnement virtuel..." -ForegroundColor Yellow

# Modifier la politique d'exécution si nécessaire
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
Write-Host "[3/8] Mise à jour de pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

Write-Host ""
Write-Host "[4/8] Vérification de PyTorch..." -ForegroundColor Yellow

# Vérifier si PyTorch est installé
$torchInstalled = python -c "import torch; print('installed')" 2>$null

if ($torchInstalled -ne "installed") {
    Write-Host "Installation de PyTorch avec CUDA (cela peut prendre 10 minutes)..." -ForegroundColor Green
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERREUR: Installation de PyTorch échouée" -ForegroundColor Red
        pause
        exit 1
    }
} else {
    Write-Host "PyTorch déjà installé" -ForegroundColor Green
}

Write-Host ""
Write-Host "[5/8] Vérification de CUDA..." -ForegroundColor Yellow
$cudaAvailable = python -c "import torch; print(torch.cuda.is_available())" 2>$null

if ($cudaAvailable -eq "True") {
    $gpuName = python -c "import torch; print(torch.cuda.get_device_name(0))" 2>$null
    Write-Host "CUDA disponible: $gpuName" -ForegroundColor Green
} else {
    Write-Host "ATTENTION: CUDA non disponible, utilisation du CPU (lent)" -ForegroundColor Red
}

Write-Host ""
Write-Host "[6/8] Installation de StreamDiffusion..." -ForegroundColor Yellow

$sdInstalled = python -c "import streamdiffusion; print('installed')" 2>$null

if ($sdInstalled -ne "installed") {
    Write-Host "Installation de StreamDiffusion et dépendances..." -ForegroundColor Green
    pip install streamdiffusion --quiet

    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERREUR: Installation de StreamDiffusion échouée" -ForegroundColor Red
        pause
        exit 1
    }
} else {
    Write-Host "StreamDiffusion déjà installé" -ForegroundColor Green
}

Write-Host ""
Write-Host "[7/8] Installation de Flask et utilitaires..." -ForegroundColor Yellow
pip install flask flask-cors pillow numpy opencv-python --quiet

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERREUR: Installation des dépendances échouée" -ForegroundColor Red
    pause
    exit 1
}

Write-Host ""
Write-Host "[8/8] Lancement du serveur..." -ForegroundColor Yellow
Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "Installation terminée avec succès!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "Démarrage du serveur StreamDiffusion..." -ForegroundColor Cyan
Write-Host ""
Write-Host "ATTENTION:" -ForegroundColor Yellow
Write-Host "- Première utilisation = Téléchargement des modèles IA (2-3 GB)" -ForegroundColor Yellow
Write-Host "- Cela peut prendre 10-20 minutes" -ForegroundColor Yellow
Write-Host "- Attendez le message 'Running on http://0.0.0.0:5002'" -ForegroundColor Yellow
Write-Host ""
Write-Host "Ensuite, ouvrez http://localhost:5002 dans votre navigateur" -ForegroundColor Cyan
Write-Host ""
Write-Host "Appuyez sur Ctrl+C pour arrêter le serveur" -ForegroundColor Gray
Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan

# Aller dans le dossier backend
Set-Location -Path "backend"

# Lancer le serveur
python server_draw2img.py
