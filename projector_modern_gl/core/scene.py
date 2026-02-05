"""
3D Scene Management System
"""

import numpy as np
from pyrr import Matrix44, Vector3
import json


class SceneObject:
    """Base 3D object in scene"""

    def __init__(self, name="Object"):
        """Initialize scene object"""
        self.name = name
        self.position = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.rotation = np.array([0.0, 0.0, 0.0], dtype=np.float32)  # Euler angles (radians)
        self.scale = np.array([1.0, 1.0, 1.0], dtype=np.float32)

        # Rendering properties
        self.visible = True
        self.cast_shadow = True
        self.receive_shadow = True

        # Geometry (VBO/IBO)
        self.vbo = None  # Vertex buffer object
        self.ibo = None  # Index buffer object
        self.vao = None  # Vertex array object
        self.vao_depth = None  # VAO for depth pass

    def get_model_matrix(self):
        """Get model transformation matrix"""
        # Translation
        trans = Matrix44.from_translation(self.position)

        # Rotation (XYZ Euler)
        rot_x = Matrix44.from_x_rotation(self.rotation[0])
        rot_y = Matrix44.from_y_rotation(self.rotation[1])
        rot_z = Matrix44.from_z_rotation(self.rotation[2])
        rot = rot_z @ rot_y @ rot_x

        # Scale
        scale = Matrix44.from_scale(self.scale)

        # Combined transform
        return trans @ rot @ scale

    def set_geometry(self, vertices, indices):
        """Set geometry data (vertices and indices)"""
        # This will be called by geometry creation functions
        pass

    def __repr__(self):
        return f"<SceneObject '{self.name}' pos={self.position}>"


class Projector(SceneObject):
    """3D Projector for projection mapping"""

    def __init__(self, name="Projector"):
        """Initialize projector"""
        super().__init__(name)

        # Projector properties
        self.active = True
        self.intensity = 1.0
        self.texture = None
        self.depth_fbo_index = 0

        # Projection parameters
        self.fov = 40.0  # Field of view in degrees
        self.aspect = 16.0 / 10.0  # Aspect ratio (16:10 typical projector)
        self.near = 0.1
        self.far = 50.0
        self.projection_far = 50.0

        # Shadow mapping
        self.shadow_bias = 0.005

        # Keystone correction (trapezoid correction)
        self.keystone_v = 0.0
        self.keystone_h = 0.0
        self.keystone_tl_x = 0.0
        self.keystone_tl_y = 0.0
        self.keystone_tr_x = 0.0
        self.keystone_tr_y = 0.0
        self.keystone_bl_x = 0.0
        self.keystone_bl_y = 0.0
        self.keystone_br_x = 0.0
        self.keystone_br_y = 0.0

        # Soft edge blending
        self.soft_edge_l = 0.0  # Left
        self.soft_edge_r = 0.0  # Right
        self.soft_edge_t = 0.0  # Top
        self.soft_edge_b = 0.0  # Bottom
        self.soft_edge_gamma = 2.2

        # Corner pin (perspective warping)
        self.corner_pin_tl_x = 0.0
        self.corner_pin_tl_y = 0.0
        self.corner_pin_tr_x = 0.0
        self.corner_pin_tr_y = 0.0
        self.corner_pin_bl_x = 0.0
        self.corner_pin_bl_y = 0.0
        self.corner_pin_br_x = 0.0
        self.corner_pin_br_y = 0.0

    def get_view_matrix(self):
        """Get view matrix (projector looking down -Z axis)"""
        # Calculate target point (projector looks down -Z in local space)
        forward = np.array([0.0, 0.0, -1.0])

        # Apply rotation
        rot_x = Matrix44.from_x_rotation(self.rotation[0])
        rot_y = Matrix44.from_y_rotation(self.rotation[1])
        rot_z = Matrix44.from_z_rotation(self.rotation[2])
        rot = rot_z @ rot_y @ rot_x

        # Transform forward vector
        forward_4d = np.array([forward[0], forward[1], forward[2], 0.0])
        forward_transformed = (rot @ forward_4d)[:3]

        target = self.position + forward_transformed

        # Up vector
        up = np.array([0.0, 1.0, 0.0])

        return Matrix44.look_at(self.position, target, up)

    def get_projection_matrix(self):
        """Get projection matrix"""
        return Matrix44.perspective_projection(
            self.fov,
            self.aspect,
            self.near,
            self.far
        )

    def get_shadow_matrix(self):
        """Get shadow matrix (bias matrix for depth comparison)"""
        bias = np.array([
            [0.5, 0.0, 0.0, 0.5],
            [0.0, 0.5, 0.0, 0.5],
            [0.0, 0.0, 0.5, 0.5],
            [0.0, 0.0, 0.0, 1.0]
        ], dtype=np.float32)

        return bias @ self.get_projection_matrix() @ self.get_view_matrix()

    def __repr__(self):
        state = "ON" if self.active else "OFF"
        return f"<Projector '{self.name}' {state} intensity={self.intensity:.2f}>"


