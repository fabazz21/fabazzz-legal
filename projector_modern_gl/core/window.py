"""
Window Management with ModernGL
"""

import moderngl
import pygame
from pygame.locals import *


class Window:
    """OpenGL Window with Pygame"""

    def __init__(self, width=1920, height=1080, title="Projector Fusion", fullscreen=False):
        """Initialize window"""
        self.width = width
        self.height = height
        self.title = title
        self.fullscreen = fullscreen

        # Initialize Pygame
        pygame.init()

        # Set OpenGL attributes
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)
        pygame.display.gl_set_attribute(pygame.GL_STENCIL_SIZE, 8)

        # Create window
        flags = OPENGL | DOUBLEBUF
        if fullscreen:
            flags |= FULLSCREEN

        self.screen = pygame.display.set_mode((width, height), flags)
        pygame.display.set_caption(title)

        # Create ModernGL context
        self.ctx = moderngl.create_context()

        # Enable depth testing
        self.ctx.enable(moderngl.DEPTH_TEST)
        self.ctx.enable(moderngl.CULL_FACE)
        self.ctx.cull_face = 'back'

        # Frame timing
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.frame_time = 0
        self.delta_time = 0

        # Event state
        self.running = True
        self.mouse_pos = (0, 0)
        self.mouse_buttons = [False, False, False]
        self.keys = pygame.key.get_pressed()

        print(f"✅ Window created: {width}x{height}")
        print(f"   OpenGL Version: {self.ctx.version_code}")
        print(f"   Vendor: {self.ctx.info['GL_VENDOR']}")
        print(f"   Renderer: {self.ctx.info['GL_RENDERER']}")

    def poll_events(self):
        """Poll window events"""
        events = []

        for event in pygame.event.get():
            events.append(event)

            # Window close
            if event.type == QUIT:
                self.running = False

            # Key events
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False

            # Mouse events
            elif event.type == MOUSEBUTTONDOWN:
                if event.button <= 3:
                    self.mouse_buttons[event.button - 1] = True

            elif event.type == MOUSEBUTTONUP:
                if event.button <= 3:
                    self.mouse_buttons[event.button - 1] = False

            elif event.type == MOUSEMOTION:
                self.mouse_pos = event.pos

        # Update key state
        self.keys = pygame.key.get_pressed()

        return events

    def swap_buffers(self):
        """Swap OpenGL buffers"""
        pygame.display.flip()

        # Update timing
        self.delta_time = self.clock.tick(self.fps) / 1000.0  # Convert to seconds
        self.frame_time += self.delta_time

    def resize(self, width, height):
        """Resize window"""
        self.width = width
        self.height = height
        self.ctx.viewport = (0, 0, width, height)

    def get_mouse_pos(self):
        """Get mouse position"""
        return self.mouse_pos

    def get_mouse_delta(self):
        """Get mouse movement delta"""
        return pygame.mouse.get_rel()

    def is_key_pressed(self, key):
        """Check if key is pressed"""
        return self.keys[key]

    def is_mouse_button_pressed(self, button):
        """Check if mouse button is pressed (0=left, 1=middle, 2=right)"""
        if 0 <= button < len(self.mouse_buttons):
            return self.mouse_buttons[button]
        return False

    def set_cursor_visible(self, visible):
        """Set mouse cursor visibility"""
        pygame.mouse.set_visible(visible)

    def set_cursor_grabbed(self, grabbed):
        """Set mouse cursor grabbed (relative mode)"""
        pygame.event.set_grab(grabbed)
        pygame.mouse.set_visible(not grabbed)

    def cleanup(self):
        """Cleanup window resources"""
        pygame.quit()
        print("✅ Window closed")

    def __repr__(self):
        return f"<Window {self.width}x{self.height} fps={int(self.clock.get_fps())}>"
