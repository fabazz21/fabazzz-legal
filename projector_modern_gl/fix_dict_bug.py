#!/usr/bin/env python3
"""
Correction rapide: PROJECTOR_DATABASE est un dict, pas une liste
Remplace PROJECTOR_DATABASE[0] par list(PROJECTOR_DATABASE.values())[0]
"""

from pathlib import Path

def fix_dict_access_bug():
    """Corrige l'accès incorrect au dictionnaire"""

    file_path = Path("ui/panels/projector_panel.py")

    if not file_path.exists():
        print("[ERROR] projector_panel.py non trouvé!")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remplacements
    replacements = [
        (
            "proj_config = PROJECTOR_DATABASE[0] if PROJECTOR_DATABASE else None",
            "proj_config = list(PROJECTOR_DATABASE.values())[0] if PROJECTOR_DATABASE else None"
        ),
        (
            "lens_config = LENS_DATABASE[0] if LENS_DATABASE else None",
            "lens_config = list(LENS_DATABASE.values())[0] if LENS_DATABASE else None"
        )
    ]

    modified = False
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            print(f"[OK] Remplacé: {old[:50]}...")
            modified = True

    if not modified:
        print("[OK] Code déjà corrigé")
        return True

    # Écrire
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("[OK] Corrections appliquées!")
    return True

if __name__ == "__main__":
    print("="*70)
    print("CORRECTION BUG: KeyError: 0")
    print("="*70)
    print()

    fix_dict_access_bug()

    print()
    print("[OK] Maintenant exécutez: py -3.11 main.py")
