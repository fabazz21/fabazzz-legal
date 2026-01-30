#!/usr/bin/env python3
"""
Test des fonctionnalités UI - Identifie les problèmes d'interaction
USAGE: py -3.11 test_ui_features.py
"""

import sys
from pathlib import Path

def check_projector_panel():
    """Vérifie le panel de création de projecteur"""
    print("\n" + "="*70)
    print("TEST: Projector Panel - Création de projecteur")
    print("="*70)

    issues = []

    try:
        sys.path.insert(0, str(Path.cwd()))
        from ui.panels.projector_panel import ProjectorPanel

        # Vérifier les méthodes essentielles
        required_methods = [
            'render',
            'render_content',
            '_render_create_modal',
            '_render_projector_list'
        ]

        for method in required_methods:
            if not hasattr(ProjectorPanel, method):
                issues.append(f"Méthode manquante: {method}")
                print(f"  [ERROR] Méthode manquante: {method}")
            else:
                print(f"  [OK] Méthode trouvée: {method}")

        # Lire le code pour détecter les problèmes
        panel_file = Path("ui/panels/projector_panel.py")
        if panel_file.exists():
            with open(panel_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Vérifier les patterns problématiques
            if 'scene.add_projector' not in content:
                issues.append("Aucun appel à scene.add_projector() trouvé")
                print("  [ERROR] Aucun appel à scene.add_projector()")

            if 'imgui.button' not in content or 'Create Projector' not in content:
                issues.append("Bouton 'Create Projector' non trouvé")
                print("  [ERROR] Bouton 'Create Projector' non trouvé")
            else:
                print("  [OK] Bouton 'Create Projector' trouvé")

    except Exception as e:
        issues.append(f"Erreur lors du chargement: {str(e)}")
        print(f"  [ERROR] {e}")

    return issues

def check_gizmo_system():
    """Vérifie le système de gizmos"""
    print("\n" + "="*70)
    print("TEST: Gizmo System - Transformation d'objets")
    print("="*70)

    issues = []

    # Vérifier dans main_ui_tabbed.py
    ui_file = Path("ui/main_ui_tabbed.py")
    if ui_file.exists():
        with open(ui_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Chercher les gizmos
        if 'gizmo_mode' not in content:
            issues.append("gizmo_mode non défini dans UI")
            print("  [ERROR] gizmo_mode non défini")
        else:
            print("  [OK] gizmo_mode trouvé")

        # Chercher les boutons de gizmo
        if 'translate' not in content or 'rotate' not in content or 'scale' not in content:
            issues.append("Boutons gizmo (translate/rotate/scale) manquants")
            print("  [ERROR] Boutons gizmo manquants")
        else:
            print("  [OK] Boutons gizmo trouvés")

        # Vérifier l'affichage des gizmos
        if '_render_gizmo_controls' not in content and 'Gizmo' not in content:
            issues.append("Pas de méthode pour render les gizmos")
            print("  [ERROR] Pas de rendu de gizmos")
        else:
            print("  [OK] Rendu de gizmos trouvé")
    else:
        issues.append("Fichier main_ui_tabbed.py non trouvé")
        print("  [ERROR] Fichier UI non trouvé")

    return issues

def check_photometric_calculations():
    """Vérifie les calculs photométriques"""
    print("\n" + "="*70)
    print("TEST: Photometric Calculations - Calculs d'éclairage")
    print("="*70)

    issues = []

    panel_file = Path("ui/panels/photometric_panel.py")
    if panel_file.exists():
        with open(panel_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Vérifier les calculs
        calc_functions = [
            'calculate_illuminance',
            'calculate_coverage',
            'calculate_overlap'
        ]

        found_calcs = []
        for func in calc_functions:
            if func in content:
                found_calcs.append(func)
                print(f"  [OK] Fonction trouvée: {func}")
            else:
                issues.append(f"Fonction manquante: {func}")
                print(f"  [ERROR] Fonction manquante: {func}")

        if len(found_calcs) == 0:
            issues.append("Aucune fonction de calcul trouvée")
            print("  [ERROR] Aucun calcul implémenté")
    else:
        issues.append("Fichier photometric_panel.py non trouvé")
        print("  [ERROR] Panel photométrique non trouvé")

    return issues

def check_scene_responsiveness():
    """Vérifie la réactivité de la scène"""
    print("\n" + "="*70)
    print("TEST: Scene Responsiveness - Interaction viewport")
    print("="*70)

    issues = []

    # Vérifier le viewport panel
    viewport_file = Path("ui/panels/viewport_panel.py")
    if viewport_file.exists():
        with open(viewport_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Vérifier les contrôles caméra
        if 'camera' not in content:
            issues.append("Pas de contrôles caméra")
            print("  [ERROR] Contrôles caméra manquants")
        else:
            print("  [OK] Contrôles caméra trouvés")

        # Vérifier les sliders
        if 'slider_float' not in content:
            issues.append("Pas de sliders pour contrôler la caméra")
            print("  [ERROR] Sliders manquants")
        else:
            print("  [OK] Sliders trouvés")
    else:
        issues.append("Fichier viewport_panel.py non trouvé")
        print("  [ERROR] Panel viewport non trouvé")

    # Vérifier le renderer
    renderer_file = Path("core/renderer.py")
    if renderer_file.exists():
        with open(renderer_file, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'render' not in content or 'camera' not in content:
            issues.append("Renderer ne semble pas complet")
            print("  [ERROR] Renderer incomplet")
        else:
            print("  [OK] Renderer semble fonctionnel")

    return issues

def check_main_app_integration():
    """Vérifie l'intégration dans main.py"""
    print("\n" + "="*70)
    print("TEST: Main App Integration - Boucle principale")
    print("="*70)

    issues = []

    main_file = Path("main.py")
    if main_file.exists():
        with open(main_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Vérifier la boucle de rendu
        if 'render_scene' not in content:
            issues.append("Pas d'appel à render_scene()")
            print("  [ERROR] render_scene() non appelé")
        else:
            print("  [OK] render_scene() appelé")

        if 'render_ui' not in content:
            issues.append("Pas d'appel à render_ui()")
            print("  [ERROR] render_ui() non appelé")
        else:
            print("  [OK] render_ui() appelé")

        if 'update' not in content:
            issues.append("Pas de mise à jour dans la boucle")
            print("  [ERROR] update() manquant")
        else:
            print("  [OK] update() présent")

    return issues

def generate_fix_report(all_issues):
    """Génère un rapport avec les corrections à apporter"""
    print("\n" + "="*70)
    print("RAPPORT FINAL - PROBLÈMES DÉTECTÉS")
    print("="*70)

    if not any(all_issues.values()):
        print("\n[OK] Aucun problème majeur détecté!")
        print("Les fonctionnalités devraient fonctionner.")
        return

    print("\nPROBLÈMES IDENTIFIÉS:\n")

    for category, issues in all_issues.items():
        if issues:
            print(f"\n{category}:")
            for issue in issues:
                print(f"  - {issue}")

    # Sauvegarder dans un fichier
    report_file = Path("ui_issues_report.txt")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("RAPPORT DE PROBLÈMES UI\n")
        f.write("="*70 + "\n\n")

        for category, issues in all_issues.items():
            if issues:
                f.write(f"\n{category}:\n")
                for issue in issues:
                    f.write(f"  - {issue}\n")

    print(f"\n[FILE] Rapport sauvegardé: {report_file}")
    print("\nEnvoyez-moi ce rapport pour que je corrige les problèmes!")

def main():
    print("="*70)
    print("TEST DES FONCTIONNALITÉS UI")
    print("="*70)
    print()
    print("Ce script identifie pourquoi les fonctionnalités ne marchent pas:")
    print("  1. Création de projecteur")
    print("  2. Gizmos (translate/rotate/scale)")
    print("  3. Calculs photométriques")
    print("  4. Réactivité de la scène")
    print()

    all_issues = {}

    # Tests
    all_issues["PROJECTOR PANEL"] = check_projector_panel()
    all_issues["GIZMO SYSTEM"] = check_gizmo_system()
    all_issues["PHOTOMETRIC CALCULATIONS"] = check_photometric_calculations()
    all_issues["SCENE RESPONSIVENESS"] = check_scene_responsiveness()
    all_issues["MAIN APP INTEGRATION"] = check_main_app_integration()

    # Rapport final
    generate_fix_report(all_issues)

    print("\n" + "="*70)
    print("PROCHAINES ÉTAPES:")
    print("="*70)
    print("\n1. Copiez le contenu de 'ui_issues_report.txt'")
    print("2. Envoyez-le moi")
    print("3. Je corrigerai tous les problèmes")
    print()

if __name__ == "__main__":
    main()
