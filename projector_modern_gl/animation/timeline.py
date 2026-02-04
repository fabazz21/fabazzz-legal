"""
Timeline System for Animation Playback
"""

import time
from .keyframe import AnimationClip


class Timeline:
    """Timeline for animation playback and recording"""

    def __init__(self):
        """Initialize timeline"""
        self.clips = []
        self.active_clip = None
        self.current_time = 0.0
        self.duration = 10.0  # Default duration in seconds

        # Playback state
        self.playing = False
        self.recording = False
        self.loop = False
        self.playback_speed = 1.0

        # Recording state
        self.record_start_time = None
        self.record_targets = []  # Objects being recorded

        # Time tracking
        self._last_update_time = None

    def create_clip(self, name="Animation"):
        """Create new animation clip"""
        clip = AnimationClip(name)
        self.clips.append(clip)
        if self.active_clip is None:
            self.active_clip = clip
        return clip

    def set_active_clip(self, clip):
        """Set active animation clip"""
        if clip in self.clips:
            self.active_clip = clip

    def remove_clip(self, clip):
        """Remove animation clip"""
        if clip in self.clips:
            self.clips.remove(clip)
            if self.active_clip == clip:
                self.active_clip = self.clips[0] if self.clips else None

    def add_keyframe(self, target, property_name, value=None, easing='linear'):
        """
        Add keyframe at current time

        Args:
            target: Target object
            property_name: Property to animate
            value: Value (if None, uses current value)
            easing: Easing function
        """
        if self.active_clip is None:
            self.create_clip()

        # Get current value if not provided
        if value is None:
            if hasattr(target, property_name):
                value = getattr(target, property_name)
            else:
                print(f"  ⚠️ Property '{property_name}' not found on {target}")
                return None

        # Add keyframe
        kf = self.active_clip.add_keyframe(
            target, property_name, self.current_time, value, easing
        )

        # Update duration
        self.duration = max(self.duration, self.active_clip.duration)

        print(f"  ✅ Keyframe added: {property_name} at {self.current_time:.2f}s")
        return kf

    def remove_keyframe(self, keyframe):
        """Remove keyframe"""
        if self.active_clip:
            self.active_clip.remove_keyframe(keyframe)

    def play(self):
        """Start playback"""
        self.playing = True
        self._last_update_time = time.time()
        print("  ▶️ Timeline playing")

    def pause(self):
        """Pause playback"""
        self.playing = False
        print("  ⏸️ Timeline paused")

    def stop(self):
        """Stop playback and reset to start"""
        self.playing = False
        self.current_time = 0.0
        self._last_update_time = None
        print("  ⏹️ Timeline stopped")

    def toggle_play_pause(self):
        """Toggle between play and pause"""
        if self.playing:
            self.pause()
        else:
            self.play()

    def start_recording(self, targets=None):
        """
        Start recording keyframes

        Args:
            targets: List of objects to record (or None for all)
        """
        self.recording = True
        self.record_start_time = self.current_time
        self.record_targets = targets or []
        print(f"  🔴 Recording started at {self.current_time:.2f}s")

    def stop_recording(self):
        """Stop recording"""
        self.recording = False
        self.record_start_time = None
        print(f"  ⏺️ Recording stopped at {self.current_time:.2f}s")

    def record_keyframe(self, target, property_name):
        """Record keyframe for specific property during recording"""
        if self.recording:
            self.add_keyframe(target, property_name)

    def seek(self, time):
        """Seek to specific time"""
        self.current_time = max(0.0, min(time, self.duration))
        self._evaluate_at_current_time()

    def update(self, dt=None):
        """
        Update timeline (call every frame)

        Args:
            dt: Delta time in seconds (if None, calculated automatically)
        """
        if not self.playing:
            return

        # Calculate delta time
        if dt is None:
            current_time = time.time()
            if self._last_update_time is not None:
                dt = current_time - self._last_update_time
            else:
                dt = 0.0
            self._last_update_time = current_time

        # Update time
        self.current_time += dt * self.playback_speed

        # Handle loop
        if self.current_time >= self.duration:
            if self.loop:
                self.current_time = self.current_time % self.duration
            else:
                self.current_time = self.duration
                self.pause()

        # Evaluate animation
        self._evaluate_at_current_time()

    def _evaluate_at_current_time(self):
        """Evaluate active clip at current time"""
        if self.active_clip:
            self.active_clip.evaluate(self.current_time)

    def get_progress(self):
        """Get playback progress (0 to 1)"""
        if self.duration == 0:
            return 0.0
        return self.current_time / self.duration

    def set_progress(self, progress):
        """Set playback progress (0 to 1)"""
        self.seek(progress * self.duration)

    def get_all_keyframes(self):
        """Get all keyframes from active clip"""
        if self.active_clip:
            return self.active_clip.get_all_keyframes()
        return []

    def clear_animation(self):
        """Clear all keyframes from active clip"""
        if self.active_clip:
            self.active_clip.clear()
            self.duration = 10.0
            print("  🗑️ Animation cleared")

    def export_to_json(self):
        """Export timeline to JSON format"""
        import json

        data = {
            'duration': self.duration,
            'clips': []
        }

        for clip in self.clips:
            clip_data = {
                'name': clip.name,
                'duration': clip.duration,
                'keyframes': []
            }

            for kf in clip.get_all_keyframes():
                kf_data = {
                    'time': kf.time,
                    'target': type(kf.target).__name__,
                    'target_id': id(kf.target),
                    'property': kf.property_name,
                    'value': str(kf.value),
                    'easing': kf.easing
                }
                clip_data['keyframes'].append(kf_data)

            data['clips'].append(clip_data)

        return json.dumps(data, indent=2)

    def __repr__(self):
        clip_info = f"({len(self.clips)} clips)" if self.clips else "(no clips)"
        state = "▶️" if self.playing else "⏸️"
        return f"<Timeline {state} {self.current_time:.2f}/{self.duration:.2f}s {clip_info}>"
