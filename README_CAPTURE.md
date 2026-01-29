# Script de Capture Automatique HTML

Ce script ouvre automatiquement le fichier `projector_TIMELINE_PROJECTOR_FIX_2.html` et capture des screenshots de toutes les fonctions en cliquant sur chaque élément interactif.

## 🚀 Installation

### 1. Installer Python (si pas déjà fait)
Télécharge Python 3.11 ou supérieur depuis https://www.python.org/

### 2. Installer Selenium
```powershell
pip install selenium
```

### 3. Installer ChromeDriver

**Option A - Installation automatique (Recommandé):**
```powershell
pip install webdriver-manager
```

Puis modifie la ligne dans `capture_html_functions.py`:
```python
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Dans __init__, remplace:
self.driver = webdriver.Chrome(options=chrome_options)
# Par:
self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
```

**Option B - Installation manuelle:**
1. Vérifie ta version de Chrome: `chrome://version/`
2. Télécharge ChromeDriver correspondant: https://chromedriver.chromium.org/downloads
3. Ajoute ChromeDriver au PATH Windows

## 📋 Utilisation

### Étape 1: Placer les fichiers
```
📁 Ton dossier/
   ├── projector_TIMELINE_PROJECTOR_FIX_2.html  ← Le fichier HTML
   └── capture_html_functions.py                ← Le script
```

### Étape 2: Lancer le script
```powershell
python capture_html_functions.py
```

### Étape 3: Attendre la capture
Le script va:
1. ✅ Ouvrir Chrome automatiquement
2. ✅ Charger le fichier HTML
3. ✅ Cliquer sur tous les boutons, menus, panneaux
4. ✅ Prendre une capture d'écran après chaque action
5. ✅ Sauvegarder toutes les images dans `html_function_captures/`

## 📸 Résultats

Les captures seront sauvegardées dans le dossier `html_function_captures/`:
```
📁 html_function_captures/
   ├── 001_initial_state.png
   ├── 002_gizmo_move_mode.png
   ├── 003_gizmo_rotate_mode.png
   ├── 004_gizmo_scale_mode.png
   ├── 005_panel_projectors_open.png
   ├── 006_panel_lens_open.png
   ├── 007_panel_correction_open.png
   ├── 008_button_...
   └── ...
```

## ⚙️ Options de Configuration

### Mode Headless (Sans fenêtre visible)
Pour lancer le script sans afficher la fenêtre Chrome, décommente cette ligne:
```python
chrome_options.add_argument('--headless')
```

### Changer le temps d'attente
Modifie le paramètre `wait_after` dans les fonctions:
```python
self.click_and_capture(btn, name, wait_after=2)  # Attendre 2 secondes
```

### Changer le dossier de sortie
```python
capturer = HTMLFunctionCapture(HTML_FILE, "mes_captures")
```

## 🐛 Dépannage

### Erreur: "chromedriver not found"
→ Installe webdriver-manager: `pip install webdriver-manager`

### Erreur: "element not clickable"
→ Le script essaiera automatiquement un clic JavaScript

### Certains éléments ne sont pas capturés
→ Augmente les temps d'attente dans le script

### Chrome ne se lance pas
→ Vérifie que Chrome est installé et à jour

## 📝 Personnalisation

Pour capturer des éléments spécifiques, ajoute des fonctions:

```python
def capture_custom_elements(self):
    """Capture tes éléments personnalisés"""
    print("\n🎨 Capturing custom elements...")

    # Exemple: capturer tous les sliders
    sliders = self.driver.find_elements(By.CSS_SELECTOR, "input[type='range']")
    for i, slider in enumerate(sliders):
        self.take_screenshot(f"slider_{i}")
```

Puis ajoute dans `capture_all()`:
```python
self.capture_custom_elements()
```

## 💡 Astuces

1. **Résolution d'écran**: Le script maximise la fenêtre automatiquement pour capturer le plus de contenu

2. **Ordre des captures**: Les captures sont numérotées dans l'ordre chronologique

3. **Relancer le script**: Tu peux relancer le script plusieurs fois, il écrasera les anciennes captures

4. **Performance**: Pour aller plus vite, réduis les `time.sleep()` dans le code

## 📧 Support

Si tu as des questions ou problèmes, vérifie:
- ✅ Python 3.11+ installé
- ✅ Selenium installé
- ✅ ChromeDriver installé
- ✅ Le fichier HTML est dans le même dossier
