#!/usr/bin/env python3
"""
Download latest Python files from GitHub
"""
import urllib.request
import os
from pathlib import Path

# Base URL
BASE_URL = "https://raw.githubusercontent.com/fabazz21/fabazzz-legal/claude/modern-opengl-ut5JW/projector_modern_gl"

# Files to download
FILES = [
    "ui/panels/photometric_panel.py",
    "ui/panels/export_panel.py",
    "ui/panels/timeline_panel.py",
    "ui/panels/projector_panel.py",
    "ui/panels/properties_panel.py",
    "ui/panels/scene_panel.py",
    "ui/panels/viewport_panel.py",
    "ui/main_ui_tabbed.py",
    "ui/theme.py",
    "main.py",
    "fix_panels.py",
    "test_all_errors.py",
    "test_html_functions.py"
]

def download_file(url, output_path):
    """Download a file from URL to output_path"""
    # Create directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"📥 Downloading {output_path.name}...")
    try:
        urllib.request.urlretrieve(url, output_path)
        print(f"   ✅ {output_path}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def main():
    print("🚀 Downloading latest Python files from GitHub...\n")

    # Get current directory
    base_dir = Path.cwd()

    for file_path in FILES:
        url = f"{BASE_URL}/{file_path}"
        output = base_dir / file_path
        download_file(url, output)

    print("\n✅ Tous les fichiers téléchargés!")
    print(f"📂 Location: {base_dir}")

if __name__ == "__main__":
    main()
