#!/usr/bin/env python3
"""
Projector Fusion - Multi-Projector Mapping Application
Main entry point
"""

import sys
import numpy as np
from pygame.locals import *

# Import core modules
from projector_modern_gl.core.window import Window
from projector_modern_gl.core.scene import Scene, Projector, SceneObject
from projector_modern_gl.core.camera import Camera
from projector_modern_gl.core.renderer import Renderer

# Import UI
from projector_modern_gl.ui.main_ui import MainUI
from projector_modern_gl.ui.theme import setup_theme
from projector_modern_gl.ui.gizmo import Gizmo

# Import animation
from projector_modern_gl.animation.timeline import Timeline

# Import utilities
from projector_modern_gl.utils.history import History


class Application:
    """Main Application"""

    def __init__(self, width=1920, height=1080):
        """Initialize application"""
        print("=" * 60)
        print("Projector Fusion - Multi-Projector Mapping")
        print("=" * 60)

        # Create window
        self.window = Window(width, height, "Projector Fusion")

        # Create scene
        self.scene = Scene()

        # Create camera
        self.camera = Camera(
            position=(0, 10, 15),
            target=(0, 0, 0)
        )
        self.camera.set_aspect_ratio(width, height)

        # Create renderer
        self.renderer = Renderer(self.window.ctx, width, height)

        # Create UI
        self.ui = MainUI(self.window)
        setup_theme()

        # Create timeline
        self.timeline = Timeline()

        # Create history
        self.history = History()

        # Create gizmo
        self.gizmo = Gizmo()

        # Camera control state
        self.camera_rotating = False
        self.camera_panning = False
        self.last_mouse_pos = (0, 0)

        # Setup test scene
        self._setup_test_scene()

        print("=" * 60)
        print("✅ Application initialized successfully")
        print("=" * 60)

    def _setup_test_scene(self):
        """Setup a test scene with projectors and objects"""
        # Create a simple plane object
        plane = SceneObject("Plane")
        plane.scale = np.array([10.0, 0.1, 10.0], dtype=np.float32)
        self._create_plane_geometry(plane)
        self.scene.add_object(plane)

        # Create a projector
        proj1 = Projector("Projector 1")
        proj1.position = np.array([0.0, 5.0, 5.0], dtype=np.float32)
        proj1.rotation = np.array([np.radians(-30), 0.0, 0.0], dtype=np.float32)
        proj1.intensity = 1.0
        self.scene.add_projector(proj1)

        print("✅ Test scene created")

    def _create_plane_geometry(self, obj):
        """Create plane geometry (simple quad)"""
        # Vertices: position (3) + normal (3)
        vertices = np.array([
            # Position            Normal
            -1.0, 0.0, -1.0,     0.0, 1.0, 0.0,  # Bottom-left
             1.0, 0.0, -1.0,     0.0, 1.0, 0.0,  # Bottom-right
             1.0, 0.0,  1.0,     0.0, 1.0, 0.0,  # Top-right
            -1.0, 0.0,  1.0,     0.0, 1.0, 0.0,  # Top-left
        ], dtype=np.float32)

        # Indices (two triangles)
        indices = np.array([
            0, 1, 2,  # First triangle
            0, 2, 3,  # Second triangle
        ], dtype=np.uint32)

        # Create VBO and IBO
        obj.vbo = self.window.ctx.buffer(vertices.tobytes())
        obj.ibo = self.window.ctx.buffer(indices.tobytes())

    def handle_camera_controls(self):
        """Handle camera orbit/pan/zoom controls"""
        # Mouse button state
        left_btn = self.window.is_mouse_button_pressed(0)
        middle_btn = self.window.is_mouse_button_pressed(1)
        right_btn = self.window.is_mouse_button_pressed(2)

        # Get mouse movement
        mouse_pos = self.window.get_mouse_pos()
        if hasattr(self, 'last_mouse_pos'):
            dx = mouse_pos[0] - self.last_mouse_pos[0]
            dy = mouse_pos[1] - self.last_mouse_pos[1]
        else:
            dx, dy = 0, 0
        self.last_mouse_pos = mouse_pos

        # Orbit (left mouse button or Alt + left)
        if left_btn and not middle_btn:
            if dx != 0 or dy != 0:
                sensitivity = 0.005
                self.camera.orbit(dx * sensitivity, -dy * sensitivity)

        # Pan (middle mouse button or Shift + left)
        if middle_btn:
            if dx != 0 or dy != 0:
                sensitivity = 0.02
                self.camera.pan(-dx * sensitivity, dy * sensitivity)

        # Zoom (mouse wheel)
        # This would be handled in the event loop

    def run(self):
        """Main application loop"""
        print("\n🚀 Starting main loop...")

        while self.window.running:
            # Poll events
            events = self.window.poll_events()

            # Process UI events
            self.ui.process_events(events)

            # Handle pygame events
            for event in events:
                if event.type == MOUSEWHEEL:
                    # Zoom camera
                    self.camera.zoom(-event.y * 0.5)

            # Handle camera controls
            self.handle_camera_controls()

            # Update timeline
            self.timeline.update(self.window.delta_time)

            # Render depth passes (shadow maps)
            for projector in self.scene.projectors:
                if projector.active:
                    self.renderer.render_depth_pass(projector, self.scene)

            # Render main scene
            self.renderer.render_scene(self.scene, self.camera)

            # Render helpers (grid, axes)
            self.renderer.render_helpers(self.scene, self.camera)

            # Render UI
            self.ui.begin_frame()
            self.ui.render_menu_bar(self.scene, self.timeline)
            self.ui.render_scene_panel(self.scene)
            self.ui.render_properties_panel()
            self.ui.render_timeline_panel(self.timeline)
            self.ui.render_debug_panel(self.window, self.renderer, self.camera)
            self.ui.end_frame()

            # Swap buffers
            self.window.swap_buffers()

    def cleanup(self):
        """Cleanup application resources"""
        print("\n🧹 Cleaning up...")
        self.renderer.cleanup()
        self.ui.cleanup()
        self.window.cleanup()
        print("✅ Cleanup complete")


def main():
    """Main entry point"""
    try:
        app = Application(width=1920, height=1080)
        app.run()
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        if 'app' in locals():
            app.cleanup()

    return 0


if __name__ == "__main__":
    sys.exit(main())
