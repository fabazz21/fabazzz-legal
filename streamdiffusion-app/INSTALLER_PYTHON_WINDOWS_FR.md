# 🔧 Guide: Installer Python sur Windows

## ❌ PROBLÈME: "Python n'est pas reconnu"

Même après installation avec PATH coché, Python n'est pas accessible.

---

## ✅ SOLUTION RAPIDE

### Étape 1: Redémarrer le Terminal

**C'EST LA CAUSE #1 !**

```cmd
1. Fermez COMPLÈTEMENT votre invite de commande / PowerShell / Terminal
2. Réouvrez-le (pas besoin d'être admin)
3. Testez: python --version
```

Le PATH ne se met à jour que dans les NOUVEAUX terminaux !

---

### Étape 2: Redémarrer l'Ordinateur

Si l'étape 1 ne fonctionne pas:

```
1. Redémarrez complètement votre PC
2. Ouvrez un nouveau terminal
3. Testez: python --version
```

---

### Étape 3: Diagnostic

Si toujours pas de Python après redémarrage:

```cmd
cd streamdiffusion-app
diagnose_python_windows.bat
```

Ce script va:
- ✓ Chercher Python sur votre système
- ✓ Afficher où il est installé
- ✓ Vérifier le PATH
- ✓ Donner des solutions

---

## 🎯 MÉTHODE COMPLÈTE: Installation Propre

### 1. Désinstaller Python Complètement

**Panneau de Configuration:**
```
1. Panneau de configuration
2. Programmes et fonctionnalités
3. Chercher "Python 3.x"
4. Clic droit → Désinstaller
5. Faire ça pour TOUTES les versions Python
```

**Vérifier que c'est bien désinstallé:**
```cmd
where python
REM Devrait dire: "INFO: Could not find files"
```

---

### 2. Télécharger Python

**Site officiel:** https://www.python.org/downloads/

1. Cliquer sur "Download Python 3.11.x" (ou plus récent)
2. Sauvegarder le fichier `.exe`

**Version recommandée:** Python 3.11 ou 3.12

---

### 3. Installer Python CORRECTEMENT

**TRÈS IMPORTANT:**

```
1. Clic droit sur l'installateur → "Exécuter en tant qu'administrateur"

2. PREMIÈRE PAGE - COCHER LES DEUX:
   ☑ Add Python 3.11 to PATH     ← IMPORTANT !
   ☑ Install launcher for all users

3. Cliquer "Install Now" (installation standard)

4. Attendre la fin

5. À la fin, si proposé:
   ☑ Disable path length limit     ← Recommandé
   Cliquer "Close"
```

---

### 4. REDÉMARRER L'ORDINATEUR

**OBLIGATOIRE !**

```
1. Fermer tous les programmes
2. Redémarrer Windows
3. Ne pas juste "fermer la session"
```

---

### 5. Vérifier l'Installation

**Ouvrir un NOUVEAU terminal:**

```cmd
REM Test 1: Python directement
python --version
REM Devrait afficher: Python 3.11.x

REM Test 2: Pip
pip --version
REM Devrait afficher: pip 23.x.x

REM Test 3: Où est Python?
where python
REM Devrait afficher un chemin comme:
REM C:\Users\VotreNom\AppData\Local\Programs\Python\Python311\python.exe
```

**Si TOUS les tests fonctionnent → C'EST BON ! ✅**

---

## 🔴 PROBLÈMES COURANTS

### Problème 1: "python n'est pas reconnu" après redémarrage

**Cause:** PATH pas configuré correctement

**Solution:** Ajouter manuellement au PATH

```cmd
REM 1. Trouver où Python est installé
diagnose_python_windows.bat

REM 2. Noter le chemin (exemple):
REM C:\Users\VotreNom\AppData\Local\Programs\Python\Python311

REM 3. Ajouter au PATH manuellement:
```

**Ajouter au PATH (méthode manuelle):**

```
1. Touche Windows + Pause → "Paramètres système avancés"
   OU
   Clic droit "Ce PC" → Propriétés → Paramètres système avancés

2. Cliquer "Variables d'environnement"

3. Dans "Variables système" (en bas), trouver "Path"

4. Sélectionner "Path" → Cliquer "Modifier"

5. Cliquer "Nouveau" et ajouter (REMPLACER PAR VOTRE CHEMIN):
   C:\Users\VotreNom\AppData\Local\Programs\Python\Python311
   C:\Users\VotreNom\AppData\Local\Programs\Python\Python311\Scripts

6. Cliquer OK sur tout

7. REDÉMARRER l'ordinateur

8. Tester dans nouveau terminal: python --version
```

---

### Problème 2: "py" fonctionne mais pas "python"

**C'est normal !** Utilisez `py` à la place:

