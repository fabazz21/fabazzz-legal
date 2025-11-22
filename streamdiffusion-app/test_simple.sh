#!/bin/bash

echo "======================================"
echo "Testing Simple Drawing Server"
echo "======================================"
echo ""
echo "This runs a SIMPLIFIED version without AI"
echo "Just to test if the basic setup works!"
echo ""

# Check if we're in the right directory
if [ ! -f "backend/server_draw2img_simple.py" ]; then
    echo "Error: Please run from streamdiffusion-app directory"
    exit 1
fi

# Install minimal requirements
echo "Installing minimal requirements..."
pip3 install flask flask-cors pillow --quiet

echo ""
echo "Starting simple test server..."
echo "Open http://localhost:5002 in your browser"
echo ""
echo "Press Ctrl+C to stop"
echo ""

cd backend
python3 server_draw2img_simple.py
