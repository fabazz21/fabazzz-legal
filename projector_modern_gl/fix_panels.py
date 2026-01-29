#!/usr/bin/env python3
"""
Quick script to add render_content() method to all panels
"""

import re
from pathlib import Path

panels_dir = Path("/home/user/fabazzz-legal/projector_modern_gl/ui/panels")

files_to_fix = [
    "projector_panel.py",
    "viewport_panel.py",
    "timeline_panel.py",
    "export_panel.py",
    "photometric_panel.py"
]

for filename in files_to_fix:
    filepath = panels_dir / filename

    if not filepath.exists():
        print(f"⚠️  {filename} not found")
        continue

    content = filepath.read_text()

    # Check if render_content already exists
    if "def render_content(self)" in content:
        print(f"✅ {filename} already has render_content()")
        continue

    # Find the render method
    # Pattern: def render(self): ... imgui.begin(...) ... if expanded: CONTENT ... imgui.end()

    # Simple approach: Add render_content() stub
    # Find the line after "if expanded:"
    lines = content.split('\n')
    new_lines = []
    in_render = False
    indent_level = 0
    content_lines = []
    found_if_expanded = False

    for i, line in enumerate(lines):
        new_lines.append(line)

        if "def render(self):" in line:
            in_render = True

        if in_render and "if expanded:" in line and "imgui.begin" in '\n'.join(lines[max(0, i-5):i]):
            found_if_expanded = True
            # Replace everything after "if expanded:" until "imgui.end()" with render_content()
            # Find indent
            indent = len(line) - len(line.lstrip())
            new_lines.pop()  # Remove the "if expanded:" line
            new_lines.append(line)  # Add it back
            new_lines.append(" " * (indent + 4) + "self.render_content()")
            new_lines.append("")

            # Skip until imgui.end() and note content
            j = i + 1
            content_start = j
            while j < len(lines):
                if "imgui.end()" in lines[j]:
                    content_lines = lines[content_start:j]
                    # Skip these lines
                    for k in range(content_start, j):
                        lines[k] = "###SKIP###"
                    break
                j += 1

    # Remove skipped lines
    new_lines = [l for l in new_lines if l != "###SKIP###"]

    # Add render_content method before last few lines
    # Find a good place (before _render_* private methods or at end)
    insert_pos = len(new_lines) - 1
    for i in range(len(new_lines) - 1, -1, -1):
        if new_lines[i].strip().startswith("def _"):
            insert_pos = i
            break

    render_content_method = [
        "",
        "    def render_content(self):",
        "        \"\"\"Render panel content (without window wrapper)\"\"\"",
    ] + ["        " + line[8:] if line.startswith("        ") else line for line in content_lines] + [
        ""
    ]

    if content_lines:
        new_lines = new_lines[:insert_pos] + render_content_method + new_lines[insert_pos:]

        filepath.write_text('\n'.join(new_lines))
        print(f"✅ {filename} - Added render_content()")
    else:
        # Simpler approach - just add empty stub
        lines = content.split('\n')

        # Find def render(self): and modify it
        for i, line in enumerate(lines):
            if "def render(self):" in line:
                # Find "if expanded:" after this
                for j in range(i, min(i+15, len(lines))):
                    if "if expanded:" in lines[j]:
                        # Add render_content() call
                        indent = len(lines[j]) - len(lines[j].lstrip())
                        lines[j] = lines[j] + "\n" + " " * (indent + 4) + "self.render_content()"
                        break
                break

        # Add stub method at end
        lines.append("")
        lines.append("    def render_content(self):")
        lines.append("        \"\"\"Render panel content (without window wrapper)\"\"\"")
        lines.append("        imgui.text('Panel content here')")

        filepath.write_text('\n'.join(lines))
        print(f"✅ {filename} - Added render_content() stub")

print("\n✅ All panels updated!")
