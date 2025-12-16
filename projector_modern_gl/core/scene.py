"""
Scene Management
Handles all 3D objects, projectors, cameras, lights
"""

import numpy as np
from pyrr import Vector3


class Scene:
    """3D Scene Manager"""

    def __init__(self, ctx):
        """Initialize scene"""
        self.ctx = ctx

        # Collections
        self.projectors = []
        self.cameras = []
        self.objects = []
        self.lights = []

        # Helpers
        self.show_helpers = True
        self.show_grid = True
        self.show_frustums = True

        # Grid
        self.grid = None
        self._create_grid()

        # Scene settings
        self.ambient_light_intensity = 0.1
        self.directional_light_intensity = 0.5
        self.directional_light_direction = Vector3([0.5, 0.8, 0.5])

        # Statistics
        self.object_count = 0
        self.projector_count = 0

        print("✅ Scene initialized")

    def _create_grid(self):
        """Create reference grid"""
        # Grid: 100x100 units, 1 unit spacing
        grid_size = 50
        grid_lines = []

        # X lines (red tint)
        for i in range(-grid_size, grid_size + 1):
            if i == 0:
                color = [1.0, 0.0, 0.0]  # Red for X axis
            else:
                color = [0.3, 0.3, 0.3]  # Gray

            grid_lines.append({
                'start': [-grid_size, 0, i],
                'end': [grid_size, 0, i],
                'color': color
            })

        # Z lines (blue tint)
        for i in range(-grid_size, grid_size + 1):
            if i == 0:
                color = [0.0, 0.0, 1.0]  # Blue for Z axis
            else:
                color = [0.3, 0.3, 0.3]  # Gray

            grid_lines.append({
                'start': [i, 0, -grid_size],
                'end': [i, 0, grid_size],
                'color': color
            })

        self.grid = grid_lines

    def add_projector(self, projector):
        """Add projector to scene"""
        self.projectors.append(projector)
        self.projector_count = len(self.projectors)
        return projector

    def remove_projector(self, projector):
        """Remove projector from scene"""
        if projector in self.projectors:
            self.projectors.remove(projector)
            self.projector_count = len(self.projectors)

    def add_camera(self, camera):
        """Add camera to scene"""
        self.cameras.append(camera)
        return camera

    def remove_camera(self, camera):
        """Remove camera from scene"""
        if camera in self.cameras:
            self.cameras.remove(camera)

    def add_object(self, obj):
        """Add object to scene"""
        self.objects.append(obj)
        self.object_count = len(self.objects)
        return obj

    def remove_object(self, obj):
        """Remove object from scene"""
        if obj in self.objects:
            self.objects.remove(obj)
            self.object_count = len(self.objects)

    def get_active_projectors(self):
        """Get all active projectors"""
        return [p for p in self.projectors if p.active]

    def get_visible_objects(self):
        """Get all visible objects"""
        return [o for o in self.objects if o.visible]

    def clear(self):
        """Clear all objects from scene"""
        self.projectors.clear()
        self.cameras.clear()
        self.objects.clear()
        self.object_count = 0
        self.projector_count = 0

    def update(self, dt):
        """Update scene objects"""
        # Update projectors
        for projector in self.projectors:
            projector.update(dt)

        # Update objects
        for obj in self.objects:
            if hasattr(obj, 'update'):
                obj.update(dt)

    def toggle_grid(self):
        """Toggle grid visibility"""
        self.show_grid = not self.show_grid

    def toggle_helpers(self):
        """Toggle all helpers"""
        self.show_helpers = not self.show_helpers

    def toggle_frustums(self):
        """Toggle frustum visibility"""
        self.show_frustums = not self.show_frustums

    def get_stats(self):
        """Get scene statistics"""
        return {
            'objects': self.object_count,
            'projectors': self.projector_count,
            'cameras': len(self.cameras),
            'active_projectors': len(self.get_active_projectors()),
            'visible_objects': len(self.get_visible_objects())
        }

    def cleanup(self):
        """Cleanup scene resources"""
        for projector in self.projectors:
            if hasattr(projector, 'cleanup'):
                projector.cleanup()

        for obj in self.objects:
            if hasattr(obj, 'cleanup'):
                obj.cleanup()

        self.clear()
