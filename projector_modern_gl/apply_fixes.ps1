# Script PowerShell pour appliquer les corrections
# Exécutez ce script dans le dossier projector_modern_gl

Write-Host "🔧 Application des corrections..." -ForegroundColor Cyan

# Fix 1: core/scene.py - Ajouter grid_size
Write-Host "`n📝 Correction 1: core/scene.py (grid_size)" -ForegroundColor Yellow

$sceneFile = "core\scene.py"
if (Test-Path $sceneFile) {
    $content = Get-Content $sceneFile -Raw

    # Vérifier si grid_size existe déjà
    if ($content -notmatch 'self\.grid_size') {
        Write-Host "   Ajout de self.grid_size..." -ForegroundColor Green

        # Remplacer la section Grid
        $content = $content -replace `
            "(\s+# Grid\r?\n\s+self\.grid = None\r?\n)",`
            "`$1        self.grid_size = 50.0  # Grid size in units`n"

        # Remplacer dans _create_grid
        $content = $content -replace `
            "(def _create_grid\(self\):\r?\n\s+`"``"``"Create reference grid`"``"``"\r?\n\s+# Grid: 100x100 units, 1 unit spacing\r?\n)\s+grid_size = 50",`
            "`${1}        grid_size = int(self.grid_size)"

        Set-Content $sceneFile -Value $content -NoNewline
        Write-Host "   ✅ core/scene.py corrigé" -ForegroundColor Green
    } else {
        Write-Host "   ⏭️  grid_size existe déjà" -ForegroundColor Gray
    }
} else {
    Write-Host "   ❌ Fichier non trouvé: $sceneFile" -ForegroundColor Red
}

# Fix 2: core/camera.py - Ajouter reset()
Write-Host "`n📝 Correction 2: core/camera.py (méthode reset)" -ForegroundColor Yellow

$cameraFile = "core\camera.py"
if (Test-Path $cameraFile) {
    $content = Get-Content $cameraFile -Raw

    # Vérifier si reset() existe déjà
    if ($content -notmatch 'def reset\(self\)') {
        Write-Host "   Ajout de la méthode reset()..." -ForegroundColor Green

        # Ajouter reset() avant resize()
        $resetMethod = @"

    def reset(self):
        `"`"`"Reset camera to default perspective view`"`"`"
        self.set_view('perspective')
        print("  🔄 Camera reset to default view")
"@

        $content = $content -replace `
            "(    def resize\(self, width, height\):)",`
            "$resetMethod`n`n`$1"

        Set-Content $cameraFile -Value $content -NoNewline
        Write-Host "   ✅ core/camera.py corrigé" -ForegroundColor Green
    } else {
        Write-Host "   ⏭️  reset() existe déjà" -ForegroundColor Gray
    }
} else {
    Write-Host "   ❌ Fichier non trouvé: $cameraFile" -ForegroundColor Red
}

# Fix 3: objects/base_object.py - Ajouter active et intensity
Write-Host "`n📝 Correction 3: objects/base_object.py (active, intensity)" -ForegroundColor Yellow

$objectFile = "objects\base_object.py"
if (Test-Path $objectFile) {
    $content = Get-Content $objectFile -Raw

    # Vérifier si active existe déjà
    if ($content -notmatch 'self\.active') {
        Write-Host "   Ajout de self.active et self.intensity..." -ForegroundColor Green

        # Remplacer la section Rendering
        $content = $content -replace `
            "(\s+# Rendering\r?\n\s+self\.visible = True\r?\n)(\s+self\.cast_shadow = True)",`
            "`${1}        self.active = True  # Whether object is active/enabled`n`${2}"

        $content = $content -replace `
            "(\s+self\.receive_shadow = True\r?\n)",`
            "`${1}        self.intensity = 1.0  # For lights or emissive objects`n"

        Set-Content $objectFile -Value $content -NoNewline
        Write-Host "   ✅ objects/base_object.py corrigé" -ForegroundColor Green
    } else {
        Write-Host "   ⏭️  active existe déjà" -ForegroundColor Gray
    }
} else {
    Write-Host "   ❌ Fichier non trouvé: $objectFile" -ForegroundColor Red
}

Write-Host "`n✅ CORRECTIONS TERMINÉES!" -ForegroundColor Green
Write-Host "`n📋 Résumé des corrections appliquées:" -ForegroundColor Cyan
Write-Host "   1. Scene.grid_size - Permet de redimensionner la grille" -ForegroundColor White
Write-Host "   2. Camera.reset() - Réinitialise la vue de la caméra" -ForegroundColor White
Write-Host "   3. Object3D.active - Active/désactive les objets" -ForegroundColor White
Write-Host "   4. Object3D.intensity - Intensité pour lumières/objets émissifs" -ForegroundColor White

Write-Host "`n🚀 Vous pouvez maintenant lancer l'application:" -ForegroundColor Cyan
Write-Host "   py -3.11 main.py" -ForegroundColor Yellow
