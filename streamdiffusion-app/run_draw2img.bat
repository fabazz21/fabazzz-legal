@echo off
echo Starting StreamDiffusion Drawing-to-Image Server...
echo.

if exist venv (
    call venv\Scripts\activate.bat
    cd backend
    python server_draw2img.py
) else (
    echo Error: Virtual environment not found.
    echo Please run setup.bat first.
    pause
)
