"""
ImGui Theme Configuration
"""

import imgui


def setup_theme():
    """Setup custom dark theme for ImGui"""
    style = imgui.get_style()

    # Window
    style.window_padding = (10, 10)
    style.window_rounding = 6.0
    style.window_border_size = 1.0
    style.window_title_align = (0.5, 0.5)

    # Frame
    style.frame_padding = (8, 4)
    style.frame_rounding = 4.0
    style.frame_border_size = 0.0

    # Items
    style.item_spacing = (8, 6)
    style.item_inner_spacing = (6, 4)
    style.indent_spacing = 20.0

    # Scrollbar
    style.scrollbar_size = 14.0
    style.scrollbar_rounding = 8.0

    # Grab
    style.grab_min_size = 10.0
    style.grab_rounding = 4.0

    # Tab
    style.tab_rounding = 4.0

    # Colors (Dark theme with blue accents)
    colors = style.colors

    # Window
    colors[imgui.COLOR_WINDOW_BACKGROUND] = (0.071, 0.078, 0.090, 1.0)  # #121418
    colors[imgui.COLOR_CHILD_BACKGROUND] = (0.09, 0.10, 0.12, 1.0)

    # Title
    colors[imgui.COLOR_TITLE_BACKGROUND] = (0.05, 0.05, 0.07, 1.0)
    colors[imgui.COLOR_TITLE_BACKGROUND_ACTIVE] = (0.10, 0.11, 0.14, 1.0)
    colors[imgui.COLOR_TITLE_BACKGROUND_COLLAPSED] = (0.05, 0.05, 0.07, 0.7)

    # Frame
    colors[imgui.COLOR_FRAME_BACKGROUND] = (0.15, 0.16, 0.19, 1.0)
    colors[imgui.COLOR_FRAME_BACKGROUND_HOVERED] = (0.20, 0.22, 0.26, 1.0)
    colors[imgui.COLOR_FRAME_BACKGROUND_ACTIVE] = (0.25, 0.27, 0.32, 1.0)

    # Button
    colors[imgui.COLOR_BUTTON] = (0.20, 0.25, 0.35, 1.0)
    colors[imgui.COLOR_BUTTON_HOVERED] = (0.25, 0.32, 0.45, 1.0)
    colors[imgui.COLOR_BUTTON_ACTIVE] = (0.18, 0.23, 0.33, 1.0)

    # Header
    colors[imgui.COLOR_HEADER] = (0.20, 0.25, 0.35, 0.8)
    colors[imgui.COLOR_HEADER_HOVERED] = (0.25, 0.32, 0.45, 0.9)
    colors[imgui.COLOR_HEADER_ACTIVE] = (0.18, 0.23, 0.33, 1.0)

    # Tab
    colors[imgui.COLOR_TAB] = (0.15, 0.17, 0.22, 1.0)
    colors[imgui.COLOR_TAB_HOVERED] = (0.25, 0.32, 0.45, 1.0)
    colors[imgui.COLOR_TAB_ACTIVE] = (0.20, 0.25, 0.35, 1.0)
    colors[imgui.COLOR_TAB_UNFOCUSED] = (0.12, 0.14, 0.18, 1.0)
    colors[imgui.COLOR_TAB_UNFOCUSED_ACTIVE] = (0.17, 0.20, 0.27, 1.0)

    # Scrollbar
    colors[imgui.COLOR_SCROLLBAR_BACKGROUND] = (0.08, 0.09, 0.11, 1.0)
    colors[imgui.COLOR_SCROLLBAR_GRAB] = (0.30, 0.30, 0.30, 1.0)
    colors[imgui.COLOR_SCROLLBAR_GRAB_HOVERED] = (0.40, 0.40, 0.40, 1.0)
    colors[imgui.COLOR_SCROLLBAR_GRAB_ACTIVE] = (0.50, 0.50, 0.50, 1.0)

    # Slider
    colors[imgui.COLOR_SLIDER_GRAB] = (0.30, 0.40, 0.55, 1.0)
    colors[imgui.COLOR_SLIDER_GRAB_ACTIVE] = (0.35, 0.47, 0.65, 1.0)

    # Check mark
    colors[imgui.COLOR_CHECK_MARK] = (0.35, 0.47, 0.65, 1.0)

    # Separator
    colors[imgui.COLOR_SEPARATOR] = (0.25, 0.27, 0.32, 1.0)
    colors[imgui.COLOR_SEPARATOR_HOVERED] = (0.30, 0.35, 0.45, 1.0)
    colors[imgui.COLOR_SEPARATOR_ACTIVE] = (0.35, 0.42, 0.55, 1.0)

    # Resize grip
    colors[imgui.COLOR_RESIZE_GRIP] = (0.20, 0.25, 0.35, 0.5)
    colors[imgui.COLOR_RESIZE_GRIP_HOVERED] = (0.25, 0.32, 0.45, 0.7)
    colors[imgui.COLOR_RESIZE_GRIP_ACTIVE] = (0.30, 0.38, 0.53, 1.0)

    # Text
    colors[imgui.COLOR_TEXT] = (0.95, 0.95, 0.95, 1.0)
    colors[imgui.COLOR_TEXT_DISABLED] = (0.50, 0.50, 0.50, 1.0)

    # Border
    colors[imgui.COLOR_BORDER] = (0.20, 0.22, 0.27, 1.0)
    colors[imgui.COLOR_BORDER_SHADOW] = (0.0, 0.0, 0.0, 0.0)

    print("✅ ImGui theme configured")
