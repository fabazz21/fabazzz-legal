#!/usr/bin/env python3
"""
Professional 3D Projection Mapping System - ModernGL
Main Application Entry Point

Features:
- Multi-projector shadow-mapped rendering
- Timeline-based animation system
- Photometric analysis
- Professional UI with ImGui
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
from ui.main_ui import MainUI
from timeline.timeline import Timeline
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

        # Application state
        self.running = True
        self.delta_time = 0.0
        self.last_frame = glfw.get_time()
        self.frame_count = 0
        self.fps = 0.0

        print(f"✅ Projection Mapping System Initialized")
        print(f"   OpenGL Version: {self.ctx.info['GL_VERSION']}")
        print(f"   GLSL Version: {self.ctx.info['GL_SHADING_LANGUAGE_VERSION']}")
        print(f"   Renderer: {self.ctx.info['GL_RENDERER']}")
        print(f"   Vendor: {self.ctx.info['GL_VENDOR']}")

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
        # Update camera
        self.camera.update(self.window, dt)

        # Update timeline if playing
        if self.timeline.playing:
            self.timeline.update(dt)
            # Apply keyframes to scene objects
            self.timeline.apply_keyframes(self.scene)

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

        # Render helpers (frustums, gizmos, grid, etc.)
        if self.scene.show_helpers:
            self.renderer.render_helpers(self.scene, self.camera)

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
