#!/bin/bash

echo "======================================"
echo "StreamDiffusion Diagnostic Tool"
echo "======================================"
echo ""

# Check Python
echo "1. Checking Python..."
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version)
    echo "✓ Python found: $python_version"
else
    echo "✗ Python not found!"
    exit 1
fi

# Check pip
echo ""
echo "2. Checking pip..."
if command -v pip3 &> /dev/null; then
    pip_version=$(pip3 --version)
    echo "✓ pip found: $pip_version"
else
    echo "✗ pip not found!"
fi

# Check virtual environment
echo ""
echo "3. Checking virtual environment..."
if [ -d "venv" ]; then
    echo "✓ Virtual environment exists"
else
    echo "✗ Virtual environment not found"
    echo "  → Run: python3 -m venv venv"
fi

# Check CUDA/GPU
echo ""
echo "4. Checking GPU..."
if command -v nvidia-smi &> /dev/null; then
    echo "✓ NVIDIA GPU detected:"
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
else
    echo "⚠ No NVIDIA GPU detected (will use CPU - very slow)"
fi

# Check if packages are installed (if venv exists)
echo ""
echo "5. Checking Python packages..."
if [ -d "venv" ]; then
    source venv/bin/activate

    packages=("torch" "flask" "pillow" "numpy")
    all_installed=true

    for pkg in "${packages[@]}"; do
        if python3 -c "import $pkg" 2>/dev/null; then
            echo "✓ $pkg installed"
        else
            echo "✗ $pkg NOT installed"
            all_installed=false
        fi
    done

    # Check StreamDiffusion (optional)
    if python3 -c "import streamdiffusion" 2>/dev/null; then
        echo "✓ streamdiffusion installed"
    else
        echo "⚠ streamdiffusion NOT installed (optional - needed for full version)"
    fi

    deactivate
else
    echo "⚠ Cannot check packages - no virtual environment"
fi

# Check ports
echo ""
echo "6. Checking ports..."
for port in 5000 5001 5002; do
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1 || netstat -an 2>/dev/null | grep ":$port.*LISTEN" >/dev/null; then
        echo "⚠ Port $port is in use"
    else
        echo "✓ Port $port is available"
    fi
done

# Check backend files
echo ""
echo "7. Checking project files..."
files=("backend/stream_engine.py" "backend/server_txt2img.py" "backend/server_draw2img.py" "frontend/draw2img/index.html")
all_files_exist=true

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file exists"
    else
        echo "✗ $file missing"
        all_files_exist=false
    fi
done

echo ""
echo "======================================"
echo "Summary"
echo "======================================"
echo ""

if [ "$all_installed" = true ] && [ "$all_files_exist" = true ]; then
    echo "✓ System looks ready!"
    echo ""
    echo "To start the server:"
    echo "  ./run_draw2img.sh"
else
    echo "⚠ Issues detected. Please:"
    echo "  1. Run setup: ./setup.sh"
    echo "  2. Then try again"
fi

echo ""
