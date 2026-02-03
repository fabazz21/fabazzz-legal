"""
Viewport Settings Panel
Camera and rendering settings
"""

import imgui


class ViewportPanel:
    """Viewport settings panel"""

    def __init__(self, ui):
        """Initialize viewport panel"""
        self.ui = ui

    def render(self):
        """Render viewport panel"""
        imgui.set_next_window_size(300, 350, imgui.FIRST_USE_EVER)
        imgui.set_next_window_position(320, 30, imgui.FIRST_USE_EVER)

        expanded, opened = imgui.begin("Viewport Settings", True)
        if not opened:
            self.ui.show_viewport_settings = False
            imgui.end()
            return

        if expanded:
            self.render_content()

        imgui.end()

    def render_content(self):
        """Render viewport panel content (without window wrapper)"""
        camera = self.ui.app.camera
        renderer = self.ui.app.renderer
        scene = self.ui.app.scene

        # Camera settings
        if imgui.collapsing_header("Camera", imgui.TREE_NODE_DEFAULT_OPEN)[0]:
            # FOV
            changed, new_fov = imgui.slider_float(
                "FOV", camera.fov, 20.0, 120.0, "%.1f°"
            )
            if changed:
                camera.fov = new_fov

            # Near/Far planes
            changed, new_near = imgui.slider_float(
                "Near Plane", camera.near, 0.01, 10.0, "%.2f"
            )
            if changed:
                camera.near = new_near

            changed, new_far = imgui.slider_float(
                "Far Plane", camera.far, 10.0, 1000.0, "%.1f"
            )
            if changed:
                camera.far = new_far

            # Orbit controls
            imgui.separator()
            imgui.text("Orbit Controls")

            changed, new_azimuth = imgui.slider_float(
                "Azimuth", camera.azimuth, -180.0, 180.0, "%.1f°"
            )
            if changed:
                camera.azimuth = new_azimuth

            changed, new_elevation = imgui.slider_float(
                "Elevation", camera.elevation, -89.0, 89.0, "%.1f°"
            )
            if changed:
                camera.elevation = new_elevation

            changed, new_distance = imgui.slider_float(
                "Distance", camera.distance, 1.0, 100.0, "%.1f"
            )
            if changed:
                camera.distance = new_distance

            imgui.separator()
            if imgui.button("Reset Camera"):
                camera.reset()

        # Rendering settings
        if imgui.collapsing_header("Rendering")[0]:
            # Background color
            changed, bg_color = imgui.color_edit3("Background", *renderer.background_color)
            if changed:
                renderer.background_color = list(bg_color)

            imgui.separator()

            # Shadow quality
            if imgui.tree_node("Shadow Quality"):
                shadow_sizes = [512, 1024, 2048, 4096]
                shadow_labels = ["512x512", "1024x1024", "2048x2048", "4096x4096"]

                current_size = renderer.shadow_map_size if hasattr(renderer, 'shadow_map_size') else 2048
                current_idx = shadow_sizes.index(current_size) if current_size in shadow_sizes else 2

                changed, selected = imgui.combo(
                    "Shadow Map Size",
                    current_idx,
                    shadow_labels
                )

                if changed:
                    renderer.shadow_map_size = shadow_sizes[selected]
                    imgui.text("⚠️ Restart required")

                imgui.tree_pop()

        # Visualization
        if imgui.collapsing_header("Visualization")[0]:
            # Grid
            changed, new_grid = imgui.checkbox(
                "Show Grid", scene.show_grid if hasattr(scene, 'show_grid') else True
            )
            if changed and hasattr(scene, 'show_grid'):
                scene.show_grid = new_grid

            # Helpers
            changed, new_helpers = imgui.checkbox(
                "Show Helpers", scene.show_helpers if hasattr(scene, 'show_helpers') else True
            )
            if changed and hasattr(scene, 'show_helpers'):
                scene.show_helpers = new_helpers

            # Frustums
            changed, new_frustums = imgui.checkbox(
                "Show Frustums", scene.show_frustums if hasattr(scene, 'show_frustums') else True
            )
            if changed and hasattr(scene, 'show_frustums'):
                scene.show_frustums = new_frustums

        # Performance stats
        if imgui.collapsing_header("Performance")[0]:
            fps = self.ui.app.fps if hasattr(self.ui.app, 'fps') else 0.0
            imgui.text(f"FPS: {fps:.1f}")
            imgui.text(f"Frame: {self.ui.app.frame_count if hasattr(self.ui.app, 'frame_count') else 0}")

            imgui.separator()

            # Draw calls (if tracked)
            if hasattr(renderer, 'stats'):
                imgui.text(f"Draw calls: {renderer.stats.get('draw_calls', 0)}")
                imgui.text(f"Triangles: {renderer.stats.get('triangles', 0)}")

            # Scene info
            imgui.separator()
            imgui.text(f"Objects: {len(scene.objects) if hasattr(scene, 'objects') else 0}")
            imgui.text(f"Projectors: {len(scene.projectors) if hasattr(scene, 'projectors') else 0}")
