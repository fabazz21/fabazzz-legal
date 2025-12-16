"""
3D Model Loader
Load 3D models from various formats (OBJ, FBX, glTF, GLB)
"""

import numpy as np
import trimesh
from ..objects.base_object import Object3D


class ModelLoader:
    """Load 3D models from files"""

    @staticmethod
    def load_model(filepath, ctx=None, name=None):
        """
        Load 3D model from file

        Args:
            filepath: Path to model file
            ctx: ModernGL context (optional)
            name: Object name (optional, defaults to filename)

        Returns:
            Object3D instance with loaded geometry

        Supported formats:
            - .obj (Wavefront OBJ)
            - .fbx (Autodesk FBX)
            - .gltf (glTF 2.0)
            - .glb (glTF Binary)
            - .stl (STL)
            - .ply (PLY)
            - .dae (COLLADA)
        """
        import os

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")

        # Load mesh using trimesh
        try:
            scene_or_mesh = trimesh.load(filepath)
        except Exception as e:
            raise ValueError(f"Failed to load model: {e}")

        # Extract name from filename if not provided
        if name is None:
            name = os.path.splitext(os.path.basename(filepath))[0]

        # Handle both Scene and Mesh objects
        if isinstance(scene_or_mesh, trimesh.Scene):
            # Scene contains multiple meshes - merge them
            meshes = []
            for geom_name, geom in scene_or_mesh.geometry.items():
                if isinstance(geom, trimesh.Trimesh):
                    meshes.append(geom)

            if len(meshes) == 0:
                raise ValueError("No valid geometry found in scene")

            # Merge all meshes
            mesh = trimesh.util.concatenate(meshes)
        else:
            mesh = scene_or_mesh

        # Create Object3D
        obj = Object3D(name=name, ctx=ctx)

        # Extract vertices and normals
        vertices = mesh.vertices.astype('f4')
        normals = mesh.vertex_normals.astype('f4')

        # Interleave position and normal data
        vertex_data = np.empty((len(vertices), 6), dtype='f4')
        vertex_data[:, 0:3] = vertices
        vertex_data[:, 3:6] = normals

        # Flatten to 1D array
        obj.vertices = vertex_data.flatten()

        # Extract indices
        if hasattr(mesh, 'faces'):
            obj.indices = mesh.faces.flatten().astype('i4')
        else:
            # Generate indices if not present
            obj.indices = np.arange(len(vertices), dtype='i4')

        # Create GPU buffers if context provided
        if ctx:
            obj.vbo = ctx.buffer(obj.vertices.tobytes())
            obj.ibo = ctx.buffer(obj.indices.tobytes())
            obj.vao = ctx.vertex_array(
                None,  # Program will be set during rendering
                [(obj.vbo, '3f 3f', 'in_position', 'in_normal')],
                obj.ibo
            )

        # Set scale based on model bounds
        bounds = mesh.bounds
        extent = bounds[1] - bounds[0]
        max_extent = max(extent)

        # Normalize to reasonable size (2.0 units)
        if max_extent > 0:
            scale_factor = 2.0 / max_extent
            obj.set_scale(scale_factor, scale_factor, scale_factor)

        print(f"  ✅ Loaded model: {name}")
        print(f"     Vertices: {len(vertices):,}")
        print(f"     Triangles: {len(obj.indices) // 3:,}")
        print(f"     Bounds: {bounds[0]} to {bounds[1]}")

        return obj

    @staticmethod
    def load_multiple_models(filepaths, ctx=None):
        """
        Load multiple models at once

        Args:
            filepaths: List of file paths
            ctx: ModernGL context

        Returns:
            List of Object3D instances
        """
        objects = []
        for filepath in filepaths:
            try:
                obj = ModelLoader.load_model(filepath, ctx)
                objects.append(obj)
            except Exception as e:
                print(f"  ⚠️ Failed to load {filepath}: {e}")

        return objects

    @staticmethod
    def get_supported_formats():
        """Get list of supported file formats"""
        return [
            '.obj',   # Wavefront OBJ
            '.fbx',   # Autodesk FBX
            '.gltf',  # glTF 2.0
            '.glb',   # glTF Binary
            '.stl',   # STL
            '.ply',   # PLY
            '.dae',   # COLLADA
            '.3ds',   # 3DS Max
            '.off',   # OFF
        ]

    @staticmethod
    def is_supported_format(filepath):
        """Check if file format is supported"""
        import os
        ext = os.path.splitext(filepath)[1].lower()
        return ext in ModelLoader.get_supported_formats()


class MannequinLoader:
    """Load and create articulated mannequin figure"""

    @staticmethod
    def create_mannequin(ctx=None, height=1.8):
        """
        Create articulated mannequin figure

        Args:
            ctx: ModernGL context
            height: Mannequin height in meters (default: 1.8m)

        Returns:
            List of Object3D parts (head, torso, arms, legs)
        """
        from ..objects.primitives import Sphere, Cube, Cylinder

        parts = []
        scale = height / 1.8  # Normalize to 1.8m standard height

        # Head (sphere)
        head = Sphere(radius=0.1 * scale, ctx=ctx)
        head.name = "Mannequin_Head"
        head.set_position(0, 1.6 * scale, 0)
        head.color = [0.8, 0.7, 0.6]  # Skin tone
        parts.append(head)

        # Torso (stretched cube)
        torso = Cube(size=0.3 * scale, ctx=ctx)
        torso.name = "Mannequin_Torso"
        torso.set_position(0, 1.2 * scale, 0)
        torso.set_scale(1.0, 1.5, 0.5)
        torso.color = [0.4, 0.4, 0.7]  # Shirt
        parts.append(torso)

        # Left arm (cylinder)
        left_arm = Cylinder(radius=0.05 * scale, height=0.6 * scale, ctx=ctx)
        left_arm.name = "Mannequin_LeftArm"
        left_arm.set_position(-0.3 * scale, 1.2 * scale, 0)
        left_arm.set_rotation(0, 0, 90)
        left_arm.color = [0.8, 0.7, 0.6]  # Skin tone
        parts.append(left_arm)

        # Right arm (cylinder)
        right_arm = Cylinder(radius=0.05 * scale, height=0.6 * scale, ctx=ctx)
        right_arm.name = "Mannequin_RightArm"
        right_arm.set_position(0.3 * scale, 1.2 * scale, 0)
        right_arm.set_rotation(0, 0, 90)
        right_arm.color = [0.8, 0.7, 0.6]  # Skin tone
        parts.append(right_arm)

        # Left leg (cylinder)
        left_leg = Cylinder(radius=0.08 * scale, height=0.9 * scale, ctx=ctx)
        left_leg.name = "Mannequin_LeftLeg"
        left_leg.set_position(-0.1 * scale, 0.45 * scale, 0)
        left_leg.color = [0.2, 0.2, 0.5]  # Pants
        parts.append(left_leg)

        # Right leg (cylinder)
        right_leg = Cylinder(radius=0.08 * scale, height=0.9 * scale, ctx=ctx)
        right_leg.name = "Mannequin_RightLeg"
        right_leg.set_position(0.1 * scale, 0.45 * scale, 0)
        right_leg.color = [0.2, 0.2, 0.5]  # Pants
        parts.append(right_leg)

        print(f"  ✅ Created mannequin (height: {height}m, {len(parts)} parts)")

        return parts
