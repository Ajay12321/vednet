#!/usr/bin/env python3
"""
Cog AI Assistant Launcher
Simple launcher script that handles missing dependencies gracefully
"""

import sys
import os
import subprocess

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'speech_recognition',
        'pyttsx3',
        'tkinter'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'tkinter':
                import tkinter
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies(packages):
    """Install missing dependencies"""
    print("Installing missing dependencies...")
    for package in packages:
        try:
            if package == 'tkinter':
                print("Note: tkinter is usually included with Python. If missing, install python3-tk")
                continue
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✓ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {package}")

def main():
    """Main launcher function"""
    print("🤖 Cog AI Assistant Launcher")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    
    print(f"✓ Python version: {sys.version.split()[0]}")
    
    # Check dependencies
    missing = check_dependencies()
    
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        
        # Ask user if they want to install
        try:
            install = input("Would you like to install missing dependencies? (y/n): ").lower()
            if install in ['y', 'yes']:
                install_dependencies(missing)
            else:
                print("Cannot proceed without required dependencies.")
                sys.exit(1)
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            sys.exit(1)
    else:
        print("✓ All dependencies are available")
    
    # Set up environment
    print("\n🚀 Starting Cog AI Assistant...")
    
    # Add current directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # Start the agent
    try:
        from cog_agent import main as cog_main
        cog_main()
    except ImportError as e:
        print(f"❌ Error importing Cog agent: {e}")
        print("Please ensure all files are in the correct location.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Cog AI Assistant stopped.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("Check cog_agent.log for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()