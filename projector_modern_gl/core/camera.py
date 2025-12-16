"""
Camera System with Orbit Controls
"""

import numpy as np
import pyrr
from pyrr import Matrix44, Vector3, Quaternion
import glfw


class Camera:
    """Perspective camera with orbit controls"""

    def __init__(self, width, height, fov=60.0, near=0.1, far=1000.0):
        """Initialize camera"""
        self.width = width
        self.height = height
        self.fov = fov
        self.near = near
        self.far = far

        # Camera position and target
        self.position = Vector3([15.0, 10.0, 15.0])
        self.target = Vector3([0.0, 0.0, 0.0])
        self.up = Vector3([0.0, 1.0, 0.0])

        # Orbit controls state
        self.distance = np.linalg.norm(self.position - self.target)
        self.azimuth = 45.0  # degrees
        self.elevation = 30.0  # degrees

        # Movement speed
        self.move_speed = 5.0
        self.rotate_speed = 0.2
        self.zoom_speed = 2.0

        # Input state
        self.last_mouse_pos = None
        self.is_orbiting = False
        self.is_panning = False

        # Update matrices
        self.update_matrices()

    def update_matrices(self):
        """Update view and projection matrices"""
        # View matrix
        self.view_matrix = Matrix44.look_at(
            self.position,
            self.target,
            self.up
        )

        # Projection matrix
        aspect = self.width / self.height if self.height > 0 else 1.0
        self.projection_matrix = Matrix44.perspective_projection(
            self.fov,
            aspect,
            self.near,
            self.far
        )

    def update(self, window, dt):
        """Update camera based on input"""
        # Keyboard movement (WASD + QE)
        move_dir = Vector3([0.0, 0.0, 0.0])

        if window.is_key_pressed(glfw.KEY_W):
            move_dir += self.get_forward()
        if window.is_key_pressed(glfw.KEY_S):
            move_dir -= self.get_forward()
        if window.is_key_pressed(glfw.KEY_A):
            move_dir -= self.get_right()
        if window.is_key_pressed(glfw.KEY_D):
            move_dir += self.get_right()
        if window.is_key_pressed(glfw.KEY_Q):
            move_dir -= self.up
        if window.is_key_pressed(glfw.KEY_E):
            move_dir += self.up

        # Apply movement
        if np.linalg.norm(move_dir) > 0:
            move_dir = move_dir / np.linalg.norm(move_dir)
            self.position += move_dir * self.move_speed * dt
            self.target += move_dir * self.move_speed * dt

        # Mouse orbit (middle mouse button)
        if window.is_mouse_button_pressed(glfw.MOUSE_BUTTON_MIDDLE):
            if not self.is_orbiting and not self.is_panning:
                self.last_mouse_pos = window.mouse_pos
                # Check if shift is pressed for panning
                if window.is_key_pressed(glfw.KEY_LEFT_SHIFT):
                    self.is_panning = True
                else:
                    self.is_orbiting = True

            delta = window.get_mouse_delta()

            if self.is_orbiting:
                # Orbit around target
                self.azimuth -= delta[0] * self.rotate_speed
                self.elevation = np.clip(
                    self.elevation - delta[1] * self.rotate_speed,
                    -89.0, 89.0
                )
                self.update_position_from_orbit()

            elif self.is_panning:
                # Pan camera
                right = self.get_right()
                up = self.up
                pan_amount = self.move_speed * dt * 0.1
                self.position -= right * delta[0] * pan_amount
                self.position -= up * delta[1] * pan_amount
                self.target -= right * delta[0] * pan_amount
                self.target -= up * delta[1] * pan_amount
        else:
            self.is_orbiting = False
            self.is_panning = False
            self.last_mouse_pos = None

        # Mouse zoom (scroll wheel)
        scroll = window.get_scroll_offset()
        if scroll != 0:
            self.distance = max(0.5, self.distance - scroll * self.zoom_speed)
            self.update_position_from_orbit()

        # Update matrices
        self.update_matrices()

    def update_position_from_orbit(self):
        """Update camera position based on orbit parameters"""
        # Convert to radians
        azimuth_rad = np.radians(self.azimuth)
        elevation_rad = np.radians(self.elevation)

        # Calculate position
        x = self.distance * np.cos(elevation_rad) * np.cos(azimuth_rad)
        y = self.distance * np.sin(elevation_rad)
        z = self.distance * np.cos(elevation_rad) * np.sin(azimuth_rad)

        self.position = self.target + Vector3([x, y, z])

    def get_forward(self):
        """Get forward direction vector"""
        forward = self.target - self.position
        if np.linalg.norm(forward) > 0:
            forward = forward / np.linalg.norm(forward)
        return forward

    def get_right(self):
        """Get right direction vector"""
        forward = self.get_forward()
        right = np.cross(forward, self.up)
        if np.linalg.norm(right) > 0:
            right = right / np.linalg.norm(right)
        return right

    def set_view(self, view_type):
        """Set camera to predefined view"""
        distance = 20.0
        self.target = Vector3([0.0, 0.0, 0.0])

        if view_type == 'top':
            self.position = Vector3([0.0, distance, 0.0])
            self.up = Vector3([0.0, 0.0, -1.0])
            self.azimuth = 0.0
            self.elevation = 90.0
        elif view_type == 'front':
            self.position = Vector3([0.0, 0.0, distance])
            self.up = Vector3([0.0, 1.0, 0.0])
            self.azimuth = 90.0
            self.elevation = 0.0
        elif view_type == 'left':
            self.position = Vector3([-distance, 0.0, 0.0])
            self.up = Vector3([0.0, 1.0, 0.0])
            self.azimuth = 0.0
            self.elevation = 0.0
        elif view_type == 'right':
            self.position = Vector3([distance, 0.0, 0.0])
            self.up = Vector3([0.0, 1.0, 0.0])
            self.azimuth = 180.0
            self.elevation = 0.0
        elif view_type == 'back':
            self.position = Vector3([0.0, 0.0, -distance])
            self.up = Vector3([0.0, 1.0, 0.0])
            self.azimuth = 270.0
            self.elevation = 0.0
        elif view_type == 'perspective':
            self.position = Vector3([15.0, 10.0, 15.0])
            self.up = Vector3([0.0, 1.0, 0.0])
            self.azimuth = 45.0
            self.elevation = 30.0

        self.distance = np.linalg.norm(self.position - self.target)
        self.update_matrices()

    def resize(self, width, height):
        """Update camera aspect ratio"""
        self.width = width
        self.height = height
        self.update_matrices()

    def get_view_matrix(self):
        """Get view matrix as numpy array"""
        return np.array(self.view_matrix, dtype=np.float32)

    def get_projection_matrix(self):
        """Get projection matrix as numpy array"""
        return np.array(self.projection_matrix, dtype=np.float32)

    def get_view_projection_matrix(self):
        """Get combined view-projection matrix"""
        return self.projection_matrix * self.view_matrix
