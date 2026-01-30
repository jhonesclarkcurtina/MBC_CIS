@echo off
REM Church Information System - Windows Startup Script
REM This script will start the Flask application

cls
echo.
echo ============================================
echo   Church Information System (CIS)
echo   Startup Script
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

echo [OK] Python is installed
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
    echo.
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

REM Check if requirements are installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing requirements...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install requirements
        pause
        exit /b 1
    )
    echo [OK] Requirements installed
    echo.
) else (
    echo [OK] Requirements already installed
    echo.
)

REM Start the application
echo [INFO] Starting Church Information System...
echo.
echo ============================================
echo   Application Started!
echo ============================================
echo.
echo Access the application at:
echo   http://localhost:5000
echo.
echo Default credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo Press Ctrl+C to stop the server
echo.
echo ============================================
echo.

python run.py

pause
