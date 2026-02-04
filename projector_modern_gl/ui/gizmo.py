"""
3D Gizmo System for Object Manipulation
"""

import numpy as np


class Gizmo:
    """3D Gizmo for transforming objects in viewport"""

    def __init__(self):
        """Initialize gizmo"""
        self.target_object = None
        self.mode = 'translate'  # 'translate', 'rotate', 'scale'

        # Axis colors (standard 3D convention)
        self.colors = {
            "x": (1.0, 0.0, 0.0),  # Red
            "y": (0.0, 1.0, 0.0),  # Green
            "z": (0.0, 0.0, 1.0),  # Blue
        }

        # Gizmo size (in world units)
        self.size = 1.5

        # Interaction state
        self.hovered_axis = None
        self.active_axis = None
        self.is_dragging = False

    def set_target(self, obj):
        """Set target object to manipulate"""
        self.target_object = obj
        if obj:
            print(f"[GIZMO] Target set: {obj.name if hasattr(obj, 'name') else obj}")

    def set_mode(self, mode):
        """Set gizmo mode: translate, rotate, or scale"""
        if mode in ['translate', 'rotate', 'scale']:
            self.mode = mode
            print(f"[GIZMO] Mode: {mode}")

    def build_lines(self):
        """
        Build line data for GPU rendering

        Returns:
            List of dicts with keys: start, end, color
            Example: [{"start": (0,0,0), "end": (1,0,0), "color": (1,0,0)}]
        """
        if not self.target_object:
            return []

        # Get target position
        p = self.target_object.position
        s = self.size

        # Build axis lines based on mode
        if self.mode == 'translate':
            # Simple arrows (lines from origin to axis tip)
            return [
                {"start": tuple(p), "end": (p[0] + s, p[1], p[2]), "color": self.colors["x"]},
                {"start": tuple(p), "end": (p[0], p[1] + s, p[2]), "color": self.colors["y"]},
                {"start": tuple(p), "end": (p[0], p[1], p[2] + s), "color": self.colors["z"]},
            ]

        elif self.mode == 'rotate':
            # Rotation circles (simplified as short line segments)
            lines = []
            segments = 16
            radius = s * 0.8

            # X-axis circle (YZ plane)
            for i in range(segments):
                angle1 = 2 * np.pi * i / segments
                angle2 = 2 * np.pi * (i + 1) / segments
                p1 = (p[0], p[1] + radius * np.cos(angle1), p[2] + radius * np.sin(angle1))
                p2 = (p[0], p[1] + radius * np.cos(angle2), p[2] + radius * np.sin(angle2))
                lines.append({"start": p1, "end": p2, "color": self.colors["x"]})

            # Y-axis circle (XZ plane)
            for i in range(segments):
                angle1 = 2 * np.pi * i / segments
                angle2 = 2 * np.pi * (i + 1) / segments
                p1 = (p[0] + radius * np.cos(angle1), p[1], p[2] + radius * np.sin(angle1))
                p2 = (p[0] + radius * np.cos(angle2), p[1], p[2] + radius * np.sin(angle2))
                lines.append({"start": p1, "end": p2, "color": self.colors["y"]})

            # Z-axis circle (XY plane)
            for i in range(segments):
                angle1 = 2 * np.pi * i / segments
                angle2 = 2 * np.pi * (i + 1) / segments
                p1 = (p[0] + radius * np.cos(angle1), p[1] + radius * np.sin(angle1), p[2])
                p2 = (p[0] + radius * np.cos(angle2), p[1] + radius * np.sin(angle2), p[2])
                lines.append({"start": p1, "end": p2, "color": self.colors["z"]})

            return lines

        elif self.mode == 'scale':
            # Scale handles (lines to cubes at endpoints)
            lines = []
            cube_size = 0.2

            # X axis
            lines.append({"start": tuple(p), "end": (p[0] + s, p[1], p[2]), "color": self.colors["x"]})
            # Small cube at end (4 edges shown)
            cx, cy, cz = p[0] + s, p[1], p[2]
            h = cube_size / 2
            lines.extend([
                {"start": (cx-h, cy-h, cz-h), "end": (cx+h, cy-h, cz-h), "color": self.colors["x"]},
                {"start": (cx-h, cy+h, cz-h), "end": (cx+h, cy+h, cz-h), "color": self.colors["x"]},
                {"start": (cx-h, cy-h, cz-h), "end": (cx-h, cy+h, cz-h), "color": self.colors["x"]},
                {"start": (cx+h, cy-h, cz-h), "end": (cx+h, cy+h, cz-h), "color": self.colors["x"]},
            ])

            # Y axis
            lines.append({"start": tuple(p), "end": (p[0], p[1] + s, p[2]), "color": self.colors["y"]})
            cy = p[1] + s
            cx, cz = p[0], p[2]
            lines.extend([
                {"start": (cx-h, cy-h, cz-h), "end": (cx+h, cy-h, cz-h), "color": self.colors["y"]},
                {"start": (cx-h, cy+h, cz-h), "end": (cx+h, cy+h, cz-h), "color": self.colors["y"]},
                {"start": (cx-h, cy-h, cz-h), "end": (cx-h, cy+h, cz-h), "color": self.colors["y"]},
                {"start": (cx+h, cy-h, cz-h), "end": (cx+h, cy+h, cz-h), "color": self.colors["y"]},
            ])

            # Z axis
            lines.append({"start": tuple(p), "end": (p[0], p[1], p[2] + s), "color": self.colors["z"]})
            cz = p[2] + s
            cx, cy = p[0], p[1]
            lines.extend([
                {"start": (cx-h, cy-h, cz-h), "end": (cx+h, cy-h, cz-h), "color": self.colors["z"]},
                {"start": (cx-h, cy+h, cz-h), "end": (cx+h, cy+h, cz-h), "color": self.colors["z"]},
                {"start": (cx-h, cy-h, cz-h), "end": (cx-h, cy+h, cz-h), "color": self.colors["z"]},
                {"start": (cx+h, cy-h, cz-h), "end": (cx+h, cy+h, cz-h), "color": self.colors["z"]},
            ])

            return lines

        return []

    def update(self, camera, mouse_pos, mouse_down):
        """Update gizmo interaction (raycast, drag, etc.)"""
        # TODO: Implement raycast-based axis selection
        # For now, just track drag state
        if mouse_down and not self.is_dragging:
            self.is_dragging = True
        elif not mouse_down:
            self.is_dragging = False
