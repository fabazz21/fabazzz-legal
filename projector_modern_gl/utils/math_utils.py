"""
Mathematical Utilities
Helper functions for 3D math, projections, and transformations
"""

import numpy as np
import math
from pyrr import Matrix44, Vector3, Quaternion


def throw_to_fov(throw_ratio, aspect=16/9):
    """
    Convert throw ratio to vertical field of view (degrees)

    Throw ratio = distance / width
    FOV calculation for vertical FOV:
    hFOV = 2 * atan(1 / (2 * throw_ratio))
    vFOV = 2 * atan(tan(hFOV/2) / aspect)

    Args:
        throw_ratio: Throw ratio (distance / screen width)
        aspect: Aspect ratio (width / height)

    Returns:
        Vertical field of view in degrees
    """
    h_fov = 2 * math.atan(1 / (2 * throw_ratio))
    v_fov = 2 * math.atan(math.tan(h_fov / 2) / aspect)
    return math.degrees(v_fov)


def fov_to_throw(fov_degrees, aspect=16/9):
    """
    Convert vertical field of view to throw ratio

    Inverse of throw_to_fov

    Args:
        fov_degrees: Vertical field of view in degrees
        aspect: Aspect ratio (width / height)

    Returns:
        Throw ratio
    """
    v_fov_rad = math.radians(fov_degrees)
    h_fov = 2 * math.atan(math.tan(v_fov_rad / 2) * aspect)
    throw_ratio = 1 / (2 * math.tan(h_fov / 2))
    return throw_ratio


def calculate_projection_size(throw_ratio, distance, aspect=16/9):
    """
    Calculate projection size given throw ratio and distance

    Args:
        throw_ratio: Throw ratio
        distance: Distance from projector to screen (meters)
        aspect: Aspect ratio

    Returns:
        Tuple of (width, height) in meters
    """
    width = distance / throw_ratio
    height = width / aspect
    return (width, height)


def calculate_distance(throw_ratio, width):
    """
    Calculate required distance for given screen width

    Args:
        throw_ratio: Throw ratio
        width: Desired screen width (meters)

    Returns:
        Required distance in meters
    """
    return throw_ratio * width


def calculate_illuminance(lumens, area, gain=1.0):
    """
    Calculate illuminance (lux) on projection surface

    Illuminance = (Lumens * Gain) / Area

    Args:
        lumens: Projector brightness in lumens
        area: Screen area in square meters
        gain: Screen gain (typically 1.0 for matte white)

    Returns:
        Illuminance in lux
    """
    if area <= 0:
        return 0.0
    return (lumens * gain) / area


def calculate_luminance(illuminance, gain=1.0):
    """
    Calculate luminance (cd/m²) from illuminance

    Simplified: Luminance ≈ Illuminance * Gain / π

    Args:
        illuminance: Illuminance in lux
        gain: Screen gain

    Returns:
        Luminance in cd/m²
    """
    return (illuminance * gain) / math.pi


def apply_lens_shift_to_matrix(projection_matrix, shift_h, shift_v):
    """
    Apply lens shift to projection matrix

    Lens shift creates an off-axis projection by modifying
    the projection matrix elements [8] and [9]

    Args:
        projection_matrix: 4x4 projection matrix
        shift_h: Horizontal shift (-1 to 1)
        shift_v: Vertical shift (-1 to 1)

    Returns:
        Modified projection matrix
    """
    proj = np.array(projection_matrix, dtype=np.float32)
    proj[2, 0] = 2.0 * shift_h  # Horizontal shift
    proj[2, 1] = 2.0 * shift_v  # Vertical shift
    return proj


def calculate_frustum_corners(fov, aspect, near, far, shift_h=0.0, shift_v=0.0):
    """
    Calculate frustum corner points for visualization

    Args:
        fov: Vertical field of view (degrees)
        aspect: Aspect ratio
        near: Near plane distance
        far: Far plane distance
        shift_h: Horizontal lens shift (-1 to 1)
        shift_v: Vertical lens shift (-1 to 1)

    Returns:
        Dictionary with near and far corner points
    """
    fov_rad = math.radians(fov)

    # Half extents at near and far planes
    near_half_v = near * math.tan(fov_rad / 2)
    near_half_h = near_half_v * aspect
    far_half_v = far * math.tan(fov_rad / 2)
    far_half_h = far_half_v * aspect

    # Apply shift
    near_corners = {
        'bl': Vector3([near_half_h * (-1 + 2*shift_h), near_half_v * (-1 + 2*shift_v), -near]),
        'br': Vector3([near_half_h * (1 + 2*shift_h), near_half_v * (-1 + 2*shift_v), -near]),
        'tr': Vector3([near_half_h * (1 + 2*shift_h), near_half_v * (1 + 2*shift_v), -near]),
        'tl': Vector3([near_half_h * (-1 + 2*shift_h), near_half_v * (1 + 2*shift_v), -near])
    }

    far_corners = {
        'bl': Vector3([far_half_h * (-1 + 2*shift_h), far_half_v * (-1 + 2*shift_v), -far]),
        'br': Vector3([far_half_h * (1 + 2*shift_h), far_half_v * (-1 + 2*shift_v), -far]),
        'tr': Vector3([far_half_h * (1 + 2*shift_h), far_half_v * (1 + 2*shift_v), -far]),
        'tl': Vector3([far_half_h * (-1 + 2*shift_h), far_half_v * (1 + 2*shift_v), -far])
    }

    return {'near': near_corners, 'far': far_corners}


def lerp(a, b, t):
    """Linear interpolation"""
    return a + (b - a) * t


def smoothstep(edge0, edge1, x):
    """Smooth interpolation (cubic Hermite)"""
    t = np.clip((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def clamp(value, min_val, max_val):
    """Clamp value between min and max"""
    return max(min_val, min(max_val, value))


def deg_to_rad(degrees):
    """Convert degrees to radians"""
    return math.radians(degrees)


def rad_to_deg(radians):
    """Convert radians to degrees"""
    return math.degrees(radians)
