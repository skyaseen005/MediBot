#!/bin/bash

# MediBot Quick Start Script
# This script provides a quick way to run the MediBot application

echo "╔════════════════════════════════════════╗"
echo "║        MediBot Quick Start             ║"
echo "║    AI Medical Chatbot                  ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python
if ! command_exists python3; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✓ Python 3 found"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "⚠️  Virtual environment not found"
    echo "Would you like to run the setup script? (y/n)"
    read -r response
    if [ "$response" = "y" ]; then
        python3 setup.py
        exit 0
    fi
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  .env file not found"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✓ Created .env file from template"
        echo "You may want to edit .env with your configurations"
    fi
fi

echo ""
echo "Select server to run:"
echo "1) FastAPI (Recommended - Port 8000)"
echo "2) Flask (Port 5000)"
echo ""
read -p "Enter choice (1 or 2): " choice

# Activate virtual environment
if [ -d "venv" ]; then
    echo ""
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

case $choice in
    1)
        echo ""
        echo "🚀 Starting FastAPI server..."
        echo "API Documentation: http://localhost:8000/docs"
        echo "Health Check: http://localhost:8000/health"
        echo ""
        cd backend && python fastapi_server.py
        ;;
    2)
        echo ""
        echo "🚀 Starting Flask server..."
        echo "API URL: http://localhost:5000"
        echo "Health Check: http://localhost:5000/health"
        echo ""
        cd backend && python flask_server.py
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
