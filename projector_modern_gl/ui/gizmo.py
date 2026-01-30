"""
3D Gizmo System
Interactive 3D transformation handles for objects
"""

import numpy as np
import moderngl
from pyrr import Vector3, Matrix44


class Gizmo:
    """3D Gizmo for object manipulation"""

    def __init__(self, ctx):
        """Initialize gizmo system"""
        self.ctx = ctx
        self.mode = 'translate'  # 'translate', 'rotate', 'scale'
        self.target_object = None
        self.hovered_axis = None
        self.active_axis = None

        # Visual settings
        self.size = 1.0
        self.line_thickness = 3.0

        # Colors for each axis
        self.colors = {
            'x': (1.0, 0.0, 0.0),  # Red
            'y': (0.0, 1.0, 0.0),  # Green
            'z': (0.0, 0.0, 1.0),  # Blue
            'hover': (1.0, 1.0, 0.0),  # Yellow
            'active': (1.0, 0.5, 0.0)  # Orange
        }

        # Mouse interaction
        self.is_dragging = False
        self.drag_start_pos = None
        self.drag_start_object_pos = None
        self.drag_start_object_rot = None
        self.drag_start_object_scale = None

        # Create geometry
        self._create_geometry()

    def _create_geometry(self):
        """Create gizmo geometry"""
        # Translation arrows
        self.translate_geometry = self._create_arrows()

        # Rotation circles
        self.rotate_geometry = self._create_circles()

        # Scale cubes
        self.scale_geometry = self._create_cubes()

    def _create_arrows(self):
        """Create arrow geometry for translation"""
        arrows = {}
        arrow_length = 2.0

        # X axis arrow (Red)
        arrows['x'] = {
            'vertices': np.array([
                # Arrow shaft
                0, 0, 0,
                arrow_length * 0.8, 0, 0,
                # Arrow head
                arrow_length * 0.8, 0, 0,
                arrow_length, 0, 0,
            ], dtype='f4'),
            'color': self.colors['x']
        }

        # Y axis arrow (Green)
        arrows['y'] = {
            'vertices': np.array([
                0, 0, 0,
                0, arrow_length * 0.8, 0,
                0, arrow_length * 0.8, 0,
                0, arrow_length, 0,
            ], dtype='f4'),
            'color': self.colors['y']
        }

        # Z axis arrow (Blue)
        arrows['z'] = {
            'vertices': np.array([
                0, 0, 0,
                0, 0, arrow_length * 0.8,
                0, 0, arrow_length * 0.8,
                0, 0, arrow_length,
            ], dtype='f4'),
            'color': self.colors['z']
        }

        return arrows

    def _create_circles(self):
        """Create circle geometry for rotation"""
        circles = {}
        segments = 64
        radius = 1.5

        # X rotation circle (around YZ plane)
        vertices_x = []
        for i in range(segments + 1):
            angle = 2 * np.pi * i / segments
            vertices_x.extend([0, np.cos(angle) * radius, np.sin(angle) * radius])

        circles['x'] = {
            'vertices': np.array(vertices_x, dtype='f4'),
            'color': self.colors['x']
        }

        # Y rotation circle (around XZ plane)
        vertices_y = []
        for i in range(segments + 1):
            angle = 2 * np.pi * i / segments
            vertices_y.extend([np.cos(angle) * radius, 0, np.sin(angle) * radius])

        circles['y'] = {
            'vertices': np.array(vertices_y, dtype='f4'),
            'color': self.colors['y']
        }

        # Z rotation circle (around XY plane)
        vertices_z = []
        for i in range(segments + 1):
            angle = 2 * np.pi * i / segments
            vertices_z.extend([np.cos(angle) * radius, np.sin(angle) * radius, 0])

        circles['z'] = {
            'vertices': np.array(vertices_z, dtype='f4'),
            'color': self.colors['z']
        }

        return circles

    def _create_cubes(self):
        """Create cube geometry for scaling"""
        cubes = {}
        cube_size = 0.2
        offset = 2.0

        # X axis cube
        cubes['x'] = {
            'position': (offset, 0, 0),
            'size': cube_size,
            'color': self.colors['x']
        }

        # Y axis cube
        cubes['y'] = {
            'position': (0, offset, 0),
            'size': cube_size,
            'color': self.colors['y']
        }

        # Z axis cube
        cubes['z'] = {
            'position': (0, 0, offset),
            'size': cube_size,
            'color': self.colors['z']
        }

        return cubes

    def set_target(self, obj):
        """Set target object for gizmo"""
        self.target_object = obj

    def set_mode(self, mode):
        """Set gizmo mode: 'translate', 'rotate', or 'scale'"""
        if mode in ['translate', 'rotate', 'scale']:
            self.mode = mode
            print(f"[GIZMO] Mode changed to: {mode}")

    def update(self, camera, mouse_pos, mouse_down):
        """Update gizmo state based on input"""
        if self.target_object is None:
            return

        # Update hover state
        if not self.is_dragging:
            self.hovered_axis = self._raycast_gizmo(camera, mouse_pos)

        # Handle mouse interaction
        if mouse_down:
            if not self.is_dragging and self.hovered_axis is not None:
                # Start dragging
                self.is_dragging = True
                self.active_axis = self.hovered_axis
                self.drag_start_pos = mouse_pos
                self.drag_start_object_pos = self.target_object.position.copy()
                self.drag_start_object_rot = self.target_object.rotation.copy()
                self.drag_start_object_scale = self.target_object.scale.copy()
            elif self.is_dragging:
                # Continue dragging
                self._apply_transformation(mouse_pos, camera)
        else:
            # Stop dragging
            self.is_dragging = False
            self.active_axis = None

    def _raycast_gizmo(self, camera, mouse_pos):
        """Raycast to detect which gizmo axis is hovered"""
        # Simplified hit detection
        # In a real implementation, this would do proper 3D raycasting
        return None

    def _apply_transformation(self, mouse_pos, camera):
        """Apply transformation based on mouse movement"""
        if self.active_axis is None:
            return

        delta = (
            mouse_pos[0] - self.drag_start_pos[0],
            mouse_pos[1] - self.drag_start_pos[1]
        )

        sensitivity = 0.01

        if self.mode == 'translate':
            # Apply translation
            if self.active_axis == 'x':
                self.target_object.position[0] = self.drag_start_object_pos[0] + delta[0] * sensitivity
            elif self.active_axis == 'y':
                self.target_object.position[1] = self.drag_start_object_pos[1] - delta[1] * sensitivity
            elif self.active_axis == 'z':
                self.target_object.position[2] = self.drag_start_object_pos[2] + (delta[0] + delta[1]) * sensitivity * 0.5

        elif self.mode == 'rotate':
            # Apply rotation
            rotation_sensitivity = 0.5
            if self.active_axis == 'x':
                self.target_object.rotation[0] = self.drag_start_object_rot[0] + delta[1] * rotation_sensitivity
            elif self.active_axis == 'y':
                self.target_object.rotation[1] = self.drag_start_object_rot[1] + delta[0] * rotation_sensitivity
            elif self.active_axis == 'z':
                self.target_object.rotation[2] = self.drag_start_object_rot[2] + delta[0] * rotation_sensitivity

        elif self.mode == 'scale':
            # Apply scaling
            scale_sensitivity = 0.005
            scale_delta = (delta[0] - delta[1]) * scale_sensitivity
            if self.active_axis == 'x':
                self.target_object.scale[0] = max(0.1, self.drag_start_object_scale[0] + scale_delta)
            elif self.active_axis == 'y':
                self.target_object.scale[1] = max(0.1, self.drag_start_object_scale[1] + scale_delta)
            elif self.active_axis == 'z':
                self.target_object.scale[2] = max(0.1, self.drag_start_object_scale[2] + scale_delta)

    def render(self, camera):
        """Render gizmo"""
        if self.target_object is None:
            return

        # Render based on current mode
        if self.mode == 'translate':
            self._render_translate_gizmo(camera)
        elif self.mode == 'rotate':
            self._render_rotate_gizmo(camera)
        elif self.mode == 'scale':
            self._render_scale_gizmo(camera)

    def _render_translate_gizmo(self, camera):
        """Render translation arrows"""
        # Would render the arrow geometry here
        pass

    def _render_rotate_gizmo(self, camera):
        """Render rotation circles"""
        # Would render the circle geometry here
        pass

    def _render_scale_gizmo(self, camera):
        """Render scale cubes"""
        # Would render the cube geometry here
        pass

    def get_position(self):
        """Get gizmo position (same as target object)"""
        if self.target_object:
            return self.target_object.position
        return Vector3([0, 0, 0])
