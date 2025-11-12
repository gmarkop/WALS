#!/bin/bash

# WALS Streamlit App Launcher

echo "=========================================="
echo "WALS Explorer - Streamlit App"
echo "=========================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.7 or higher from https://www.python.org/"
    exit 1
fi

# Navigate to app directory
cd "$(dirname "$0")/streamlit_app" || exit 1

# Check if requirements are installed
echo "Checking dependencies..."
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "Installing required packages..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install requirements."
        echo "Please run manually: pip install -r requirements.txt"
        exit 1
    fi
fi

echo ""
echo "Starting WALS Explorer..."
echo "The app will open in your browser automatically"
echo "Press Ctrl+C to stop the server"
echo ""
echo "=========================================="

# Run the application
streamlit run Home.py
