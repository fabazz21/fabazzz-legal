# 🔧 Guide de Dépannage - StreamDiffusion App

## ❌ Problème: Le site est inaccessible

Ne vous inquiétez pas ! Suivez ces étapes dans l'ordre :

---

## 🚀 Solution Rapide (TEST SIMPLE)

**Testez d'abord avec la version simplifiée (SANS IA) :**

```bash
cd streamdiffusion-app
./test_simple.sh
```

Puis ouvrez : **http://localhost:5002**

✅ **Si ça marche** → Le problème vient de l'installation StreamDiffusion/PyTorch
❌ **Si ça ne marche pas** → Le problème est plus basique (Python, Flask, etc.)

---

## 📋 Diagnostic Complet

### Étape 1: Vérifier le système

```bash
cd streamdiffusion-app
./diagnose.sh
```

Ce script vérifie :
- ✓ Python est installé
- ✓ Les packages sont installés
- ✓ Les ports sont disponibles
- ✓ Les fichiers existent

---

## 🔍 Problèmes Courants et Solutions

### Problème 1: "Command not found"

**Symptôme:** `./run_draw2img.sh: command not found`

**Solution:**
```bash
chmod +x run_draw2img.sh
chmod +x diagnose.sh
chmod +x test_simple.sh
./run_draw2img.sh
```

---

### Problème 2: "Python not found"

**Symptôme:** `python3: command not found`

**Solution:**
```bash
# Installer Python 3.10 ou plus récent
# Ubuntu/Debian:
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Mac (avec Homebrew):
brew install python@3.11

# Vérifier l'installation:
python3 --version
```

---

### Problème 3: "Virtual environment not found"

**Symptôme:** Message d'erreur sur le venv

**Solution:**
```bash
cd streamdiffusion-app

# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement
source venv/bin/activate  # Linux/Mac
# OU
venv\Scripts\activate     # Windows

# Vérifier
which python  # Devrait montrer le chemin vers venv
```

---

### Problème 4: "Module not found" ou "No module named 'flask'"

**Symptôme:** Erreurs d'import Python

**Solution Minimale (pour tester):**
```bash
# Installer uniquement les packages de base
pip3 install flask flask-cors pillow numpy

# Puis tester avec la version simple
cd streamdiffusion-app
python3 backend/server_draw2img_simple.py
```

