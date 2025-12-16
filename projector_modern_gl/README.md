# Professional 3D Projection Mapping System - ModernGL
## Panasonic PT-RQ25K Shadow-Mapped Projection Shader

A complete professional-grade 3D projection mapping and visualization tool built with ModernGL (Python), featuring advanced shadow mapping, multi-projector management, timeline animation, and photometric analysis.

## Features

### 🎥 Multi-Projector System
- **18 Professional Projector Models** from 4 manufacturers:
  - Panasonic PT-RQ Series (7 models): 10,000 - 30,500 lumens
  - Epson EB/PowerLite Series (6 models): 6,000 - 30,000 lumens
  - Barco UDX/G62 Series (5 models): 11,000 - 31,000 lumens
  - Optoma ZU Series (5 models): 7,500 - 22,000 lumens
- **24 Compatible Lenses** with precise throw ratios and lens shift
- **Up to 4 simultaneous projectors** with advanced blending
- **Shadow mapping** with depth buffer rendering
- **Off-axis frustum** visualization for lens shift

### 🎨 Advanced Correction Tools
- **Keystone Correction**: Vertical/horizontal + 4-corner independent control
- **Corner Pin**: Homographic perspective correction
- **Soft Edge Blending**: Per-edge gamma-controlled falloff (L/R/T/B)
- **Mesh Warping**: Grid-based geometric distortion

### 📽️ Shadow-Mapped Projection Shader
- Custom GLSL shaders with:
  - Linear depth rendering
  - Multi-projector shadow maps
  - Keystone correction in shader space
  - Corner pin transformation
  - Soft edge blending with gamma curves
  - Distance attenuation
  - Normal-based lighting

### 🎬 Timeline & Animation
- **Keyframe-based animation** system
- **12 easing functions**: Linear, Quad, Cubic, Quart, Expo (In/Out/InOut)
- **Multi-layer timeline** with play/pause/scrub
- **Per-object animation**: Position, rotation, scale
- **Frame-by-frame export** to ZIP archives

### 📐 Photometric Analysis
- **Illuminance calculation** (lux)
- **Luminance calculation** (cd/m²)
- **Coverage area analysis**
- **Pixel size computation**
- **Blueprint/Widescreen calculator** with automatic optimization
- **Landscape/Portrait/Square** layout modes

### 🖼️ 3D Model Support
- **Import formats**: OBJ, FBX, glTF 2.0, GLB
- **Primitive shapes**: Cube, Sphere, Cylinder, Cone, Torus, Plane
- **Articulated mannequin** (1.80m with moveable joints)
- **Custom projection screens** (4m - custom sizes)

### 📊 Test Pattern Generator
- Numbered Grid (with coordinates)
- Color Grid (RGB color space)
- Cross Pattern (alignment)
- Overlap Gradient (blend zones)
- Circle Pattern (distortion testing)
- Checkerboard

### 💾 Export Capabilities
- **PNG Screenshots** (high resolution)
- **PDF Reports** with:
  - Viewport screenshot
  - Projector specifications
  - Photometric analysis
  - Custom notes
- **Video/Frame Sequences** (ZIP export)
- **Blueprint Images** (calculation diagrams)

### 🎮 Professional UI
- **ImGui-based interface** with dark theme
- **Floating draggable windows**:
  - Transform Parameters
  - Keystone Controls
  - Corner Pin Controls
  - Soft Edge Controls
  - Photometric Analysis
  - Timeline Editor
- **Collapsible panels**:
  - Projector Selection
  - Lens Configuration
  - Correction Tools
  - Advanced Settings
- **Undo/Redo system** (Ctrl+Z / Ctrl+Y)

### 🎯 Transform & Gizmos
- **3-axis gizmos**: Translate, Rotate, Scale
- **Snap points**: Top-Left, Top-Right, Center, Bottom-Left, Bottom-Right
- **Rotation snapping** (15° increments)
- **Manual input** with live sync (X, Y, Z values)

### 🎥 Multi-Camera System
- Multiple camera instances
- Camera helpers & frustum visualization
- Assignable to viewers
- Free orbit controls

### 🔄 Scene Management
- **Object hierarchy** with solo/visibility/rename
- **Scene statistics** display
- **Shadow quality** control
- **Ambient & directional lighting** control
- **Grid & measurement tools**

## Installation

