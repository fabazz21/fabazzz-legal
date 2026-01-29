"""
Main UI Manager avec système de Tabs (Setup/Calibration/Export)
Reproduit exactement la structure du HTML
"""

import imgui
from imgui.integrations.glfw import GlfwRenderer
from .theme import ProjectorTheme


class MainUITabbed:
    """
    Main UI Manager avec tabs comme dans le HTML
    Structure: Setup | Calibration | Export
    """

    def __init__(self, app):
        """Initialize UI"""
        self.app = app

        # Initialize ImGui
        imgui.create_context()
        self.impl = GlfwRenderer(app.window.glfw_window)

        # Apply HTML theme
        ProjectorTheme.apply()

        # Tab system state
        self.current_tab = "Setup"  # Setup, Calibration, Export

        # Gizmo mode state
        self.gizmo_mode = "translate"  # translate, rotate, scale

        # Selected objects
        self.selected_object = None
        self.selected_projector = None

        # Camera view
        self.camera_view = "Perspective"

        # Panel visibility
        self.show_grid = True
        self.show_frustums = True
        self.show_measurements = True
        self.show_brightness_panel = False

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

        print("  ✅ Tabbed UI initialized with HTML theme")

    def render(self):
        """Render UI (call every frame)"""
        # Top bar with logo, tabs, and controls
        self._render_top_bar()

        # Left sidebar panels (based on current tab)
        self._render_left_sidebar()

        # Right sidebar (Properties)
        self._render_right_sidebar()

        # Bottom timeline
        self._render_bottom_timeline()

    def _render_top_bar(self):
        """Render top bar: Logo | Tabs | Camera | Gizmos | Grid"""
        # Use full width menu bar
        if imgui.begin_main_menu_bar():
            # Logo
            imgui.text("🎯 Projector Simulator")
            imgui.separator()

            # Tabs (Setup | Calibration | Export)
            imgui.push_style_var(imgui.STYLE_FRAME_PADDING, (12, 8))

            if self.current_tab == "Setup":
                ProjectorTheme.push_primary_button()
            if imgui.button("Setup"):
                self.current_tab = "Setup"
            if self.current_tab == "Setup":
                ProjectorTheme.pop_primary_button()

            imgui.same_line()

            if self.current_tab == "Calibration":
                ProjectorTheme.push_primary_button()
            if imgui.button("Calibration"):
                self.current_tab = "Calibration"
            if self.current_tab == "Calibration":
                ProjectorTheme.pop_primary_button()

            imgui.same_line()

            if self.current_tab == "Export":
                ProjectorTheme.push_primary_button()
            if imgui.button("Export"):
                self.current_tab = "Export"
            if self.current_tab == "Export":
                ProjectorTheme.pop_primary_button()

            imgui.pop_style_var()

            imgui.separator()

            # Camera Views Dropdown
            imgui.set_next_item_width(150)
            camera_views = ["Perspective", "Top", "Bottom", "Front", "Back", "Left", "Right"]
            clicked, current_view = imgui.combo("🎥", camera_views.index(self.camera_view), camera_views)
            if clicked:
                self.camera_view = camera_views[current_view]
                print(f"  📹 Camera view: {self.camera_view}")

            imgui.separator()

            # Gizmo buttons (Move | Rotate | Scale)
            if ProjectorTheme.render_gizmo_button("➜", self.gizmo_mode == "translate", "Move (G)"):
                self.gizmo_mode = "translate"

            imgui.same_line()

            if ProjectorTheme.render_gizmo_button("↻", self.gizmo_mode == "rotate", "Rotate (R)"):
                self.gizmo_mode = "rotate"

            imgui.same_line()

            if ProjectorTheme.render_gizmo_button("⇔", self.gizmo_mode == "scale", "Scale (S)"):
                self.gizmo_mode = "scale"

            imgui.separator()

            # Brightness button
            if imgui.button("☀️"):
                self.show_brightness_panel = not self.show_brightness_panel

            imgui.same_line()

            # Undo/Redo
            can_undo = self.app.history.can_undo()
            can_redo = self.app.history.can_redo()

            if not can_undo:
                imgui.push_style_var(imgui.STYLE_ALPHA, 0.3)

            if imgui.button("↶"):
                if can_undo:
                    self.app.history.undo()

            if not can_undo:
                imgui.pop_style_var()

            if imgui.is_item_hovered():
                imgui.set_tooltip("Undo (Ctrl+Z)")

            imgui.same_line()

            if not can_redo:
                imgui.push_style_var(imgui.STYLE_ALPHA, 0.3)

            if imgui.button("↷"):
                if can_redo:
                    self.app.history.redo()

            if not can_redo:
                imgui.pop_style_var()

            if imgui.is_item_hovered():
                imgui.set_tooltip("Redo (Ctrl+Y)")

            imgui.separator()

            # Grid toggle
            clicked, self.show_grid = imgui.checkbox("Grid", self.show_grid)
            if clicked:
                print(f"  Grid: {self.show_grid}")

            imgui.same_line()

            # Frustum toggle
            clicked, self.show_frustums = imgui.checkbox("Frustums", self.show_frustums)
            if clicked:
                self.app.renderer.show_frustums = self.show_frustums

            imgui.end_main_menu_bar()

    def _render_left_sidebar(self):
        """Render left sidebar based on current tab"""
        imgui.set_next_window_position(0, 40)  # Below top bar
        imgui.set_next_window_size(320, self.app.window.height - 250)  # Leave space for timeline

        imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 0)
        imgui.begin("Left Sidebar", False,
                   imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_RESIZE)

        if self.current_tab == "Setup":
            self._render_setup_panels()
        elif self.current_tab == "Calibration":
            self._render_calibration_panels()
        elif self.current_tab == "Export":
            self._render_export_panels()

        imgui.end()
        imgui.pop_style_var()

    def _render_setup_panels(self):
        """Render Setup tab panels"""
        # Scene panel (collapsible)
        if imgui.collapsing_header("Scene", imgui.TREE_NODE_DEFAULT_OPEN)[0]:
            self.scene_panel.render_content()

        # Projectors panel
        if imgui.collapsing_header("Projectors", imgui.TREE_NODE_DEFAULT_OPEN)[0]:
            self.projector_panel.render_content()

        # Viewport panel
        if imgui.collapsing_header("Viewport", imgui.TREE_NODE_DEFAULT_OPEN)[0]:
            self.viewport_panel.render_content()

    def _render_calibration_panels(self):
        """Render Calibration tab panels"""
        # Correction panel
        if imgui.collapsing_header("Keystone & Corner Pin", imgui.TREE_NODE_DEFAULT_OPEN)[0]:
            imgui.text("Keystone correction controls")
            imgui.text("TODO: Implement correction UI")

        # Advanced panel
        if imgui.collapsing_header("Advanced", imgui.TREE_NODE_DEFAULT_OPEN)[0]:
            imgui.text("Advanced calibration settings")
            imgui.text("TODO: Implement advanced UI")

        # Photometric panel
        if imgui.collapsing_header("Photometric Analysis")[0]:
            self.photometric_panel.render_content()

    def _render_export_panels(self):
        """Render Export tab panels"""
        if imgui.collapsing_header("Export Settings", imgui.TREE_NODE_DEFAULT_OPEN)[0]:
            self.export_panel.render_content()

    def _render_right_sidebar(self):
        """Render right sidebar (Properties)"""
        imgui.set_next_window_position(self.app.window.width - 320, 40)
        imgui.set_next_window_size(320, self.app.window.height - 250)

        imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 0)
        imgui.begin("Properties", False,
                   imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_RESIZE)

        self.properties_panel.render_content()

        imgui.end()
        imgui.pop_style_var()

    def _render_bottom_timeline(self):
        """Render bottom timeline panel"""
        imgui.set_next_window_position(0, self.app.window.height - 200)
        imgui.set_next_window_size(self.app.window.width, 200)

        imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 0)
        imgui.begin("Timeline", False,
                   imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_RESIZE)

        self.timeline_panel.render_content()

        imgui.end()
        imgui.pop_style_var()

    def shutdown(self):
        """Cleanup ImGui"""
        self.impl.shutdown()
