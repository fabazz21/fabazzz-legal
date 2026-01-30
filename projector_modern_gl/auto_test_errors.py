#!/usr/bin/env python3
"""
Script de test automatisé - Lance l'app et note toutes les erreurs
USAGE: py -3.11 auto_test_errors.py
"""

import subprocess
import time
import sys
from pathlib import Path
from datetime import datetime

class ErrorTester:
    def __init__(self):
        self.errors_found = []
        self.test_count = 0
        self.current_test = None

    def log_error(self, test_name, error_message, traceback):
        """Enregistre une erreur"""
        self.errors_found.append({
            'test': test_name,
            'error': error_message,
            'traceback': traceback,
            'timestamp': datetime.now().isoformat()
        })

    def run_app_test(self, timeout=5):
        """Lance l'app et capture les erreurs"""
        print(f"🚀 Lancement de l'application (timeout: {timeout}s)...")

        try:
            # Lance l'application
            process = subprocess.Popen(
                [sys.executable, "main.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Attendre un peu
            try:
                stdout, stderr = process.communicate(timeout=timeout)
                returncode = process.returncode

                if returncode != 0:
                    print(f"❌ L'application a crashé (code: {returncode})")
                    return False, stderr
                else:
                    print(f"✅ L'application s'est fermée normalement")
                    return True, None

            except subprocess.TimeoutExpired:
                print(f"⏱️  Timeout - l'application tourne toujours")
                process.kill()
                stdout, stderr = process.communicate()

                # Si elle a tourné sans crash, c'est bon signe
                if 'Fatal error' in stderr or 'Traceback' in stderr:
                    return False, stderr
                return True, None

        except Exception as e:
            print(f"❌ Erreur lors du lancement: {e}")
            return False, str(e)

    def parse_error(self, error_text):
        """Parse le texte d'erreur pour extraire les détails"""
        lines = error_text.split('\n')

        error_type = None
        error_msg = None
        file_location = None
        full_traceback = []

        for line in lines:
            if 'Fatal error:' in line:
                error_msg = line.split('Fatal error:')[1].strip()
            elif 'Error:' in line and not error_msg:
                error_msg = line.split('Error:')[1].strip()
            elif 'File "' in line:
                file_location = line.strip()
                full_traceback.append(line.strip())
            elif line.strip().startswith('raise ') or 'Exception' in line:
                error_type = line.strip()
            elif line.strip() and (full_traceback or error_msg):
                full_traceback.append(line.strip())

        return {
            'type': error_type or 'Unknown',
            'message': error_msg or 'No error message',
            'location': file_location or 'Unknown location',
            'traceback': '\n'.join(full_traceback)
        }

    def test_startup(self):
        """Test 1: Démarrage de l'application"""
        self.test_count += 1
        print(f"\n{'='*70}")
        print(f"TEST {self.test_count}: Démarrage de l'application")
        print('='*70)

        success, error = self.run_app_test(timeout=10)

        if not success and error:
            parsed = self.parse_error(error)
            self.log_error('startup', parsed['message'], parsed['traceback'])
            print(f"\n❌ ERREUR DÉTECTÉE:")
            print(f"   Type: {parsed['type']}")
            print(f"   Message: {parsed['message']}")
            print(f"   Location: {parsed['location']}")
        else:
            print("✅ Démarrage OK")

        return success

    def analyze_codebase(self):
        """Analyse statique du code pour détecter les problèmes potentiels"""
        print(f"\n{'='*70}")
        print("ANALYSE STATIQUE DU CODE")
        print('='*70)

        potential_issues = []

        # Vérifier les imports manquants potentiels
        print("\n🔍 Recherche de problèmes potentiels...")

        # Liste des fichiers à analyser
        python_files = list(Path('.').rglob('*.py'))

        issues_by_type = {
            'missing_attributes': [],
            'incorrect_calls': [],
            'import_errors': []
        }

        for py_file in python_files:
            if 'venv' in str(py_file) or '__pycache__' in str(py_file):
                continue

            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')

                    for i, line in enumerate(lines, 1):
                        # Chercher des appels à des méthodes qui n'existent peut-être pas
                        if 'self.' in line and '=' not in line and 'def ' not in line:
                            # Potentiel appel de méthode/attribut
                            if '.push_style_color(' in line and '*' in line and ', ' in line:
                                issues_by_type['incorrect_calls'].append({
                                    'file': str(py_file),
                                    'line': i,
                                    'issue': 'Incorrect push_style_color call',
                                    'code': line.strip()
                                })

            except Exception as e:
                pass

        # Afficher les problèmes trouvés
        total_issues = sum(len(v) for v in issues_by_type.values())

        if total_issues > 0:
            print(f"\n⚠️  {total_issues} problèmes potentiels détectés:")
            for issue_type, issues in issues_by_type.items():
                if issues:
                    print(f"\n   {issue_type.upper()}:")
                    for issue in issues:
                        print(f"      - {issue['file']}:{issue['line']}")
                        print(f"        {issue['issue']}")
        else:
            print("✅ Aucun problème évident détecté")

        return issues_by_type

    def generate_report(self):
        """Génère un rapport final"""
        print(f"\n{'='*70}")
        print("RAPPORT FINAL")
        print('='*70)

        print(f"\nTests effectués: {self.test_count}")
        print(f"Erreurs trouvées: {len(self.errors_found)}")

        if self.errors_found:
            print(f"\n❌ ERREURS À CORRIGER:\n")
            for i, error in enumerate(self.errors_found, 1):
                print(f"{i}. TEST: {error['test']}")
                print(f"   MESSAGE: {error['error']}")
                print(f"   TRACEBACK:")
                for line in error['traceback'].split('\n'):
                    if line.strip():
                        print(f"      {line}")
                print()
        else:
            print("\n✅ Aucune erreur détectée!")

        # Sauvegarder le rapport
        report_file = Path("error_report.txt")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("RAPPORT D'ERREURS - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
            f.write("="*70 + "\n\n")

            f.write(f"Tests effectués: {self.test_count}\n")
            f.write(f"Erreurs trouvées: {len(self.errors_found)}\n\n")

            if self.errors_found:
                f.write("ERREURS DÉTECTÉES:\n\n")
                for i, error in enumerate(self.errors_found, 1):
                    f.write(f"{i}. TEST: {error['test']}\n")
                    f.write(f"   MESSAGE: {error['error']}\n")
                    f.write(f"   TIMESTAMP: {error['timestamp']}\n")
                    f.write(f"   TRACEBACK:\n")
                    f.write(error['traceback'] + "\n\n")

        print(f"\n📄 Rapport sauvegardé dans: {report_file}")


def main():
    print("="*70)
    print("TEST AUTOMATISÉ - DÉTECTION D'ERREURS")
    print("="*70)

    tester = ErrorTester()

    # Test 1: Startup
    startup_ok = tester.test_startup()

    # Analyse statique
    tester.analyze_codebase()

    # Rapport final
    tester.generate_report()

    print(f"\n{'='*70}")
    print("INSTRUCTIONS POUR LA SUITE:")
    print('='*70)
    print("\n1. Copiez le contenu de 'error_report.txt'")
    print("2. Envoyez-le moi pour que je corrige les erreurs")
    print("3. Relancez ce script après chaque correction")
    print(f"\nCommande: py -3.11 auto_test_errors.py\n")


if __name__ == "__main__":
    main()
