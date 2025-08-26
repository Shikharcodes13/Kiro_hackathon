#!/usr/bin/env python3
"""
Full-stack startup script for AutoAgent platform
Starts both backend (FastAPI) and frontend (React) servers
"""

import subprocess
import sys
import os
import time
import threading
from pathlib import Path

def run_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting FastAPI backend server...")
    try:
        # Change to root directory
        os.chdir(Path(__file__).parent)
        
        # Start FastAPI server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Backend server failed: {e}")
    except KeyboardInterrupt:
        print("🛑 Backend server stopped")

def run_frontend():
    """Start the React frontend server"""
    print("🎨 Starting React frontend server...")
    try:
        # Change to frontend directory
        frontend_dir = Path(__file__).parent / "frontend"
        os.chdir(frontend_dir)
        
        # Check if node_modules exists
        if not (frontend_dir / "node_modules").exists():
            print("📦 Installing frontend dependencies...")
            subprocess.run(["npm", "install"], check=True)
        
        # Start React development server
        subprocess.run(["npm", "start"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Frontend server failed: {e}")
        print("Make sure Node.js and npm are installed")
    except KeyboardInterrupt:
        print("🛑 Frontend server stopped")

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python dependencies
    try:
        import fastapi
        import uvicorn
        print("✅ Python dependencies found")
    except ImportError:
        print("❌ Python dependencies missing. Run: pip install -r requirements.txt")
        return False
    
    # Check Node.js
    try:
        subprocess.run(["node", "--version"], check=True, capture_output=True)
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
        print("✅ Node.js and npm found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js or npm not found. Please install Node.js from https://nodejs.org/")
        return False
    
    return True

def main():
    """Main function to start both servers"""
    print("🚗 AutoAgent Full-Stack Startup")
    print("=" * 40)
    
    if not check_dependencies():
        print("\n❌ Dependency check failed. Please install missing dependencies.")
        sys.exit(1)
    
    print("\n🚀 Starting servers...")
    print("Backend will be available at: http://localhost:8000")
    print("Frontend will be available at: http://localhost:3000")
    print("\nPress Ctrl+C to stop both servers\n")
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Give backend time to start
    time.sleep(3)
    
    try:
        # Start frontend in main thread
        run_frontend()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()