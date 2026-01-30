#!/usr/bin/env python3
"""
Automated Error Diagnostic Script
Tests all panels and UI interactions, reports all errors
"""

import sys
import ast
import re
from pathlib import Path

# Color codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}{text:^70}{RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠️  {text}{RESET}")

def print_info(text):
    print(f"   {text}")


class AttributeChecker:
    """Check for missing attributes across the codebase"""

    def __init__(self):
        self.errors = []
        self.warnings = []

        # Define expected attributes for each class
        self.expected_attributes = {
            'Scene': [
                'ctx', 'projectors', 'cameras', 'objects', 'lights',
                'show_helpers', 'show_grid', 'show_frustums', 'grid', 'grid_size',
                'ambient_light_intensity', 'directional_light_intensity',
                'directional_light_direction', 'object_count', 'projector_count'
            ],
            'Camera': [
                'position', 'target', 'up', 'fov', 'near', 'far',
                'azimuth', 'elevation', 'distance', 'zoom'
            ],
            'Projector': [
                'name', 'id', 'active', 'position', 'rotation', 'config',
                'model', 'brand', 'lumens', 'resolution', 'throw_ratio',
                'lens_shift_h', 'lens_shift_v', 'depth_fbo_index'
            ],
            'Timeline': [
                'duration', 'current_time', 'fps', 'keyframes',
                'playing', 'loop', 'speed'
            ],
            'Renderer': [
                'ctx', 'shader', 'fbo', 'depth_fbo'
            ],
            'Object3D': [
                'name', 'id', 'position', 'rotation', 'scale',
                'visible', 'mesh', 'color'
            ]
        }

        # Track actual attributes found in source files
        self.found_attributes = {cls: set() for cls in self.expected_attributes}

    def extract_attributes_from_file(self, filepath, class_name):
        """Extract attribute assignments from a Python file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse the AST
            tree = ast.parse(content)

            # Find the class definition
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == class_name:
                    # Look for self.attribute assignments
                    for item in ast.walk(node):
                        if isinstance(item, ast.Attribute):
                            if isinstance(item.value, ast.Name) and item.value.id == 'self':
                                self.found_attributes[class_name].add(item.attr)

            print_success(f"Analyzed {class_name} in {filepath.name}")

        except Exception as e:
            print_error(f"Failed to analyze {filepath}: {e}")

    def find_attribute_usage_in_panels(self, panels_dir):
        """Find all attribute accesses in panel files"""
        usage = {}

        for panel_file in Path(panels_dir).glob("*_panel.py"):
            try:
                with open(panel_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Find patterns like scene.attribute, projector.attribute, etc.
                patterns = {
                    'scene': r'scene\.(\w+)',
                    'projector': r'projector\.(\w+)',
                    'camera': r'camera\.(\w+)',
                    'timeline': r'timeline\.(\w+)',
                    'obj': r'obj\.(\w+)',
                }

                for obj_type, pattern in patterns.items():
                    matches = re.findall(pattern, content)
                    if matches:
                        if obj_type not in usage:
                            usage[obj_type] = {}
                        if panel_file.name not in usage[obj_type]:
                            usage[obj_type][panel_file.name] = set()
                        usage[obj_type][panel_file.name].update(matches)

            except Exception as e:
                print_error(f"Failed to read {panel_file}: {e}")

        return usage

    def check_missing_attributes(self):
        """Check for attributes used in panels but not defined in classes"""
        print_header("CHECKING FOR MISSING ATTRIBUTES")

        # Map object types to class names
        type_to_class = {
            'scene': 'Scene',
            'projector': 'Projector',
            'camera': 'Camera',
            'timeline': 'Timeline',
            'obj': 'Object3D'
        }

        # Find attribute usage in panels
        usage = self.find_attribute_usage_in_panels('ui/panels')

        # Check each usage
        for obj_type, files in usage.items():
            class_name = type_to_class.get(obj_type)
            if not class_name:
                continue

            print(f"\n{MAGENTA}Checking {class_name} attributes:{RESET}")

            for filename, attributes in files.items():
                for attr in attributes:
                    # Skip common methods
                    if attr in ['update', 'render', 'cleanup', 'append', 'remove',
                               'clear', 'get', 'set', 'add', 'delete']:
                        continue

                    # Check if expected
                    if class_name in self.expected_attributes:
                        if attr not in self.expected_attributes[class_name]:
                            error_msg = f"{filename} uses {obj_type}.{attr} - NOT in expected attributes"
                            print_error(error_msg)
                            self.errors.append({
                                'file': filename,
                                'class': class_name,
                                'attribute': attr,
                                'type': 'MISSING_DEFINITION'
                            })
                        else:
                            print_success(f"{filename}: {obj_type}.{attr} ✓")

    def scan_for_common_errors(self):
        """Scan for common error patterns"""
        print_header("SCANNING FOR COMMON ERROR PATTERNS")

        patterns = [
            (r'self\.ui\.app\.scene\.(\w+)', 'Scene attribute access'),
            (r'self\.ui\.app\.camera\.(\w+)', 'Camera attribute access'),
            (r'self\.ui\.app\.timeline\.(\w+)', 'Timeline attribute access'),
            (r'self\.ui\.app\.renderer\.(\w+)', 'Renderer attribute access'),
        ]

        for panel_file in Path('ui/panels').glob("*_panel.py"):
            try:
                with open(panel_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                for line_num, line in enumerate(lines, 1):
                    for pattern, description in patterns:
                        matches = re.findall(pattern, line)
                        for attr in matches:
                            print_info(f"{panel_file.name}:{line_num} - {description}: {attr}")

            except Exception as e:
                print_error(f"Failed to scan {panel_file}: {e}")

    def generate_report(self):
        """Generate final error report"""
        print_header("ERROR REPORT")

        if not self.errors:
            print_success("No missing attributes detected!")
            return True

        print(f"\n{RED}Found {len(self.errors)} potential issues:{RESET}\n")

        # Group by class
        by_class = {}
        for error in self.errors:
            cls = error['class']
            if cls not in by_class:
                by_class[cls] = []
            by_class[cls].append(error)

        for cls, errors in by_class.items():
            print(f"\n{MAGENTA}{cls}:{RESET}")
            for err in errors:
                print(f"  {RED}•{RESET} {err['file']}: missing attribute '{err['attribute']}'")

        print(f"\n{YELLOW}Recommendation: Add these attributes to their respective class __init__ methods{RESET}\n")

        return False


def main():
    """Main diagnostic function"""
    print_header("AUTOMATED ERROR DIAGNOSTIC")

    print("This script will analyze the codebase for potential runtime errors")
    print("related to missing attributes and method calls.\n")

    checker = AttributeChecker()

    # Check Scene class
    scene_file = Path('core/scene.py')
    if scene_file.exists():
        checker.extract_attributes_from_file(scene_file, 'Scene')

    # Check Camera class
    camera_file = Path('core/camera.py')
    if camera_file.exists():
        checker.extract_attributes_from_file(camera_file, 'Camera')

    # Check for missing attributes
    checker.check_missing_attributes()

    # Scan for common errors
    checker.scan_for_common_errors()

    # Generate report
    success = checker.generate_report()

    # Print manual testing instructions
    print_header("MANUAL TESTING CHECKLIST")
    print("""
After fixing the errors above, manually test these UI interactions:

Setup Tab:
  ☐ Open Scene panel → Try to change Grid Size slider
  ☐ Open Projectors panel → Create new projector
  ☐ Open Viewport panel → Adjust camera FOV, azimuth, elevation

Calibration Tab:
  ☐ Select a projector → Adjust lens shift
  ☐ Adjust throw ratio
  ☐ Change projector position

Export Tab:
  ☐ Try PDF export
  ☐ Try Video export
  ☐ Try Image sequence export

Perspective Tab:
  ☐ Change view angle
  ☐ Test camera controls

Timeline:
  ☐ Play/Pause animation
  ☐ Add keyframe
  ☐ Scrub timeline

Each crash will show an AttributeError - report all of them!
    """)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
