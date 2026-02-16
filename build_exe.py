"""
Build script to create executable from the application
"""

import PyInstaller.__main__
import os
import sys

def build_exe():
    """Build the executable"""
    print("Building AI Call Assistant executable...")
    
    # PyInstaller arguments
    args = [
        'main.py',
        '--name=AI-Call-Assistant',
        '--onefile',
        '--windowed',  # No console window
        '--icon=NONE',  # Add icon file path here if you have one
        '--add-data=requirements.txt;.',  # Include requirements if needed
        '--hidden-import=win32timezone',
        '--hidden-import=win32api',
        '--hidden-import=win32con',
        '--hidden-import=win32com',
        '--collect-all=win32com',
        '--noconfirm',  # Overwrite output without asking
    ]
    
    try:
        PyInstaller.__main__.run(args)
        print("\n✓ Build completed successfully!")
        print("Executable location: dist/AI-Call-Assistant.exe")
    except Exception as e:
        print(f"\n✗ Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()

