#!/usr/bin/env python3
"""
COMPLETE ERROR DETECTION SCRIPT
Tests everything at once without opening a window
Reports ALL errors in one go
"""

import sys
import traceback
from io import StringIO

class ErrorCollector:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.success = []

    def add_error(self, category, message, trace=None):
        self.errors.append({
            'category': category,
            'message': message,
            'trace': trace
        })

    def add_warning(self, category, message):
        self.warnings.append({
            'category': category,
            'message': message
        })

    def add_success(self, category, message):
        self.success.append({
            'category': category,
            'message': message
        })

    def print_report(self):
        print("\n" + "="*70)
        print("  COMPLETE ERROR DETECTION REPORT")
        print("="*70)

        if self.errors:
            print(f"\n❌ ERRORS FOUND: {len(self.errors)}")
            print("-"*70)
            for i, err in enumerate(self.errors, 1):
                print(f"\n{i}. [{err['category']}]")
                print(f"   {err['message']}")
                if err['trace']:
                    # Print last 3 lines of traceback
                    trace_lines = err['trace'].strip().split('\n')
                    for line in trace_lines[-3:]:
                        print(f"   {line}")

        if self.warnings:
            print(f"\n⚠️  WARNINGS: {len(self.warnings)}")
            print("-"*70)
            for i, warn in enumerate(self.warnings, 1):
                print(f"{i}. [{warn['category']}] {warn['message']}")

        if self.success:
            print(f"\n✅ SUCCESSFUL: {len(self.success)}")
            print("-"*70)
            for msg in self.success[:10]:  # Show first 10
                print(f"   ✓ [{msg['category']}] {msg['message']}")
            if len(self.success) > 10:
                print(f"   ... and {len(self.success) - 10} more")

        print("\n" + "="*70)
        print(f"SUMMARY: {len(self.success)} ✅  |  {len(self.warnings)} ⚠️   |  {len(self.errors)} ❌")
        print("="*70)

        if self.errors:
            print("\n🔧 FIX THESE ERRORS FIRST (in order of priority):")
            for i, err in enumerate(self.errors[:5], 1):
                print(f"   {i}. {err['message']}")
        else:
            print("\n🎉 NO ERRORS DETECTED! Application should start successfully.")

collector = ErrorCollector()

# ============================================================
# TEST 1: Module Imports
# ============================================================
print("Testing module imports...")

def test_imports():
    modules_to_test = [
        ('moderngl', 'ModernGL'),
        ('glfw', 'GLFW'),
        ('numpy', 'NumPy'),
        ('pyrr', 'Pyrr'),
        ('imgui', 'ImGui'),
        ('PIL', 'Pillow'),
        ('cv2', 'OpenCV'),
    ]

    for module_name, display_name in modules_to_test:
        try:
            __import__(module_name)
            collector.add_success('Import', display_name)
        except ImportError as e:
            collector.add_error('Import', f'Missing: {display_name} ({module_name})', str(e))

test_imports()

# ============================================================
# TEST 2: Project Module Imports
# ============================================================
print("Testing project modules...")

def test_project_modules():
    modules = [
        'core.window',
        'core.scene',
        'core.camera',
        'core.renderer',
        'objects.primitives',
        'objects.base_object',
        'projectors.projector',
        'projectors.projector_database',
        'projectors.lens_database',
        'animation.timeline',
        'animation.easing',
        'utils.history',
        'utils.math_utils',
        'ui.theme',
        'ui.main_ui_tabbed',
        'ui.panels.scene_panel',
        'ui.panels.properties_panel',
        'ui.panels.projector_panel',
        'ui.panels.viewport_panel',
        'ui.panels.timeline_panel',
        'ui.panels.export_panel',
        'ui.panels.photometric_panel',
    ]

    for mod_name in modules:
        try:
            __import__(mod_name)
            collector.add_success('Module', mod_name)
        except Exception as e:
            tb = traceback.format_exc()
            collector.add_error('Module', f'Failed to import {mod_name}: {str(e)}', tb)

test_project_modules()

# ============================================================
# TEST 3: Class Instantiation (Mock Mode)
# ============================================================
print("Testing class instantiation...")

def test_class_instantiation():
    # Test if classes can be instantiated (dry run)
    try:
        from projectors.projector_database import get_all_projectors, get_projector_by_id
        projectors = get_all_projectors()
        if len(projectors) > 0:
            collector.add_success('Database', f'Projector database: {len(projectors)} models')
        else:
            collector.add_warning('Database', 'No projectors in database')

        # Test getting a specific projector
        proj = get_projector_by_id('panasonic_pt_rq13k')
        if proj:
            collector.add_success('Database', 'Projector lookup works')
        else:
            collector.add_error('Database', 'Failed to get projector by ID', None)
    except Exception as e:
        tb = traceback.format_exc()
        collector.add_error('Database', f'Projector database error: {str(e)}', tb)

    try:
        from projectors.lens_database import get_all_lenses
        lenses = get_all_lenses()
        if len(lenses) > 0:
            collector.add_success('Database', f'Lens database: {len(lenses)} lenses')
        else:
            collector.add_warning('Database', 'No lenses in database')
    except Exception as e:
        tb = traceback.format_exc()
        collector.add_error('Database', f'Lens database error: {str(e)}', tb)

    try:
        from animation.easing import get_easing_function, get_easing_names
        names = get_easing_names()
        if len(names) > 0:
            collector.add_success('Animation', f'Easing functions: {len(names)} available')
        else:
            collector.add_warning('Animation', 'No easing functions')

        # Test an easing function
        func = get_easing_function('linear')
        result = func(0.5)
        if result is not None:
            collector.add_success('Animation', 'Easing function execution works')
    except Exception as e:
        tb = traceback.format_exc()
        collector.add_error('Animation', f'Easing error: {str(e)}', tb)

