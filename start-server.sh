#!/bin/bash

echo "================================================"
echo "   🎨 AI Drawing to Art Server"
echo "================================================"
echo ""

# Check if server.py exists
if [ ! -f "server.py" ]; then
    echo "❌ Error: server.py not found!"
    echo "Make sure you're running this from the app directory."
    exit 1
fi

# Try to run with Python 3
if command -v python3 &> /dev/null; then
    echo "✅ Starting server with Python 3..."
    echo ""
    python3 server.py
elif command -v python &> /dev/null; then
    echo "✅ Starting server with Python..."
    echo ""
    python server.py
else
    echo "❌ Error: Python is not installed!"
    echo ""
    echo "Please install Python from:"
    echo "  https://www.python.org/downloads/"
    echo ""
    echo "After installation, run this script again."
    exit 1
fi
