"""
Keyframe System for Timeline Animation
"""

import copy
from pyrr import Vector3, Quaternion


class Keyframe:
    """Single keyframe in animation timeline"""

    def __init__(self, time, target, property_name, value, easing='linear'):
        """
        Initialize keyframe

        Args:
            time: Time in seconds
            target: Target object (projector, camera, object)
            property_name: Property to animate (e.g., 'position', 'rotation', 'intensity')
            value: Target value at this keyframe
            easing: Easing function name
        """
        self.time = time
        self.target = target
        self.property_name = property_name
        self.value = copy.deepcopy(value)
        self.easing = easing

    def apply_value(self):
        """Apply keyframe value to target object"""
        if hasattr(self.target, self.property_name):
            setattr(self.target, self.property_name, copy.deepcopy(self.value))

    def __repr__(self):
        return f"<Keyframe t={self.time:.2f}s {self.property_name}={self.value}>"


class PropertyTrack:
    """Animation track for a single property"""

    def __init__(self, target, property_name):
        """
        Initialize property track

        Args:
            target: Target object
            property_name: Property to animate
        """
        self.target = target
        self.property_name = property_name
        self.keyframes = []

    def add_keyframe(self, time, value, easing='linear'):
        """Add keyframe to track"""
        kf = Keyframe(time, self.target, self.property_name, value, easing)
        self.keyframes.append(kf)
        self.keyframes.sort(key=lambda k: k.time)
        return kf

    def remove_keyframe(self, keyframe):
        """Remove keyframe from track"""
        if keyframe in self.keyframes:
            self.keyframes.remove(keyframe)

    def get_keyframes_at_time(self, time):
        """Get keyframes surrounding given time"""
        if not self.keyframes:
            return None, None

        # Find keyframes before and after time
        kf_before = None
        kf_after = None

        for kf in self.keyframes:
            if kf.time <= time:
                kf_before = kf
            elif kf.time > time and kf_after is None:
                kf_after = kf
                break

        return kf_before, kf_after

    def evaluate(self, time):
        """Evaluate track at given time"""
        if not self.keyframes:
            return None

        kf_before, kf_after = self.get_keyframes_at_time(time)

        # Before first keyframe
        if kf_before is None:
            return self.keyframes[0].value

        # After last keyframe
        if kf_after is None:
            return kf_before.value

        # Exact match
        if kf_before.time == time:
            return kf_before.value

        # Interpolate between keyframes
        duration = kf_after.time - kf_before.time
        if duration == 0:
            return kf_before.value

        # Calculate interpolation factor (0 to 1)
        t = (time - kf_before.time) / duration

        # Apply easing function
        from .easing import get_easing_function
        easing_func = get_easing_function(kf_after.easing)
        t = easing_func(t)

        # Interpolate based on value type
        return self._interpolate_values(kf_before.value, kf_after.value, t)

    def _interpolate_values(self, v1, v2, t):
        """Interpolate between two values"""
        # Float/Int
        if isinstance(v1, (int, float)):
            return v1 + (v2 - v1) * t

        # Vector3
        if isinstance(v1, Vector3):
            return Vector3([
                v1[0] + (v2[0] - v1[0]) * t,
                v1[1] + (v2[1] - v1[1]) * t,
                v1[2] + (v2[2] - v1[2]) * t
            ])

        # Quaternion (SLERP)
        if isinstance(v1, Quaternion):
            return v1.slerp(v2, t)

        # List/Tuple (component-wise)
        if isinstance(v1, (list, tuple)):
            result = []
            for i in range(len(v1)):
                if isinstance(v1[i], (int, float)):
                    result.append(v1[i] + (v2[i] - v1[i]) * t)
                else:
                    result.append(v1[i])
            return type(v1)(result)

        # Default: return v2 (no interpolation)
        return v2

    def __repr__(self):
        return f"<PropertyTrack {self.property_name} ({len(self.keyframes)} keyframes)>"


class AnimationClip:
    """Collection of property tracks forming a complete animation"""

    def __init__(self, name="Animation"):
        """Initialize animation clip"""
        self.name = name
        self.tracks = {}  # {(target_id, property_name): PropertyTrack}
        self.duration = 0.0

    def get_or_create_track(self, target, property_name):
        """Get existing track or create new one"""
        key = (id(target), property_name)
        if key not in self.tracks:
            self.tracks[key] = PropertyTrack(target, property_name)
        return self.tracks[key]

    def add_keyframe(self, target, property_name, time, value, easing='linear'):
        """Add keyframe to animation"""
        track = self.get_or_create_track(target, property_name)
        kf = track.add_keyframe(time, value, easing)

        # Update duration
        self.duration = max(self.duration, time)

        return kf

    def remove_keyframe(self, keyframe):
        """Remove keyframe from animation"""
        key = (id(keyframe.target), keyframe.property_name)
        if key in self.tracks:
            self.tracks[key].remove_keyframe(keyframe)

    def evaluate(self, time):
        """Evaluate all tracks at given time"""
        for track in self.tracks.values():
            value = track.evaluate(time)
            if value is not None:
                setattr(track.target, track.property_name, value)

    def get_all_keyframes(self):
        """Get all keyframes sorted by time"""
        keyframes = []
        for track in self.tracks.values():
            keyframes.extend(track.keyframes)
        keyframes.sort(key=lambda k: k.time)
        return keyframes

    def clear(self):
        """Clear all tracks"""
        self.tracks.clear()
        self.duration = 0.0

    def __repr__(self):
        return f"<AnimationClip '{self.name}' ({len(self.tracks)} tracks, {self.duration:.2f}s)>"
