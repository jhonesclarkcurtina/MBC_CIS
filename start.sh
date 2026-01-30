#!/bin/bash

# Church Information System - Unix/Mac Startup Script
# This script will start the Flask application

clear
echo ""
echo "============================================"
echo "  Church Information System (CIS)"
echo "  Startup Script"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ from https://www.python.org"
    exit 1
fi

python3 --version
echo "[OK] Python is installed"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[INFO] Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment"
        exit 1
    fi
    echo "[OK] Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "[INFO] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate virtual environment"
    exit 1
fi
echo "[OK] Virtual environment activated"
echo ""

# Check if requirements are installed
python -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[INFO] Installing requirements..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install requirements"
        exit 1
    fi
    echo "[OK] Requirements installed"
    echo ""
else
    echo "[OK] Requirements already installed"
    echo ""
fi

# Start the application
echo "[INFO] Starting Church Information System..."
echo ""
echo "============================================"
echo "  Application Started!"
echo "============================================"
echo ""
echo "Access the application at:"
echo "  http://localhost:5000"
echo ""
echo "Default credentials:"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "============================================"
echo ""

python run.py
