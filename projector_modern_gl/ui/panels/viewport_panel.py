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
            camera = self.ui.app.camera
            renderer = self.ui.app.renderer

            # Camera settings
            if imgui.collapsing_header("Camera", imgui.TREE_NODE_DEFAULT_OPEN)[0]:
                # FOV
                changed, camera.fov = imgui.slider_float(
                    "FOV", camera.fov, 20.0, 120.0, "%.1f°"
                )

                # Near/Far planes
                changed, camera.near = imgui.slider_float(
                    "Near Plane", camera.near, 0.01, 10.0, "%.2f"
                )

                changed, camera.far = imgui.slider_float(
                    "Far Plane", camera.far, 10.0, 1000.0, "%.1f"
                )

                # Orbit controls
                imgui.text("Orbit Controls")
                changed, camera.azimuth = imgui.slider_float(
                    "Azimuth", camera.azimuth, -180.0, 180.0, "%.1f°"
                )

                changed, camera.elevation = imgui.slider_float(
                    "Elevation", camera.elevation, -89.0, 89.0, "%.1f°"
                )

                changed, camera.distance = imgui.slider_float(
                    "Distance", camera.distance, 1.0, 100.0, "%.1f"
                )

                if imgui.button("Reset Camera"):
                    camera.reset()

            # Rendering settings
            if imgui.collapsing_header("Rendering")[0]:
                # Wireframe mode
                if hasattr(renderer, 'wireframe_mode'):
                    changed, renderer.wireframe_mode = imgui.checkbox(
                        "Wireframe", renderer.wireframe_mode
                    )

                # Shadow quality
                if imgui.tree_node("Shadow Quality"):
                    shadow_sizes = [512, 1024, 2048, 4096]
                    shadow_labels = ["512x512", "1024x1024", "2048x2048", "4096x4096"]

                    current_size = renderer.shadow_map_size
                    current_idx = shadow_sizes.index(current_size) if current_size in shadow_sizes else 2

                    changed, selected = imgui.combo(
                        "Shadow Map Size",
                        current_idx,
                        shadow_labels
                    )

                    if changed:
                        renderer.shadow_map_size = shadow_sizes[selected]
                        # TODO: Recreate shadow maps

                    imgui.tree_pop()

                # Background color
                changed, bg_color = imgui.color_edit3("Background", *renderer.background_color)
                if changed:
                    renderer.background_color = list(bg_color)

            # Frustum visualization
            if imgui.collapsing_header("Visualization")[0]:
                if hasattr(renderer, 'show_frustums'):
                    changed, renderer.show_frustums = imgui.checkbox(
                        "Show Projector Frustums", renderer.show_frustums
                    )

                if hasattr(self.ui.app.scene, 'show_grid'):
                    changed, self.ui.app.scene.show_grid = imgui.checkbox(
                        "Show Grid", self.ui.app.scene.show_grid
                    )

                # Gizmos
                imgui.text("Gizmos: (TODO)")

            # Performance stats
            if imgui.collapsing_header("Performance")[0]:
                fps = self.ui.app.clock.get_fps() if hasattr(self.ui.app, 'clock') else 0
                imgui.text(f"FPS: {fps:.1f}")

                # Draw calls (if tracked)
                if hasattr(renderer, 'stats'):
                    imgui.text(f"Draw calls: {renderer.stats.get('draw_calls', 0)}")
                    imgui.text(f"Triangles: {renderer.stats.get('triangles', 0)}")

        imgui.end()
