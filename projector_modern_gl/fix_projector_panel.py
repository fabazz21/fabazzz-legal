#!/usr/bin/env python3
"""
Ajoute les méthodes manquantes au ProjectorPanel
- _render_create_modal() pour créer des projecteurs
- _render_projector_list() pour afficher la liste
- Bouton "Create Projector"
"""

from pathlib import Path

def add_projector_creation_methods():
    """Ajoute les méthodes de création de projecteur"""

    file_path = Path("ui/panels/projector_panel.py")

    if not file_path.exists():
        print("[ERROR] projector_panel.py non trouvé!")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Vérifier si déjà ajouté
    content = ''.join(lines)
    if '_render_create_modal' in content:
        print("[OK] Méthodes déjà présentes")
        return True

    # Trouver où insérer (après __init__)
    insert_index = None
    for i, line in enumerate(lines):
        if 'def __init__(self, ui):' in line:
            # Trouver la fin de __init__
            for j in range(i, len(lines)):
                if j > i and lines[j].strip() and not lines[j].startswith('        '):
                    insert_index = j
                    break
            break

    if insert_index is None:
        print("[ERROR] Impossible de trouver où insérer")
        return False

    # Code à insérer après __init__
    new_code = '''
        # Modal state for creating projectors
        self.show_create_modal = False
        self.selected_brand = 0
        self.selected_model = 0
        self.selected_lens = 0
        self.projector_name = "New Projector"
'''

    # Insérer dans __init__
    init_end = insert_index - 1
    lines.insert(init_end, new_code)

    # Maintenant ajouter les nouvelles méthodes après render_content
    for i, line in enumerate(lines):
        if 'def render_content(self):' in line:
            # Trouver la fin de render_content
            for j in range(i, len(lines)):
                if j > i and 'def ' in lines[j] and lines[j].startswith('    def '):
                    insert_index = j
                    break
            break

    # Nouvelles méthodes à ajouter
    methods_code = '''
    def _render_projector_list(self):
        """Render list of projectors with create button"""
        imgui.text("Projectors in Scene:")
        imgui.separator()

        scene = self.ui.app.scene

        # Create button
        if imgui.button("+ Create Projector", -1, 30):
            self.show_create_modal = True

        imgui.spacing()

        # List projectors
        if len(scene.projectors) == 0:
            imgui.text_colored("No projectors", 0.6, 0.6, 0.6)
        else:
            for proj in scene.projectors:
                selected = (self.ui.selected_projector == proj)
                if imgui.selectable(f"[PROJECTOR] {proj.name}", selected)[0]:
                    self.ui.selected_projector = proj
                    self.ui.selected_object = None

    def _render_create_modal(self):
        """Render modal for creating a new projector"""
        if not self.show_create_modal:
            return

        # Open modal
        imgui.open_popup("Create Projector")

        # Modal window
        if imgui.begin_popup_modal("Create Projector", True, imgui.WINDOW_ALWAYS_AUTO_RESIZE)[0]:
            imgui.text("Create a new projector in the scene")
            imgui.separator()
            imgui.spacing()

            # Projector name
            changed, self.projector_name = imgui.input_text(
                "Name",
                self.projector_name,
                256
            )

            imgui.spacing()

            # Brand selection
            brands = ["Epson", "Barco", "Christie", "Panasonic", "Sony", "NEC"]
            changed, self.selected_brand = imgui.combo(
                "Brand",
                self.selected_brand,
                brands
            )

            # Model selection (depends on brand)
            models = self._get_models_for_brand(brands[self.selected_brand])
            changed, self.selected_model = imgui.combo(
                "Model",
                self.selected_model,
                models
            )

            # Lens selection
            lenses = ["Standard", "Short Throw", "Long Throw", "Ultra Short Throw"]
            changed, self.selected_lens = imgui.combo(
                "Lens",
                self.selected_lens,
                lenses
            )

            imgui.spacing()
            imgui.separator()
            imgui.spacing()

            # Buttons
            if imgui.button("Create", 120, 30):
                self._create_projector(
                    brands[self.selected_brand],
                    models[self.selected_model]
                )
                self.show_create_modal = False
                imgui.close_current_popup()

            imgui.same_line()

            if imgui.button("Cancel", 120, 30):
                self.show_create_modal = False
                imgui.close_current_popup()

            imgui.end_popup()

    def _get_models_for_brand(self, brand):
        """Get projector models for a brand"""
        models_db = {
            "Epson": ["EB-L1505U", "EB-PU1007", "EB-L25000U", "EB-800F"],
            "Barco": ["UDX-4K32", "G60-W10", "F90-4K13", "UDM-W40"],
            "Christie": ["D13WU-HS", "D20WU-HS", "DHD850-GS", "CP4330-RGB"],
            "Panasonic": ["PT-RZ21K", "PT-RQ50K", "PT-MZ16K", "PT-VMZ60"],
            "Sony": ["VPL-FHZ131L", "VPL-GTZ380", "SRX-R815P", "VPL-XW7000"],
            "NEC": ["PX2000UL", "PH3501QL", "PV800UL", "PA1004UL"]
        }
        return models_db.get(brand, ["Generic Model"])

    def _create_projector(self, brand, model):
        """Create a new projector and add it to the scene"""
        from projectors.projector import Projector
        from projectors.projector_database import PROJECTOR_DATABASE
        from projectors.lens_database import LENS_DATABASE

        # Find projector config
        proj_config = None
        for config in PROJECTOR_DATABASE:
            if config['brand'] == brand and config['name'] == model:
                proj_config = config
                break

        if proj_config is None:
            # Use first available config
            proj_config = PROJECTOR_DATABASE[0] if PROJECTOR_DATABASE else None

        if proj_config is None:
            print("[ERROR] No projector config found")
            return

        # Find lens config
        lens_config = LENS_DATABASE[0] if LENS_DATABASE else None

        if lens_config is None:
            print("[ERROR] No lens config found")
            return

        # Create projector
        projector = Projector(
            self.ui.app.ctx,
            config=proj_config,
            lens_config=lens_config,
            name=self.projector_name
        )

        # Position it in front of camera
        projector.position = [0, 2, 5]

        # Add to scene
        self.ui.app.scene.add_projector(projector)

        # Select it
        self.ui.selected_projector = projector

        print(f"[OK] Created projector: {self.projector_name}")

'''

    # Insérer les méthodes
    lines.insert(insert_index, methods_code)

    # Maintenant modifier render_content pour afficher la liste
    new_render_content = '''    def render_content(self):
        """Render projector panel content (without window wrapper)"""
        # Render create modal if open
        self._render_create_modal()

        proj = self.ui.selected_projector

        if proj is None:
            # Show projector list when none selected
            self._render_projector_list()
        else:
            # Show back button
            if imgui.button("< Back to List"):
                self.ui.selected_projector = None
            imgui.separator()

            self._render_projector_controls(proj)
'''

    # Remplacer render_content
    for i, line in enumerate(lines):
        if 'def render_content(self):' in line:
            # Trouver la fin de la méthode
            end_index = i + 1
            indent_count = 0
            for j in range(i + 1, len(lines)):
                if lines[j].strip() and not lines[j].startswith('        '):
                    end_index = j
                    break

            # Remplacer
            lines[i:end_index] = [new_render_content + '\n']
            break

    # Écrire le fichier
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print("[OK] Méthodes ajoutées à projector_panel.py!")
    return True

if __name__ == "__main__":
    print("="*70)
    print("AJOUT DES MÉTHODES DE CRÉATION DE PROJECTEUR")
    print("="*70)
    print()

    success = add_projector_creation_methods()

    if success:
        print()
        print("[OK] Modifications terminées!")
        print()
        print("Maintenant vous pouvez:")
        print("  1. Lancer l'application: py -3.11 main.py")
        print("  2. Cliquer sur '+ Create Projector'")
        print("  3. Choisir marque, modèle, lentille")
        print("  4. Créer votre projecteur!")
    else:
        print()
        print("[ERROR] Échec de la modification")
        print("Vérifiez que le fichier ui/panels/projector_panel.py existe")
