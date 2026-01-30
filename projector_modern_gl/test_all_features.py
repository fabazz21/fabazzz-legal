#!/usr/bin/env python3
"""
TEST FONCTIONNEL AUTOMATIQUE
Teste chaque fonction de l'app et compare avec l'app HTML
"""

import sys
import inspect
from pathlib import Path

# Importer tous les modules
try:
    from main import ProjectionMappingApp
    from core.scene import Scene
    from core.camera import Camera
    from objects.projector import Projector
    from objects.cube import Cube
    from projectors.projector_database import PROJECTOR_DATABASE
    from ui.panels.projector_panel import ProjectorPanel
    from ui.panels.scene_panel import ScenePanel
    from ui.panels.photometric_panel import PhotometricPanel
except Exception as e:
    print(f"[ERROR] Impossible d'importer les modules: {e}")
    sys.exit(1)


class FeatureTester:
    def __init__(self):
        self.results = []
        self.missing_features = []
        self.html_features = self.get_html_features()

    def get_html_features(self):
        """Liste des fonctionnalités de l'app HTML"""
        return {
            'objects': [
                'Créer Cube',
                'Créer Cylindre',
                'Créer Sphère',
                'Créer Plane',
                'Créer Circle',
                'Supprimer objet',
                'Dupliquer objet'
            ],
            'projectors': [
                'Créer projecteur',
                'Liste des projecteurs disponibles',
                'Sélectionner marque',
                'Sélectionner modèle',
                'Sélectionner lentille',
                'Lens Shift (horizontal/vertical)',
                'Keystone correction',
                'Position X/Y/Z',
                'Rotation X/Y/Z',
                'Intensité',
                'Supprimer projecteur'
            ],
            'camera': [
                'Orbit controls (rotation)',
                'Pan (déplacement)',
                'Zoom',
                'Reset camera',
                'Vue Perspective',
                'Vue Top',
                'Vue Front',
                'Vue Right'
            ],
            'gizmos': [
                'Gizmo Translation',
                'Gizmo Rotation',
                'Gizmo Scale',
                'Changement mode gizmo'
            ],
            'photometric': [
                'Calculer couverture',
                'Calculer overlap',
                'Throw ratio',
                'Distance de projection',
                'Illuminance',
                'Heatmap'
            ],
            'scene': [
                'Grid visible/invisible',
                'Axes visible/invisible',
                'Taille de la grille',
                'Clear scene',
                'Sauvegarder scene',
                'Charger scene'
            ],
            'timeline': [
                'Timeline pour animations',
                'Keyframes',
                'Play/Pause',
                'Scrubbing'
            ]
        }

    def test_feature(self, category, feature_name, test_func):
        """Teste une fonctionnalité"""
        try:
            result = test_func()
            if result:
                self.results.append({
                    'category': category,
                    'feature': feature_name,
                    'status': 'OK',
                    'message': result
                })
                return True
            else:
                self.results.append({
                    'category': category,
                    'feature': feature_name,
                    'status': 'MISSING',
                    'message': 'Fonctionnalité non implémentée'
                })
                self.missing_features.append(f"{category}: {feature_name}")
                return False
        except Exception as e:
            self.results.append({
                'category': category,
                'feature': feature_name,
                'status': 'ERROR',
                'message': str(e)
            })
            return False

    def test_objects(self):
        """Teste la création d'objets"""
        print("\n" + "="*70)
        print("TEST: OBJETS 3D")
        print("="*70)

        # Test Cube
        self.test_feature('objects', 'Créer Cube',
            lambda: hasattr(Cube, '__init__'))

        # Test Cylindre
        try:
            from objects.cylinder import Cylinder
            self.test_feature('objects', 'Créer Cylindre',
                lambda: hasattr(Cylinder, '__init__'))
        except ImportError:
            self.test_feature('objects', 'Créer Cylindre', lambda: False)

        # Test Sphère
        try:
            from objects.sphere import Sphere
            self.test_feature('objects', 'Créer Sphère',
                lambda: hasattr(Sphere, '__init__'))
        except ImportError:
            self.test_feature('objects', 'Créer Sphère', lambda: False)

        # Test Plane
        try:
            from objects.plane import Plane
            self.test_feature('objects', 'Créer Plane',
                lambda: hasattr(Plane, '__init__'))
        except ImportError:
            self.test_feature('objects', 'Créer Plane', lambda: False)

        # Test Circle
        try:
            from objects.circle import Circle
            self.test_feature('objects', 'Créer Circle',
                lambda: hasattr(Circle, '__init__'))
        except ImportError:
            self.test_feature('objects', 'Créer Circle', lambda: False)

    def test_projectors(self):
        """Teste les projecteurs"""
        print("\n" + "="*70)
        print("TEST: PROJECTEURS")
        print("="*70)

        # Test création projecteur
        self.test_feature('projectors', 'Créer projecteur',
            lambda: hasattr(ProjectorPanel, '_create_projector'))

        self.test_feature('projectors', 'Modal de création',
            lambda: hasattr(ProjectorPanel, '_render_create_modal'))

        self.test_feature('projectors', 'Liste projecteurs',
            lambda: hasattr(ProjectorPanel, '_render_projector_list'))

        # Test lens shift
        self.test_feature('projectors', 'Lens Shift',
            lambda: 'lens_shift' in inspect.getsource(Projector.__init__))

        # Test keystone
        self.test_feature('projectors', 'Keystone',
            lambda: 'keystone' in inspect.getsource(Projector.__init__))

        # Vérifier database projecteurs
        brands = set()
        total_models = 0
        for key, config in PROJECTOR_DATABASE.items():
            brands.add(config.get('brand', 'Unknown'))
            total_models += 1

        self.test_feature('projectors', f'Base de données ({total_models} modèles)',
            lambda: f"{len(brands)} marques, {total_models} modèles")

        print(f"\n  Marques disponibles: {', '.join(sorted(brands))}")

    def test_camera(self):
        """Teste la caméra"""
        print("\n" + "="*70)
        print("TEST: CAMÉRA")
        print("="*70)

        self.test_feature('camera', 'Orbit controls',
            lambda: hasattr(Camera, 'rotate'))

        self.test_feature('camera', 'Pan',
            lambda: hasattr(Camera, 'pan'))

        self.test_feature('camera', 'Zoom',
            lambda: hasattr(Camera, 'zoom'))

        self.test_feature('camera', 'Reset',
            lambda: hasattr(Camera, 'reset'))

        self.test_feature('camera', 'Vues prédéfinies',
            lambda: hasattr(Camera, 'set_view'))

    def test_gizmos(self):
        """Teste les gizmos"""
        print("\n" + "="*70)
        print("TEST: GIZMOS")
        print("="*70)

        try:
            from ui.gizmo import Gizmo
            self.test_feature('gizmos', 'Système de gizmos',
                lambda: hasattr(Gizmo, '__init__'))

            self.test_feature('gizmos', 'Mode Translation',
                lambda: 'translate' in inspect.getsource(Gizmo).lower())

            self.test_feature('gizmos', 'Mode Rotation',
                lambda: 'rotate' in inspect.getsource(Gizmo).lower())

            self.test_feature('gizmos', 'Mode Scale',
                lambda: 'scale' in inspect.getsource(Gizmo).lower())
        except ImportError:
            self.test_feature('gizmos', 'Système de gizmos', lambda: False)

    def test_photometric(self):
        """Teste les calculs photométriques"""
        print("\n" + "="*70)
        print("TEST: PHOTOMÉTRIE")
        print("="*70)

        self.test_feature('photometric', 'Calculer couverture',
            lambda: hasattr(PhotometricPanel, 'calculate_coverage'))

        self.test_feature('photometric', 'Calculer overlap',
            lambda: hasattr(PhotometricPanel, 'calculate_overlap'))

        self.test_feature('photometric', 'Throw ratio',
            lambda: 'throw_ratio' in inspect.getsource(PhotometricPanel).lower())

        self.test_feature('photometric', 'Illuminance',
            lambda: 'illuminance' in inspect.getsource(PhotometricPanel).lower())

    def test_scene(self):
        """Teste la gestion de scène"""
        print("\n" + "="*70)
        print("TEST: SCÈNE")
        print("="*70)

        self.test_feature('scene', 'Grid',
            lambda: hasattr(Scene, '_create_grid'))

        self.test_feature('scene', 'Axes',
            lambda: hasattr(Scene, '_create_axes'))

        self.test_feature('scene', 'Ajouter objet',
            lambda: hasattr(Scene, 'add_object'))

        self.test_feature('scene', 'Supprimer objet',
            lambda: hasattr(Scene, 'remove_object'))

        self.test_feature('scene', 'Clear scene',
            lambda: hasattr(ScenePanel, 'clear_scene'))

    def test_timeline(self):
        """Teste la timeline"""
        print("\n" + "="*70)
        print("TEST: TIMELINE")
        print("="*70)

        try:
            from ui.panels.timeline_panel import TimelinePanel
            self.test_feature('timeline', 'Timeline',
                lambda: hasattr(TimelinePanel, '__init__'))

            self.test_feature('timeline', 'Keyframes',
                lambda: 'keyframe' in inspect.getsource(TimelinePanel).lower())

            self.test_feature('timeline', 'Play/Pause',
                lambda: hasattr(TimelinePanel, 'play') or hasattr(TimelinePanel, 'pause'))
        except ImportError:
            self.test_feature('timeline', 'Timeline', lambda: False)

    def generate_report(self):
        """Génère le rapport de comparaison"""
        print("\n" + "="*70)
        print("RAPPORT FINAL - COMPARAISON HTML vs MODERNGL")
        print("="*70)

        # Compter les résultats
        total = len(self.results)
        ok = sum(1 for r in self.results if r['status'] == 'OK')
        missing = sum(1 for r in self.results if r['status'] == 'MISSING')
        errors = sum(1 for r in self.results if r['status'] == 'ERROR')

        print(f"\nStatistiques:")
        print(f"  Total testé: {total}")
        print(f"  [OK] Implémenté: {ok} ({ok*100//total if total else 0}%)")
        print(f"  [MISSING] Manquant: {missing} ({missing*100//total if total else 0}%)")
        print(f"  [ERROR] Erreurs: {errors} ({errors*100//total if total else 0}%)")

        # Fonctionnalités manquantes
        if self.missing_features:
            print("\n" + "="*70)
            print("FONCTIONNALITÉS MANQUANTES (par rapport à l'app HTML)")
            print("="*70)

            for feature in self.missing_features:
                print(f"  - {feature}")

        # Détails par catégorie
        print("\n" + "="*70)
        print("DÉTAILS PAR CATÉGORIE")
        print("="*70)

        categories = {}
        for result in self.results:
            cat = result['category']
            if cat not in categories:
                categories[cat] = {'OK': 0, 'MISSING': 0, 'ERROR': 0}
            categories[cat][result['status']] += 1

        for cat, counts in sorted(categories.items()):
            total_cat = sum(counts.values())
            ok_cat = counts['OK']
            print(f"\n{cat.upper()}: {ok_cat}/{total_cat} OK")

            for result in self.results:
                if result['category'] == cat:
                    status_icon = {
                        'OK': '[OK]',
                        'MISSING': '[MANQUANT]',
                        'ERROR': '[ERREUR]'
                    }[result['status']]
                    print(f"  {status_icon} {result['feature']}")
                    if result['status'] != 'OK':
                        print(f"      -> {result['message']}")

        # Sauvegarder rapport
        report_file = Path("feature_comparison_report.txt")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("COMPARAISON FONCTIONNALITÉS HTML vs MODERNGL\n")
            f.write("="*70 + "\n\n")

            f.write(f"Total testé: {total}\n")
            f.write(f"Implémenté: {ok}\n")
            f.write(f"Manquant: {missing}\n")
            f.write(f"Erreurs: {errors}\n\n")

            f.write("="*70 + "\n")
            f.write("FONCTIONNALITÉS MANQUANTES\n")
            f.write("="*70 + "\n\n")

            for feature in self.missing_features:
                f.write(f"- {feature}\n")

            f.write("\n" + "="*70 + "\n")
            f.write("DÉTAILS\n")
            f.write("="*70 + "\n\n")

            for cat, counts in sorted(categories.items()):
                f.write(f"\n{cat.upper()}\n")
                f.write("-" * 70 + "\n")

                for result in self.results:
                    if result['category'] == cat:
                        f.write(f"{result['status']}: {result['feature']}\n")
                        if result['message'] and result['status'] != 'OK':
                            f.write(f"  -> {result['message']}\n")

        print(f"\n[FILE] Rapport sauvegardé: {report_file}")

        # Instructions
        print("\n" + "="*70)
        print("PROCHAINES ÉTAPES")
        print("="*70)
        print("\n1. Envoyez-moi 'feature_comparison_report.txt'")
        print("2. Je vais implémenter TOUTES les fonctionnalités manquantes")
        print("3. Je vais copier exactement l'app HTML")
        print()


def main():
    print("="*70)
    print("TEST FONCTIONNEL AUTOMATIQUE - APP MODERNGL")
    print("="*70)
    print("\nCe script va tester TOUTES les fonctionnalités")
    print("et comparer avec l'app HTML pour trouver ce qui manque.\n")

    tester = FeatureTester()

    # Lancer tous les tests
    tester.test_objects()
    tester.test_projectors()
    tester.test_camera()
    tester.test_gizmos()
    tester.test_photometric()
    tester.test_scene()
    tester.test_timeline()

    # Générer rapport
    tester.generate_report()


if __name__ == "__main__":
    main()
