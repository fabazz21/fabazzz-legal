#!/usr/bin/env python3
"""
Complete test script to identify all errors at once
Run this and send me the complete output
"""
import sys
import os
from pathlib import Path

# Colors for terminal output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text:^60}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠️  {text}{RESET}")

def print_info(text):
    print(f"   {text}")

# Test results
total_tests = 0
passed_tests = 0
failed_tests = 0
errors = []

def test_import(module_name, description=""):
    """Test if a module can be imported"""
    global total_tests, passed_tests, failed_tests
    total_tests += 1

    try:
        __import__(module_name)
        passed_tests += 1
        print_success(f"{module_name:30} {description}")
        return True
    except ImportError as e:
        failed_tests += 1
        print_error(f"{module_name:30} {description}")
        print_info(f"Error: {str(e)}")
        errors.append(f"{module_name}: {str(e)}")
        return False

def test_file_exists(filepath, description=""):
    """Test if a file exists"""
    global total_tests, passed_tests, failed_tests
    total_tests += 1

    if Path(filepath).exists():
        passed_tests += 1
        print_success(f"{filepath:40} {description}")
        return True
    else:
        failed_tests += 1
        print_error(f"{filepath:40} {description}")
        errors.append(f"Missing file: {filepath}")
        return False

def test_ui_panel(panel_name):
    """Test if a UI panel can be imported"""
    global total_tests, passed_tests, failed_tests
    total_tests += 1

    try:
        module = __import__(f"ui.panels.{panel_name}_panel", fromlist=[f"{panel_name.title()}Panel"])
        panel_class = getattr(module, f"{panel_name.title()}Panel")
        passed_tests += 1
        print_success(f"Panel: {panel_name:25}")
        return True
    except Exception as e:
        failed_tests += 1
        print_error(f"Panel: {panel_name:25}")
        print_info(f"Error: {str(e)}")
        errors.append(f"Panel {panel_name}: {str(e)}")
        return False

