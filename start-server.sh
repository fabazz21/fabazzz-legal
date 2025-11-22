#!/bin/bash

echo "🎨 Starting AI Drawing to Art Server..."
echo ""
echo "This will start a local web server on port 8000"
echo "Open your browser to: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================================"
echo ""

# Try different methods to start server
if command -v python3 &> /dev/null; then
    echo "Using Python 3..."
    python3 -m http.server 8000
elif command -v python &> /dev/null; then
    echo "Using Python..."
    python -m http.server 8000
elif command -v php &> /dev/null; then
    echo "Using PHP..."
    php -S localhost:8000
elif command -v npx &> /dev/null; then
    echo "Using Node.js..."
    npx http-server -p 8000
else
    echo "❌ Error: No suitable server found!"
    echo ""
    echo "Please install one of the following:"
    echo "  - Python: https://www.python.org/downloads/"
    echo "  - Node.js: https://nodejs.org/"
    echo "  - PHP: https://www.php.net/downloads"
    exit 1
fi
