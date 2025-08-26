#!/usr/bin/env python3
"""
Setup script for AutoAgent LangChain platform
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def create_env_file():
    """Create .env file template"""
    env_content = """# AutoAgent Environment Configuration

# OpenAI API Key (required for LangChain features)
# Get your API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Customize LLM model
LLM_MODEL=gpt-3.5-turbo

# Optional: Enable debug mode
DEBUG=false

# Optional: Custom port for FastAPI server
PORT=8000
"""
    
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write(env_content)
        print("✅ Created .env file template")
        print("   Please edit .env and add your OpenAI API key")
    else:
        print("⚠️  .env file already exists")

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def main():
    """Main setup function"""
    print("🚗 AutoAgent LangChain Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("⚠️  Some packages failed to install. You can try manually:")
        print("   pip install -r requirements.txt")
    
    # Create environment file
    create_env_file()
    
    print("\n🎉 Setup completed!")
    print("\nNext steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Run the demo: python demo_langchain.py")
    print("3. Start the server: python main.py")
    print("4. Visit http://localhost:8000 for the API")

if __name__ == "__main__":
    main()