"""
ImGui Theme - Reproduit exactement le design du HTML
Couleurs et styles identiques à projector_TIMELINE_PROJECTOR_FIX_2.html
"""

import imgui

class ProjectorTheme:
    """Theme matching HTML design"""

    # HTML CSS Variables (extracted from :root)
    BACKGROUND = (0.071, 0.078, 0.094)       # #121418
    FOREGROUND = (0.937, 0.945, 0.961)       # #eff1f5
    PRIMARY = (0.078, 0.722, 0.651)          # #14b8a6 (teal)
    PRIMARY_GLOW = (0.176, 0.831, 0.749)     # #2dd4bf
    PANEL_BG = (0.086, 0.090, 0.110)         # #16171c
    PANEL_HEADER = (0.102, 0.106, 0.129)     # #1a1b21
    BORDER = (0.176, 0.184, 0.212)           # #2d2f36
    MUTED = (0.149, 0.153, 0.180)            # #26272e
    MUTED_FOREGROUND = (0.545, 0.553, 0.596) # #8b8d98
    ACCENT = (0.122, 0.161, 0.216)           # #1f2937

    # Button colors
    BUTTON_ACTIVE = (0.078, 0.722, 0.651, 0.2)    # Primary with alpha
    BUTTON_HOVERED = (0.078, 0.722, 0.651, 0.4)
    BUTTON_NORMAL = (0.086, 0.090, 0.110, 1.0)

    @staticmethod
    def apply():
        """Apply the HTML-matching theme to ImGui"""
        style = imgui.get_style()

        # ========================================
        # WINDOW STYLING
        # ========================================
        style.window_padding = (12, 12)
        style.window_rounding = 8.0
        style.window_border_size = 1.0
        style.window_title_align = (0.5, 0.5)  # Center title

        # ========================================
        # FRAME STYLING (inputs, buttons)
        # ========================================
        style.frame_padding = (8, 6)
        style.frame_rounding = 4.0
        style.frame_border_size = 1.0

        # ========================================
        # ITEM SPACING
        # ========================================
        style.item_spacing = (8, 6)
        style.item_inner_spacing = (6, 4)
        style.indent_spacing = 20.0

        # ========================================
        # SCROLLBAR
        # ========================================
        style.scrollbar_size = 12.0
        style.scrollbar_rounding = 4.0
        style.grab_min_size = 8.0
        style.grab_rounding = 4.0

        # ========================================
        # TAB STYLING
        # ========================================
        style.tab_rounding = 4.0
        style.tab_border_size = 0.0

        # ========================================
        # COLORS (matching HTML exactly)
        # ========================================
        colors = style.colors

        # Window colors
        colors[imgui.COLOR_WINDOW_BACKGROUND] = (*ProjectorTheme.PANEL_BG, 0.98)
        colors[imgui.COLOR_CHILD_BACKGROUND] = (*ProjectorTheme.PANEL_BG, 1.0)
        colors[imgui.COLOR_POPUP_BACKGROUND] = (*ProjectorTheme.PANEL_BG, 0.98)

        # Border
        colors[imgui.COLOR_BORDER] = (*ProjectorTheme.BORDER, 1.0)
        colors[imgui.COLOR_BORDER_SHADOW] = (0, 0, 0, 0)

        # Title bar
        colors[imgui.COLOR_TITLE_BACKGROUND] = (*ProjectorTheme.PANEL_HEADER, 1.0)
        colors[imgui.COLOR_TITLE_BACKGROUND_ACTIVE] = (*ProjectorTheme.PANEL_HEADER, 1.0)
        colors[imgui.COLOR_TITLE_BACKGROUND_COLLAPSED] = (*ProjectorTheme.PANEL_HEADER, 0.8)

        # Text
        colors[imgui.COLOR_TEXT] = (*ProjectorTheme.FOREGROUND, 1.0)
        colors[imgui.COLOR_TEXT_DISABLED] = (*ProjectorTheme.MUTED_FOREGROUND, 1.0)

        # Frames (inputs, combos, etc)
        colors[imgui.COLOR_FRAME_BACKGROUND] = (*ProjectorTheme.MUTED, 0.5)
        colors[imgui.COLOR_FRAME_BACKGROUND_HOVERED] = (*ProjectorTheme.MUTED, 0.7)
        colors[imgui.COLOR_FRAME_BACKGROUND_ACTIVE] = (*ProjectorTheme.MUTED, 0.9)

        # Buttons
        colors[imgui.COLOR_BUTTON] = (*ProjectorTheme.MUTED, 0.6)
        colors[imgui.COLOR_BUTTON_HOVERED] = (*ProjectorTheme.PRIMARY, 0.4)
        colors[imgui.COLOR_BUTTON_ACTIVE] = (*ProjectorTheme.PRIMARY, 0.6)

        # Headers (collapsing, tree nodes)
        colors[imgui.COLOR_HEADER] = (*ProjectorTheme.PRIMARY, 0.2)
        colors[imgui.COLOR_HEADER_HOVERED] = (*ProjectorTheme.PRIMARY, 0.3)
        colors[imgui.COLOR_HEADER_ACTIVE] = (*ProjectorTheme.PRIMARY, 0.4)

        # Separator
        colors[imgui.COLOR_SEPARATOR] = (*ProjectorTheme.BORDER, 0.8)
        colors[imgui.COLOR_SEPARATOR_HOVERED] = (*ProjectorTheme.PRIMARY, 0.6)
        colors[imgui.COLOR_SEPARATOR_ACTIVE] = (*ProjectorTheme.PRIMARY, 0.8)

        # Resize grip
        colors[imgui.COLOR_RESIZE_GRIP] = (*ProjectorTheme.PRIMARY, 0.2)
        colors[imgui.COLOR_RESIZE_GRIP_HOVERED] = (*ProjectorTheme.PRIMARY, 0.4)
        colors[imgui.COLOR_RESIZE_GRIP_ACTIVE] = (*ProjectorTheme.PRIMARY, 0.6)

        # Tabs (if available)
        try:
            colors[imgui.COLOR_TAB] = (*ProjectorTheme.MUTED, 0.6)
            colors[imgui.COLOR_TAB_HOVERED] = (*ProjectorTheme.PRIMARY, 0.5)
            colors[imgui.COLOR_TAB_ACTIVE] = (*ProjectorTheme.PRIMARY, 0.7)
            colors[imgui.COLOR_TAB_UNFOCUSED] = (*ProjectorTheme.MUTED, 0.4)
            colors[imgui.COLOR_TAB_UNFOCUSED_ACTIVE] = (*ProjectorTheme.MUTED, 0.6)
        except AttributeError:
            pass  # Tab colors not available in this imgui version

        # Scrollbar
        colors[imgui.COLOR_SCROLLBAR_BACKGROUND] = (*ProjectorTheme.MUTED, 0.3)
        colors[imgui.COLOR_SCROLLBAR_GRAB] = (*ProjectorTheme.BORDER, 0.8)
        colors[imgui.COLOR_SCROLLBAR_GRAB_HOVERED] = (*ProjectorTheme.PRIMARY, 0.8)
        colors[imgui.COLOR_SCROLLBAR_GRAB_ACTIVE] = (*ProjectorTheme.PRIMARY, 1.0)

        # Checkmark
        colors[imgui.COLOR_CHECK_MARK] = (*ProjectorTheme.PRIMARY, 1.0)

        # Slider
        colors[imgui.COLOR_SLIDER_GRAB] = (*ProjectorTheme.PRIMARY, 0.8)
        colors[imgui.COLOR_SLIDER_GRAB_ACTIVE] = (*ProjectorTheme.PRIMARY, 1.0)

        # Plot
        colors[imgui.COLOR_PLOT_LINES] = (*ProjectorTheme.PRIMARY, 1.0)
        colors[imgui.COLOR_PLOT_LINES_HOVERED] = (*ProjectorTheme.PRIMARY_GLOW, 1.0)
        colors[imgui.COLOR_PLOT_HISTOGRAM] = (*ProjectorTheme.PRIMARY, 0.7)
        colors[imgui.COLOR_PLOT_HISTOGRAM_HOVERED] = (*ProjectorTheme.PRIMARY_GLOW, 0.9)

        # Text selection
        colors[imgui.COLOR_TEXT_SELECTED_BACKGROUND] = (*ProjectorTheme.PRIMARY, 0.3)

        # Drag and drop
        colors[imgui.COLOR_DRAG_DROP_TARGET] = (*ProjectorTheme.PRIMARY_GLOW, 0.9)

        # Nav highlight (if available)
        try:
            colors[imgui.COLOR_NAV_HIGHLIGHT] = (*ProjectorTheme.PRIMARY, 1.0)
            colors[imgui.COLOR_NAV_WINDOWING_HIGHLIGHT] = (*ProjectorTheme.PRIMARY_GLOW, 0.7)
            colors[imgui.COLOR_NAV_WINDOWING_DIM_BACKGROUND] = (0.2, 0.2, 0.2, 0.2)
        except AttributeError:
            pass

        # Modal background (if available)
        try:
            colors[imgui.COLOR_MODAL_WINDOW_DIM_BACKGROUND] = (0.0, 0.0, 0.0, 0.6)
        except AttributeError:
            pass

        print("✅ HTML theme applied to ImGui")

    @staticmethod
    def push_primary_button():
        """Style for primary buttons (teal glow)"""
        imgui.push_style_color(imgui.COLOR_BUTTON, (*ProjectorTheme.PRIMARY, 0.3))
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, (*ProjectorTheme.PRIMARY, 0.5))
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, (*ProjectorTheme.PRIMARY, 0.7))
        imgui.push_style_color(imgui.COLOR_TEXT, (1.0, 1.0, 1.0, 1.0))

    @staticmethod
    def pop_primary_button():
        """Pop primary button style"""
        imgui.pop_style_color(4)

    @staticmethod
    def push_secondary_button():
        """Style for secondary buttons (muted)"""
        imgui.push_style_color(imgui.COLOR_BUTTON, (*ProjectorTheme.MUTED, 0.5))
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, (*ProjectorTheme.MUTED, 0.7))
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, (*ProjectorTheme.MUTED, 0.9))
        imgui.push_style_color(imgui.COLOR_TEXT, (*ProjectorTheme.MUTED_FOREGROUND, 1.0))

    @staticmethod
    def pop_secondary_button():
        """Pop secondary button style"""
        imgui.pop_style_color(4)

    @staticmethod
    def render_gizmo_button(label, is_active, tooltip=None):
        """Render a gizmo button matching HTML style"""
        if is_active:
            ProjectorTheme.push_primary_button()
        else:
            ProjectorTheme.push_secondary_button()

        clicked = imgui.button(label, 35, 28)

        if is_active:
            ProjectorTheme.pop_primary_button()
        else:
            ProjectorTheme.pop_secondary_button()

        if tooltip and imgui.is_item_hovered():
            imgui.set_tooltip(tooltip)

        return clicked
