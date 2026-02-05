# INSTALLATION GUIDE - Projector Fusion

## Installation complète selon votre système d'exploitation

### 🪟 Windows

#### Option 1 : Installation avec wheels pré-compilés (RECOMMANDÉ)

```bash
# 1. Mettre à jour pip
python -m pip install --upgrade pip

# 2. Installer pygame depuis les wheels officiels
python -m pip install pygame --only-binary :all:

# 3. Installer les autres dépendances
pip install -r requirements.txt
```

#### Option 2 : Utiliser un environnement virtuel

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
venv\Scripts\activate

# Mettre à jour pip
python -m pip install --upgrade pip

# Installer pygame
pip install pygame --only-binary :all:

# Installer les autres dépendances
pip install -r requirements.txt
```

#### Option 3 : Installer les dépendances une par une

```bash
pip install --upgrade pip
pip install pygame==2.5.2
pip install moderngl==5.10.0
pip install numpy==1.26.4
pip install pyrr==0.10.3
pip install imgui[pygame]==2.0.0
pip install Pillow==10.2.0
```

#### Problèmes courants Windows :

**Erreur "Microsoft Visual C++ 14.0 or greater is required"**
- Téléchargez et installez [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- OU utilisez `--only-binary :all:` pour forcer l'utilisation de wheels pré-compilés

**Erreur avec imgui[pygame]**
```bash
# Installer sans les extras
pip install imgui==2.0.0
pip install imgui[pygame] --no-build-isolation
```

### 🐧 Linux (Ubuntu/Debian)

```bash
# 1. Installer les dépendances système
sudo apt-get update
sudo apt-get install -y python3-dev python3-pip
sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
sudo apt-get install -y libfreetype6-dev libportmidi-dev libjpeg-dev
sudo apt-get install -y libgl1-mesa-dev libglu1-mesa-dev

# 2. Créer un environnement virtuel (optionnel mais recommandé)
python3 -m venv venv
source venv/bin/activate

# 3. Mettre à jour pip
pip install --upgrade pip

# 4. Installer les dépendances
pip install -r requirements.txt
```

### 🍎 macOS

```bash
# 1. Installer Homebrew si ce n'est pas déjà fait
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Installer les dépendances système
brew install python3 sdl2 sdl2_image sdl2_mixer sdl2_ttf portmidi

# 3. Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 4. Mettre à jour pip
pip install --upgrade pip

# 5. Installer les dépendances
pip install -r requirements.txt
```

## 🔍 Vérifier l'installation

```bash
# Tester l'import de pygame
python -c "import pygame; print(f'Pygame {pygame.version.ver} OK')"

# Tester l'import de moderngl
python -c "import moderngl; print('ModernGL OK')"

# Tester l'import de imgui
python -c "import imgui; print('ImGui OK')"

# Tester tous les imports du projet
python -c "from projector_modern_gl.core import Window, Camera, Scene, Renderer; print('All imports OK')"
```

## 🚀 Lancer l'application

```bash
python main.py
```

## ⚠️ Problèmes connus et solutions

### Erreur : "No module named 'pygame'"
```bash
pip install pygame --upgrade --force-reinstall
```

### Erreur : "OpenGL context creation failed"
- Vérifiez que vos drivers graphiques sont à jour
- Vérifiez que votre carte graphique supporte OpenGL 3.3+
- Essayez de lancer avec :
  ```bash
  python main.py --no-vsync
  ```

### Erreur : "Failed to load GL library"
**Windows :** Installez les derniers drivers graphiques
**Linux :**
```bash
sudo apt-get install mesa-utils
glxinfo | grep "OpenGL version"
```

### Performance faible
- Réduisez la résolution de la fenêtre dans `main.py`
- Désactivez les shadow maps dans le renderer
- Réduisez le nombre de projecteurs actifs

## 📦 Installation minimale (sans UI)

Si vous voulez juste tester le rendu sans l'interface :

```bash
pip install moderngl pygame numpy pyrr
```

## 🐍 Versions Python supportées

- Python 3.8+
- Python 3.9 ✅ (Recommandé)
- Python 3.10 ✅ (Recommandé)
- Python 3.11 ✅
- Python 3.12 ⚠️ (Certaines dépendances peuvent nécessiter des wheels spécifiques)

## 💡 Conseils

1. **Utilisez toujours un environnement virtuel**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

2. **Gardez pip à jour**
   ```bash
   python -m pip install --upgrade pip
   ```

3. **Vérifiez votre version de Python**
   ```bash
   python --version
   ```

4. **Si tout échoue, essayez Anaconda/Miniconda**
   ```bash
   conda create -n projector python=3.10
   conda activate projector
   conda install pygame numpy
   pip install moderngl pyrr imgui[pygame] Pillow
   ```

## 📞 Besoin d'aide ?

Si vous rencontrez toujours des problèmes :
1. Vérifiez les issues GitHub
2. Postez votre erreur complète avec :
   - Votre OS et version
   - Votre version de Python
   - Le message d'erreur complet
