# Guide UI - Design HTML reproduit dans ModernGL/ImGui

Ce document explique comment le design du HTML a été reproduit dans l'application ModernGL.

## 🎨 Thème et Couleurs

### Couleurs HTML (extraites du CSS)
```css
--background: #121418      (R:18, G:20, B:24)
--foreground: #eff1f5      (R:239, G:241, B:245)
--primary: #14b8a6          (R:20, G:184, B:166) ← Couleur teal principale
--primary-glow: #2dd4bf    (R:45, G:212, B:191)
--panel-bg: #16171c         (R:22, G:23, B:28)
--panel-header: #1a1b21    (R:26, G:27, B:33)
--border: #2d2f36           (R:45, G:47, B:54)
--muted: #26272e            (R:38, G:39, B:46)
--muted-foreground: #8b8d98 (R:139, G:141, B:152)
```

### Implémentation ImGui
Fichier: `ui/theme.py`

Toutes les couleurs HTML ont été converties en RGB normalisé (0.0-1.0) pour ImGui:
```python
PRIMARY = (0.078, 0.722, 0.651)  # #14b8a6 teal
BACKGROUND = (0.071, 0.078, 0.094)  # #121418
FOREGROUND = (0.937, 0.945, 0.961)  # #eff1f5
```

Le thème applique ces couleurs à tous les éléments ImGui:
- Fenêtres, panels, popups
- Boutons, sliders, checkboxes
- Tabs, headers, scrollbars
- Bordures, séparateurs

## 📐 Structure de l'Interface

### HTML (projector_TIMELINE_PROJECTOR_FIX_2.html)
```
┌────────────────────────────────────────────────────────┐
│  🎯 Logo │ Setup │ Calib │ Export │ 🎥 ➜ ↻ ⇔ ☀️ ↶ ↷  │ ← Top Bar
├─────────┬──────────────────────────────────┬───────────┤
│         │                                  │           │
│  Scene  │                                  │Properties │
│  ├─📽️   │       3D Viewport                │           │
│  ├─🧊   │                                  │Transform  │
│  ├─💡   │                                  │Material   │
│         │                                  │           │
│Projector│                                  │           │
│  Model  │                                  │           │
│  Lens   │                                  │           │
│         │                                  │           │
│Viewport │                                  │           │
│  Camera │                                  │           │
│  Grid   │                                  │           │
├─────────┴──────────────────────────────────┴───────────┤
│  Timeline ═══════════════════════════════════════════  │ ← Timeline
└────────────────────────────────────────────────────────┘
```

### ModernGL/ImGui (ui/main_ui_tabbed.py)
**Structure identique:**
- **Top Bar (40px)**: Logo, Tabs, Controls
- **Left Sidebar (320px)**: Panels contextuels selon le tab actif
- **Right Sidebar (320px)**: Propriétés de l'objet sélectionné
- **Bottom Timeline (200px)**: Animation timeline

## 🔧 Système de Tabs

### HTML
```html
<button class="nav-tab active" onclick="switchTab('setup')">Setup</button>
<button class="nav-tab" onclick="switchTab('calibration')">Calibration</button>
<button class="nav-tab" onclick="switchTab('export')">Export</button>
```

### ImGui
```python
if self.current_tab == "Setup":
    ProjectorTheme.push_primary_button()
if imgui.button("Setup"):
    self.current_tab = "Setup"
if self.current_tab == "Setup":
    ProjectorTheme.pop_primary_button()
```

### Contenu des Tabs

| Tab | HTML Panels | ImGui Panels |
|-----|-------------|--------------|
| **Setup** | Scene, Projectors, Lens, Viewport | ScenePanel, ProjectorPanel, ViewportPanel |
| **Calibration** | Correction, Advanced, Photometric | Keystone/Corner Pin, Advanced, PhotometricPanel |
| **Export** | Export Settings, Formats | ExportPanel |

## 🎮 Contrôles Gizmo

### HTML
```html
<button id="gizmo-move-btn" onclick="setGizmoMode('translate')">➜</button>
<button id="gizmo-rotate-btn" onclick="setGizmoMode('rotate')">↻</button>
<button id="gizmo-scale-btn" onclick="setGizmoMode('scale')">⇔</button>
```

### ImGui
```python
if ProjectorTheme.render_gizmo_button("➜", self.gizmo_mode == "translate", "Move (G)"):
    self.gizmo_mode = "translate"
```

