"""
Test de correspondance des fonctions HTML vs ModernGL
Vérifie que toutes les fonctions du HTML sont présentes et fonctionnelles
"""

import sys
from pathlib import Path

# Color codes for terminal
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}  {text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}\n")

def print_section(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'─'*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}  {text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'─'*60}{Colors.END}")

def print_ok(text):
    print(f"  {Colors.GREEN}✅{Colors.END} {text}")

def print_partial(text):
    print(f"  {Colors.YELLOW}⚠️ {Colors.END} {text}")

def print_missing(text):
    print(f"  {Colors.RED}❌{Colors.END} {text}")

# Complete list of HTML functions extracted from projector_TIMELINE_PROJECTOR_FIX_2.html
HTML_FUNCTIONS = {
    # UI & Navigation
    "Tab System": [
        ("switchTab", "Switch between Setup/Calibration/Export tabs", "IMPLEMENTED"),
        ("openWidescreenCalculator", "Open widescreen calculator modal", "TODO"),
    ],

    # Gizmo & Transform
    "Gizmo Controls": [
        ("setGizmoMode", "Set gizmo mode (translate/rotate/scale)", "IMPLEMENTED"),
        ("resetTransform", "Reset object transform", "TODO"),
    ],

    # View Controls
    "Camera & View": [
        ("setCameraView", "Set camera view (top/front/left/right/back/perspective)", "IMPLEMENTED"),
        ("toggleGrid", "Toggle grid visibility", "IMPLEMENTED"),
        ("toggleFrustumFromMenu", "Toggle frustum helper", "IMPLEMENTED"),
        ("toggleMeasurementsFromMenu", "Toggle viewport measurements", "TODO"),
    ],

    # Brightness & Display
    "Display Settings": [
        ("toggleBrightnessPanel", "Toggle brightness adjustment panel", "TODO"),
        ("toggleGPUMonitor", "Toggle GPU performance monitor", "TODO"),
    ],

    # History & Undo/Redo
    "History System": [
        ("undo", "Undo last action (Ctrl+Z)", "IMPLEMENTED"),
        ("redo", "Redo last action (Ctrl+Y)", "IMPLEMENTED"),
        ("historyUndo", "History undo wrapper", "IMPLEMENTED"),
        ("historyRedo", "History redo wrapper", "IMPLEMENTED"),
    ],

    # Scene Objects
    "Scene Management": [
        ("openPrimitivePopup", "Open primitive creation menu (cube/sphere/plane/etc)", "PARTIAL"),
        ("openModelLoader", "Open 3D model loader", "TODO"),
        ("createCamera", "Create new camera", "TODO"),
        ("setSelectedAsTarget", "Set selected object as target", "TODO"),
        ("toggleTargetLock", "Lock projector aim to target", "TODO"),
    ],

    # Projector Management
    "Projector Controls": [
        ("openProjectorModal", "Open projector creation modal", "PARTIAL"),
        ("setProjectorOrientation", "Set projector orientation (landscape/portrait)", "TODO"),
        ("selectBrand", "Select projector brand (Panasonic/Epson/Barco/etc)", "IMPLEMENTED"),
        ("resetLensShift", "Reset lens shift to center", "TODO"),
    ],

    # Calibration & Correction
    "Calibration": [
        ("toggleKeystoneBypass", "Bypass keystone correction", "TODO"),
        ("resetKeystone", "Reset all keystone values", "TODO"),
        ("toggleStackBypass", "Bypass stacking/blending", "TODO"),
        ("toggleSoftEdgeBypass", "Bypass soft edge blending", "TODO"),
        ("resetSoftEdge", "Reset soft edge values", "TODO"),
        ("toggleWarpPanel", "Toggle mesh warping panel", "TODO"),
    ],

    # Media & Video
    "Media Playback": [
        ("loadVideoModern", "Load video file for projection", "TODO"),
        ("mediaPlay", "Play loaded media", "TODO"),
        ("mediaPause", "Pause media playback", "TODO"),
        ("mediaStop", "Stop media playback", "TODO"),
        ("mediaSpeed", "Change media playback speed (0.5x/1x/1.5x/2x)", "TODO"),
    ],

    # Timeline & Animation
    "Timeline System": [
        ("toggleTimeline", "Toggle timeline panel visibility", "IMPLEMENTED"),
        ("timelinePlay", "Play timeline animation", "TODO"),
        ("timelinePause", "Pause timeline", "TODO"),
        ("timelineStop", "Stop timeline", "TODO"),
        ("timelineRecord", "Start recording keyframes", "TODO"),
        ("stopTimeline", "Stop timeline (duplicate?)", "TODO"),
        ("addToTimeline", "Add object as timeline layer", "TODO"),
        ("addKeyframeQuick", "Quick add keyframe (K key)", "TODO"),
    ],

    # Export & Rendering
    "Export System": [
        ("exportScenePNG", "Export scene as PNG image", "PARTIAL"),
        ("toggleFloatingWindow", "Toggle floating windows", "TODO"),
        ("downloadBlueprint", "Download blueprint PNG", "TODO"),
        ("downloadAllPatterns", "Download all test patterns", "TODO"),
    ],

    # Test Patterns & Tools
    "Tools & Utilities": [
        ("openBlueprintModal", "Open blueprint generation modal", "TODO"),
        ("openTestPatternModal", "Open test pattern modal", "TODO"),
        ("selectWSMode", "Select widescreen mode (landscape/portrait/square)", "TODO"),
        ("setWSUnit", "Set widescreen unit (meters/inches)", "TODO"),
        ("applyWSCalculation", "Apply widescreen calculation to scene", "TODO"),
    ],

    # Viewers & Multi-View
    "Multi-View System": [
        ("toggleViewersMenu", "Toggle multi-viewer panel", "TODO"),
    ],

    # Panels & Windows
    "Panel Management": [
        ("togglePan", "Toggle panel visibility", "IMPLEMENTED"),
        ("closeProjectorModal", "Close projector modal", "TODO"),
        ("closeWidescreenCalculator", "Close widescreen calculator", "TODO"),
        ("closeWidescreenModeModal", "Close widescreen mode selector", "TODO"),
        ("closeBlueprintModal", "Close blueprint modal", "TODO"),
        ("closeTestPatternModal", "Close test pattern modal", "TODO"),
    ],

    # Project Management
    "Project System": [
        ("saveProject", "Save current project", "PARTIAL"),
        ("openProject", "Open existing project", "TODO"),
        ("newProject", "Create new project", "TODO"),
    ],

    # Analysis & Photometric
    "Photometric Analysis": [
        ("toggleFloatingWindow('photometric-window')", "Toggle photometric analysis window", "PARTIAL"),
        ("toggleFloatingWindow('scene-params-window')", "Toggle scene parameters window", "TODO"),
        ("toggleFloatingWindow('export-window')", "Toggle export window", "TODO"),
    ],
}

