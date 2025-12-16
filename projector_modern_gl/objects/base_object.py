"""
Base 3D Object Class
"""

import numpy as np
from pyrr import Matrix44, Vector3, Quaternion


class Object3D:
    """Base class for all 3D objects in the scene"""

    # Class-level ID counter
    _id_counter = 0

    def __init__(self, name="Object", ctx=None):
        """Initialize 3D object"""
        # Generate unique ID
        Object3D._id_counter += 1
        self.id = Object3D._id_counter

        self.name = name
        self.ctx = ctx

        # Transform
        self.position = Vector3([0.0, 0.0, 0.0])
        self.rotation = Quaternion()
        self.scale = Vector3([1.0, 1.0, 1.0])

        # Rendering
        self.visible = True
        self.cast_shadow = True
        self.receive_shadow = True

        # Geometry
        self.vao = None  # Vertex Array Object
        self.vbo = None  # Vertex Buffer Object
        self.vertices = None
        self.indices = None

        # Material
        self.color = [0.533, 0.533, 0.533]  # #888888

    def get_model_matrix(self):
        """Calculate model matrix from transform"""
        # Translation
        translation = Matrix44.from_translation(self.position)

        # Rotation (from quaternion)
        rotation = self.rotation.matrix44

        # Scale
        scale = Matrix44.from_scale(self.scale)

        # Combine: T * R * S
        model = translation * rotation * scale

        return np.array(model, dtype=np.float32)

    def set_position(self, x, y, z):
        """Set object position"""
        self.position = Vector3([x, y, z])

    def set_rotation(self, x_deg, y_deg, z_deg):
        """Set rotation from Euler angles (degrees)"""
        import math
        x_rad = math.radians(x_deg)
        y_rad = math.radians(y_deg)
        z_rad = math.radians(z_deg)

        # Create quaternion from Euler angles
        qx = Quaternion.from_x_rotation(x_rad)
        qy = Quaternion.from_y_rotation(y_rad)
        qz = Quaternion.from_z_rotation(z_rad)

        self.rotation = qz * qy * qx

    def set_scale(self, x, y, z):
        """Set object scale"""
        self.scale = Vector3([x, y, z])

    def update(self, dt):
        """Update object (override in subclass if needed)"""
        pass

    def cleanup(self):
        """Cleanup resources"""
        if self.vao:
            self.vao.release()
        if self.vbo:
            self.vbo.release()

    def __repr__(self):
        return f"<{self.__class__.__name__} '{self.name}' at ({self.position[0]:.1f}, {self.position[1]:.1f}, {self.position[2]:.1f})>"
