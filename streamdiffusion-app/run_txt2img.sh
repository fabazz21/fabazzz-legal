#!/bin/bash

# Quick start script for Text-to-Image server

echo "Starting StreamDiffusion Text-to-Image Server..."
echo ""

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Error: Virtual environment not found."
    echo "Please run setup.sh first."
    exit 1
fi

# Start server
cd backend
python server_txt2img.py
