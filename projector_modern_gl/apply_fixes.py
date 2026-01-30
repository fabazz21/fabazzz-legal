#!/usr/bin/env python3
"""
Script pour appliquer automatiquement les corrections
Exécutez: py -3.11 apply_fixes.py
"""

import os
from pathlib import Path

def apply_scene_fix():
    """Fix 1: Ajouter grid_size à Scene"""
    file_path = Path("core/scene.py")

    if not file_path.exists():
        print(f"❌ Fichier non trouvé: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Vérifier si déjà corrigé
    if any('self.grid_size' in line for line in lines):
        print("⏭️  Scene.grid_size existe déjà")
        return True

    # Trouver et corriger
    modified = False
    for i, line in enumerate(lines):
        # Ajouter grid_size après "self.grid = None"
        if 'self.grid = None' in line:
            lines.insert(i + 1, '        self.grid_size = 50.0  # Grid size in units\n')
            modified = True
            print("✅ Ajouté: self.grid_size = 50.0")

        # Remplacer "grid_size = 50" par "grid_size = int(self.grid_size)"
        if 'grid_size = 50' in line and 'self.grid_size' not in line:
            lines[i] = line.replace('grid_size = 50', 'grid_size = int(self.grid_size)')
            print("✅ Modifié: grid_size = int(self.grid_size)")

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"✅ {file_path} corrigé")
        return True

    return False


def apply_camera_fix():
    """Fix 2: Ajouter reset() à Camera"""
    file_path = Path("core/camera.py")

    if not file_path.exists():
        print(f"❌ Fichier non trouvé: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Vérifier si déjà corrigé
    if any('def reset(self)' in line for line in lines):
        print("⏭️  Camera.reset() existe déjà")
        return True

    # Trouver et ajouter reset() avant resize()
    for i, line in enumerate(lines):
        if 'def resize(self, width, height):' in line:
            reset_method = [
                '\n',
                '    def reset(self):\n',
                '        """Reset camera to default perspective view"""\n',
                '        self.set_view(\'perspective\')\n',
                '        print("  🔄 Camera reset to default view")\n',
                '\n'
            ]
            lines = lines[:i] + reset_method + lines[i:]

            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)

            print(f"✅ {file_path} corrigé - ajouté reset()")
            return True

    return False


def apply_object_fix():
    """Fix 3: Ajouter active et intensity à Object3D"""
    file_path = Path("objects/base_object.py")

    if not file_path.exists():
        print(f"❌ Fichier non trouvé: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Vérifier si déjà corrigé
    if any('self.active' in line for line in lines):
        print("⏭️  Object3D.active existe déjà")
        return True

    # Trouver et corriger
    modified = False
    for i, line in enumerate(lines):
        # Ajouter active après visible
        if 'self.visible = True' in line and i + 1 < len(lines):
            if 'self.active' not in lines[i + 1]:
                lines.insert(i + 1, '        self.active = True  # Whether object is active/enabled\n')
                modified = True
                print("✅ Ajouté: self.active = True")

        # Ajouter intensity après receive_shadow
        if 'self.receive_shadow = True' in line and i + 1 < len(lines):
            if 'self.intensity' not in lines[i + 1]:
                lines.insert(i + 1, '        self.intensity = 1.0  # For lights or emissive objects\n')
                modified = True
                print("✅ Ajouté: self.intensity = 1.0")

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"✅ {file_path} corrigé")
        return True

    return False


def main():
    print("🔧 Application des corrections...\n")

    # Vérifier qu'on est dans le bon dossier
    if not Path("core").exists():
        print("❌ ERREUR: Exécutez ce script depuis le dossier projector_modern_gl")
        print("   cd projector_modern_gl")
        print("   py -3.11 apply_fixes.py")
        return

    print("📝 Correction 1: Scene.grid_size")
    apply_scene_fix()

    print("\n📝 Correction 2: Camera.reset()")
    apply_camera_fix()

    print("\n📝 Correction 3: Object3D.active et intensity")
    apply_object_fix()

    print("\n" + "="*60)
    print("✅ CORRECTIONS TERMINÉES!")
    print("="*60)
    print("\n📋 Résumé des corrections appliquées:")
    print("   1. Scene.grid_size - Permet de redimensionner la grille")
    print("   2. Camera.reset() - Réinitialise la vue de la caméra")
    print("   3. Object3D.active - Active/désactive les objets")
    print("   4. Object3D.intensity - Intensité pour lumières/objets émissifs")
    print("\n🚀 Lancez maintenant l'application:")
    print("   py -3.11 main.py")


if __name__ == "__main__":
    main()
