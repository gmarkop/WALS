#!/bin/bash

# WALS Local Explorer Launcher Script

echo "=========================================="
echo "WALS Local Explorer"
echo "=========================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.7 or higher from https://www.python.org/"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"

# Navigate to app directory
cd "$(dirname "$0")/wals_app" || exit 1

# Check if requirements are installed
echo "Checking dependencies..."
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installing required packages..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install requirements."
        echo "Please run manually: pip install -r requirements.txt"
        exit 1
    fi
fi

echo ""
echo "Starting WALS Local Explorer..."
echo "Open your browser and go to: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""
echo "=========================================="

# Run the application
python3 app.py