**Solution Complète (pour l'IA):**
```bash
cd streamdiffusion-app
source venv/bin/activate

# Installer PyTorch (CPU version pour tester)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Installer les autres dépendances
cd backend
pip install -r requirements.txt
```

---

### Problème 5: "Port already in use"

**Symptôme:** `Address already in use` ou port 5002 occupé

**Solution:**
```bash
# Trouver le processus qui utilise le port
lsof -i :5002
# OU
netstat -ano | grep :5002

# Tuer le processus (remplacer PID par le numéro trouvé)
kill -9 PID

# OU changer le port
export PORT=5003
python3 backend/server_draw2img_simple.py
# Puis ouvrir http://localhost:5003
```

---

### Problème 6: "No module named 'streamdiffusion'"

**Symptôme:** Erreur lors du lancement du serveur complet

**Solution:**

**Option A - Utiliser la version simple (RECOMMANDÉ pour tester):**
```bash
cd streamdiffusion-app
./test_simple.sh
```

**Option B - Installer StreamDiffusion:**
```bash
source venv/bin/activate

# Installer les dépendances
pip install git+https://github.com/cumulo-autumn/StreamDiffusion.git
# OU
pip install streamdiffusion

# Note: Cela nécessite PyTorch et peut être complexe
```

---

### Problème 7: Page blanche / Nothing loads

**Symptôme:** Le serveur démarre mais la page est vide

**Solutions:**

1. **Vérifier que le serveur tourne:**
```bash
# Dans un autre terminal
curl http://localhost:5002
# Devrait retourner du HTML
```

2. **Vérifier la console du navigateur:**
   - Ouvrir les outils de développement (F12)
   - Onglet "Console"
   - Chercher les erreurs en rouge

3. **Vérifier que les fichiers existent:**
```bash
ls -la frontend/draw2img/
# Devrait montrer: index.html, style.css, app.js
```

4. **Tester avec un autre navigateur:**
   - Chrome (recommandé)
   - Firefox
   - Edge

---

### Problème 8: CUDA / GPU errors

**Symptôme:** Erreurs mentionnant CUDA, GPU, NVIDIA

**Solution - Utiliser le CPU:**
```bash
# Éditer le fichier serveur pour forcer CPU
# Dans backend/server_draw2img.py, changer:
device = "cpu"  # Au lieu de "cuda"

# OU utiliser la version simple sans GPU
./test_simple.sh
```

---

## 🎯 Plan d'Action Étape par Étape

### Niveau 1: Test Basique (5 minutes)

```bash
# 1. Aller dans le dossier
cd streamdiffusion-app

# 2. Tester la version simple
./test_simple.sh

# 3. Ouvrir http://localhost:5002
```

**Si ça marche ✅** → Passez au Niveau 2
**Si ça ne marche pas ❌** → Vérifiez Python et pip (voir Problème 2)

---

### Niveau 2: Installation Propre (15 minutes)

```bash
# 1. Créer environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 2. Installer packages minimaux
pip install --upgrade pip
pip install flask flask-cors pillow numpy

# 3. Tester la version simple
python3 backend/server_draw2img_simple.py

# 4. Ouvrir http://localhost:5002
```

**Si ça marche ✅** → Vous pouvez utiliser la version simple
**Si vous voulez l'IA ✅** → Passez au Niveau 3

---

### Niveau 3: Installation Complète avec IA (30-60 minutes)

```bash
# 1. Environnement virtuel actif
source venv/bin/activate

# 2. Installer PyTorch (choisir selon votre GPU)

# Pour CPU uniquement:
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Pour GPU NVIDIA (CUDA 11.8):
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# 3. Installer les autres dépendances
cd backend
pip install -r requirements.txt

# 4. Installer StreamDiffusion
pip install streamdiffusion
# OU
pip install git+https://github.com/cumulo-autumn/StreamDiffusion.git

# 5. Lancer le serveur complet
cd ..
./run_draw2img.sh

# 6. Ouvrir http://localhost:5002
```

---

## 💡 Astuces pour Déboguer

### Voir les logs en temps réel

```bash
# Lancer avec verbose logging
python3 backend/server_draw2img_simple.py --debug

# Ou regarder les erreurs
python3 backend/server_draw2img_simple.py 2>&1 | tee debug.log
```

### Tester uniquement le frontend

```bash
# Installer un serveur HTTP simple
python3 -m http.server 8000 --directory frontend/draw2img

# Ouvrir http://localhost:8000
# (Ne fonctionnera pas complètement sans backend)
```

### Vérifier les connexions réseau

```bash
# Vérifier que le serveur écoute
netstat -an | grep 5002
# OU
lsof -i :5002

# Devrait montrer LISTEN
```

---

## 📞 Checklist de Dépannage

Avant de demander de l'aide, vérifiez :

- [ ] Python 3.10+ est installé (`python3 --version`)
- [ ] pip fonctionne (`pip3 --version`)
- [ ] Vous êtes dans le bon dossier (`ls` montre backend/ frontend/)
- [ ] Les fichiers existent (`ls frontend/draw2img/index.html`)
- [ ] Le port 5002 est libre (`lsof -i :5002` ne retourne rien)
- [ ] Vous avez essayé `./test_simple.sh`
- [ ] Vous avez regardé les erreurs dans le terminal
- [ ] Vous avez regardé la console du navigateur (F12)

---

## 🆘 Commandes Rapides de Réparation

### Reset Complet

```bash
cd streamdiffusion-app

# Supprimer l'environnement virtuel
rm -rf venv

# Recréer
python3 -m venv venv
source venv/bin/activate

# Réinstaller minimal
pip install flask flask-cors pillow numpy

# Tester
./test_simple.sh
```

### Test Ultra-Minimal

```bash
# Créer un fichier test.py
cat > test_server.py << 'EOF'
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Test OK!</h1>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
EOF

# Installer Flask
pip3 install flask

# Lancer
python3 test_server.py

# Ouvrir http://localhost:5002
# Si vous voyez "Test OK!" → Flask fonctionne!
```

---

## 🌟 Versions Alternatives

### Version 1: Simple (SANS IA)
```bash
./test_simple.sh
```
- ✅ Fonctionne immédiatement
- ✅ Pas besoin de GPU
- ✅ Installation rapide
- ❌ Pas d'IA (juste des filtres)

### Version 2: Serveur de Développement
```bash
cd frontend/draw2img
python3 -m http.server 5002
```
- ✅ Test rapide du frontend
- ❌ Pas de backend / pas de génération

### Version 3: Complète (AVEC IA)
```bash
./run_draw2img.sh
```
- ✅ IA complète avec StreamDiffusion
- ✅ Génération réaliste
- ❌ Installation complexe
- ❌ Nécessite GPU pour être rapide

---

## 📚 Ressources Supplémentaires

### Fichiers de Log

Les logs sont affichés dans le terminal où vous avez lancé le serveur.

Pour sauvegarder :
```bash
python3 backend/server_draw2img_simple.py > logs.txt 2>&1
```

### Versions de Packages

```bash
# Voir ce qui est installé
pip list

# Versions recommandées:
# flask >= 3.0.0
# pillow >= 10.0.0
# numpy >= 1.24.0
```

---

## ✅ Test de Fonctionnement

### Test 1: Le serveur démarre

```bash
./test_simple.sh

# Vous devriez voir:
# "Starting server on http://localhost:5002"
# "Running on http://0.0.0.0:5002"
```

### Test 2: La page s'ouvre

```
Ouvrir http://localhost:5002

Vous devriez voir:
- Titre "StreamDiffusion"
- Canvas blanc à gauche
- Image noire à droite
- Palette de couleurs
```

### Test 3: Le dessin fonctionne

```
1. Cliquer sur une couleur
2. Dessiner sur le canvas blanc
3. Vous devriez voir vos traits
```

### Test 4: La transformation fonctionne

```
Version simple:
1. Taper "blur" dans le prompt
2. Cliquer "Apply Style"
3. L'image de droite devrait être floue

Version IA:
1. Dessiner un visage simple
2. Taper "anime character"
3. Voir la transformation IA
```

---

## 🎉 C'est Résolu !

Si vous voyez le canvas et pouvez dessiner → **Succès!** 🎨

- **Version simple** → Fonctionnel pour tester
- **Version IA** → Installation avancée nécessaire

---

## 💬 Besoin d'Aide Supplémentaire?

**Informations à fournir:**

1. Système d'exploitation:
2. Version Python (`python3 --version`):
3. Message d'erreur complet (copier-coller du terminal):
4. Résultat de `./diagnose.sh`:
5. Le `./test_simple.sh` fonctionne-t-il ? (oui/non):

---

**Bonne chance ! 🚀**
