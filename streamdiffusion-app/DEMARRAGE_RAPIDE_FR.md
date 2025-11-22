# 🚀 Démarrage Rapide - StreamDiffusion App

## Option 1: TEST SIMPLE (Recommandé pour commencer) ⭐

**Fonctionne immédiatement, SANS installation complexe, SANS GPU**

```bash
cd streamdiffusion-app
./test_simple.sh
```

Ouvrez **http://localhost:5002**

✅ **Avantages:**
- Installation en 30 secondes
- Fonctionne sur n'importe quel PC
- Pas besoin de GPU/CUDA
- Parfait pour tester

❌ **Limitations:**
- Utilise des filtres simples au lieu de l'IA
- Pas de génération réaliste

### Styles disponibles (version simple):
Tapez dans le prompt:
- `blur` → Image floue
- `sharp` → Image nette
- `edge` → Détection des contours
- `emboss` → Effet relief
- `vibrant` → Couleurs vives
- `dramatic` → Contraste élevé
- `invert` → Négatif

---

## Option 2: VERSION COMPLÈTE avec IA

**Pour génération réaliste avec intelligence artificielle**

### Prérequis

- Python 3.10 ou plus récent
- GPU NVIDIA recommandé (RTX 2060 ou mieux)
- 10 GB d'espace disque
- 6 GB de VRAM (pour GPU)

### Installation

```bash
cd streamdiffusion-app

# 1. Exécuter le script d'installation
chmod +x setup.sh
./setup.sh

# 2. Attendre 5-10 minutes (télécharge les modèles IA)

# 3. Lancer le serveur
./run_draw2img.sh

# 4. Ouvrir http://localhost:5002
```

---

## 🎨 Comment Utiliser

### 1. Choisir une couleur
- Cliquer sur une couleur de la palette
- OU utiliser le sélecteur de couleur personnalisé

### 2. Dessiner
- Cliquer et glisser sur le canvas blanc (gauche)
- Ajuster la taille du pinceau avec le slider

### 3. Appliquer un style

**Version Simple:**
```
Taper "blur" ou "edge" dans le prompt
Cliquer "Apply Style"
```

**Version IA:**
```
Exemples de prompts:
- "anime character, detailed"
- "photorealistic portrait"
- "watercolor painting, soft"
- "digital art, vibrant colors"
```

### 4. Voir le résultat
L'image transformée apparaît à droite en temps réel!

---

## 📚 Guides Disponibles

- **[DEPANNAGE_FR.md](DEPANNAGE_FR.md)** → Si ça ne marche pas
- **[TUTORIAL_DRAW2IMG.md](TUTORIAL_DRAW2IMG.md)** → Guide complet (anglais)
- **[README.md](README.md)** → Documentation technique complète

---

## 🔧 Problèmes?

**Le site ne s'ouvre pas?**
```bash
./diagnose.sh   # Diagnostique le problème
./test_simple.sh  # Test avec version simple
```

**Voir le guide:** [DEPANNAGE_FR.md](DEPANNAGE_FR.md)

---

## 🌟 Les 3 Modes

L'app a 3 modes différents:

| Mode | Commande | Port | Pour |
|------|----------|------|------|
| **Texte → Image** | `./run_txt2img.sh` | 5000 | Générer depuis texte |
| **Webcam → Image** | `./run_img2img.sh` | 5001 | Transformer vidéo |
| **Dessin → Image** | `./run_draw2img.sh` | 5002 | Transformer dessins |

---

## ⚡ Exemples Rapides

### Exemple 1: Visage Simple (2 min)

**Dessiner:**
1. Cercle pour la tête
2. Deux points pour les yeux
3. Ligne pour la bouche

**Prompt (IA):** `anime character, cute, detailed`

**Résultat:** Personnage anime détaillé! 🎭

---

### Exemple 2: Paysage (3 min)

**Dessiner:**
1. Ligne ondulée verte (collines)
2. Cercle jaune (soleil)
3. Triangles verts (arbres)

**Prompt (IA):** `beautiful landscape, watercolor painting`

**Résultat:** Peinture aquarelle! 🏞️

---

### Exemple 3: Test Simple

**Dessiner:** N'importe quoi!

**Prompt (simple):** `edge`

**Résultat:** Détection des contours

---

## 💡 Conseils

1. **Commencez simple** → Formes basiques fonctionnent mieux
2. **Testez les styles** → Même dessin, styles différents
3. **Utilisez des couleurs** → Les couleurs guident l'IA
4. **Soyez patient** → Première fois = téléchargement modèles

---

## ✅ Vérification Rapide

Tout fonctionne si vous voyez:

- ✓ Canvas blanc à gauche
- ✓ Palette de couleurs
- ✓ Vous pouvez dessiner
- ✓ Image apparaît à droite

---

## 🎉 Prêt à Créer!

**Commencez maintenant:**
```bash
./test_simple.sh  # Version rapide
```

**Bon dessin! 🎨✨**