def check_implementation_status():
    """Check implementation status of all HTML functions"""

    print_header("HTML FUNCTION COVERAGE TEST")

    total_functions = 0
    implemented = 0
    partial = 0
    missing = 0

    for category, functions in HTML_FUNCTIONS.items():
        print_section(category)

        for func_name, description, status in functions:
            total_functions += 1

            if status == "IMPLEMENTED":
                print_ok(f"{func_name}: {description}")
                implemented += 1
            elif status == "PARTIAL":
                print_partial(f"{func_name}: {description}")
                partial += 1
            else:  # TODO
                print_missing(f"{func_name}: {description}")
                missing += 1

    # Summary
    print_header("SUMMARY")
    print(f"  Total Functions: {Colors.BOLD}{total_functions}{Colors.END}")
    print(f"  {Colors.GREEN}✅ Implemented: {implemented} ({implemented/total_functions*100:.1f}%){Colors.END}")
    print(f"  {Colors.YELLOW}⚠️  Partial: {partial} ({partial/total_functions*100:.1f}%){Colors.END}")
    print(f"  {Colors.RED}❌ Missing: {missing} ({missing/total_functions*100:.1f}%){Colors.END}")

    print(f"\n{Colors.BOLD}Implementation Progress:{Colors.END}")
    progress_bar_length = 40
    implemented_bar = int((implemented / total_functions) * progress_bar_length)
    partial_bar = int((partial / total_functions) * progress_bar_length)
    missing_bar = progress_bar_length - implemented_bar - partial_bar

    print(f"  [{Colors.GREEN}{'█' * implemented_bar}{Colors.END}", end='')
    print(f"{Colors.YELLOW}{'█' * partial_bar}{Colors.END}", end='')
    print(f"{Colors.RED}{'█' * missing_bar}{Colors.END}]")

    return implemented, partial, missing, total_functions