```cmd
REM Au lieu de:
python --version

REM Utilisez:
py --version

REM Au lieu de:
python script.py

REM Utilisez:
py script.py

REM Au lieu de:
pip install flask

REM Utilisez:
py -m pip install flask
```

**Créer un alias "python" → "py":**

```cmd
REM Créer un fichier python.bat dans C:\Windows\
REM Contenu du fichier:
@echo off
py %*
```

---

### Problème 3: Plusieurs versions de Python

**Vérifier les versions:**

```cmd
py -0
REM Affiche toutes les versions installées

REM Utiliser une version spécifique:
py -3.11 --version
py -3.10 --version
```

**Choisir la version par défaut:**

```cmd
REM Utiliser Python 3.11 par défaut:
py -3.11 -m pip install flask

REM Créer environnement virtuel avec version spécifique:
py -3.11 -m venv venv
```

---

### Problème 4: Permission refusée

**Solution:**

```cmd
REM 1. Ouvrir PowerShell EN ADMINISTRATEUR
REM Clic droit menu Démarrer → Windows PowerShell (admin)

REM 2. Autoriser les scripts:
Set-ExecutionPolicy RemoteSigned

REM 3. Réessayer l'installation
```

---

## 🎯 SOLUTION ALTERNATIVE: Microsoft Store

**Plus simple, mais peut avoir des limitations:**

```
1. Ouvrir Microsoft Store
2. Chercher "Python 3.11"
3. Cliquer "Obtenir" / "Installer"
4. Attendre la fin
5. Redémarrer le terminal
6. Tester: python --version
```

**Avantages:**
- ✅ Installation automatique
- ✅ PATH configuré automatiquement
- ✅ Mises à jour automatiques

**Inconvénients:**
- ⚠️ Peut avoir des restrictions
- ⚠️ Pas toujours la dernière version

---

## 📋 CHECKLIST COMPLÈTE

Suivez dans l'ordre:

```
☐ 1. Désinstaller Python complètement
☐ 2. Télécharger Python depuis python.org
☐ 3. Installer EN ADMIN avec "Add to PATH" COCHÉ
☐ 4. Redémarrer l'ordinateur (pas juste le terminal!)
☐ 5. Ouvrir NOUVEAU terminal
☐ 6. Tester: python --version
☐ 7. Tester: pip --version
☐ 8. Si ça ne marche pas: diagnose_python_windows.bat
```

---

## 🚀 APRÈS INSTALLATION - Lancer l'App

**Une fois Python installé et fonctionnel:**

```cmd
cd streamdiffusion-app

REM Installer les dépendances minimales
pip install flask flask-cors pillow numpy

REM OU avec py:
py -m pip install flask flask-cors pillow numpy

REM Lancer le test simple
test_simple.bat

REM Ouvrir http://localhost:5002
```

---

## 🆘 COMMANDES DE DIAGNOSTIC

### Vérification Complète

```cmd
REM Version Python
python --version
py --version

REM Version pip
pip --version
py -m pip --version

REM Où est Python?
where python
where py

REM Lister les versions
py -0

REM Tester l'import
python -c "print('Python fonctionne!')"
py -c "print('Python fonctionne!')"

REM PATH actuel
echo %PATH%
```

---

## 💡 ASTUCES

### Astuce 1: Utiliser py au lieu de python

Si `py` fonctionne mais pas `python`:

```cmd
REM Remplacer python par py partout:
py --version
py -m pip install flask
py script.py
py -m venv venv
```

### Astuce 2: Environnement virtuel

```cmd
REM Créer
py -m venv venv

REM Activer
venv\Scripts\activate

REM Vérifier
where python
REM Devrait montrer: ...\venv\Scripts\python.exe

REM Désactiver
deactivate
```

### Astuce 3: Réinitialiser PATH

Si PATH est corrompu:

```cmd
REM 1. Ouvrir PowerShell en admin
REM 2. Réinitialiser:
[Environment]::SetEnvironmentVariable("Path", $env:Path, [System.EnvironmentVariableTarget]::Machine)

REM 3. Redémarrer
```

---

## ✅ TEST FINAL

**Si tout fonctionne, vous devriez pouvoir:**

```cmd
REM Test 1
python --version
REM → Python 3.11.x (ou version installée)

REM Test 2
pip --version
REM → pip 23.x.x

REM Test 3
python -c "import flask; print('Flask OK')"
REM → Aucune erreur (après: pip install flask)
```

---

## 🎉 C'EST PRÊT!

**Une fois Python fonctionnel:**

```cmd
cd streamdiffusion-app
pip install flask flask-cors pillow numpy
python backend\server_draw2img_simple.py
```

**Ouvrir:** http://localhost:5002

---

**Bonne chance! 🚀**
