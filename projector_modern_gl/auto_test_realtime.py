#!/usr/bin/env python3
"""
TEST AUTOMATISÉ TEMPS RÉEL
Lance l'app plusieurs fois, capture TOUTES les erreurs
Teste jusqu'à ce que l'app tourne 10 secondes sans crash
"""

import subprocess
import time
import sys
import re
from pathlib import Path
from datetime import datetime

class RealtimeAppTester:
    def __init__(self):
        self.all_errors = []
        self.test_runs = []
        self.max_attempts = 10
        self.success_duration = 10  # secondes sans crash = succès
        self.report_file = Path("complete_error_report.txt")

        # Charger les erreurs existantes si le rapport existe
        self.load_existing_errors()

    def load_existing_errors(self):
        """Charge les erreurs du rapport précédent s'il existe"""
        if not self.report_file.exists():
            return

        print("[INFO] Chargement des erreurs du rapport précédent...")
        try:
            with open(self.report_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parser les erreurs du rapport
            # Format: "X. ErrorType\n   Message: ...\n   Fichier: ...\n"
            error_blocks = re.split(r'\n\d+\. ', content)
            for block in error_blocks[1:]:  # Skip header
                lines = block.split('\n')
                if len(lines) >= 3:
                    error_type = lines[0].strip()
                    message = None
                    file_loc = None

                    for line in lines[1:]:
                        if line.strip().startswith('Message:'):
                            message = line.split('Message:', 1)[1].strip()
                        elif line.strip().startswith('Fichier:'):
                            file_loc = line.split('Fichier:', 1)[1].strip()

                    if message:
                        self.all_errors.append({
                            'type': error_type,
                            'message': message,
                            'file': file_loc,
                            'traceback': []
                        })

            print(f"[OK] {len(self.all_errors)} erreur(s) chargée(s) du rapport précédent")
        except Exception as e:
            print(f"[WARNING] Impossible de charger le rapport: {e}")

    def run_test_cycle(self, attempt_num):
        """Lance un cycle de test"""
        print(f"\n{'='*70}")
        print(f"TEST RUN #{attempt_num}")
        print('='*70)

        start_time = time.time()
        error_found = None
        stdout_log = []
        stderr_log = []

        try:
            # Lancer l'application
            print(f"[LAUNCH] Lancement de l'application...")

            process = subprocess.Popen(
                [sys.executable, "main.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )

            # Surveiller la sortie en temps réel
            import select
            import threading

            def read_stdout():
                for line in iter(process.stdout.readline, ''):
                    if line:
                        stdout_log.append(line)
                        print(f"  OUT: {line.rstrip()}")

            def read_stderr():
                for line in iter(process.stderr.readline, ''):
                    if line:
                        stderr_log.append(line)
                        if 'error' in line.lower() or 'traceback' in line.lower():
                            print(f"  [ERROR] {line.rstrip()}")
                        else:
                            print(f"  ERR: {line.rstrip()}")

            # Threads pour lire stdout/stderr en parallèle
            stdout_thread = threading.Thread(target=read_stdout)
            stderr_thread = threading.Thread(target=read_stderr)
            stdout_thread.daemon = True
            stderr_thread.daemon = True
            stdout_thread.start()
            stderr_thread.start()

            # Attendre jusqu'à success_duration ou crash
            elapsed = 0
            while elapsed < self.success_duration:
                # Vérifier si le process est toujours vivant
                poll = process.poll()
                if poll is not None:
                    # Process terminé
                    error_found = f"Process crashed with code {poll}"
                    print(f"\n[ERROR] App crashed after {elapsed:.1f}s (code {poll})")
                    break

                time.sleep(0.5)
                elapsed = time.time() - start_time

            # Si on arrive ici et process vivant = succès
            if error_found is None and process.poll() is None:
                print(f"\n[OK] App tourne depuis {elapsed:.1f}s sans crash!")
                process.kill()
                return {
                    'success': True,
                    'duration': elapsed,
                    'stdout': stdout_log,
                    'stderr': stderr_log
                }

            # Sinon, tuer le process et analyser
            if process.poll() is None:
                process.kill()

            # Attendre que les threads finissent de lire
            time.sleep(0.5)

        except Exception as e:
            error_found = f"Exception: {str(e)}"
            print(f"[ERROR] Exception during test: {e}")

        # Analyser les erreurs
        errors = self.extract_errors(stderr_log)

        return {
            'success': False,
            'duration': time.time() - start_time,
            'error': error_found,
            'errors_found': errors,
            'stdout': stdout_log,
            'stderr': stderr_log
        }

    def extract_errors(self, stderr_lines):
        """Extrait les erreurs du stderr"""
        errors = []
        current_error = None
        traceback_lines = []

        for line in stderr_lines:
            # Détecter le début d'une traceback
            if 'Traceback (most recent call last):' in line:
                if current_error:
                    errors.append(current_error)
                current_error = {
                    'traceback': [],
                    'type': None,
                    'message': None,
                    'file': None
                }
                traceback_lines = []

            # Collecter les lignes de traceback
            if current_error is not None:
                traceback_lines.append(line)

                # Extraire fichier
                if 'File "' in line:
                    match = re.search(r'File "([^"]+)", line (\d+)', line)
                    if match and not current_error['file']:
                        current_error['file'] = f"{match.group(1)}:{match.group(2)}"

                # Extraire type d'erreur
                if ': ' in line and any(err in line for err in ['Error:', 'Exception:', 'Warning:']):
                    parts = line.split(': ', 1)
                    if len(parts) == 2:
                        current_error['type'] = parts[0].strip()
                        current_error['message'] = parts[1].strip()

                current_error['traceback'] = traceback_lines

        if current_error:
            errors.append(current_error)

        return errors

    def run_all_tests(self):
        """Lance tous les cycles de test"""
        print("="*70)
        print("TEST AUTOMATISÉ TEMPS RÉEL - DÉTECTION D'ERREURS")
        print("="*70)
        print()
        print(f"Configuration:")
        print(f"  - Maximum {self.max_attempts} tentatives")
        print(f"  - Succès = {self.success_duration}s sans crash")
        print(f"  - Relance automatique après chaque crash")

        if self.all_errors:
            print(f"  - Erreurs déjà connues: {len(self.all_errors)}")
            print(f"  - Mode: INCRÉMENTIEL (nouvelles erreurs seront ajoutées)")
        else:
            print(f"  - Mode: NOUVEAU RAPPORT")

        print()

        new_errors_count = 0

        for attempt in range(1, self.max_attempts + 1):
            result = self.run_test_cycle(attempt)
            self.test_runs.append(result)

            # Collecter les erreurs
            if not result['success'] and result.get('errors_found'):
                for error in result['errors_found']:
                    # Éviter les doublons
                    if not any(e.get('message') == error.get('message') for e in self.all_errors):
                        self.all_errors.append(error)
                        new_errors_count += 1
                        print(f"\n[NEW ERROR] Nouvelle erreur détectée: {error.get('type')}")

            # Si succès, on arrête
            if result['success']:
                print(f"\n[OK] SUCCÈS! L'application est stable.")
                break

            # Sinon, petite pause avant relance
            if attempt < self.max_attempts:
                print(f"\n[INFO] Relance dans 2 secondes...")
                time.sleep(2)

        return new_errors_count

    def generate_report(self, new_errors_count=0):
        """Génère le rapport final"""
        print("\n" + "="*70)
        print("RAPPORT FINAL")
        print("="*70)

        # Statistiques
        total_runs = len(self.test_runs)
        successful_runs = sum(1 for r in self.test_runs if r['success'])
        failed_runs = total_runs - successful_runs

        print(f"\nStatistiques:")
        print(f"  Total de tests: {total_runs}")
        print(f"  Succès: {successful_runs}")
        print(f"  Échecs: {failed_runs}")

        # Erreurs uniques trouvées
        print(f"\nErreurs totales: {len(self.all_errors)}")
        if new_errors_count > 0:
            print(f"  - Nouvelles erreurs trouvées: {new_errors_count}")
            print(f"  - Erreurs déjà connues: {len(self.all_errors) - new_errors_count}")
        else:
            print(f"  - Aucune nouvelle erreur (toutes déjà connues)")

        if self.all_errors:
            print("\n" + "="*70)
            print("LISTE DES ERREURS")
            print("="*70)

            for i, error in enumerate(self.all_errors, 1):
                print(f"\n{i}. {error.get('type', 'Unknown Error')}")
                print(f"   Message: {error.get('message', 'N/A')}")
                print(f"   Fichier: {error.get('file', 'N/A')}")
                if error.get('traceback'):
                    print(f"   Traceback ({len(error['traceback'])} lignes)")

        # Sauvegarder rapport (mode incrémentiel)
        with open(self.report_file, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("RAPPORT DE TEST AUTOMATISÉ\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*70 + "\n\n")

            f.write(f"Total de tests: {total_runs}\n")
            f.write(f"Succès: {successful_runs}\n")
            f.write(f"Échecs: {failed_runs}\n\n")

            f.write("="*70 + "\n")
            f.write(f"ERREURS UNIQUES TROUVÉES: {len(self.all_errors)}\n")
            f.write("="*70 + "\n\n")

            for i, error in enumerate(self.all_errors, 1):
                f.write(f"\n{i}. {error.get('type', 'Unknown Error')}\n")
                f.write(f"   Message: {error.get('message', 'N/A')}\n")
                f.write(f"   Fichier: {error.get('file', 'N/A')}\n\n")

                if error.get('traceback'):
                    f.write("   Traceback:\n")
                    for line in error['traceback']:
                        f.write(f"   {line}")
                    f.write("\n")

        print(f"\n[FILE] Rapport sauvegardé: {self.report_file}")
        if new_errors_count > 0:
            print(f"[FILE] {new_errors_count} nouvelle(s) erreur(s) ajoutée(s) au rapport")

        # Instructions
        print("\n" + "="*70)
        print("PROCHAINES ÉTAPES")
        print("="*70)
        print("\n1. Envoyez-moi le fichier 'complete_error_report.txt'")
        print("2. Je corrigerai TOUTES les erreurs d'un coup")
        print("3. Relancez ce script pour vérifier")
        print()

def main():
    tester = RealtimeAppTester()
    new_errors = tester.run_all_tests()
    tester.generate_report(new_errors)

if __name__ == "__main__":
    main()
