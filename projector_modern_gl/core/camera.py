"""
3D Camera System
"""

import numpy as np
from pyrr import Matrix44, Vector3


class Camera:
    """3D Perspective Camera"""

    def __init__(self, position=(0, 5, 10), target=(0, 0, 0), up=(0, 1, 0)):
        """Initialize camera"""
        self.position = np.array(position, dtype=np.float32)
        self.target = np.array(target, dtype=np.float32)
        self.up = np.array(up, dtype=np.float32)

        # Projection parameters
        self.fov = 45.0  # Field of view in degrees
        self.aspect = 16.0 / 9.0  # Aspect ratio
        self.near = 0.1
        self.far = 1000.0

        # Orbit controls
        self.orbit_distance = np.linalg.norm(self.position - self.target)
        self.orbit_theta = 0.0  # Horizontal angle
        self.orbit_phi = 0.0  # Vertical angle

        self._update_orbit_angles()

    def _update_orbit_angles(self):
        """Update orbit angles from position and target"""
        offset = self.position - self.target
        self.orbit_distance = np.linalg.norm(offset)

        if self.orbit_distance > 0.0001:
            offset_normalized = offset / self.orbit_distance
            self.orbit_phi = np.arcsin(np.clip(offset_normalized[1], -1.0, 1.0))
            self.orbit_theta = np.arctan2(offset_normalized[0], offset_normalized[2])

    def orbit(self, delta_theta, delta_phi):
        """Orbit camera around target"""
        self.orbit_theta += delta_theta
        self.orbit_phi = np.clip(self.orbit_phi + delta_phi, -np.pi / 2 + 0.01, np.pi / 2 - 0.01)

        # Calculate new position
        x = self.orbit_distance * np.cos(self.orbit_phi) * np.sin(self.orbit_theta)
        y = self.orbit_distance * np.sin(self.orbit_phi)
        z = self.orbit_distance * np.cos(self.orbit_phi) * np.cos(self.orbit_theta)

        self.position = self.target + np.array([x, y, z], dtype=np.float32)

    def pan(self, delta_x, delta_y):
        """Pan camera (move target and position together)"""
        # Get camera right and up vectors
        forward = self.target - self.position
        forward = forward / np.linalg.norm(forward)
        right = np.cross(forward, self.up)
        right = right / np.linalg.norm(right)
        up = np.cross(right, forward)

        # Move target and position
        offset = right * delta_x + up * delta_y
        self.position += offset
        self.target += offset

    def zoom(self, delta):
        """Zoom camera (change orbit distance)"""
        self.orbit_distance = max(0.1, self.orbit_distance + delta)

        # Recalculate position
        offset = self.position - self.target
        if np.linalg.norm(offset) > 0.0001:
            offset = offset / np.linalg.norm(offset) * self.orbit_distance
            self.position = self.target + offset

    def look_at(self, target):
        """Point camera at target"""
        self.target = np.array(target, dtype=np.float32)
        self._update_orbit_angles()

    def set_position(self, position):
        """Set camera position"""
        self.position = np.array(position, dtype=np.float32)
        self._update_orbit_angles()

    def get_view_matrix(self):
        """Get view matrix (look-at matrix)"""
        return Matrix44.look_at(
            self.position,
            self.target,
            self.up
        )

    def get_projection_matrix(self):
        """Get projection matrix"""
        return Matrix44.perspective_projection(
            self.fov,
            self.aspect,
            self.near,
            self.far
        )

    def set_aspect_ratio(self, width, height):
        """Set aspect ratio from window dimensions"""
        if height > 0:
            self.aspect = width / height

    def __repr__(self):
        return f"<Camera pos={self.position} target={self.target}>"