class Scene:
    """3D Scene Container"""

    def __init__(self):
        """Initialize scene"""
        self.objects = []
        self.projectors = []

        # Lighting
        self.ambient_light_intensity = 0.3
        self.directional_light_intensity = 0.7
        self.directional_light_direction = np.array([-0.5, -1.0, -0.5], dtype=np.float32)
        self.directional_light_direction /= np.linalg.norm(self.directional_light_direction)

        # Grid and axes
        self.show_grid = True
        self.show_axes = True
        self.show_helpers = True
        self.grid_size = 20
        self.grid_spacing = 1.0

        # Generate grid and axes
        self._generate_grid()
        self._generate_axes()

        print("✅ Scene initialized")

    def add_object(self, obj):
        """Add object to scene"""
        self.objects.append(obj)
        return obj

    def add_projector(self, projector):
        """Add projector to scene"""
        projector.depth_fbo_index = len(self.projectors)
        self.projectors.append(projector)
        return projector

    def remove_object(self, obj):
        """Remove object from scene"""
        if obj in self.objects:
            self.objects.remove(obj)

    def remove_projector(self, projector):
        """Remove projector from scene"""
        if projector in self.projectors:
            self.projectors.remove(projector)

    def get_visible_objects(self):
        """Get all visible objects"""
        return [obj for obj in self.objects if obj.visible]

    def _generate_grid(self):
        """Generate grid lines"""
        self.grid = []
        half_size = self.grid_size / 2

        # Grid color
        color = (0.2, 0.2, 0.2)

        # Lines parallel to X axis
        for i in range(self.grid_size + 1):
            z = -half_size + i * self.grid_spacing
            self.grid.append({
                "start": np.array([-half_size, 0.0, z]),
                "end": np.array([half_size, 0.0, z]),
                "color": color
            })

        # Lines parallel to Z axis
        for i in range(self.grid_size + 1):
            x = -half_size + i * self.grid_spacing
            self.grid.append({
                "start": np.array([x, 0.0, -half_size]),
                "end": np.array([x, 0.0, half_size]),
                "color": color
            })

    def _generate_axes(self):
        """Generate axis lines"""
        self.axes = [
            # X axis (red)
            {
                "start": np.array([0.0, 0.0, 0.0]),
                "end": np.array([2.0, 0.0, 0.0]),
                "color": (1.0, 0.0, 0.0)
            },
            # Y axis (green)
            {
                "start": np.array([0.0, 0.0, 0.0]),
                "end": np.array([0.0, 2.0, 0.0]),
                "color": (0.0, 1.0, 0.0)
            },
            # Z axis (blue)
            {
                "start": np.array([0.0, 0.0, 0.0]),
                "end": np.array([0.0, 0.0, 2.0]),
                "color": (0.0, 0.0, 1.0)
            },
        ]

    def export_to_json(self, filepath):
        """Export scene to JSON"""
        data = {
            "objects": [],
            "projectors": [],
            "lighting": {
                "ambient": self.ambient_light_intensity,
                "directional_intensity": self.directional_light_intensity,
                "directional_direction": self.directional_light_direction.tolist()
            }
        }

        # Export objects
        for obj in self.objects:
            data["objects"].append({
                "name": obj.name,
                "position": obj.position.tolist(),
                "rotation": obj.rotation.tolist(),
                "scale": obj.scale.tolist(),
                "visible": obj.visible
            })

        # Export projectors
        for proj in self.projectors:
            data["projectors"].append({
                "name": proj.name,
                "position": proj.position.tolist(),
                "rotation": proj.rotation.tolist(),
                "active": proj.active,
                "intensity": proj.intensity,
                "fov": proj.fov,
                "aspect": proj.aspect
            })

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"✅ Scene exported to {filepath}")

    def load_from_json(self, filepath):
        """Load scene from JSON"""
        with open(filepath, 'r') as f:
            data = json.load(f)

        # Clear scene
        self.objects.clear()
        self.projectors.clear()

        # Load lighting
        if "lighting" in data:
            self.ambient_light_intensity = data["lighting"].get("ambient", 0.3)
            self.directional_light_intensity = data["lighting"].get("directional_intensity", 0.7)
            self.directional_light_direction = np.array(
                data["lighting"].get("directional_direction", [-0.5, -1.0, -0.5]),
                dtype=np.float32
            )

        # Load objects
        for obj_data in data.get("objects", []):
            obj = SceneObject(obj_data["name"])
            obj.position = np.array(obj_data["position"], dtype=np.float32)
            obj.rotation = np.array(obj_data["rotation"], dtype=np.float32)
            obj.scale = np.array(obj_data["scale"], dtype=np.float32)
            obj.visible = obj_data.get("visible", True)
            self.add_object(obj)

        # Load projectors
        for proj_data in data.get("projectors", []):
            proj = Projector(proj_data["name"])
            proj.position = np.array(proj_data["position"], dtype=np.float32)
            proj.rotation = np.array(proj_data["rotation"], dtype=np.float32)
            proj.active = proj_data.get("active", True)
            proj.intensity = proj_data.get("intensity", 1.0)
            proj.fov = proj_data.get("fov", 40.0)
            proj.aspect = proj_data.get("aspect", 1.6)
            self.add_projector(proj)

        print(f"✅ Scene loaded from {filepath}")

    def __repr__(self):
        return f"<Scene objects={len(self.objects)} projectors={len(self.projectors)}>"
