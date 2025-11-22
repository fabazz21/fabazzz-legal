#!/bin/bash

echo "======================================"
echo "StreamDiffusion App Setup"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Check for CUDA
echo ""
echo "Checking for CUDA..."
if command -v nvidia-smi &> /dev/null; then
    echo "NVIDIA GPU detected:"
    nvidia-smi --query-gpu=name --format=csv,noheader
else
    echo "WARNING: No NVIDIA GPU detected. The app will run on CPU and be very slow."
    echo "For best performance, use a system with CUDA-capable GPU."
fi

# Create virtual environment
echo ""
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install PyTorch (with CUDA if available)
echo ""
echo "Installing PyTorch..."
if command -v nvidia-smi &> /dev/null; then
    echo "Installing PyTorch with CUDA 11.8 support..."
    pip install torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cu118
else
    echo "Installing PyTorch CPU version..."
    pip install torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cpu
fi

# Install StreamDiffusion and dependencies
echo ""
echo "Installing StreamDiffusion and dependencies..."
cd backend
pip install -r requirements.txt

# Install optional dependencies
echo ""
read -p "Do you want to install xformers for memory-efficient attention? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    pip install xformers
fi

echo ""
echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "To start the applications:"
echo ""
echo "1. Text-to-Image:"
echo "   source venv/bin/activate"
echo "   cd backend"
echo "   python server_txt2img.py"
echo "   Then open http://localhost:5000 in your browser"
echo ""
echo "2. Image-to-Image (Webcam):"
echo "   source venv/bin/activate"
echo "   cd backend"
echo "   python server_img2img.py"
echo "   Then open http://localhost:5001 in your browser"
echo ""
echo "Note: First run will download AI models (~2-3 GB)"
echo "======================================"
