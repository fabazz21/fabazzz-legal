@echo off
echo Starting StreamDiffusion Text-to-Image Server...
echo.

if exist venv (
    call venv\Scripts\activate.bat
    cd backend
    python server_txt2img.py
) else (
    echo Error: Virtual environment not found.
    echo Please run setup.bat first.
    pause
)
