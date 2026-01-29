#!/usr/bin/env python3
"""
Test script to check all dependencies and modules
Run this BEFORE launching main.py to catch all errors at once
"""

import sys

print("=" * 60)
print("  TESTING PROJECTION MAPPING SYSTEM")
print("=" * 60)
print()

errors = []
warnings = []

# Test 1: Python packages
print("🔍 Testing Python packages...")
packages = {
    'moderngl': 'ModernGL',
    'glfw': 'GLFW',
    'numpy': 'NumPy',
    'pyrr': 'Pyrr',
    'imgui': 'ImGui',
    'PIL': 'Pillow',
    'cv2': 'OpenCV',
    'reportlab': 'ReportLab',
    'trimesh': 'Trimesh'
}

for module, name in packages.items():
    try:
        __import__(module)
        print(f"  ✅ {name}")
    except ImportError:
        errors.append(f"Missing package: {name} (pip install {module if module != 'PIL' else 'Pillow'} {module if module != 'cv2' else 'opencv-python'})")
        print(f"  ❌ {name} - NOT INSTALLED")

print()

# Test 2: Project modules
print("🔍 Testing project modules...")
sys.path.insert(0, '.')

modules_to_test = [
    ('core.window', 'Window'),
    ('core.scene', 'Scene'),
    ('core.camera', 'Camera'),
    ('core.renderer', 'Renderer'),
    ('objects.primitives', 'create_primitive'),
    ('objects.base_object', 'Object3D'),
    ('projectors.projector', 'Projector'),
    ('projectors.projector_database', 'get_projector_by_id'),
    ('projectors.lens_database', 'get_lens_by_id'),
    ('animation.timeline', 'Timeline'),
    ('animation.easing', 'get_easing_function'),
    ('utils.history', 'History'),
    ('utils.math_utils', 'throw_to_fov'),
]

for module_name, class_name in modules_to_test:
    try:
        module = __import__(module_name, fromlist=[class_name])
        getattr(module, class_name)
        print(f"  ✅ {module_name}.{class_name}")
    except Exception as e:
        errors.append(f"Module error: {module_name}.{class_name} - {e}")
        print(f"  ❌ {module_name}.{class_name} - {e}")

print()

# Test 3: Renderer attributes
print("🔍 Testing Renderer class attributes...")
try:
    from core.renderer import Renderer
    import moderngl

    ctx = moderngl.create_context(standalone=True, require=330)
    renderer = Renderer(ctx, 800, 600)

    required_attrs = [
        'ctx', 'width', 'height',
        'depth_shader', 'projector_shader',
        'depth_framebuffers', 'depth_textures',
        'background_color', 'shadow_map_size',
        'show_frustums', 'wireframe_mode', 'stats'
    ]

    for attr in required_attrs:
        if hasattr(renderer, attr):
            print(f"  ✅ renderer.{attr}")
        else:
            errors.append(f"Missing Renderer attribute: {attr}")
            print(f"  ❌ renderer.{attr} - MISSING")

except Exception as e:
    errors.append(f"Renderer test failed: {e}")
    print(f"  ❌ Renderer test failed: {e}")

print()

# Test 4: Shaders
print("🔍 Testing shader files...")
shader_files = [
    'shaders/depth_vertex.glsl',
    'shaders/depth_fragment.glsl',
    'shaders/projector_vertex.glsl',
    'shaders/projector_fragment.glsl'
]

import os
for shader in shader_files:
    if os.path.exists(shader):
        print(f"  ✅ {shader}")
    else:
        errors.append(f"Missing shader: {shader}")
        print(f"  ❌ {shader} - NOT FOUND")

print()

# Summary
print("=" * 60)
if errors:
    print(f"❌ FOUND {len(errors)} ERROR(S):")
    for i, error in enumerate(errors, 1):
        print(f"   {i}. {error}")
    print()
    print("🔧 TO FIX ALL ERRORS:")
    print("   1. Install missing packages:")
    print("      pip install Pillow opencv-python reportlab trimesh")
    print("   2. Download latest version from GitHub:")
    print("      https://github.com/fabazz21/fabazzz-legal/archive/refs/heads/claude/modern-opengl-ut5JW.zip")
    print()
    sys.exit(1)
else:
    print("✅ ALL TESTS PASSED!")
    print()
    print("🚀 You can now run: python main.py")
    print()
    sys.exit(0)
