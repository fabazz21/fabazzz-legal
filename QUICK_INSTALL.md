# Quick Install Scripts

## Windows - install.bat

```batch
@echo off
echo ================================
echo Projector Fusion - Installation
echo ================================
echo.

echo Mise a jour de pip...
python -m pip install --upgrade pip

echo.
echo Installation de pygame (pre-compile)...
pip install pygame==2.5.2 --only-binary :all:

echo.
echo Installation des autres dependances...
pip install moderngl==5.10.0
pip install numpy==1.26.4
pip install pyrr==0.10.3
pip install imgui[pygame]==2.0.0
pip install Pillow==10.2.0

echo.
echo ================================
echo Installation terminee !
echo ================================
echo.
echo Pour lancer l'application :
echo python main.py
pause
```

## Linux/macOS - install.sh

```bash
#!/bin/bash

echo "================================"
echo "Projector Fusion - Installation"
echo "================================"
echo ""

# Détecter l'OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Détection : Linux"
    echo "Installation des dépendances système..."
    sudo apt-get update
    sudo apt-get install -y python3-dev python3-pip
    sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
    sudo apt-get install -y libfreetype6-dev libportmidi-dev libjpeg-dev
    sudo apt-get install -y libgl1-mesa-dev libglu1-mesa-dev
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Détection : macOS"
    echo "Installation des dépendances avec Homebrew..."
    brew install python3 sdl2 sdl2_image sdl2_mixer sdl2_ttf portmidi
fi

echo ""
echo "Création d'un environnement virtuel..."
python3 -m venv venv
source venv/bin/activate

echo ""
echo "Mise à jour de pip..."
pip install --upgrade pip

echo ""
echo "Installation des dépendances Python..."
pip install -r requirements.txt

echo ""
echo "================================"
echo "Installation terminée !"
echo "================================"
echo ""
echo "Pour activer l'environnement :"
echo "source venv/bin/activate"
echo ""
echo "Pour lancer l'application :"
echo "python main.py"
```

## Créer les scripts

### Windows
Créez un fichier `install.bat` avec le contenu ci-dessus, puis double-cliquez dessus.

### Linux/macOS
```bash
# Créer le script
cat > install.sh << 'EOF'
[coller le contenu du script ci-dessus]
EOF

# Rendre exécutable
chmod +x install.sh

# Lancer
./install.sh
```

## Installation rapide avec pip uniquement

### Option 1 : Versions spécifiques (stable)
```bash
pip install pygame==2.5.2 --only-binary :all:
pip install moderngl==5.10.0 numpy==1.26.4 pyrr==0.10.3 Pillow==10.2.0
pip install imgui[pygame]==2.0.0
```

### Option 2 : Dernières versions compatibles
```bash
pip install --upgrade pip
pip install pygame --only-binary :all:
pip install moderngl numpy pyrr Pillow
pip install imgui[pygame]
```
