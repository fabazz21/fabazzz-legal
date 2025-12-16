"""
Scene Hierarchy Panel
Displays scene objects in a tree view
"""

import imgui


class ScenePanel:
    """Scene hierarchy panel"""

    def __init__(self, ui):
        """Initialize scene panel"""
        self.ui = ui

    def render(self):
        """Render scene panel"""
        imgui.set_next_window_size(300, 400, imgui.FIRST_USE_EVER)
        imgui.set_next_window_position(10, 30, imgui.FIRST_USE_EVER)

        expanded, opened = imgui.begin("Scene", True)
        if not opened:
            self.ui.show_scene_panel = False
            imgui.end()
            return

        if expanded:
            scene = self.ui.app.scene

            # Scene statistics
            imgui.text(f"Objects: {len(scene.objects)}")
            imgui.text(f"Projectors: {len(scene.projectors)}")
            imgui.text(f"Lights: {len(scene.lights)}")
            imgui.separator()

            # Projectors
            if imgui.tree_node("Projectors", imgui.TREE_NODE_DEFAULT_OPEN):
                for projector in scene.projectors:
                    selected = (self.ui.selected_projector == projector)

                    if imgui.selectable(
                        f"📽️ {projector.name}",
                        selected,
                        imgui.SELECTABLE_ALLOW_DOUBLE_CLICK
                    )[0]:
                        self.ui.selected_projector = projector
                        self.ui.selected_object = None

                    # Context menu
                    if imgui.begin_popup_context_item(f"ctx_{projector.id}"):
                        if imgui.selectable("Delete")[0]:
                            scene.remove_projector(projector)
                            if self.ui.selected_projector == projector:
                                self.ui.selected_projector = None
                        if imgui.selectable("Duplicate")[0]:
                            # TODO: Duplicate projector
                            pass
                        imgui.end_popup()

                imgui.tree_pop()

            # Objects
            if imgui.tree_node("Objects", imgui.TREE_NODE_DEFAULT_OPEN):
                for obj in scene.objects:
                    selected = (self.ui.selected_object == obj)

                    icon = self._get_object_icon(obj)
                    if imgui.selectable(
                        f"{icon} {obj.name}",
                        selected,
                        imgui.SELECTABLE_ALLOW_DOUBLE_CLICK
                    )[0]:
                        self.ui.selected_object = obj
                        self.ui.selected_projector = None

                    # Context menu
                    if imgui.begin_popup_context_item(f"ctx_{obj.id}"):
                        if imgui.selectable("Delete")[0]:
                            scene.remove_object(obj)
                            if self.ui.selected_object == obj:
                                self.ui.selected_object = None
                        if imgui.selectable("Duplicate")[0]:
                            # TODO: Duplicate object
                            pass
                        imgui.separator()
                        if imgui.selectable("Focus Camera")[0]:
                            self._focus_camera_on_object(obj)
                        imgui.end_popup()

                imgui.tree_pop()

            # Lights
            if imgui.tree_node("Lights"):
                for light in scene.lights:
                    imgui.selectable(f"💡 {light.name}")
                imgui.tree_pop()

            # Grid
            imgui.separator()
            if imgui.tree_node("Grid"):
                changed, scene.show_grid = imgui.checkbox("Show Grid", scene.show_grid)
                if scene.show_grid:
                    changed, scene.grid_size = imgui.slider_float(
                        "Grid Size", scene.grid_size, 1.0, 100.0
                    )
                imgui.tree_pop()

        imgui.end()

    def _get_object_icon(self, obj):
        """Get icon for object type"""
        obj_type = type(obj).__name__.lower()
        icons = {
            'cube': '🧊',
            'sphere': '⚪',
            'plane': '▭',
            'cylinder': '🛢',
            'cone': '🔺',
            'object3d': '📦'
        }
        return icons.get(obj_type, '📦')

    def _focus_camera_on_object(self, obj):
        """Focus camera on object"""
        # Calculate camera position to look at object
        from pyrr import Vector3
        camera = self.ui.app.camera
        camera.target = Vector3([obj.position[0], obj.position[1], obj.position[2]])
        print(f"  🎯 Camera focused on {obj.name}")
