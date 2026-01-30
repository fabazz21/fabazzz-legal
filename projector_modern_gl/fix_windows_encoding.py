#!/usr/bin/env python3
"""
Fix Windows Console Encoding - Remove emojis
Windows console (cp1252) doesn't support Unicode emojis
This script replaces all emojis with simple text
"""

from pathlib import Path
import re

# Map emojis to text replacements
EMOJI_MAP = {
    '✅': '[OK]',
    '❌': '[ERROR]',
    '⚠️': '[WARNING]',
    '🎯': '[TARGET]',
    '📝': '[NOTE]',
    '🚀': '[LAUNCH]',
    '💾': '[SAVE]',
    '📊': '[STATS]',
    '🔧': '[FIX]',
    '⏱️': '[TIME]',
    '🔍': '[SEARCH]',
    '📄': '[FILE]',
    '🔴': '[REC]',
    '⏺️': '[STOP]',
    '▶️': '[PLAY]',
    '⏸️': '[PAUSE]',
    '⏹️': '[STOP]',
    '🗑️': '[DELETE]',
    '🔄': '[RESET]',
    '📦': '[PACKAGE]',
    '💡': '[TIP]',
    '⚪': '[CIRCLE]',
    '🧊': '[CUBE]',
    '📽️': '[PROJECTOR]',
    '💡': '[LIGHT]',
}

def fix_file(filepath):
    """Remove emojis from a Python file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # Replace each emoji
        for emoji, replacement in EMOJI_MAP.items():
            if emoji in content:
                content = content.replace(emoji, replacement)

        # If changed, write back
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Fixed: {filepath}")
            return True

        return False

    except Exception as e:
        print(f"  Error fixing {filepath}: {e}")
        return False

def main():
    print("="*70)
    print("FIX WINDOWS CONSOLE ENCODING - REMOVE EMOJIS")
    print("="*70)
    print()
    print("Windows console uses cp1252 encoding which doesn't support")
    print("Unicode emojis. This script replaces them with [TEXT].")
    print()

    # Find all Python files
    python_files = list(Path('.').rglob('*.py'))

    # Filter out virtual environments and cache
    python_files = [
        f for f in python_files
        if 'venv' not in str(f) and '__pycache__' not in str(f)
    ]

    print(f"Found {len(python_files)} Python files to check...")
    print()

    fixed_count = 0

    for py_file in python_files:
        if fix_file(py_file):
            fixed_count += 1

    print()
    print("="*70)
    if fixed_count > 0:
        print(f"[OK] Fixed {fixed_count} files!")
        print()
        print("Now run: py -3.11 main.py")
    else:
        print("[OK] No files needed fixing (or already fixed)")
    print("="*70)

if __name__ == "__main__":
    main()