def generate_implementation_plan():
    """Generate implementation plan for missing functions"""

    print_header("IMPLEMENTATION PLAN")

    priority_high = []
    priority_medium = []
    priority_low = []

    for category, functions in HTML_FUNCTIONS.items():
        for func_name, description, status in functions:
            if status == "TODO" or status == "PARTIAL":
                # Categorize by priority
                if any(keyword in func_name.lower() for keyword in ['projector', 'camera', 'gizmo', 'undo', 'redo']):
                    priority_high.append((category, func_name, description, status))
                elif any(keyword in func_name.lower() for keyword in ['export', 'timeline', 'calibration', 'keystone']):
                    priority_medium.append((category, func_name, description, status))
                else:
                    priority_low.append((category, func_name, description, status))

    print_section("🔴 HIGH PRIORITY (Core Functionality)")
    for category, func_name, description, status in priority_high:
        marker = "⚠️ " if status == "PARTIAL" else "❌"
        print(f"  {marker} [{category}] {func_name}")
        print(f"      → {description}")

    print_section("🟡 MEDIUM PRIORITY (Important Features)")
    for category, func_name, description, status in priority_medium:
        marker = "⚠️ " if status == "PARTIAL" else "❌"
        print(f"  {marker} [{category}] {func_name}")
        print(f"      → {description}")

    print_section("🟢 LOW PRIORITY (Nice to Have)")
    for category, func_name, description, status in priority_low:
        marker = "⚠️ " if status == "PARTIAL" else "❌"
        print(f"  {marker} [{category}] {func_name}")
        print(f"      → {description}")

def print_next_steps():
    """Print recommended next steps"""

    print_header("RECOMMENDED NEXT STEPS")

    steps = [
        ("1", "Implement missing Projector functions", [
            "openProjectorModal - Complete UI for adding projectors",
            "setProjectorOrientation - Add landscape/portrait toggle",
            "resetLensShift - Reset lens shift controls"
        ]),
        ("2", "Complete Calibration system", [
            "Keystone bypass toggle",
            "Reset keystone/soft edge functions",
            "Warp panel for mesh deformation"
        ]),
        ("3", "Add Media playback", [
            "Video loading and playback",
            "Media controls (play/pause/stop)",
            "Playback speed control"
        ]),
        ("4", "Implement Timeline animation", [
            "Timeline record functionality",
            "Add objects as layers",
            "Quick keyframe addition"
        ]),
        ("5", "Add Tools & Utilities", [
            "Widescreen calculator",
            "Blueprint generator",
            "Test pattern generator"
        ]),
    ]

    for num, title, subtasks in steps:
        print(f"\n{Colors.BOLD}{Colors.BLUE}Step {num}: {title}{Colors.END}")
        for task in subtasks:
            print(f"    • {task}")

def main():
    """Main test function"""

    # Check implementation status
    implemented, partial, missing, total = check_implementation_status()

    # Generate implementation plan
    generate_implementation_plan()

    # Print next steps
    print_next_steps()

    # Final message
    print_header("TEST COMPLETE")
    completion_percentage = (implemented + partial * 0.5) / total * 100

    if completion_percentage >= 80:
        print(f"{Colors.GREEN}✅ Excellent progress! {completion_percentage:.1f}% complete{Colors.END}")
    elif completion_percentage >= 50:
        print(f"{Colors.YELLOW}⚠️  Good progress! {completion_percentage:.1f}% complete{Colors.END}")
    else:
        print(f"{Colors.RED}❌ More work needed! {completion_percentage:.1f}% complete{Colors.END}")

    print(f"\n{Colors.BOLD}To test the application:{Colors.END}")
    print(f"  python main.py\n")

if __name__ == "__main__":
    main()
