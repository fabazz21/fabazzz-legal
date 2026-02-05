"""
Main User Interface with ImGui
"""

import imgui
import numpy as np
from imgui.integrations.pygame import PygameRenderer


class MainUI:
    """Main ImGui Interface"""

    def __init__(self, window):
        """Initialize UI"""
        self.window = window

        # Setup ImGui context
        imgui.create_context()
        self.renderer = PygameRenderer()

        # UI state
        self.show_scene_panel = True
        self.show_projector_panel = True
        self.show_properties_panel = True
        self.show_timeline_panel = True
        self.show_debug_panel = False

        # Selection
        self.selected_object = None
        self.selected_projector = None

        print("✅ UI initialized")

    def process_events(self, events):
        """Process pygame events for ImGui"""
        for event in events:
            self.renderer.process_event(event)

    def begin_frame(self):
        """Begin ImGui frame"""
        imgui.new_frame()

    def render_scene_panel(self, scene):
        """Render scene hierarchy panel"""
        if not self.show_scene_panel:
            return

        imgui.set_next_window_position(10, 10, imgui.FIRST_USE_EVER)
        imgui.set_next_window_size(300, 400, imgui.FIRST_USE_EVER)

        expanded, opened = imgui.begin("Scene", True)
        if opened:
            self.show_scene_panel = True

            # Objects
            if imgui.tree_node("Objects"):
                for i, obj in enumerate(scene.objects):
                    clicked, _ = imgui.selectable(f"{obj.name}##obj{i}", self.selected_object == obj)
                    if clicked:
                        self.selected_object = obj
                        self.selected_projector = None
                imgui.tree_pop()

            # Projectors
            if imgui.tree_node("Projectors"):
                for i, proj in enumerate(scene.projectors):
                    clicked, _ = imgui.selectable(
                        f"{proj.name} ({'ON' if proj.active else 'OFF'})##proj{i}",
                        self.selected_projector == proj
                    )
                    if clicked:
                        self.selected_projector = proj
                        self.selected_object = None
                imgui.tree_pop()

            imgui.separator()

            # Add buttons
            if imgui.button("Add Projector"):
                from core.scene import Projector
                proj = Projector(f"Projector {len(scene.projectors) + 1}")
                scene.add_projector(proj)

        else:
            self.show_scene_panel = False

        imgui.end()

    def render_properties_panel(self):
        """Render properties panel"""
        if not self.show_properties_panel:
            return

        imgui.set_next_window_position(self.window.width - 310, 10, imgui.FIRST_USE_EVER)
        imgui.set_next_window_size(300, 600, imgui.FIRST_USE_EVER)

        expanded, opened = imgui.begin("Properties", True)
        if opened:
            self.show_properties_panel = True

            # Object properties
            if self.selected_object:
                imgui.text(f"Object: {self.selected_object.name}")
                imgui.separator()

                # Transform
                if imgui.tree_node("Transform", imgui.TREE_NODE_DEFAULT_OPEN):
                    # Position
                    changed, pos = imgui.drag_float3("Position", *self.selected_object.position, 0.1)
                    if changed:
                        self.selected_object.position = np.array(pos, dtype=np.float32)

                    # Rotation (degrees)
                    rot_deg = np.degrees(self.selected_object.rotation)
                    changed, rot = imgui.drag_float3("Rotation", *rot_deg, 1.0)
                    if changed:
                        self.selected_object.rotation = np.radians(rot).astype(np.float32)

                    # Scale
                    changed, scale = imgui.drag_float3("Scale", *self.selected_object.scale, 0.1)
                    if changed:
                        self.selected_object.scale = np.array(scale, dtype=np.float32)

                    imgui.tree_pop()

            # Projector properties
            elif self.selected_projector:
                imgui.text(f"Projector: {self.selected_projector.name}")
                imgui.separator()

                # Active
                changed, active = imgui.checkbox("Active", self.selected_projector.active)
                if changed:
                    self.selected_projector.active = active

                # Intensity
                changed, intensity = imgui.slider_float("Intensity", self.selected_projector.intensity, 0.0, 2.0)
                if changed:
                    self.selected_projector.intensity = intensity

                # Transform
                if imgui.tree_node("Transform", imgui.TREE_NODE_DEFAULT_OPEN):
                    # Position
                    changed, pos = imgui.drag_float3("Position", *self.selected_projector.position, 0.1)
                    if changed:
                        self.selected_projector.position = np.array(pos, dtype=np.float32)

                    # Rotation (degrees)
                    rot_deg = np.degrees(self.selected_projector.rotation)
                    changed, rot = imgui.drag_float3("Rotation", *rot_deg, 1.0)
                    if changed:
                        self.selected_projector.rotation = np.radians(rot).astype(np.float32)

                    imgui.tree_pop()

                # Projection
                if imgui.tree_node("Projection"):
                    changed, fov = imgui.slider_float("FOV", self.selected_projector.fov, 10.0, 120.0)
                    if changed:
                        self.selected_projector.fov = fov

                    changed, aspect = imgui.slider_float("Aspect", self.selected_projector.aspect, 0.5, 2.5)
                    if changed:
                        self.selected_projector.aspect = aspect

                    imgui.tree_pop()

            else:
                imgui.text("No selection")

        else:
            self.show_properties_panel = False

        imgui.end()

    def render_timeline_panel(self, timeline):
        """Render timeline panel"""
        if not self.show_timeline_panel:
            return

        imgui.set_next_window_position(10, self.window.height - 210, imgui.FIRST_USE_EVER)
        imgui.set_next_window_size(self.window.width - 20, 200, imgui.FIRST_USE_EVER)

        expanded, opened = imgui.begin("Timeline", True)
        if opened:
            self.show_timeline_panel = True

            # Playback controls
            if timeline.playing:
                if imgui.button("Pause"):
                    timeline.pause()
            else:
                if imgui.button("Play"):
                    timeline.play()

            imgui.same_line()
            if imgui.button("Stop"):
                timeline.stop()

            imgui.same_line()
            if imgui.button("Record"):
                if timeline.recording:
                    timeline.stop_recording()
                else:
                    timeline.start_recording()

            imgui.same_line()
            imgui.text(f"Time: {timeline.current_time:.2f}s / {timeline.duration:.2f}s")

            # Timeline scrubber
            changed, progress = imgui.slider_float("##timeline", timeline.get_progress(), 0.0, 1.0, "")
            if changed:
                timeline.set_progress(progress)

            # Keyframes
            imgui.text(f"Keyframes: {len(timeline.get_all_keyframes())}")

        else:
            self.show_timeline_panel = False

        imgui.end()

    def render_debug_panel(self, window, renderer, camera):
        """Render debug information panel"""
        if not self.show_debug_panel:
            return

        imgui.set_next_window_position(10, 420, imgui.FIRST_USE_EVER)
        imgui.set_next_window_size(300, 200, imgui.FIRST_USE_EVER)

        expanded, opened = imgui.begin("Debug", True)
        if opened:
            self.show_debug_panel = True

            imgui.text(f"FPS: {int(window.clock.get_fps())}")
            imgui.text(f"Frame time: {window.delta_time * 1000:.2f}ms")
            imgui.separator()

            imgui.text(f"Camera pos: ({camera.position[0]:.1f}, {camera.position[1]:.1f}, {camera.position[2]:.1f})")
            imgui.text(f"Camera target: ({camera.target[0]:.1f}, {camera.target[1]:.1f}, {camera.target[2]:.1f})")
            imgui.separator()

            imgui.text(f"OpenGL: {window.ctx.version_code}")

        else:
            self.show_debug_panel = False

        imgui.end()

    def render_menu_bar(self, scene, timeline):
        """Render main menu bar"""
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File"):
                clicked, _ = imgui.menu_item("Save Scene")
                if clicked:
                    scene.export_to_json("scene.json")

                clicked, _ = imgui.menu_item("Load Scene")
                if clicked:
                    try:
                        scene.load_from_json("scene.json")
                    except Exception as e:
                        print(f"Error loading scene: {e}")

                imgui.separator()

                clicked, _ = imgui.menu_item("Quit", "Esc")
                if clicked:
                    self.window.running = False

                imgui.end_menu()

            if imgui.begin_menu("View"):
                clicked, self.show_scene_panel = imgui.menu_item("Scene", "", self.show_scene_panel)
                clicked, self.show_properties_panel = imgui.menu_item("Properties", "", self.show_properties_panel)
                clicked, self.show_timeline_panel = imgui.menu_item("Timeline", "", self.show_timeline_panel)
                clicked, self.show_debug_panel = imgui.menu_item("Debug", "", self.show_debug_panel)
                imgui.end_menu()

            if imgui.begin_menu("Timeline"):
                clicked, _ = imgui.menu_item("Export Animation")
                if clicked:
                    json_data = timeline.export_to_json()
                    with open("animation.json", "w") as f:
                        f.write(json_data)
                    print("✅ Animation exported to animation.json")

                clicked, _ = imgui.menu_item("Clear Animation")
                if clicked:
                    timeline.clear_animation()

                imgui.end_menu()

            imgui.end_main_menu_bar()

    def end_frame(self):
        """End ImGui frame and render"""
        imgui.render()
        self.renderer.render(imgui.get_draw_data())

    def cleanup(self):
        """Cleanup UI resources"""
        self.renderer.shutdown()
        print("✅ UI cleaned up")
