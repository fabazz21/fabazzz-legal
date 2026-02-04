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

        # Visual settings (LARGER for better visibility)
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

        print("[GIZMO] ✅ Initialized with LARGE arrows (5.0 units)")

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
        arrow_length = 5.0  # LARGER arrows (was 2.0)

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
        radius = 3.0  # LARGER radius (was 1.5)

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
        cube_size = 0.4  # LARGER cubes (was 0.2)
        offset = 4.0  # Further offset (was 2.0)

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
        if obj:
            print(f"[GIZMO] 🎯 Target set: {obj.name}")

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

    def render(self, renderer, camera):
        """
        Render gizmo

        Args:
            renderer: Renderer object (provides draw_line/draw_lines methods)
            camera: Camera object (for MVP matrix)
        """
        if self.target_object is None:
            print("[GIZMO] ⚠️ render() called but NO TARGET")
            return

        print(f"[GIZMO] 🎨 Rendering {self.mode} gizmo for {self.target_object.name} at {self.target_object.position}")

        # Render based on current mode
        if self.mode == 'translate':
            self._render_translate_gizmo(renderer, camera)
        elif self.mode == 'rotate':
            self._render_rotate_gizmo(renderer, camera)
        elif self.mode == 'scale':
            self._render_scale_gizmo(renderer, camera)

    def _render_translate_gizmo(self, renderer, camera):
        """Render translation arrows"""
        if self.target_object is None:
            return

        # Get gizmo position (target object position)
        gizmo_pos = self.target_object.position
        print(f"[GIZMO] Drawing translate arrows at {gizmo_pos}")

        # Render each arrow
        for axis, data in self.translate_geometry.items():
            # Get color (highlight if hovered/active)
            if self.active_axis == axis:
                color = self.colors['active']
            elif self.hovered_axis == axis:
                color = self.colors['hover']
            else:
                color = data['color']

            # Extract vertices (4 points = 2 lines for arrow shaft + head)
            vertices = data['vertices']

            # Build lines for this arrow
            start_positions = []
            end_positions = []

            # Arrow is stored as [start1, end1, start2, end2]
            # We need to transform to world space
            for i in range(0, len(vertices), 6):  # 6 floats per pair (x,y,z start + x,y,z end)
                start = vertices[i:i+3] + gizmo_pos
                end = vertices[i+3:i+6] + gizmo_pos
                start_positions.append(tuple(start))
                end_positions.append(tuple(end))

            print(f"[GIZMO]   {axis} axis: {len(start_positions)} lines, color={color}")

            # Draw arrow with THICKER lines for visibility
            try:
                renderer.draw_lines(start_positions, end_positions, color, width=5.0, camera=camera)
                print(f"[GIZMO]   ✅ {axis} axis drawn successfully")
            except Exception as e:
                print(f"[GIZMO]   ❌ ERROR drawing {axis} axis: {e}")

    def _render_rotate_gizmo(self, renderer, camera):
        """Render rotation circles"""
        if self.target_object is None:
            return

        # Get gizmo position
        gizmo_pos = self.target_object.position

        # Render each circle
        for axis, data in self.rotate_geometry.items():
            # Get color
            if self.active_axis == axis:
                color = self.colors['active']
            elif self.hovered_axis == axis:
                color = self.colors['hover']
            else:
                color = data['color']

            # Extract vertices (circle as line strip)
            vertices = data['vertices']

            # Build lines for circle (connecting consecutive points)
            start_positions = []
            end_positions = []

            # Circle vertices: [x0, y0, z0, x1, y1, z1, ...]
            for i in range(0, len(vertices) - 3, 3):  # -3 to avoid last point
                start = vertices[i:i+3] + gizmo_pos
                end = vertices[i+3:i+6] + gizmo_pos
                start_positions.append(tuple(start))
                end_positions.append(tuple(end))

            # Draw circle with THICKER lines
            renderer.draw_lines(start_positions, end_positions, color, width=4.0, camera=camera)

    def _render_scale_gizmo(self, renderer, camera):
        """Render scale cubes"""
        if self.target_object is None:
            return

        # Get gizmo position
        gizmo_pos = self.target_object.position

        # Render each cube (as wireframe box)
        for axis, data in self.scale_geometry.items():
            # Get color
            if self.active_axis == axis:
                color = self.colors['active']
            elif self.hovered_axis == axis:
                color = self.colors['hover']
            else:
                color = data['color']

            # Cube center and size
            cube_center = np.array(data['position']) + gizmo_pos
            cube_size = data['size']
            half = cube_size / 2.0

            # Cube corners
            corners = [
                cube_center + np.array([-half, -half, -half]),
                cube_center + np.array([half, -half, -half]),
                cube_center + np.array([half, half, -half]),
                cube_center + np.array([-half, half, -half]),
                cube_center + np.array([-half, -half, half]),
                cube_center + np.array([half, -half, half]),
                cube_center + np.array([half, half, half]),
                cube_center + np.array([-half, half, half]),
            ]

            # Cube edges (12 edges)
            edges = [
                (0, 1), (1, 2), (2, 3), (3, 0),  # Bottom face
                (4, 5), (5, 6), (6, 7), (7, 4),  # Top face
                (0, 4), (1, 5), (2, 6), (3, 7),  # Vertical edges
            ]

            start_positions = []
            end_positions = []

            for edge in edges:
                start_positions.append(tuple(corners[edge[0]]))
                end_positions.append(tuple(corners[edge[1]]))

            # Draw cube wireframe with THICKER lines
            renderer.draw_lines(start_positions, end_positions, color, width=4.0, camera=camera)

            # Also draw line from origin to cube center
            renderer.draw_line(tuple(gizmo_pos), tuple(cube_center), color, width=5.0, camera=camera)

    def get_position(self):
        """Get gizmo position (same as target object)"""
        if self.target_object:
            return self.target_object.position
        return Vector3([0, 0, 0])