def main():
    print_header("COMPLETE PROJECT TEST SUITE")

    print(f"Python version: {sys.version}")
    print(f"Python path: {sys.executable}")
    print(f"Working directory: {os.getcwd()}\n")

    # ========== TEST 1: CRITICAL DEPENDENCIES ==========
    print_header("TEST 1: CRITICAL DEPENDENCIES")

    test_import("moderngl", "Modern OpenGL binding")
    test_import("moderngl_window", "ModernGL window management")
    test_import("imgui", "ImGui UI library")
    test_import("OpenGL.GL", "PyOpenGL")
    test_import("glfw", "GLFW window library")
    test_import("numpy", "Numerical computing")
    test_import("pyrr", "3D math library")
    test_import("PIL", "Pillow image library")

    # ========== TEST 2: OPTIONAL DEPENDENCIES ==========
    print_header("TEST 2: OPTIONAL DEPENDENCIES")

    test_import("pygame", "Pygame (alternative window)")
    test_import("trimesh", "3D mesh loading")
    test_import("reportlab", "PDF export")
    test_import("matplotlib", "Plotting")
    test_import("cv2", "OpenCV video export")
    test_import("yaml", "YAML parsing")
    test_import("scipy", "Scientific computing")

    # ========== TEST 3: PROJECT FILES ==========
    print_header("TEST 3: PROJECT FILES")

    test_file_exists("main.py", "Main entry point")
    test_file_exists("main_simple.py", "Simple entry point")
    test_file_exists("requirements.txt", "Dependencies list")

    # ========== TEST 4: CORE MODULES ==========
    print_header("TEST 4: CORE MODULES")

    test_file_exists("core/__init__.py", "Core package")
    test_file_exists("core/camera.py", "Camera module")
    test_file_exists("core/renderer.py", "Renderer module")
    test_file_exists("core/scene.py", "Scene module")
    test_file_exists("core/window.py", "Window module")

    # ========== TEST 5: PROJECTOR MODULES ==========
    print_header("TEST 5: PROJECTOR MODULES")

    test_file_exists("projectors/__init__.py", "Projectors package")
    test_file_exists("projectors/projector.py", "Projector class")
    test_file_exists("projectors/projector_database.py", "Projector DB")
    test_file_exists("projectors/lens_database.py", "Lens DB")

    # ========== TEST 6: UI MODULES ==========
    print_header("TEST 6: UI MODULES")

    test_file_exists("ui/__init__.py", "UI package")
    test_file_exists("ui/main_ui.py", "Main UI")
    test_file_exists("ui/main_ui_tabbed.py", "Tabbed UI")
    test_file_exists("ui/theme.py", "UI theme")

    # ========== TEST 7: UI PANELS ==========
    print_header("TEST 7: UI PANELS")

    test_file_exists("ui/panels/__init__.py", "Panels package")
    test_file_exists("ui/panels/projector_panel.py", "Projector panel")
    test_file_exists("ui/panels/properties_panel.py", "Properties panel")
    test_file_exists("ui/panels/scene_panel.py", "Scene panel")
    test_file_exists("ui/panels/viewport_panel.py", "Viewport panel")
    test_file_exists("ui/panels/timeline_panel.py", "Timeline panel")
    test_file_exists("ui/panels/export_panel.py", "Export panel")
    test_file_exists("ui/panels/photometric_panel.py", "Photometric panel")

    # ========== TEST 8: SHADERS ==========
    print_header("TEST 8: SHADERS")

    test_file_exists("shaders/projector_vertex.glsl", "Vertex shader")
    test_file_exists("shaders/projector_fragment.glsl", "Fragment shader")
    test_file_exists("shaders/depth_vertex.glsl", "Depth vertex")
    test_file_exists("shaders/depth_fragment.glsl", "Depth fragment")

    # ========== TEST 9: IMPORT MAIN MODULES ==========
    print_header("TEST 9: IMPORT PROJECT MODULES")

    # Add current directory to path
    sys.path.insert(0, os.getcwd())

    try:
        print_info("Testing core imports...")
        test_import("core", "Core package")
        test_import("projectors", "Projectors package")
        test_import("ui", "UI package")
        test_import("ui.theme", "UI theme")
    except Exception as e:
        print_error(f"Module import failed: {e}")

    # ========== TEST 10: UI PANELS IMPORT ==========
    print_header("TEST 10: UI PANELS IMPORT")

    panels = ["projector", "properties", "scene", "viewport", "timeline", "export", "photometric"]
    for panel in panels:
        test_ui_panel(panel)

    # ========== TEST 11: IMGUI INTEGRATION ==========
    print_header("TEST 11: IMGUI INTEGRATION")

    global total_tests, passed_tests, failed_tests
    total_tests += 1

    try:
        import imgui
        from imgui.integrations.glfw import GlfwRenderer
        print_success("ImGui GLFW integration")
        print_info(f"ImGui version: {imgui.get_version()}")
        passed_tests += 1
    except Exception as e:
        print_error("ImGui GLFW integration")
        print_info(f"Error: {str(e)}")
        errors.append(f"ImGui integration: {str(e)}")
        failed_tests += 1

    # ========== FINAL REPORT ==========
    print_header("FINAL REPORT")

    print(f"\nTotal tests: {total_tests}")
    print_success(f"Passed: {passed_tests}")
    print_error(f"Failed: {failed_tests}")

    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    print(f"\n{BLUE}Success rate: {success_rate:.1f}%{RESET}\n")

    if errors:
        print_header("ERRORS SUMMARY")
        for i, error in enumerate(errors, 1):
            print(f"{RED}{i}. {error}{RESET}")

    if failed_tests == 0:
        print_header("🎉 ALL TESTS PASSED! 🎉")
        print(f"{GREEN}The application should work correctly!{RESET}\n")
    else:
        print_header("⚠️  ISSUES FOUND")
        print(f"{YELLOW}Please share this complete output so I can help fix the issues.{RESET}\n")

    return failed_tests == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
