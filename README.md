# Projector Fusion - Multi-Projector Mapping Application

A professional 3D projection mapping application built with ModernGL, featuring real-time multi-projector rendering, shadow mapping, keystone correction, soft edge blending, and timeline-based animation.

## Features

- **Multi-Projector Support**: Up to 4 simultaneous projectors with independent control
- **Real-time 3D Rendering**: Hardware-accelerated OpenGL 3.3 rendering
- **Shadow Mapping**: Dynamic shadow casting for realistic projections
- **Keystone Correction**: Trapezoid and perspective correction
- **Soft Edge Blending**: Seamless multi-projector blending
- **Timeline Animation**: Keyframe-based animation system with 30+ easing functions
- **Interactive UI**: ImGui-based interface with scene hierarchy, properties, and timeline
- **Camera Controls**: Orbit, pan, and zoom controls
- **Scene Management**: Load/save scenes and animations in JSON format

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenGL 3.3 compatible graphics card

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
python main.py
```

### Controls

#### Camera Controls
- **Left Mouse Drag**: Orbit camera around target
- **Middle Mouse Drag**: Pan camera
- **Mouse Wheel**: Zoom in/out

#### Keyboard Shortcuts
- **Esc**: Exit application
- **Ctrl+Z**: Undo (when implemented)
- **Ctrl+Y**: Redo (when implemented)

## Project Structure

```
projector_modern_gl/
├── animation/          # Animation system
│   ├── timeline.py     # Timeline management
│   ├── keyframe.py     # Keyframe system
│   └── easing.py       # Easing functions
├── core/               # Core rendering
│   ├── camera.py       # 3D camera
│   ├── scene.py        # Scene management
│   ├── window.py       # Window management
│   ├── renderer.py     # Main renderer
│   └── line_renderer.py # GPU line rendering
├── shaders/            # GLSL shaders
│   ├── projector_vertex.glsl
│   ├── projector_fragment.glsl
│   ├── depth_vertex.glsl
│   ├── depth_fragment.glsl
│   └── line.glsl
├── ui/                 # User interface
│   ├── main_ui.py      # Main UI panels
│   ├── theme.py        # ImGui theme
│   └── gizmo.py        # 3D gizmo system
└── utils/              # Utilities
    └── history.py      # Undo/redo system
main.py                 # Application entry point
```

## Architecture

### Rendering Pipeline

1. **Depth Pass**: Render scene from each projector's perspective to generate shadow maps
2. **Main Pass**: Render scene from camera perspective with multi-projector lighting
3. **Helper Pass**: Render grid, axes, and gizmos using GPU line renderer
4. **UI Pass**: Render ImGui interface overlay

### Scene Graph

- **Scene**: Container for all objects, projectors, and lighting
- **SceneObject**: Base class for 3D objects with transform and geometry
- **Projector**: Specialized object with projection and shadow mapping capabilities
- **Camera**: Viewport camera with orbit controls

### Animation System

- **Timeline**: Manages playback, recording, and clips
- **AnimationClip**: Collection of property tracks
- **PropertyTrack**: Keyframe animation for a single property
- **Keyframe**: Single animation keyframe with value and easing

## Configuration

### Scene Files

Scenes can be saved/loaded as JSON:

```json
{
  "objects": [
    {
      "name": "Plane",
      "position": [0, 0, 0],
      "rotation": [0, 0, 0],
      "scale": [10, 0.1, 10]
    }
  ],
  "projectors": [
    {
      "name": "Projector 1",
      "position": [0, 5, 5],
      "rotation": [-0.524, 0, 0],
      "active": true,
      "intensity": 1.0,
      "fov": 40.0,
      "aspect": 1.6
    }
  ]
}
```

## Development

### Adding New Objects

```python
from projector_modern_gl.core.scene import SceneObject
import numpy as np

obj = SceneObject("My Object")
obj.position = np.array([0, 0, 0], dtype=np.float32)
obj.rotation = np.array([0, 0, 0], dtype=np.float32)
obj.scale = np.array([1, 1, 1], dtype=np.float32)
scene.add_object(obj)
```

### Adding Animation

```python
# Add keyframe for projector position
timeline.add_keyframe(
    target=projector,
    property_name="position",
    value=np.array([0, 10, 5]),
    easing='easeInOutCubic'
)
```

## Troubleshooting

### OpenGL Errors

If you encounter OpenGL errors, ensure your graphics drivers are up to date and support OpenGL 3.3 or higher.

### Performance Issues

- Reduce shadow map resolution (default: 2048x2048)
- Disable shadow mapping for non-essential projectors
- Reduce number of active projectors

## License

MIT License - See LICENSE file for details

## Author

fabazz21

## Acknowledgments

- ModernGL for high-performance OpenGL rendering
- ImGui for the UI framework
- Pygame for window management and event handling
