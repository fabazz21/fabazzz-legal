@echo off
echo ======================================
echo StreamDiffusion App Setup (Windows)
echo ======================================
echo.

REM Check Python version
echo Checking Python version...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.10 or higher.
    pause
    exit /b 1
)

REM Check for CUDA
echo.
echo Checking for CUDA...
nvidia-smi >nul 2>&1
if %errorlevel% equ 0 (
    echo NVIDIA GPU detected:
    nvidia-smi --query-gpu=name --format=csv,noheader
) else (
    echo WARNING: No NVIDIA GPU detected. The app will run on CPU and be very slow.
    echo For best performance, use a system with CUDA-capable GPU.
)

REM Create virtual environment
echo.
echo Creating Python virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install PyTorch
echo.
echo Installing PyTorch...
nvidia-smi >nul 2>&1
if %errorlevel% equ 0 (
    echo Installing PyTorch with CUDA 11.8 support...
    pip install torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cu118
) else (
    echo Installing PyTorch CPU version...
    pip install torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cpu
)

REM Install dependencies
echo.
echo Installing StreamDiffusion and dependencies...
cd backend
pip install -r requirements.txt

echo.
echo ======================================
echo Setup Complete!
echo ======================================
echo.
echo To start the applications:
echo.
echo 1. Text-to-Image:
echo    venv\Scripts\activate
echo    cd backend
echo    python server_txt2img.py
echo    Then open http://localhost:5000 in your browser
echo.
echo 2. Image-to-Image (Webcam):
echo    venv\Scripts\activate
echo    cd backend
echo    python server_img2img.py
echo    Then open http://localhost:5001 in your browser
echo.
echo Note: First run will download AI models (~2-3 GB)
echo ======================================
pause
