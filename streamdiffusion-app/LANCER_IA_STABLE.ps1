# Script de lancement version IA (SANS StreamDiffusion)
# Plus compatible, moins de bugs

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Lancement IA Drawing-to-Image" -ForegroundColor Cyan
Write-Host "Version Stable Diffusion (sans StreamDiffusion)" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -Path $ScriptPath

Write-Host "Activation de l'environnement virtuel..." -ForegroundColor Yellow
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
& ".\venv_sd\Scripts\Activate.ps1"

Write-Host ""
Write-Host "Vérification des dépendances..." -ForegroundColor Yellow

# Check if diffusers is installed
$diffusersCheck = python -c "import diffusers; print('ok')" 2>$null

if ($diffusersCheck -ne "ok") {
    Write-Host "Installation des dépendances..." -ForegroundColor Green
    pip install diffusers transformers accelerate flask flask-cors pillow numpy opencv-python --quiet
}

Write-Host ""
Write-Host "Vérification de PyTorch et CUDA..." -ForegroundColor Yellow
python -c "import torch; print('PyTorch:', torch.__version__); print('CUDA:', torch.cuda.is_available())"

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "Lancement du serveur IA" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "ATTENTION - Première fois:" -ForegroundColor Yellow
Write-Host "- Téléchargement modèle SD-Turbo (~2 GB)" -ForegroundColor Yellow
Write-Host "- Peut prendre 10-15 minutes" -ForegroundColor Yellow
Write-Host ""
Write-Host "Ensuite:" -ForegroundColor Cyan
Write-Host "1. Ouvrez http://localhost:5002" -ForegroundColor White
Write-Host "2. Dessinez sur le canvas" -ForegroundColor White
Write-Host "3. Tapez un prompt IA" -ForegroundColor White
Write-Host "   Exemples:" -ForegroundColor Gray
Write-Host "   - anime character, detailed" -ForegroundColor Gray
Write-Host "   - photorealistic portrait" -ForegroundColor Gray
Write-Host "   - watercolor painting" -ForegroundColor Gray
Write-Host "4. Cliquez 'Apply Style'" -ForegroundColor White
Write-Host "5. Regardez la magie!" -ForegroundColor White
Write-Host ""
Write-Host "Note: Génération = 5-10 FPS (plus lent que StreamDiffusion mais ça marche!)" -ForegroundColor Gray
Write-Host ""
Write-Host "Appuyez sur Ctrl+C pour arrêter" -ForegroundColor Gray
Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan

Set-Location -Path "backend"
python server_draw2img_ai.py
