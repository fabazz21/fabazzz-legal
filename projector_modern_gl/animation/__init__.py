"""
Animation System
Timeline, Keyframes, and Easing Functions
"""

from .timeline import Timeline
from .keyframe import Keyframe, PropertyTrack, AnimationClip
from .easing import (
    EASING_FUNCTIONS,
    get_easing_function,
    get_easing_names,
    linear,
    ease_in_quad,
    ease_out_quad,
    ease_in_out_quad,
)

__all__ = [
    'Timeline',
    'Keyframe',
    'PropertyTrack',
    'AnimationClip',
    'EASING_FUNCTIONS',
    'get_easing_function',
    'get_easing_names',
    'linear',
    'ease_in_quad',
    'ease_out_quad',
    'ease_in_out_quad',
]
