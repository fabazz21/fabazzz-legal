"""
Light Objects
Point lights, directional lights, and spot lights
"""

import numpy as np
from pyrr import Vector3
from .base_object import Object3D


class Light(Object3D):
    """Base light class"""

    # Class-level ID counter
    _light_id_counter = 0

    def __init__(self, name="Light", light_type="point", ctx=None):
        """Initialize light"""
        super().__init__(name, ctx)

        # Generate unique light ID
        Light._light_id_counter += 1
        self.light_id = Light._light_id_counter

        self.light_type = light_type

        # Light properties
        self.color = [1.0, 1.0, 1.0]  # White
        self.intensity = 1.0
        self.enabled = True

        # Shadows
        self.cast_shadows = False
        self.shadow_bias = 0.003

    def get_light_data(self):
        """Get light data for shader uniforms"""
        return {
            'position': self.position,
            'color': self.color,
            'intensity': self.intensity,
            'type': self.light_type,
            'enabled': self.enabled
        }


class PointLight(Light):
    """Point light (omni-directional)"""

    def __init__(self, name="PointLight", ctx=None):
        """Initialize point light"""
        super().__init__(name, "point", ctx)

        # Attenuation
        self.constant = 1.0
        self.linear = 0.09
        self.quadratic = 0.032

        # Range (calculated from attenuation)
        self.range = 100.0

    def get_light_data(self):
        """Get light data including attenuation"""
        data = super().get_light_data()
        data.update({
            'constant': self.constant,
            'linear': self.linear,
            'quadratic': self.quadratic,
            'range': self.range
        })
        return data

    def calculate_range(self, threshold=0.01):
        """
        Calculate effective range where light intensity drops below threshold

        Args:
            threshold: Intensity threshold (0.01 = 1%)

        Returns:
            Effective range in units
        """
        # Solve quadratic equation for range
        # I = 1 / (c + l*d + q*d²)
        # threshold = 1 / (c + l*d + q*d²)
        # q*d² + l*d + (c - 1/threshold) = 0

        a = self.quadratic
        b = self.linear
        c = self.constant - (1.0 / threshold)

        if a == 0:
            # Linear attenuation only
            if b == 0:
                return float('inf')
            return max(0, -c / b)

        # Quadratic formula
        discriminant = b*b - 4*a*c
        if discriminant < 0:
            return 0.0

        range_val = (-b + np.sqrt(discriminant)) / (2*a)
        self.range = max(0.0, range_val)
        return self.range


class DirectionalLight(Light):
    """Directional light (sun-like, parallel rays)"""

    def __init__(self, name="DirectionalLight", ctx=None):
        """Initialize directional light"""
        super().__init__(name, "directional", ctx)

        # Direction (pointing towards light source)
        self.direction = Vector3([0.0, -1.0, 0.0])  # Pointing down

        # Directional lights often cast shadows
        self.cast_shadows = True

    def set_direction(self, x, y, z):
        """Set light direction"""
        direction = Vector3([x, y, z])
        length = np.linalg.norm(direction)
        if length > 0:
            self.direction = direction / length

    def get_light_data(self):
        """Get light data including direction"""
        data = super().get_light_data()
        data['direction'] = self.direction
        return data


class SpotLight(Light):
    """Spot light (cone of light)"""

    def __init__(self, name="SpotLight", ctx=None):
        """Initialize spot light"""
        super().__init__(name, "spot", ctx)

        # Direction
        self.direction = Vector3([0.0, -1.0, 0.0])

        # Cone angles (in degrees)
        self.inner_cone_angle = 12.5  # Full intensity
        self.outer_cone_angle = 17.5  # Fade to zero

        # Attenuation
        self.constant = 1.0
        self.linear = 0.09
        self.quadratic = 0.032
        self.range = 100.0

    def set_direction(self, x, y, z):
        """Set spotlight direction"""
        direction = Vector3([x, y, z])
        length = np.linalg.norm(direction)
        if length > 0:
            self.direction = direction / length

    def set_cone_angles(self, inner, outer):
        """
        Set cone angles

        Args:
            inner: Inner cone angle (full intensity) in degrees
            outer: Outer cone angle (fade to zero) in degrees
        """
        self.inner_cone_angle = inner
        self.outer_cone_angle = max(inner, outer)  # Outer must be >= inner

    def get_light_data(self):
        """Get light data including direction and cone"""
        data = super().get_light_data()
        data.update({
            'direction': self.direction,
            'inner_cone': np.cos(np.radians(self.inner_cone_angle)),
            'outer_cone': np.cos(np.radians(self.outer_cone_angle)),
            'constant': self.constant,
            'linear': self.linear,
            'quadratic': self.quadratic,
            'range': self.range
        })
        return data


class AmbientLight:
    """Ambient light (global illumination)"""

    def __init__(self, color=(0.2, 0.2, 0.2), intensity=1.0):
        """
        Initialize ambient light

        Args:
            color: Ambient color RGB (0-1)
            intensity: Intensity multiplier
        """
        self.color = list(color)
        self.intensity = intensity
        self.enabled = True

    def get_light_data(self):
        """Get ambient light data"""
        return {
            'color': self.color,
            'intensity': self.intensity,
            'enabled': self.enabled
        }


def create_light(light_type, ctx=None):
    """
    Factory function to create lights

    Args:
        light_type: 'point', 'directional', or 'spot'
        ctx: ModernGL context

    Returns:
        Light instance
    """
    light_types = {
        'point': PointLight,
        'directional': DirectionalLight,
        'spot': SpotLight
    }

    if light_type.lower() in light_types:
        return light_types[light_type.lower()](ctx=ctx)
    else:
        raise ValueError(f"Unknown light type: {light_type}")
