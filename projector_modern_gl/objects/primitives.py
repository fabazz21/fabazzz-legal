"""
3D Primitive Shapes
Cube, Sphere, Plane, Cylinder, Cone, Torus
"""

import numpy as np
import moderngl
from .base_object import Object3D


class Cube(Object3D):
    """Cube primitive"""

    def __init__(self, size=1.0, ctx=None):
        super().__init__("Cube", ctx)
        self.size = size
        self._create_geometry()

    def _create_geometry(self):
        """Create cube geometry"""
        s = self.size / 2

        # Cube vertices (position + normal)
        vertices = np.array([
            # Front face
            -s, -s,  s,  0,  0,  1,
             s, -s,  s,  0,  0,  1,
             s,  s,  s,  0,  0,  1,
            -s,  s,  s,  0,  0,  1,
            # Back face
            -s, -s, -s,  0,  0, -1,
            -s,  s, -s,  0,  0, -1,
             s,  s, -s,  0,  0, -1,
             s, -s, -s,  0,  0, -1,
            # Top face
            -s,  s, -s,  0,  1,  0,
            -s,  s,  s,  0,  1,  0,
             s,  s,  s,  0,  1,  0,
             s,  s, -s,  0,  1,  0,
            # Bottom face
            -s, -s, -s,  0, -1,  0,
             s, -s, -s,  0, -1,  0,
             s, -s,  s,  0, -1,  0,
            -s, -s,  s,  0, -1,  0,
            # Right face
             s, -s, -s,  1,  0,  0,
             s,  s, -s,  1,  0,  0,
             s,  s,  s,  1,  0,  0,
             s, -s,  s,  1,  0,  0,
            # Left face
            -s, -s, -s, -1,  0,  0,
            -s, -s,  s, -1,  0,  0,
            -s,  s,  s, -1,  0,  0,
            -s,  s, -s, -1,  0,  0,
        ], dtype='f4')

        # Indices
        indices = np.array([
            0,  1,  2,   0,  2,  3,   # Front
            4,  5,  6,   4,  6,  7,   # Back
            8,  9, 10,   8, 10, 11,   # Top
            12, 13, 14,  12, 14, 15,  # Bottom
            16, 17, 18,  16, 18, 19,  # Right
            20, 21, 22,  20, 22, 23   # Left
        ], dtype='i4')

        self.vertices = vertices
        self.indices = indices

        if self.ctx:
            self.vbo = self.ctx.buffer(vertices.tobytes())
            self.ibo = self.ctx.buffer(indices.tobytes())
            self.vao = self.ctx.vertex_array(
                None,  # Program will be set during rendering
                [(self.vbo, '3f 3f', 'in_position', 'in_normal')],
                self.ibo
            )


class Plane(Object3D):
    """Plane primitive"""

    def __init__(self, width=4.0, height=4.0, ctx=None):
        super().__init__("Plane", ctx)
        self.width = width
        self.height = height
        self._create_geometry()

    def _create_geometry(self):
        """Create plane geometry"""
        w = self.width / 2
        h = self.height / 2

        # Plane vertices (facing +Z)
        vertices = np.array([
            -w, -h, 0,  0, 0, 1,
             w, -h, 0,  0, 0, 1,
             w,  h, 0,  0, 0, 1,
            -w,  h, 0,  0, 0, 1,
        ], dtype='f4')

        indices = np.array([
            0, 1, 2,  0, 2, 3
        ], dtype='i4')

        self.vertices = vertices
        self.indices = indices

        if self.ctx:
            self.vbo = self.ctx.buffer(vertices.tobytes())
            self.ibo = self.ctx.buffer(indices.tobytes())
            self.vao = self.ctx.vertex_array(
                None,
                [(self.vbo, '3f 3f', 'in_position', 'in_normal')],
                self.ibo
            )


