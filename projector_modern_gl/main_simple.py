#!/usr/bin/env python3
"""
Simple Version - No ImGui (for testing)
"""

import sys
import moderngl
import glfw
import numpy as np

from core.window import Window
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from animation.timeline import Timeline
from utils.history import History


class ProjectionMappingAppSimple:
    """Main Application Class - Simple Version"""

    def __init__(self, width=1920, height=1080, title="Projection Mapping - ModernGL (Simple)"):
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

        # Core systems
        self.scene = Scene(self.ctx)
        self.camera = Camera(width, height)
        self.renderer = Renderer(self.ctx, width, height)
        self.timeline = Timeline()
        self.history = History()

        # Application state
        self.running = True
        self.delta_time = 0.0
        self.last_frame = glfw.get_time()
        self.frame_count = 0
        self.fps = 0.0

        print(f"✅ Projection Mapping System Initialized (Simple Mode)")
        print(f"   OpenGL Version: {self.ctx.info['GL_VERSION']}")
        print(f"   GLSL Version: {self.ctx.info['GL_SHADING_LANGUAGE_VERSION']}")
        print(f"   Renderer: {self.ctx.info['GL_RENDERER']}")
        print(f"   Vendor: {self.ctx.info['GL_VENDOR']}")
        print()
        print("   Controls:")
        print("   - WASD: Move camera")
        print("   - Mouse: Rotate camera")
        print("   - ESC: Exit")
        print()

        # Add a test cube and projector
        self._setup_test_scene()

    def _setup_test_scene(self):
        """Create a simple test scene"""
        from objects.primitives import create_primitive
        from projectors.projector import Projector

        # Add a cube
        cube = create_primitive('cube', self.ctx)
        cube.name = "Test Cube"
        cube.set_position(0, 0, 0)
        self.scene.add_object(cube)
        print(f"✅ Added test cube")

        # Add a projector
        projector = Projector('panasonic_rq13k', 'et_dle055', self.ctx)
        projector.set_position(0, 3, 8)
        projector.look_at([0, 0, 0])
        self.scene.add_projector(projector)
        print(f"✅ Added test projector: {projector.name}")

    def run(self):
        """Main application loop"""
        print("\n🚀 Starting main render loop...\n")

        while self.running and not glfw.window_should_close(self.window.glfw_window):
            # Calculate delta time
            current_frame = glfw.get_time()
            self.delta_time = current_frame - self.last_frame
            self.last_frame = current_frame

            # Calculate FPS
            self.frame_count += 1
            if self.frame_count % 60 == 0:
                self.fps = 1.0 / self.delta_time if self.delta_time > 0 else 0.0
                print(f"FPS: {self.fps:.1f}")

            # Poll events
            glfw.poll_events()

            # Check for ESC key
            if glfw.get_key(self.window.glfw_window, glfw.KEY_ESCAPE) == glfw.PRESS:
                self.running = False

            # Update systems
            self.update(self.delta_time)

            # Render frame
            self.render()

            # Swap buffers
            glfw.swap_buffers(self.window.glfw_window)

        self.cleanup()

    def update(self, dt):
        """Update application state"""
        # Update camera
        self.camera.update(self.window, dt)

        # Update timeline if playing
        if self.timeline.playing:
            self.timeline.update(dt)

        # Update scene
        self.scene.update(dt)

    def render(self):
        """Render the scene"""
        # Clear framebuffer
        self.ctx.clear(0.071, 0.078, 0.090)  # #121418 background

        # Render depth pass for shadow mapping (for each active projector)
        for projector in self.scene.get_active_projectors():
            self.renderer.render_depth_pass(projector, self.scene)

        # Render main scene
        self.renderer.render_scene(self.scene, self.camera)

    def cleanup(self):
        """Cleanup resources"""
        print("\n🧹 Cleaning up resources...")

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
    print("  PROJECTION MAPPING SYSTEM - SIMPLE VERSION")
    print("  (No ImGui UI - Testing Mode)")
    print("=" * 60)
    print()

    try:
        app = ProjectionMappingAppSimple(1280, 720)
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