```bash
# Clone repository
git clone <repository-url>
cd projector_modern_gl

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Run the application
python main.py
```

### Keyboard Shortcuts

- **W/A/S/D**: Camera movement
- **Q/E**: Camera up/down
- **G**: Toggle translate mode
- **R**: Toggle rotate mode
- **S**: Toggle scale mode
- **K**: Add keyframe at current time
- **Spacebar**: Play/Pause timeline
- **Delete**: Delete selected object
- **Ctrl+Z**: Undo
- **Ctrl+Y**: Redo
- **Ctrl+D**: Duplicate object
- **L**: Rename selected object
- **V**: Toggle visibility
- **Shift+S**: Solo selected object

### Mouse Controls

- **Left Click**: Select object
- **Right Click**: Context menu
- **Middle Mouse**: Pan camera (with Shift)
- **Scroll**: Zoom camera
- **Left Drag (on gizmo)**: Transform object

## Architecture

```
projector_modern_gl/
├── main.py                       # Application entry point
├── requirements.txt              # Python dependencies
│
├── core/                         # Core rendering engine
│   ├── renderer.py               # ModernGL renderer
│   ├── window.py                 # GLFW window management
│   ├── camera.py                 # Camera system
│   ├── scene.py                  # 3D scene management
│   └── transform.py              # Transform operations
│
├── shaders/                      # GLSL shaders
│   ├── depth_vertex.glsl         # Depth pass vertex
│   ├── depth_fragment.glsl       # Depth pass fragment
│   ├── projector_vertex.glsl     # Multi-projector vertex
│   ├── projector_fragment.glsl   # Multi-projector fragment
│   └── warp_*.glsl               # Mesh warp shaders
│
├── projectors/                   # Projector system
│   ├── projector.py              # Projector class
│   ├── projector_database.py    # 18 projector models
│   ├── lens_database.py          # 24 lens models
│   ├── shadow_mapping.py         # Shadow system
│   ├── keystone.py               # Keystone correction
│   ├── corner_pin.py             # Corner pin
│   └── soft_edge.py              # Soft edge blending
│
├── timeline/                     # Animation system
│   ├── timeline.py               # Timeline manager
│   ├── keyframe.py               # Keyframe system
│   ├── easing.py                 # Easing functions
│   └── animation.py              # Animation controller
│
├── objects/                      # 3D objects
│   ├── primitives.py             # Primitive shapes
│   ├── model_loader.py           # 3D model loading
│   ├── mannequin.py              # Articulated figure
│   └── screen.py                 # Projection screens
│
├── ui/                           # User interface
│   ├── main_ui.py                # Main ImGui interface
│   ├── panels/                   # UI panels
│   └── windows/                  # Floating windows
│
├── photometric/                  # Photometric analysis
│   ├── calculator.py             # Photometric calculations
│   └── blueprint.py              # Blueprint generator
│
├── export/                       # Export system
│   ├── png_export.py             # PNG screenshots
│   ├── pdf_export.py             # PDF reports
│   ├── video_export.py           # Video export
│   └── pattern_generator.py     # Test patterns
│
└── utils/                        # Utilities
    ├── math_utils.py             # Mathematical utilities
    ├── history.py                # Undo/Redo system
    └── file_utils.py             # File operations
```

## Technical Specifications

### Rendering
- **API**: ModernGL (OpenGL 3.3+ Core Profile)
- **Window**: GLFW
- **UI**: Dear ImGui
- **Shaders**: GLSL 330 core

### Performance
- **Multi-threaded rendering**
- **Frustum culling**
- **Depth pre-pass** for shadow optimization
- **Texture streaming** for large models
- **GPU-accelerated** geometry processing

### Supported Formats

**Import**:
- 3D Models: OBJ, FBX, glTF 2.0, GLB
- Textures: PNG, JPG, BMP, TGA, HDR
- Videos: MP4, MOV, AVI, WebM

**Export**:
- Images: PNG (high-res, alpha channel)
- Documents: PDF (with embedded images)
- Video: Frame sequences (ZIP), MP4
- Patterns: PNG test patterns

## License

[Your License Here]

## Credits

- Original Three.js version: [Link if applicable]
- ModernGL: [Szabolcs Dombi](https://github.com/moderngl/moderngl)
- Dear ImGui: [Omar Cornut](https://github.com/ocornut/imgui)

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Support

For issues, feature requests, or questions, please open an issue on GitHub.