test_class_instantiation()

# ============================================================
# TEST 4: UI Panels render_content() Method
# ============================================================
print("Testing UI panel structure...")

def test_ui_panels():
    panels = [
        ('ui.panels.scene_panel', 'ScenePanel'),
        ('ui.panels.properties_panel', 'PropertiesPanel'),
        ('ui.panels.projector_panel', 'ProjectorPanel'),
        ('ui.panels.viewport_panel', 'ViewportPanel'),
        ('ui.panels.timeline_panel', 'TimelinePanel'),
        ('ui.panels.export_panel', 'ExportPanel'),
        ('ui.panels.photometric_panel', 'PhotometricPanel'),
    ]

    for module_name, class_name in panels:
        try:
            module = __import__(module_name, fromlist=[class_name])
            panel_class = getattr(module, class_name)

            # Check if render_content method exists
            if hasattr(panel_class, 'render_content'):
                collector.add_success('UI Panel', f'{class_name}.render_content() exists')
            else:
                collector.add_error('UI Panel', f'{class_name} missing render_content() method', None)

            # Check if __init__ method exists
            if hasattr(panel_class, '__init__'):
                collector.add_success('UI Panel', f'{class_name}.__init__() exists')
            else:
                collector.add_error('UI Panel', f'{class_name} missing __init__() method', None)

        except Exception as e:
            tb = traceback.format_exc()
            collector.add_error('UI Panel', f'{class_name} error: {str(e)}', tb)

test_ui_panels()

# ============================================================
# TEST 5: Theme Colors
# ============================================================
print("Testing theme...")

def test_theme():
    try:
        from ui.theme import ProjectorTheme

        # Check if colors are defined
        colors = ['BACKGROUND', 'FOREGROUND', 'PRIMARY', 'PRIMARY_GLOW',
                  'PANEL_BG', 'PANEL_HEADER', 'BORDER', 'MUTED']

        for color_name in colors:
            if hasattr(ProjectorTheme, color_name):
                collector.add_success('Theme', f'{color_name} color defined')
            else:
                collector.add_error('Theme', f'Missing color: {color_name}', None)

        # Check if methods exist
        methods = ['apply', 'push_primary_button', 'pop_primary_button',
                   'render_gizmo_button']

        for method_name in methods:
            if hasattr(ProjectorTheme, method_name):
                collector.add_success('Theme', f'{method_name}() method exists')
            else:
                collector.add_warning('Theme', f'Missing method: {method_name}()')

    except Exception as e:
        tb = traceback.format_exc()
        collector.add_error('Theme', f'Theme error: {str(e)}', tb)

test_theme()

# ============================================================
# TEST 6: Shader Files
# ============================================================
print("Testing shader files...")

def test_shaders():
    from pathlib import Path

    shaders = [
        'shaders/depth_vertex.glsl',
        'shaders/depth_fragment.glsl',
        'shaders/projector_vertex.glsl',
        'shaders/projector_fragment.glsl',
    ]

    for shader_path in shaders:
        path = Path(shader_path)
        if path.exists():
            content = path.read_text()
            if len(content) > 0:
                collector.add_success('Shader', f'{shader_path} OK ({len(content)} bytes)')
            else:
                collector.add_error('Shader', f'{shader_path} is empty', None)
        else:
            collector.add_error('Shader', f'{shader_path} not found', None)

test_shaders()

# ============================================================
# TEST 7: Mock Application Start (Dry Run)
# ============================================================
print("Testing mock application startup...")

def test_mock_app_start():
    try:
        # Test imports needed for main app
        import moderngl
        import glfw
        import imgui
        from imgui.integrations.glfw import GlfwRenderer
        import numpy as np

        from core.window import Window
        from core.renderer import Renderer
        from core.scene import Scene
        from core.camera import Camera
        from ui.main_ui_tabbed import MainUITabbed
        from animation.timeline import Timeline
        from utils.history import History

        collector.add_success('App Start', 'All main imports successful')

        # Check if MainUITabbed can be checked
        if hasattr(MainUITabbed, '__init__'):
            collector.add_success('App Start', 'MainUITabbed.__init__() exists')

    except Exception as e:
        tb = traceback.format_exc()
        collector.add_error('App Start', f'Mock startup failed: {str(e)}', tb)

test_mock_app_start()

# ============================================================
# FINAL REPORT
# ============================================================
collector.print_report()

# Return exit code
sys.exit(0 if len(collector.errors) == 0 else 1)
