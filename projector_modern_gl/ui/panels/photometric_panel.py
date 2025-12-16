"""
Photometric Analysis Panel
Calculate and display illuminance, luminance, and projection coverage
"""

import imgui


class PhotometricPanel:
    """Photometric analysis panel"""

    def __init__(self, ui):
        """Initialize photometric panel"""
        self.ui = ui
        self.analysis_distance = 5.0
        self.screen_width = 4.0
        self.screen_height = 2.25
        self.screen_gain = 1.0

    def render(self):
        """Render photometric panel"""
        imgui.set_next_window_size(400, 500, imgui.FIRST_USE_EVER)
        imgui.set_next_window_position(1170, 280, imgui.FIRST_USE_EVER)

        expanded, opened = imgui.begin("Photometric Analysis", True)
        if not opened:
            self.ui.show_photometric_panel = False
            imgui.end()
            return

        if expanded:
            proj = self.ui.selected_projector

            if proj is None:
                imgui.text("No projector selected")
                imgui.text_colored("Select a projector to analyze", 0.6, 0.6, 0.6)
            else:
                self._render_photometric_analysis(proj)

        imgui.end()

    def _render_photometric_analysis(self, proj):
        """Render photometric analysis for projector"""
        from ...utils.math_utils import (
            calculate_projection_size,
            calculate_distance,
            calculate_illuminance,
            calculate_luminance
        )

        # Projector specifications
        imgui.text(f"Projector: {proj.name}")
        imgui.text(f"Brightness: {proj.config['lumens']:,} lumens")
        imgui.separator()

        # Input parameters
        if imgui.collapsing_header("Screen Parameters", imgui.TREE_NODE_DEFAULT_OPEN)[0]:
            changed, self.analysis_distance = imgui.slider_float(
                "Distance (m)", self.analysis_distance, 1.0, 50.0, "%.2f"
            )

            changed, (self.screen_width, self.screen_height) = imgui.drag_float2(
                "Screen Size (m)",
                self.screen_width, self.screen_height,
                0.1, 0.5, 50.0
            )

            # Presets
            if imgui.button("16:9 (4.0m)"):
                self.screen_width = 4.0
                self.screen_height = 2.25
            imgui.same_line()
            if imgui.button("16:9 (6.0m)"):
                self.screen_width = 6.0
                self.screen_height = 3.375
            imgui.same_line()
            if imgui.button("16:9 (8.0m)"):
                self.screen_width = 8.0
                self.screen_height = 4.5

            changed, self.screen_gain = imgui.slider_float(
                "Screen Gain", self.screen_gain, 0.5, 3.0, "%.2f"
            )

        # Calculations
        if imgui.collapsing_header("Throw Calculations", imgui.TREE_NODE_DEFAULT_OPEN)[0]:
            # Required distance for screen width
            required_distance = calculate_distance(proj.throw_ratio, self.screen_width)
            imgui.text(f"Required Distance: {required_distance:.2f} m")

            # Projected size at distance
            proj_width, proj_height = calculate_projection_size(
                proj.throw_ratio,
                self.analysis_distance,
                proj.aspect
            )
            imgui.text(f"Projected Size: {proj_width:.2f} x {proj_height:.2f} m")

            # Coverage area
            coverage_area = proj_width * proj_height
            imgui.text(f"Coverage Area: {coverage_area:.2f} m²")

        # Photometric calculations
        if imgui.collapsing_header("Photometric Values", imgui.TREE_NODE_DEFAULT_OPEN)[0]:
            screen_area = self.screen_width * self.screen_height

            # Illuminance (lux)
            illuminance = calculate_illuminance(
                proj.config['lumens'],
                screen_area,
                self.screen_gain
            )
            imgui.text(f"Illuminance: {illuminance:.1f} lux")

            # Luminance (cd/m²)
            luminance = calculate_luminance(illuminance, self.screen_gain)
            imgui.text(f"Luminance: {luminance:.1f} cd/m²")

            # Foot-lamberts (US cinema standard)
            foot_lamberts = luminance * 0.2919
            imgui.text(f"Luminance: {foot_lamberts:.1f} fL")

            imgui.separator()

            # Cinema standards
            imgui.text_colored("Cinema Standards:", 0.7, 0.7, 0.7)
            imgui.bullet_text("DCI Standard: 14 fL (48 cd/m²)")
            imgui.bullet_text("Recommended: 12-16 fL")

            # Status indicator
            if 12 <= foot_lamberts <= 16:
                imgui.text_colored("✓ Within recommended range", 0.2, 0.8, 0.2)
            elif 10 <= foot_lamberts <= 20:
                imgui.text_colored("⚠ Acceptable range", 0.8, 0.8, 0.2)
            else:
                imgui.text_colored("✗ Outside recommended range", 0.8, 0.2, 0.2)

        # Multi-projector analysis
        if imgui.collapsing_header("Multi-Projector Setup")[0]:
            num_projectors = len(self.ui.app.scene.projectors)
            imgui.text(f"Active Projectors: {num_projectors}")

            if num_projectors > 1:
                # Combined brightness
                total_lumens = sum(p.config['lumens'] for p in self.ui.app.scene.projectors)
                combined_illuminance = calculate_illuminance(
                    total_lumens,
                    screen_area,
                    self.screen_gain
                )
                combined_luminance = calculate_luminance(combined_illuminance, self.screen_gain)
                combined_fl = combined_luminance * 0.2919

                imgui.separator()
                imgui.text(f"Combined Brightness: {total_lumens:,} lumens")
                imgui.text(f"Combined Illuminance: {combined_illuminance:.1f} lux")
                imgui.text(f"Combined Luminance: {combined_fl:.1f} fL")

        # Lens information
        if imgui.collapsing_header("Lens Information")[0]:
            imgui.text(f"Lens: {proj.lens_config['name']}")
            imgui.text(f"Throw Ratio: {proj.throw_ratio:.2f}:1")
            imgui.text(f"FOV: {proj.get_fov():.1f}°")
            imgui.separator()
            imgui.text(f"Throw Range: {proj.lens_config['throw_min']:.2f} - {proj.lens_config['throw_max']:.2f}")
            imgui.text(f"Lens Shift V: ±{proj.lens_config['shift_v']}%")
            imgui.text(f"Lens Shift H: ±{proj.lens_config['shift_h']}%")

        # Export analysis
        imgui.separator()
        if imgui.button("Export Analysis Report (PDF)", width=250):
            print("  📄 Exporting photometric analysis report...")
            print("  ⚠️ PDF export not yet implemented")
