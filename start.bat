@echo off
REM MediBot Quick Start Script for Windows

echo ========================================
echo        MediBot Quick Start
echo    AI Medical Chatbot
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed
    pause
    exit /b 1
)

echo [OK] Python found

REM Check if virtual environment exists
if not exist "venv\" (
    echo.
    echo [WARNING] Virtual environment not found
    echo Would you like to run the setup script? (Y/N)
    set /p response=
    if /i "%response%"=="Y" (
        python setup.py
        exit /b 0
    )
)

REM Check if .env exists
if not exist ".env" (
    echo.
    echo [WARNING] .env file not found
    if exist ".env.example" (
        copy .env.example .env
        echo [OK] Created .env file from template
        echo You may want to edit .env with your configurations
    )
)

echo.
echo Select server to run:
echo 1) FastAPI (Recommended - Port 8000)
echo 2) Flask (Port 5000)
echo.
set /p choice=Enter choice (1 or 2): 

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    echo.
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

if "%choice%"=="1" (
    echo.
    echo Starting FastAPI server...
    echo API Documentation: http://localhost:8000/docs
    echo Health Check: http://localhost:8000/health
    echo.
    cd backend
    python fastapi_server.py
) else if "%choice%"=="2" (
    echo.
    echo Starting Flask server...
    echo API URL: http://localhost:5000
    echo Health Check: http://localhost:5000/health
    echo.
    cd backend
    python flask_server.py
) else (
    echo Invalid choice. Exiting.
    pause
    exit /b 1
)
