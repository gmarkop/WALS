@echo off
REM WALS Streamlit App Launcher for Windows

echo ==========================================
echo WALS Explorer - Streamlit App
echo ==========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.7 or higher from https://www.python.org/
    pause
    exit /b 1
)

REM Navigate to app directory
cd /d "%~dp0\streamlit_app"

REM Check if requirements are installed
echo Checking dependencies...
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install requirements.
        echo Please run manually: pip install -r requirements.txt
        pause
        exit /b 1
    )
)

echo.
echo Starting WALS Explorer...
echo The app will open in your browser automatically
echo Press Ctrl+C to stop the server
echo.
echo ==========================================
echo.

REM Run the application
streamlit run Home.py

pause
