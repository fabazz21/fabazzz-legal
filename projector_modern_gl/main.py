#!/usr/bin/env python3
"""
Professional 3D Projection Mapping System - ModernGL
Main Application Entry Point

Features:
- Multi-projector shadow-mapped rendering
- Timeline-based animation system
- Photometric analysis
- Professional UI with ImGui
- Interactive 3D Gizmo System
"""

import sys
import moderngl
import glfw
import imgui
from imgui.integrations.glfw import GlfwRenderer
import numpy as np

from core.window import Window
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from ui.main_ui_tabbed import MainUITabbed as MainUI  # Using tabbed UI (HTML-style)
from ui.gizmo import Gizmo
from animation.timeline import Timeline
from utils.history import History


class ProjectionMappingApp:
    """Main Application Class"""

    def __init__(self, width=1920, height=1080, title="Professional Projection Mapping - ModernGL"):
        """Initialize the application"""
        self.width = width
        self.height = height
        self.title = title

        # Initialize GLFW
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW")

        # Create window
        self.window = Window(width, height, title)

        # Create ModernGL context
        self.ctx = moderngl.create_context(require=330)
        self.ctx.enable(moderngl.DEPTH_TEST)
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA

        # Initialize ImGui
        imgui.create_context()
        self.imgui_impl = GlfwRenderer(self.window.glfw_window)

        # Core systems
        self.scene = Scene(self.ctx)
        self.camera = Camera(width, height)
        self.renderer = Renderer(self.ctx, width, height)
        self.timeline = Timeline()
        self.history = History()

        # UI
        self.ui = MainUI(self)

        # Gizmo system for 3D object manipulation
        self.gizmo = Gizmo(self.ctx)
        self.gizmo_mode = 'translate'
        self.gizmo_active = True
        self.key_pressed = {}  # Track key states to prevent repeats

        # Application state
        self.running = True
        self.delta_time = 0.0
        self.last_frame = glfw.get_time()
        self.frame_count = 0
        self.fps = 0.0

        print(f"✅ Projection Mapping System Initialized")
        print(f"   OpenGL Version: {self.ctx.info.get('GL_VERSION', 'Unknown')}")
        print(f"   Renderer: {self.ctx.info.get('GL_RENDERER', 'Unknown')}")
        print(f"   Vendor: {self.ctx.info.get('GL_VENDOR', 'Unknown')}")

        # Print keyboard shortcuts
        print("\n⌨️  KEYBOARD SHORTCUTS:")
        print("  G = Toggle Gizmo On/Off")
        print("  W = Translate Mode")
        print("  E = Rotate Mode")
        print("  R = Scale Mode")
        print("  H = Toggle Helpers (Grid/Axes)")
        print("  F = Toggle Frustums (Projectors)")
        print()

        # Add default test scene
        self._create_test_scene()

    def _create_test_scene(self):
        """Create initial test scene"""
        from objects.primitives import create_primitive
        from projectors.projector import Projector

        # Add a cube
        cube = create_primitive('cube', self.ctx)
        cube.name = "Test Cube"
        self.scene.add_object(cube)
        print(f"  ✅ Added test cube to scene")

        # Add a projector
        projector = Projector('panasonic_pt_rq13k', 'panasonic_et_d3lew10', self.ctx, position=(0, 3, 8))
        self.scene.add_projector(projector)
        print(f"  ✅ Added test projector: {projector.name}")

    def _handle_keyboard(self):
        """Handle keyboard shortcuts"""
        window = self.window.glfw_window

        # G = Toggle Gizmo
        if glfw.get_key(window, glfw.KEY_G) == glfw.PRESS:
            if not self.key_pressed.get('G', False):
                self.gizmo_active = not self.gizmo_active
                print(f"[GIZMO] {'✅ Enabled' if self.gizmo_active else '❌ Disabled'}")
                self.key_pressed['G'] = True
        else:
            self.key_pressed['G'] = False

        # W = Translate Mode
        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            if not self.key_pressed.get('W', False):
                self.gizmo.set_mode('translate')
                self.key_pressed['W'] = True
        else:
            self.key_pressed['W'] = False

        # E = Rotate Mode
        if glfw.get_key(window, glfw.KEY_E) == glfw.PRESS:
            if not self.key_pressed.get('E', False):
                self.gizmo.set_mode('rotate')
                self.key_pressed['E'] = True
        else:
            self.key_pressed['E'] = False

        # R = Scale Mode
        if glfw.get_key(window, glfw.KEY_R) == glfw.PRESS:
            if not self.key_pressed.get('R', False):
                self.gizmo.set_mode('scale')
                self.key_pressed['R'] = True
        else:
            self.key_pressed['R'] = False

        # H = Toggle Helpers
        if glfw.get_key(window, glfw.KEY_H) == glfw.PRESS:
            if not self.key_pressed.get('H', False):
                self.scene.show_helpers = not self.scene.show_helpers
                print(f"[HELPERS] {'✅ Enabled' if self.scene.show_helpers else '❌ Disabled'}")
                self.key_pressed['H'] = True
        else:
            self.key_pressed['H'] = False

        # F = Toggle Frustums
        if glfw.get_key(window, glfw.KEY_F) == glfw.PRESS:
            if not self.key_pressed.get('F', False):
                self.scene.show_frustums = not self.scene.show_frustums
                print(f"[FRUSTUMS] {'✅ Enabled' if self.scene.show_frustums else '❌ Disabled'}")
                self.key_pressed['F'] = True
        else:
            self.key_pressed['F'] = False

    def run(self):
        """Main application loop"""
        print("\n🚀 Starting main render loop...")

        while self.running and not glfw.window_should_close(self.window.glfw_window):
            # Calculate delta time
            current_frame = glfw.get_time()
            self.delta_time = current_frame - self.last_frame
            self.last_frame = current_frame

            # Calculate FPS
            self.frame_count += 1
            if self.frame_count % 60 == 0:
                self.fps = 1.0 / self.delta_time if self.delta_time > 0 else 0.0

            # Poll events
            glfw.poll_events()

            # Handle ImGui input
            self.imgui_impl.process_inputs()

            # Handle keyboard shortcuts
            self._handle_keyboard()

            # Update systems
            self.update(self.delta_time)

            # Render frame
            self.render()

            # Render UI
            self.render_ui()

            # Swap buffers
            glfw.swap_buffers(self.window.glfw_window)

        self.cleanup()

    def update(self, dt):
        """Update application state"""
        io = imgui.get_io()

        # Update camera (only if ImGui doesn't want the mouse)
        if not io.want_capture_mouse:
            self.camera.update(self.window, dt)

        # Update timeline if playing
        if self.timeline.playing:
            self.timeline.update(dt)
            # Apply keyframes to scene objects
            self.timeline.apply_keyframes(self.scene)

        # Update scene
        self.scene.update(dt)

        # Update gizmo if active and an object is selected
        if self.gizmo_active and not io.want_capture_mouse:
            # Get selected object or projector from UI
            selected_target = None
            if hasattr(self.ui, 'selected_object') and self.ui.selected_object is not None:
                selected_target = self.ui.selected_object
            elif hasattr(self.ui, 'selected_projector') and self.ui.selected_projector is not None:
                selected_target = self.ui.selected_projector

            # Set gizmo target
            if selected_target:
                self.gizmo.set_target(selected_target)

                # Get mouse state
                mouse_x, mouse_y = glfw.get_cursor_pos(self.window.glfw_window)
                mouse_down = glfw.get_mouse_button(self.window.glfw_window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS

                # Update gizmo
                self.gizmo.update(self.camera, (mouse_x, mouse_y), mouse_down)
            else:
                self.gizmo.set_target(None)

    def render(self):
        """Render the scene"""
        # Clear framebuffer
        self.ctx.clear(0.071, 0.078, 0.090)  # #121418 background

        # Render depth pass for shadow mapping (for each active projector)
        for projector in self.scene.get_active_projectors():
            self.renderer.render_depth_pass(projector, self.scene)

        # Render main scene
        self.renderer.render_scene(self.scene, self.camera)

        # Render helpers (frustums, grid, etc.)
        if self.scene.show_helpers:
            self.renderer.render_helpers(self.scene, self.camera)

        # Render gizmo (on top of everything)
        if self.gizmo_active and self.gizmo.target_object is not None:
            # Disable depth test for gizmo (always on top)
            self.ctx.disable(moderngl.DEPTH_TEST)
            self.gizmo.render(self.renderer, self.camera)
            self.ctx.enable(moderngl.DEPTH_TEST)

    def render_ui(self):
        """Render ImGui interface"""
        imgui.new_frame()

        # Main UI panels and windows
        self.ui.render()

        # FPS counter
        imgui.set_next_window_position(10, 10)
        imgui.set_next_window_bg_alpha(0.3)
        imgui.begin("##fps", False,
                   imgui.WINDOW_NO_TITLE_BAR |
                   imgui.WINDOW_NO_RESIZE |
                   imgui.WINDOW_NO_MOVE |
                   imgui.WINDOW_NO_SCROLLBAR)
        imgui.text(f"FPS: {self.fps:.1f}")
        imgui.text(f"Frame: {self.frame_count}")

        # Gizmo status
        if self.gizmo_active:
            imgui.text(f"Gizmo: {self.gizmo.mode.upper()}")

        imgui.end()

        imgui.render()
        self.imgui_impl.render(imgui.get_draw_data())

    def cleanup(self):
        """Cleanup resources"""
        print("\n🧹 Cleaning up resources...")

        # Cleanup UI
        self.imgui_impl.shutdown()

        # Cleanup renderer
        self.renderer.cleanup()

        # Cleanup scene
        self.scene.cleanup()

        # Cleanup ModernGL context
        self.ctx.release()

        # Cleanup GLFW
        glfw.terminate()

        print("✅ Cleanup complete\n")


def main():
    """Application entry point"""
    print("=" * 60)
    print("  PROFESSIONAL 3D PROJECTION MAPPING SYSTEM")
    print("  ModernGL Edition")
    print("=" * 60)
    print()

    try:
        app = ProjectionMappingApp(1920, 1080)
        app.run()
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
