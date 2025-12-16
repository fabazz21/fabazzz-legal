"""
Main UI Manager
ImGui interface for the projection mapping application
"""

import imgui
from imgui.integrations.glfw import GlfwRenderer


class MainUI:
    """Main UI Manager"""

    def __init__(self, app):
        """
        Initialize UI

        Args:
            app: Main application instance
        """
        self.app = app

        # Initialize ImGui
        imgui.create_context()
        self.impl = GlfwRenderer(app.window.glfw_window)

        # UI state
        self.show_scene_panel = True
        self.show_properties_panel = True
        self.show_projector_panel = True
        self.show_timeline_panel = True
        self.show_viewport_settings = True
        self.show_export_panel = False
        self.show_photometric_panel = False
        self.show_demo_window = False

        # Selected objects
        self.selected_object = None
        self.selected_projector = None

        # Import panels
        from .panels.scene_panel import ScenePanel
        from .panels.properties_panel import PropertiesPanel
        from .panels.projector_panel import ProjectorPanel
        from .panels.timeline_panel import TimelinePanel
        from .panels.viewport_panel import ViewportPanel
        from .panels.export_panel import ExportPanel
        from .panels.photometric_panel import PhotometricPanel

        # Create panels
        self.scene_panel = ScenePanel(self)
        self.properties_panel = PropertiesPanel(self)
        self.projector_panel = ProjectorPanel(self)
        self.timeline_panel = TimelinePanel(self)
        self.viewport_panel = ViewportPanel(self)
        self.export_panel = ExportPanel(self)
        self.photometric_panel = PhotometricPanel(self)

        print("  ✅ UI initialized")

    def render(self):
        """Render UI (call every frame)"""
        # Start new frame
        imgui.new_frame()

        # Main menu bar
        self._render_menu_bar()

        # Panels
        if self.show_scene_panel:
            self.scene_panel.render()

        if self.show_properties_panel:
            self.properties_panel.render()

        if self.show_projector_panel:
            self.projector_panel.render()

        if self.show_timeline_panel:
            self.timeline_panel.render()

        if self.show_viewport_settings:
            self.viewport_panel.render()

        if self.show_export_panel:
            self.export_panel.render()

        if self.show_photometric_panel:
            self.photometric_panel.render()

        # Demo window (for development)
        if self.show_demo_window:
            imgui.show_demo_window()

        # Render ImGui
        imgui.render()
        self.impl.render(imgui.get_draw_data())

    def _render_menu_bar(self):
        """Render main menu bar"""
        if imgui.begin_main_menu_bar():
            # File menu
            if imgui.begin_menu("File", True):
                clicked, _ = imgui.menu_item("New Project", "Ctrl+N")
                if clicked:
                    self._new_project()

                clicked, _ = imgui.menu_item("Open Project", "Ctrl+O")
                if clicked:
                    self._open_project()

                clicked, _ = imgui.menu_item("Save Project", "Ctrl+S")
                if clicked:
                    self._save_project()

                imgui.separator()

                clicked, _ = imgui.menu_item("Export", "Ctrl+E")
                if clicked:
                    self.show_export_panel = True

                imgui.separator()

                clicked, _ = imgui.menu_item("Exit", "Alt+F4")
                if clicked:
                    self.app.running = False

                imgui.end_menu()

            # Edit menu
            if imgui.begin_menu("Edit", True):
                clicked, _ = imgui.menu_item("Undo", "Ctrl+Z", False, self.app.history.can_undo())
                if clicked:
                    self.app.history.undo()

                clicked, _ = imgui.menu_item("Redo", "Ctrl+Y", False, self.app.history.can_redo())
                if clicked:
                    self.app.history.redo()

                imgui.separator()

                clicked, _ = imgui.menu_item("Delete", "Del", False, self.selected_object is not None)
                if clicked:
                    self._delete_selected()

                imgui.end_menu()

            # View menu
            if imgui.begin_menu("View", True):
                clicked, self.show_scene_panel = imgui.menu_item(
                    "Scene", None, self.show_scene_panel
                )
                clicked, self.show_properties_panel = imgui.menu_item(
                    "Properties", None, self.show_properties_panel
                )
                clicked, self.show_projector_panel = imgui.menu_item(
                    "Projector", None, self.show_projector_panel
                )
                clicked, self.show_timeline_panel = imgui.menu_item(
                    "Timeline", None, self.show_timeline_panel
                )
                clicked, self.show_viewport_settings = imgui.menu_item(
                    "Viewport", None, self.show_viewport_settings
                )

                imgui.separator()

                clicked, self.show_photometric_panel = imgui.menu_item(
                    "Photometric Analysis", None, self.show_photometric_panel
                )

                imgui.separator()

                clicked, self.show_demo_window = imgui.menu_item(
                    "ImGui Demo", None, self.show_demo_window
                )

                imgui.end_menu()

            # Add menu
            if imgui.begin_menu("Add", True):
                if imgui.begin_menu("Projector", True):
                    # List projector models
                    from ..projectors.projector_database import get_all_projectors
                    projectors = get_all_projectors()

                    for proj in projectors:
                        clicked, _ = imgui.menu_item(proj['name'])
                        if clicked:
                            self._add_projector(proj['id'])

                    imgui.end_menu()

                if imgui.begin_menu("Object", True):
                    clicked, _ = imgui.menu_item("Cube")
                    if clicked:
                        self._add_primitive('cube')

                    clicked, _ = imgui.menu_item("Sphere")
                    if clicked:
                        self._add_primitive('sphere')

                    clicked, _ = imgui.menu_item("Plane")
                    if clicked:
                        self._add_primitive('plane')

                    clicked, _ = imgui.menu_item("Cylinder")
                    if clicked:
                        self._add_primitive('cylinder')

                    clicked, _ = imgui.menu_item("Cone")
                    if clicked:
                        self._add_primitive('cone')

                    imgui.separator()

                    clicked, _ = imgui.menu_item("Load 3D Model...")
                    if clicked:
                        self._load_3d_model()

                    imgui.end_menu()

                if imgui.begin_menu("Light", True):
                    clicked, _ = imgui.menu_item("Point Light")
                    if clicked:
                        self._add_light('point')

                    clicked, _ = imgui.menu_item("Directional Light")
                    if clicked:
                        self._add_light('directional')

                    imgui.end_menu()

                imgui.end_menu()

            # Timeline menu
            if imgui.begin_menu("Timeline", True):
                is_playing = self.app.timeline.playing

                clicked, _ = imgui.menu_item("Play" if not is_playing else "Pause", "Space")
                if clicked:
                    self.app.timeline.toggle_play_pause()

                clicked, _ = imgui.menu_item("Stop", None, False, is_playing or self.app.timeline.current_time > 0)
                if clicked:
                    self.app.timeline.stop()

                imgui.separator()

                clicked, _ = imgui.menu_item("Add Keyframe", "K")
                if clicked:
                    self._add_keyframe()

                imgui.separator()

                clicked, self.app.timeline.loop = imgui.menu_item(
                    "Loop", None, self.app.timeline.loop
                )

                imgui.end_menu()

            # Help menu
            if imgui.begin_menu("Help", True):
                clicked, _ = imgui.menu_item("About")
                if clicked:
                    pass

                imgui.end_menu()

            imgui.end_main_menu_bar()

    def _new_project(self):
        """Create new project"""
        # Clear scene
        self.app.scene.clear()
        self.app.timeline.clear_animation()
        self.selected_object = None
        self.selected_projector = None
        print("  ✅ New project created")

    def _open_project(self):
        """Open project from file"""
        # TODO: File dialog and project loading
        print("  📂 Open project dialog (TODO)")

    def _save_project(self):
        """Save project to file"""
        # TODO: File dialog and project saving
        print("  💾 Save project dialog (TODO)")

    def _add_projector(self, model_id):
        """Add projector to scene"""
        from ..projectors.projector import Projector
        from ..projectors.lens_database import get_all_lenses

        # Get first compatible lens
        lenses = get_all_lenses()
        lens_id = lenses[0]['id'] if lenses else 'standard'

        projector = Projector(model_id, lens_id, self.app.ctx)
        self.app.scene.add_projector(projector)
        self.selected_projector = projector
        print(f"  ✅ Added {projector.name}")

    def _add_primitive(self, primitive_type):
        """Add primitive object to scene"""
        from ..objects.primitives import create_primitive

        obj = create_primitive(primitive_type, self.app.ctx)
        self.app.scene.add_object(obj)
        self.selected_object = obj
        print(f"  ✅ Added {primitive_type}")

    def _add_light(self, light_type):
        """Add light to scene"""
        # TODO: Light implementation
        print(f"  💡 Add {light_type} light (TODO)")

    def _load_3d_model(self):
        """Load 3D model from file"""
        # TODO: File dialog and model loading
        print("  📦 Load 3D model dialog (TODO)")

    def _delete_selected(self):
        """Delete selected object"""
        if self.selected_object:
            self.app.scene.remove_object(self.selected_object)
            self.selected_object = None
            print("  🗑️ Object deleted")
        elif self.selected_projector:
            self.app.scene.remove_projector(self.selected_projector)
            self.selected_projector = None
            print("  🗑️ Projector deleted")

    def _add_keyframe(self):
        """Add keyframe for selected object"""
        if self.selected_object:
            self.app.timeline.add_keyframe(self.selected_object, 'position')
            print("  ✅ Keyframe added")
        elif self.selected_projector:
            self.app.timeline.add_keyframe(self.selected_projector, 'position')
            print("  ✅ Keyframe added")

    def process_inputs(self, window, key, scancode, action, mods):
        """Process keyboard inputs"""
        # Pass to ImGui first
        io = imgui.get_io()
        if io.want_capture_keyboard:
            return

        # Application shortcuts
        if action == 1:  # Key press
            # Ctrl+N - New
            if key == 78 and mods == 2:
                self._new_project()
            # Ctrl+O - Open
            elif key == 79 and mods == 2:
                self._open_project()
            # Ctrl+S - Save
            elif key == 83 and mods == 2:
                self._save_project()
            # Ctrl+Z - Undo
            elif key == 90 and mods == 2:
                if self.app.history.can_undo():
                    self.app.history.undo()
            # Ctrl+Y - Redo
            elif key == 89 and mods == 2:
                if self.app.history.can_redo():
                    self.app.history.redo()
            # Space - Play/Pause
            elif key == 32:
                self.app.timeline.toggle_play_pause()
            # K - Add keyframe
            elif key == 75:
                self._add_keyframe()
            # Delete - Delete selected
            elif key == 261:
                self._delete_selected()

    def cleanup(self):
        """Cleanup UI resources"""
        self.impl.shutdown()
