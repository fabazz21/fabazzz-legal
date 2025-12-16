"""
Properties Panel
Display and edit properties of selected object
"""

import imgui
from pyrr import Vector3


class PropertiesPanel:
    """Properties panel for selected objects"""

    def __init__(self, ui):
        """Initialize properties panel"""
        self.ui = ui

    def render(self):
        """Render properties panel"""
        imgui.set_next_window_size(320, 500, imgui.FIRST_USE_EVER)
        imgui.set_next_window_position(10, 440, imgui.FIRST_USE_EVER)

        expanded, opened = imgui.begin("Properties", True)
        if not opened:
            self.ui.show_properties_panel = False
            imgui.end()
            return

        if expanded:
            # Get selected object
            obj = self.ui.selected_object or self.ui.selected_projector

            if obj is None:
                imgui.text("No object selected")
            else:
                self._render_object_properties(obj)

        imgui.end()

    def _render_object_properties(self, obj):
        """Render properties for object"""
        # Object name
        imgui.text(f"Name: {obj.name}")
        imgui.text(f"Type: {type(obj).__name__}")
        imgui.separator()

        # Transform
        if imgui.collapsing_header("Transform", imgui.TREE_NODE_DEFAULT_OPEN)[0]:
            # Position
            changed, (x, y, z) = imgui.drag_float3(
                "Position",
                obj.position[0], obj.position[1], obj.position[2],
                0.1
            )
            if changed:
                obj.position = Vector3([x, y, z])

            # Rotation (Euler angles)
            if hasattr(obj, 'rotation'):
                # Convert quaternion to Euler for display
                # For now, show simplified rotation
                imgui.text("Rotation: (Quaternion)")

            # Scale
            if hasattr(obj, 'scale'):
                changed, (sx, sy, sz) = imgui.drag_float3(
                    "Scale",
                    obj.scale[0], obj.scale[1], obj.scale[2],
                    0.01, 0.01, 100.0
                )
                if changed:
                    obj.scale = Vector3([sx, sy, sz])

        # Visibility
        if hasattr(obj, 'visible'):
            if imgui.collapsing_header("Visibility")[0]:
                changed, obj.visible = imgui.checkbox("Visible", obj.visible)

                if hasattr(obj, 'cast_shadow'):
                    changed, obj.cast_shadow = imgui.checkbox("Cast Shadow", obj.cast_shadow)

                if hasattr(obj, 'receive_shadow'):
                    changed, obj.receive_shadow = imgui.checkbox("Receive Shadow", obj.receive_shadow)

        # Material
        if hasattr(obj, 'color'):
            if imgui.collapsing_header("Material")[0]:
                changed, color = imgui.color_edit3("Color", *obj.color)
                if changed:
                    obj.color = list(color)

        # Projector-specific properties
        if hasattr(obj, 'intensity'):
            if imgui.collapsing_header("Projector Settings", imgui.TREE_NODE_DEFAULT_OPEN)[0]:
                changed, obj.intensity = imgui.slider_float(
                    "Intensity", obj.intensity, 0.0, 2.0
                )

                changed, obj.active = imgui.checkbox("Active", obj.active)

        # Keyframe controls
        imgui.separator()
        if imgui.button("Add Keyframe (K)"):
            self.ui.app.timeline.add_keyframe(obj, 'position')
