@echo off
title SmartAgri AI Server Launcher
echo ===================================================
echo   SmartAgri AI — Launching Application Server
echo ===================================================
echo.
echo Checking Python environment...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    pause
    exit /b
)

echo.
echo Ensuring dependencies are installed...
pip install -r requirements.txt

echo.
echo Verifying ML Model...
if not exist "model\crop_model.pkl" (
    echo Model not found. Training model now...
    python training\train_model.py
)

echo.
echo Starting Flask Server...
echo Application will be available at: http://127.0.0.1:5000
echo Press Ctrl+C to stop the server.
echo.
python app.py
pause