**Styles:**
- Bouton actif: Couleur teal (#14b8a6) avec glow
- Bouton inactif: Gris muted (#8b8d98)
- Hover: Transition smooth vers teal

## 📹 Camera Views

### HTML
```html
<select onchange="setCameraView(this.value)">
    <option value="top">⬆️ Top</option>
    <option value="perspective">🎥 Perspective</option>
    ...
</select>
```

### ImGui
```python
camera_views = ["Perspective", "Top", "Bottom", "Front", "Back", "Left", "Right"]
clicked, current_view = imgui.combo("🎥", camera_views.index(self.camera_view), camera_views)
```

## 📋 Panels Collapsibles

### HTML
```html
<div class="collapsible-panel" id="panel-projectors">
    <div class="panel-header" onclick="togglePanel('projectors')">
        <span>Projectors</span>
    </div>
    <div class="panel-content">...</div>
</div>
```

### ImGui
```python
if imgui.collapsing_header("Projectors", imgui.TREE_NODE_DEFAULT_OPEN)[0]:
    self.projector_panel.render_content()
```

## 🔘 Boutons Stylisés

### Boutons Primaires (Teal)
```python
ProjectorTheme.push_primary_button()
if imgui.button("Add Projector"):
    # Action...
ProjectorTheme.pop_primary_button()
```

### Boutons Secondaires (Muted)
```python
ProjectorTheme.push_secondary_button()
if imgui.button("Cancel"):
    # Action...
ProjectorTheme.pop_secondary_button()
```

## 📊 Comparaison Visuelle

| Élément | HTML | ImGui | Status |
|---------|------|-------|--------|
| Couleur de fond | #121418 | (0.071, 0.078, 0.094) | ✅ Identique |
| Couleur primaire | #14b8a6 teal | (0.078, 0.722, 0.651) | ✅ Identique |
| Structure tabs | Setup/Calib/Export | Setup/Calibration/Export | ✅ Identique |
| Top bar height | 40px | 40px (menu bar) | ✅ Identique |
| Left sidebar | 320px | 320px | ✅ Identique |
| Gizmo buttons | ➜ ↻ ⇔ | ➜ ↻ ⇔ | ✅ Identique |
| Camera dropdown | Combo box | imgui.combo() | ✅ Identique |
| Panel headers | Collapsible | collapsing_header() | ✅ Identique |
| Rounded corners | 8px border-radius | 8.0 window_rounding | ✅ Identique |
| Button glow | box-shadow rgba(20,184,166,0.4) | Primary color alpha | ✅ Similaire |

## 🚀 Utilisation

### Activer la nouvelle UI
Fichier: `main.py`

**Option 1: Remplacer l'import**
```python
# Ancienne UI
# from ui.main_ui import MainUI

# Nouvelle UI avec tabs
from ui.main_ui_tabbed import MainUITabbed as MainUI
```

**Option 2: Variable de configuration**
```python
USE_TABBED_UI = True  # False pour l'ancienne UI

if USE_TABBED_UI:
    from ui.main_ui_tabbed import MainUITabbed
    self.ui = MainUITabbed(self)
else:
    from ui.main_ui import MainUI
    self.ui = MainUI(self)
```

## 🎯 Prochaines Étapes

### À implémenter:
1. ⏳ **Warp Control Panel** - Contrôles de déformation d'image
2. ⏳ **Brightness Panel** - Panneau d'ajustement luminosité
3. ⏳ **Multi-viewer System** - Vues multiples en bas de l'écran
4. ⏳ **Calculatrice Widescreen** - Calculateur d'aspect ratio
5. ⏳ **Context Menu** - Menu contextuel clic droit
6. ⏳ **Keyboard Shortcuts** - Raccourcis clavier (G, R, S, Ctrl+Z, etc.)

### Panels restants à adapter:
- [ ] `properties_panel.py` - Ajouter render_content()
- [ ] `projector_panel.py` - Ajouter render_content()
- [ ] `timeline_panel.py` - Ajouter render_content()
- [ ] `viewport_panel.py` - Ajouter render_content()
- [ ] `export_panel.py` - Ajouter render_content()
- [ ] `photometric_panel.py` - Ajouter render_content()

## 📝 Notes de Développement

### Pourquoi deux systèmes UI?
- `main_ui.py` - UI originale avec fenêtres flottantes
- `main_ui_tabbed.py` - Nouvelle UI avec tabs fixes (comme HTML)

Les deux coexistent pour permettre:
1. Test et comparaison
2. Migration progressive
3. Choix utilisateur

### Avantages du système tabbé:
✅ Plus organisé (contexte clair par tab)
✅ Moins de fenêtres flottantes
✅ Structure identique au HTML
✅ Navigation intuitive

### Limitations ImGui vs HTML/CSS:
- ❌ Pas de box-shadow natif (simulé avec couleurs alpha)
- ❌ Pas d'animations CSS (transitions figées)
- ❌ Pas de backdrop-filter blur
- ✅ Mais: Performance native, intégration OpenGL directe

## 🔗 Fichiers Importants

```
projector_modern_gl/
├── ui/
│   ├── theme.py              ← Thème HTML converti
│   ├── main_ui.py            ← UI originale
│   ├── main_ui_tabbed.py     ← Nouvelle UI avec tabs ⭐
│   └── panels/
│       ├── scene_panel.py        ← Adapté avec render_content()
│       ├── properties_panel.py
│       ├── projector_panel.py
│       ├── timeline_panel.py
│       └── ...
└── main.py                   ← Point d'entrée
```

## 💡 Astuces

### Changer les couleurs
Modifier `ui/theme.py`:
```python
PRIMARY = (0.078, 0.722, 0.651)  # Change cette valeur
```

### Ajouter un nouveau tab
Dans `main_ui_tabbed.py`:
```python
# 1. Ajouter le bouton dans _render_top_bar()
if imgui.button("Mon Tab"):
    self.current_tab = "MonTab"

# 2. Ajouter le contenu dans _render_left_sidebar()
elif self.current_tab == "MonTab":
    self._render_mon_tab_panels()

# 3. Créer la méthode
def _render_mon_tab_panels(self):
    if imgui.collapsing_header("Mon Panel")[0]:
        imgui.text("Contenu...")
```

### Debug du thème
```python
# Afficher les couleurs actuelles
style = imgui.get_style()
print(f"Button color: {style.colors[imgui.COLOR_BUTTON]}")
```

---

✅ **Résultat:** Une interface ImGui qui ressemble visuellement au HTML tout en conservant les avantages de la performance native!
