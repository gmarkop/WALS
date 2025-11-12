@echo off
REM WALS Local Explorer Launcher Script for Windows

echo ==========================================
echo WALS Local Explorer
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

REM Show Python version
python --version

REM Navigate to app directory
cd /d "%~dp0\wals_app"

REM Check if requirements are installed
echo Checking dependencies...
python -c "import flask" >nul 2>&1
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
echo Starting WALS Local Explorer...
echo Open your browser and go to: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
echo ==========================================
echo.

REM Run the application
python app.py

pause
