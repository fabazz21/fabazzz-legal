#!/bin/bash
set -e

echo "================================"
echo "Projector Fusion - Installation"
echo "================================"
echo ""

# Détecter l'OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Détection : Linux"
    echo ""
    echo "Installation des dépendances système..."
    sudo apt-get update -qq
    sudo apt-get install -y python3-dev python3-pip \
        libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
        libfreetype6-dev libportmidi-dev libjpeg-dev \
        libgl1-mesa-dev libglu1-mesa-dev
    echo "✅ Dépendances système installées"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Détection : macOS"
    echo ""
    if ! command -v brew &> /dev/null; then
        echo "Homebrew n'est pas installé. Installation..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    echo "Installation des dépendances avec Homebrew..."
    brew install python3 sdl2 sdl2_image sdl2_mixer sdl2_ttf portmidi
    echo "✅ Dépendances système installées"
fi

echo ""
echo "[1/5] Création d'un environnement virtuel..."
python3 -m venv venv
source venv/bin/activate
echo "✅ Environnement virtuel créé"

echo ""
echo "[2/5] Mise à jour de pip..."
pip install --upgrade pip
echo "✅ Pip mis à jour"

echo ""
echo "[3/5] Installation de pygame..."
pip install pygame==2.5.2
echo "✅ Pygame installé"

echo ""
echo "[4/5] Installation des dépendances principales..."
pip install moderngl==5.10.0 numpy==1.26.4 pyrr==0.10.3 Pillow==10.2.0
echo "✅ Dépendances principales installées"

echo ""
echo "[5/5] Installation de imgui..."
pip install imgui[pygame]==2.0.0 || pip install imgui==2.0.0
echo "✅ ImGui installé"

echo ""
echo "================================"
echo "Installation terminée avec succès !"
echo "================================"
echo ""
echo "Pour activer l'environnement virtuel :"
echo "  source venv/bin/activate"
echo ""
echo "Pour lancer l'application :"
echo "  python main.py"
echo ""