class Sphere(Object3D):
    """Sphere primitive"""

    def __init__(self, radius=1.0, segments=32, ctx=None):
        super().__init__("Sphere", ctx)
        self.radius = radius
        self.segments = segments
        self._create_geometry()

    def _create_geometry(self):
        """Create sphere geometry using UV sphere method"""
        vertices = []
        indices = []

        # Generate vertices
        for lat in range(self.segments + 1):
            theta = lat * np.pi / self.segments
            sin_theta = np.sin(theta)
            cos_theta = np.cos(theta)

            for lon in range(self.segments + 1):
                phi = lon * 2 * np.pi / self.segments
                sin_phi = np.sin(phi)
                cos_phi = np.cos(phi)

                x = cos_phi * sin_theta
                y = cos_theta
                z = sin_phi * sin_theta

                # Position
                vertices.extend([
                    x * self.radius,
                    y * self.radius,
                    z * self.radius
                ])

                # Normal
                vertices.extend([x, y, z])

        # Generate indices
        for lat in range(self.segments):
            for lon in range(self.segments):
                first = lat * (self.segments + 1) + lon
                second = first + self.segments + 1

                indices.extend([first, second, first + 1])
                indices.extend([second, second + 1, first + 1])

        self.vertices = np.array(vertices, dtype='f4')
        self.indices = np.array(indices, dtype='i4')

        if self.ctx:
            self.vbo = self.ctx.buffer(self.vertices.tobytes())
            self.ibo = self.ctx.buffer(self.indices.tobytes())
            self.vao = self.ctx.vertex_array(
                None,
                [(self.vbo, '3f 3f', 'in_position', 'in_normal')],
                self.ibo
            )


class Cylinder(Object3D):
    """Cylinder primitive"""

    def __init__(self, radius=1.0, height=2.0, segments=32, ctx=None):
        super().__init__("Cylinder", ctx)
        self.radius = radius
        self.height = height
        self.segments = segments
        self._create_geometry()

    def _create_geometry(self):
        """Create cylinder geometry"""
        vertices = []
        indices = []

        h = self.height / 2

        # Side vertices
        for i in range(self.segments + 1):
            angle = 2 * np.pi * i / self.segments
            x = np.cos(angle) * self.radius
            z = np.sin(angle) * self.radius

            # Bottom vertex
            vertices.extend([x, -h, z, x, 0, z])
            # Top vertex
            vertices.extend([x, h, z, x, 0, z])

        # Side indices
        for i in range(self.segments):
            base = i * 2
            indices.extend([base, base + 1, base + 2])
            indices.extend([base + 1, base + 3, base + 2])

        self.vertices = np.array(vertices, dtype='f4')
        self.indices = np.array(indices, dtype='i4')

        if self.ctx:
            self.vbo = self.ctx.buffer(self.vertices.tobytes())
            self.ibo = self.ctx.buffer(self.indices.tobytes())
            self.vao = self.ctx.vertex_array(
                None,
                [(self.vbo, '3f 3f', 'in_position', 'in_normal')],
                self.ibo
            )


class Cone(Object3D):
    """Cone primitive"""

    def __init__(self, radius=1.0, height=2.0, segments=32, ctx=None):
        super().__init__("Cone", ctx)
        self.radius = radius
        self.height = height
        self.segments = segments
        self._create_geometry()

    def _create_geometry(self):
        """Create cone geometry"""
        vertices = []
        indices = []

        h = self.height / 2

        # Apex vertex
        apex_index = 0
        vertices.extend([0, h, 0, 0, 1, 0])

        # Base vertices
        for i in range(self.segments + 1):
            angle = 2 * np.pi * i / self.segments
            x = np.cos(angle) * self.radius
            z = np.sin(angle) * self.radius

            # Normal calculation for cone side
            nx = x
            nz = z
            ny = self.radius / self.height
            length = np.sqrt(nx*nx + ny*ny + nz*nz)
            nx, ny, nz = nx/length, ny/length, nz/length

            vertices.extend([x, -h, z, nx, ny, nz])

        # Side indices
        for i in range(self.segments):
            indices.extend([apex_index, i + 2, i + 1])

        self.vertices = np.array(vertices, dtype='f4')
        self.indices = np.array(indices, dtype='i4')

        if self.ctx:
            self.vbo = self.ctx.buffer(self.vertices.tobytes())
            self.ibo = self.ctx.buffer(self.indices.tobytes())
            self.vao = self.ctx.vertex_array(
                None,
                [(self.vbo, '3f 3f', 'in_position', 'in_normal')],
                self.ibo
            )


def create_primitive(primitive_type, ctx=None):
    """Factory function to create primitives"""
    primitives = {
        'cube': Cube,
        'plane': Plane,
        'sphere': Sphere,
        'cylinder': Cylinder,
        'cone': Cone
    }

    if primitive_type.lower() in primitives:
        return primitives[primitive_type.lower()](ctx=ctx)
    else:
        raise ValueError(f"Unknown primitive type: {primitive_type}")
