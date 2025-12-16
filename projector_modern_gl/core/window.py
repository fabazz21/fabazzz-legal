"""
Window Management with GLFW
Handles window creation, input, and events
"""

import glfw
import sys


class Window:
    """GLFW Window Manager"""

    def __init__(self, width=1920, height=1080, title="Projection Mapping", vsync=True):
        """Initialize GLFW window"""
        self.width = width
        self.height = height
        self.title = title
        self.vsync = vsync

        # Input state
        self.keys = {}
        self.mouse_pos = (0, 0)
        self.mouse_delta = (0, 0)
        self.mouse_buttons = {}
        self.scroll_offset = 0.0

        # Create window
        self._create_window()

    def _create_window(self):
        """Create GLFW window with OpenGL 3.3 Core context"""
        # Window hints
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)
        glfw.window_hint(glfw.RESIZABLE, glfw.TRUE)
        glfw.window_hint(glfw.SAMPLES, 4)  # 4x MSAA

        # Create window
        self.glfw_window = glfw.create_window(
            self.width, self.height, self.title, None, None
        )

        if not self.glfw_window:
            glfw.terminate()
            raise RuntimeError("Failed to create GLFW window")

        # Make context current
        glfw.make_context_current(self.glfw_window)

        # Set vsync
        glfw.swap_interval(1 if self.vsync else 0)

        # Setup callbacks
        self._setup_callbacks()

        print(f"✅ Window created: {self.width}x{self.height}")

    def _setup_callbacks(self):
        """Setup GLFW callbacks for input"""
        glfw.set_key_callback(self.glfw_window, self._key_callback)
        glfw.set_cursor_pos_callback(self.glfw_window, self._mouse_callback)
        glfw.set_mouse_button_callback(self.glfw_window, self._mouse_button_callback)
        glfw.set_scroll_callback(self.glfw_window, self._scroll_callback)
        glfw.set_framebuffer_size_callback(self.glfw_window, self._resize_callback)

    def _key_callback(self, window, key, scancode, action, mods):
        """Keyboard callback"""
        if action == glfw.PRESS:
            self.keys[key] = True
        elif action == glfw.RELEASE:
            self.keys[key] = False

    def _mouse_callback(self, window, xpos, ypos):
        """Mouse movement callback"""
        old_pos = self.mouse_pos
        self.mouse_pos = (xpos, ypos)
        self.mouse_delta = (xpos - old_pos[0], ypos - old_pos[1])

    def _mouse_button_callback(self, window, button, action, mods):
        """Mouse button callback"""
        if action == glfw.PRESS:
            self.mouse_buttons[button] = True
        elif action == glfw.RELEASE:
            self.mouse_buttons[button] = False

    def _scroll_callback(self, window, xoffset, yoffset):
        """Scroll callback"""
        self.scroll_offset = yoffset

    def _resize_callback(self, window, width, height):
        """Framebuffer resize callback"""
        self.width = width
        self.height = height

    def is_key_pressed(self, key):
        """Check if key is currently pressed"""
        return self.keys.get(key, False)

    def is_mouse_button_pressed(self, button):
        """Check if mouse button is pressed"""
        return self.mouse_buttons.get(button, False)

    def get_mouse_delta(self):
        """Get mouse movement delta and reset"""
        delta = self.mouse_delta
        self.mouse_delta = (0, 0)
        return delta

    def get_scroll_offset(self):
        """Get scroll offset and reset"""
        offset = self.scroll_offset
        self.scroll_offset = 0.0
        return offset

    def should_close(self):
        """Check if window should close"""
        return glfw.window_should_close(self.glfw_window)

    def swap_buffers(self):
        """Swap front and back buffers"""
        glfw.swap_buffers(self.glfw_window)

    def poll_events(self):
        """Poll for events"""
        glfw.poll_events()

    def get_time(self):
        """Get current time"""
        return glfw.get_time()

    def set_title(self, title):
        """Set window title"""
        self.title = title
        glfw.set_window_title(self.glfw_window, title)

    def close(self):
        """Close window"""
        glfw.set_window_should_close(self.glfw_window, True)

    def __del__(self):
        """Cleanup"""
        if hasattr(self, 'glfw_window'):
            glfw.destroy_window(self.glfw_window)
