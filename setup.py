#!/usr/bin/env python3
"""
MediBot Setup Script
Automates the setup process for the MediBot application
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"→ {description}...")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True,
            capture_output=True,
            text=True
        )
        print(f"  ✓ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Error: {e}")
        print(f"  Output: {e.stdout}")
        print(f"  Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("✗ Python 3.8 or higher is required!")
        return False
    
    print("✓ Python version is compatible")
    return True

def check_mongodb():
    """Check if MongoDB is accessible"""
    print_header("Checking MongoDB")
    try:
        import pymongo
        client = pymongo.MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
        client.server_info()
        print("✓ MongoDB is running locally")
        return True
    except Exception as e:
        print("⚠ MongoDB not accessible locally")
        print("  You can either:")
        print("  1. Install MongoDB locally")
        print("  2. Use MongoDB Atlas (free cloud database)")
        print("  3. Continue without MongoDB (limited functionality)")
        return False

def create_virtual_environment():
    """Create and activate virtual environment"""
    print_header("Setting Up Virtual Environment")
    
    venv_path = Path("venv")
    if venv_path.exists():
        print("⚠ Virtual environment already exists")
        response = input("Do you want to recreate it? (y/n): ").lower()
        if response == 'y':
            shutil.rmtree(venv_path)
        else:
            print("Using existing virtual environment")
            return True
    
    if run_command("python -m venv venv", "Creating virtual environment"):
        print("\n✓ Virtual environment created successfully")
        print("\nTo activate:")
        print("  - Linux/Mac: source venv/bin/activate")
        print("  - Windows: venv\\Scripts\\activate")
        return True
    return False

def install_dependencies():
    """Install required Python packages"""
    print_header("Installing Dependencies")
    
    # Determine pip command
    if sys.platform == "win32":
        pip_cmd = "venv\\Scripts\\pip"
    else:
        pip_cmd = "venv/bin/pip"
    
    # Check if venv exists
    if not Path("venv").exists():
        print("⚠ Virtual environment not found. Installing globally...")
        pip_cmd = "pip"
    
    commands = [
        (f"{pip_cmd} install --upgrade pip", "Upgrading pip"),
        (f"{pip_cmd} install -r requirements.txt", "Installing requirements"),
    ]
    
    for cmd, desc in commands:
        if not run_command(cmd, desc):
            return False
    
    print("\n✓ All dependencies installed successfully")
    return True

def setup_environment_file():
    """Create .env file from template"""
    print_header("Setting Up Environment File")
    
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if env_path.exists():
        print("⚠ .env file already exists")
        response = input("Do you want to overwrite it? (y/n): ").lower()
        if response != 'y':
            print("Keeping existing .env file")
            return True
    
    if env_example_path.exists():
        shutil.copy(env_example_path, env_path)
        print("✓ Created .env file from template")
        print("\n⚠ Please edit .env file with your configurations:")
        print("  - MongoDB connection string")
        print("  - API keys (optional)")
        return True
    else:
        print("✗ .env.example file not found")
        return False

def download_models():
    """Download required NLP models"""
    print_header("Downloading NLP Models")
    
    print("Downloading Sentence Transformer model...")
    print("(This may take a few minutes on first run)")
    
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        print("✓ Model downloaded successfully")
        return True
    except Exception as e:
        print(f"⚠ Could not download model: {e}")
        print("  Model will be downloaded on first use")
        return True

def initialize_database():
    """Initialize MongoDB with medical knowledge"""
    print_header("Initializing Database")
    
    try:
        from backend.database import MediBotDB
        import json
        
        db = MediBotDB()
        knowledge_path = Path("data/medical_knowledge.json")
        
        if knowledge_path.exists():
            with open(knowledge_path, 'r') as f:
                data = json.load(f)
            
            db.initialize_knowledge_base(str(knowledge_path))
            print(f"✓ Loaded {len(data)} medical conditions into database")
            return True
        else:
            print("⚠ Medical knowledge file not found")
            return False
    except Exception as e:
        print(f"⚠ Could not initialize database: {e}")
        print("  Database will be initialized on first server start")
        return True

def run_tests():
    """Run basic tests"""
    print_header("Running Tests")
    
    print("Testing imports...")
    try:
        import fastapi
        import flask
        import pymongo
        import sentence_transformers
        import langchain
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def print_next_steps():
    """Print next steps for user"""
    print_header("Setup Complete! 🎉")
    
    print("Next steps:")
    print("\n1. Activate virtual environment:")
    print("   - Linux/Mac: source venv/bin/activate")
    print("   - Windows: venv\\Scripts\\activate")
    
    print("\n2. Configure .env file with your settings")
    
    print("\n3. Start the server:")
    print("   - FastAPI: python backend/fastapi_server.py")
    print("   - Flask: python backend/flask_server.py")
    
    print("\n4. Open the frontend:")
    print("   - Open frontend/index.html in your browser")
    print("   - Or serve it: python -m http.server 3000 (from frontend folder)")
    
    print("\n5. Test the API:")
    print("   - Visit: http://localhost:8000/docs (FastAPI)")
    print("   - Or: http://localhost:5000 (Flask)")
    
    print("\n📚 For more information, see README.md")
    print("\n💡 Quick start: Run 'python backend/fastapi_server.py' after activating venv")

def main():
    """Main setup function"""
    print("""
    ╔════════════════════════════════════════╗
    ║        MediBot Setup Script            ║
    ║    AI Medical Chatbot Installation     ║
    ╚════════════════════════════════════════╝
    """)
    
    steps = [
        ("Checking Python version", check_python_version),
        ("Checking MongoDB", check_mongodb),
        ("Creating virtual environment", create_virtual_environment),
        ("Installing dependencies", install_dependencies),
        ("Setting up environment file", setup_environment_file),
        ("Downloading NLP models", download_models),
        ("Running tests", run_tests),
    ]
    
    results = []
    for step_name, step_func in steps:
        try:
            result = step_func()
            results.append((step_name, result))
        except Exception as e:
            print(f"\n✗ Error in {step_name}: {e}")
            results.append((step_name, False))
    
    # Print summary
    print_header("Setup Summary")
    for step_name, result in results:
        status = "✓" if result else "✗"
        print(f"{status} {step_name}")
    
    # Print next steps if setup was successful
    if all(result for _, result in results[:-2]):  # Ignore MongoDB and tests for success
        print_next_steps()
    else:
        print("\n⚠ Some steps failed. Please review the errors above.")
        print("You can still proceed, but some features may not work correctly.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)
