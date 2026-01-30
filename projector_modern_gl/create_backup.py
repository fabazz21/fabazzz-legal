#!/usr/bin/env python3
"""
Script pour sauvegarder tous les changements en local
Génère un dossier de backup avec tous les fichiers modifiés
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

def create_local_backup():
    """Crée un backup de tous les fichiers modifiés"""

    # Créer dossier de backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(f"backup_moderngl_{timestamp}")
    backup_dir.mkdir(exist_ok=True)

    # Liste des fichiers à sauvegarder (tous les fichiers modifiés)
    files_to_backup = [
        # Core
        "core/camera.py",
        "core/scene.py",

        # Objects
        "objects/primitives.py",

        # UI
        "ui/gizmo.py",
        "ui/panels/scene_panel.py",
        "ui/panels/photometric_panel.py",
        "ui/panels/timeline_panel.py",

        # Projectors
        "projectors/projector_database.py",

        # Tests
        "test_all_features.py",
        "auto_test_realtime.py",
        "fix_dict_bug.py",

        # Main
        "main.py",
    ]

    print(f"Creation du backup dans: {backup_dir}")
    print("="*70)

    copied_count = 0

    for file_path in files_to_backup:
        src = Path(file_path)
        if src.exists():
            # Créer les sous-dossiers si nécessaire
            dst = backup_dir / file_path
            dst.parent.mkdir(parents=True, exist_ok=True)

            # Copier le fichier
            shutil.copy2(src, dst)
            print(f"[OK] Copie: {file_path}")
            copied_count += 1
        else:
            print(f"[SKIP] Non trouve: {file_path}")

    print("="*70)
    print(f"[OK] {copied_count} fichiers copies dans {backup_dir}")
    print()

    # Créer un fichier récapitulatif
    summary_file = backup_dir / "CHANGELOG.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("CHANGEMENTS MODERNGL APP\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*70 + "\n\n")

        f.write("FONCTIONNALITES AJOUTEES:\n\n")

        features = [
            "1. Orbit Controls - Rotation camera avec souris (middle click)",
            "2. Pan - Deplacement camera (shift + middle click)",
            "3. Zoom - Molette souris",
            "4. Objet Circle - Nouvelle primitive 3D",
            "5. Axes 3D - X (rouge), Y (vert), Z (bleu)",
            "6. Clear Scene - Bouton pour vider la scene",
            "7. Calculate Coverage - Calcul surface de projection",
            "8. Calculate Overlap - Calcul chevauchement projecteurs",
            "9. Play/Pause Timeline - Controles timeline",
            "10. Systeme Gizmos - Translate/Rotate/Scale 3D",
            "11. Base de donnees complete:",
            "    - 29 projecteurs (etait 18)",
            "    - 5 marques: Panasonic, Christie, Barco, Epson, Digital Projection",
            "    - 20 lentilles avec lens shift complet",
            "    - Lentilles UST Epson (ELPLX02S)",
        ]

        for feature in features:
            f.write(f"  {feature}\n")

        f.write("\n" + "="*70 + "\n")
        f.write("FICHIERS MODIFIES:\n\n")

        for file_path in files_to_backup:
            f.write(f"  - {file_path}\n")

        f.write("\n" + "="*70 + "\n")
        f.write("INSTALLATION:\n\n")
        f.write("1. Copiez tous les fichiers dans votre projet projector_modern_gl/\n")
        f.write("2. Lancez: py -3.11 main.py\n")
        f.write("3. Test: py -3.11 test_all_features.py\n")
        f.write("\n")
        f.write("CONTROLES:\n")
        f.write("  - Middle Mouse: Rotation camera (orbit)\n")
        f.write("  - Shift + Middle Mouse: Pan camera\n")
        f.write("  - Scroll: Zoom\n")
        f.write("  - WASD: Deplacement camera\n")
        f.write("  - Q/E: Haut/Bas\n")

    print(f"[FILE] Recapitulatif cree: {summary_file}")
    print()
    print("="*70)
    print("PROCHAINES ETAPES:")
    print("="*70)
    print(f"1. Le dossier '{backup_dir}' contient tous vos fichiers")
    print(f"2. Telechargez ce dossier sur votre machine locale")
    print(f"3. Remplacez les fichiers dans votre projet")
    print()

    return backup_dir

if __name__ == "__main__":
    backup_dir = create_local_backup()
    print(f"[OK] Backup termine: {backup_dir}")
