#!/usr/bin/env python3
"""
Simple launcher for Papertrail Dashboard
"""

import subprocess
import sys
import webbrowser
import time
from threading import Timer

def open_browser():
    """Open browser after a short delay to allow server to start."""
    time.sleep(3)
    webbrowser.open('http://localhost:8501')

if __name__ == "__main__":
    print("🚀 Launching Papertrail Interactive Dashboard...")
    print("🌐 Opening browser automatically...")
    
    # Start browser opener in background
    Timer(3.0, open_browser).start()
    
    # Launch Streamlit
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py"])
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped. Thank you for using Papertrail!")
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")
        print("💡 Try running manually: streamlit run dashboard.py") 