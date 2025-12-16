"""
Projector Panel
Advanced projector configuration and correction tools
"""

import imgui


class ProjectorPanel:
    """Projector configuration panel"""

    def __init__(self, ui):
        """Initialize projector panel"""
        self.ui = ui

    def render(self):
        """Render projector panel"""
        imgui.set_next_window_size(380, 600, imgui.FIRST_USE_EVER)
        imgui.set_next_window_position(1530, 30, imgui.FIRST_USE_EVER)

        expanded, opened = imgui.begin("Projector Control", True)
        if not opened:
            self.ui.show_projector_panel = False
            imgui.end()
            return

        if expanded:
            proj = self.ui.selected_projector

            if proj is None:
                imgui.text("No projector selected")
                imgui.text_colored("Select a projector from the Scene panel", 0.6, 0.6, 0.6)
            else:
                self._render_projector_controls(proj)

        imgui.end()

    def _render_projector_controls(self, proj):
        """Render projector controls"""
        # Projector info
        imgui.text(f"{proj.name}")
        imgui.text_colored(f"Model: {proj.config['name']}", 0.7, 0.7, 0.7)
        imgui.text_colored(f"Lens: {proj.lens_config['name']}", 0.7, 0.7, 0.7)
        imgui.separator()

        # Basic settings
        if imgui.collapsing_header("Basic Settings", imgui.TREE_NODE_DEFAULT_OPEN)[0]:
            changed, proj.intensity = imgui.slider_float(
                "Intensity", proj.intensity, 0.0, 2.0
            )

            changed, proj.active = imgui.checkbox("Active", proj.active)

            # Orientation
            current_orient = 0 if proj.orientation == 'landscape' else 1
            changed, selected = imgui.combo(
                "Orientation",
                current_orient,
                ["Landscape", "Portrait"]
            )
            if changed:
                proj.orientation = 'landscape' if selected == 0 else 'portrait'

        # Lens settings
        if imgui.collapsing_header("Lens Settings", imgui.TREE_NODE_DEFAULT_OPEN)[0]:
            # Throw ratio
            changed, proj.throw_ratio = imgui.slider_float(
                "Throw Ratio",
                proj.throw_ratio,
                proj.lens_config['throw_min'],
                proj.lens_config['throw_max'],
                "%.2f"
            )
            if changed:
                fov = proj.get_fov()
                imgui.text_colored(f"  FOV: {fov:.1f}°", 0.6, 0.6, 0.6)

            # Lens shift
            imgui.text("Lens Shift")
            max_h = proj.lens_config['shift_h'] / 100.0
            max_v = proj.lens_config['shift_v'] / 100.0

            changed, proj.lens_shift_h = imgui.slider_float(
                "Horizontal##lens_shift", proj.lens_shift_h, -max_h, max_h, "%.3f"
            )

            changed, proj.lens_shift_v = imgui.slider_float(
                "Vertical##lens_shift", proj.lens_shift_v, -max_v, max_v, "%.3f"
            )

            if imgui.button("Reset Lens Shift"):
                proj.lens_shift_h = 0.0
                proj.lens_shift_v = 0.0

        # Keystone correction
        if imgui.collapsing_header("Keystone Correction")[0]:
            # Basic keystone
            imgui.text("Basic Keystone")
            changed, proj.keystone_v = imgui.slider_float(
                "Vertical##keystone", proj.keystone_v, -50.0, 50.0, "%.1f"
            )

            changed, proj.keystone_h = imgui.slider_float(
                "Horizontal##keystone", proj.keystone_h, -50.0, 50.0, "%.1f"
            )

            # Corner keystone
            if imgui.tree_node("Corner Keystone"):
                # Top-left
                imgui.text("Top-Left")
                changed, proj.keystone_tl_x = imgui.slider_float(
                    "X##ksTLx", proj.keystone_tl_x, -100.0, 100.0, "%.1f"
                )
                changed, proj.keystone_tl_y = imgui.slider_float(
                    "Y##ksTLy", proj.keystone_tl_y, -100.0, 100.0, "%.1f"
                )

                # Top-right
                imgui.text("Top-Right")
                changed, proj.keystone_tr_x = imgui.slider_float(
                    "X##ksTRx", proj.keystone_tr_x, -100.0, 100.0, "%.1f"
                )
                changed, proj.keystone_tr_y = imgui.slider_float(
                    "Y##ksTRy", proj.keystone_tr_y, -100.0, 100.0, "%.1f"
                )

                # Bottom-left
                imgui.text("Bottom-Left")
                changed, proj.keystone_bl_x = imgui.slider_float(
                    "X##ksBLx", proj.keystone_bl_x, -100.0, 100.0, "%.1f"
                )
                changed, proj.keystone_bl_y = imgui.slider_float(
                    "Y##ksBLy", proj.keystone_bl_y, -100.0, 100.0, "%.1f"
                )

                # Bottom-right
                imgui.text("Bottom-Right")
                changed, proj.keystone_br_x = imgui.slider_float(
                    "X##ksBRx", proj.keystone_br_x, -100.0, 100.0, "%.1f"
                )
                changed, proj.keystone_br_y = imgui.slider_float(
                    "Y##ksBRy", proj.keystone_br_y, -100.0, 100.0, "%.1f"
                )

                imgui.tree_pop()

            if imgui.button("Reset Keystone"):
                proj.reset_keystone()

        # Corner pin
        if imgui.collapsing_header("Corner Pin")[0]:
            # Top-left
            imgui.text("Top-Left")
            changed, proj.corner_pin_tl_x = imgui.slider_float(
                "X##cpTLx", proj.corner_pin_tl_x, -100.0, 100.0, "%.1f"
            )
            changed, proj.corner_pin_tl_y = imgui.slider_float(
                "Y##cpTLy", proj.corner_pin_tl_y, -100.0, 100.0, "%.1f"
            )

            # Top-right
            imgui.text("Top-Right")
            changed, proj.corner_pin_tr_x = imgui.slider_float(
                "X##cpTRx", proj.corner_pin_tr_x, -100.0, 100.0, "%.1f"
            )
            changed, proj.corner_pin_tr_y = imgui.slider_float(
                "Y##cpTRy", proj.corner_pin_tr_y, -100.0, 100.0, "%.1f"
            )

            # Bottom-left
            imgui.text("Bottom-Left")
            changed, proj.corner_pin_bl_x = imgui.slider_float(
                "X##cpBLx", proj.corner_pin_bl_x, -100.0, 100.0, "%.1f"
            )
            changed, proj.corner_pin_bl_y = imgui.slider_float(
                "Y##cpBLy", proj.corner_pin_bl_y, -100.0, 100.0, "%.1f"
            )

            # Bottom-right
            imgui.text("Bottom-Right")
            changed, proj.corner_pin_br_x = imgui.slider_float(
                "X##cpBRx", proj.corner_pin_br_x, -100.0, 100.0, "%.1f"
            )
            changed, proj.corner_pin_br_y = imgui.slider_float(
                "Y##cpBRy", proj.corner_pin_br_y, -100.0, 100.0, "%.1f"
            )

            if imgui.button("Reset Corner Pin"):
                proj.reset_corner_pin()

        # Soft edge blending
        if imgui.collapsing_header("Soft Edge Blending")[0]:
            changed, proj.soft_edge_l = imgui.slider_float(
                "Left Edge", proj.soft_edge_l, 0.0, 100.0, "%.1f%%"
            )

            changed, proj.soft_edge_r = imgui.slider_float(
                "Right Edge", proj.soft_edge_r, 0.0, 100.0, "%.1f%%"
            )

            changed, proj.soft_edge_t = imgui.slider_float(
                "Top Edge", proj.soft_edge_t, 0.0, 100.0, "%.1f%%"
            )

            changed, proj.soft_edge_b = imgui.slider_float(
                "Bottom Edge", proj.soft_edge_b, 0.0, 100.0, "%.1f%%"
            )

            changed, proj.soft_edge_gamma = imgui.slider_float(
                "Gamma", proj.soft_edge_gamma, 0.1, 10.0, "%.2f"
            )

            if imgui.button("Reset Soft Edge"):
                proj.reset_soft_edge()

        # Texture
        if imgui.collapsing_header("Projection Texture")[0]:
            if proj.texture:
                imgui.text("Texture loaded")
                if imgui.button("Clear Texture"):
                    proj.texture = None
            else:
                imgui.text("No texture loaded")

            if imgui.button("Load Image..."):
                # TODO: File dialog
                print("  📁 Load image dialog (TODO)")

            if imgui.button("Create Test Pattern"):
                proj.create_test_pattern()

        # Shadow mapping
        if imgui.collapsing_header("Shadow Settings")[0]:
            changed, proj.shadow_bias = imgui.slider_float(
                "Shadow Bias", proj.shadow_bias, 0.0001, 0.01, "%.4f"
            )
