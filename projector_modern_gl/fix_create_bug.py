#!/usr/bin/env python3
"""
Corrige l'erreur dans _create_projector()
PROJECTOR_DATABASE est un dict, pas une liste
"""

from pathlib import Path

def fix_create_projector_bug():
    """Corrige le bug de type dans _create_projector"""

    file_path = Path("ui/panels/projector_panel.py")

    if not file_path.exists():
        print("[ERROR] projector_panel.py non trouvé!")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Chercher le mauvais code
    old_code = """        # Find projector config
        proj_config = None
        for config in PROJECTOR_DATABASE:
            if config['brand'] == brand and config['name'] == model:
                proj_config = config
                break"""

    # Nouveau code corrigé
    new_code = """        # Find projector config
        proj_config = None
        for key, config in PROJECTOR_DATABASE.items():
            if config['brand'] == brand and config['name'] == model:
                proj_config = config
                break"""

    if old_code not in content:
        print("[OK] Code déjà corrigé ou pattern non trouvé")
        return True

    # Remplacer
    content = content.replace(old_code, new_code)

    # Écrire
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("[OK] Bug corrigé dans _create_projector()!")
    return True

if __name__ == "__main__":
    print("="*70)
    print("CORRECTION DU BUG PROJECTOR_DATABASE")
    print("="*70)
    print()
    print("Problème: PROJECTOR_DATABASE est un dict, pas une liste")
    print("Solution: Utiliser .items() pour itérer")
    print()

    success = fix_create_projector_bug()

    if success:
        print()
        print("[OK] Correction appliquée!")
        print()
        print("Maintenant relancez: py -3.11 main.py")
        print("Et essayez de créer un projecteur!")
    else:
        print()
        print("[ERROR] Échec de la correction")
