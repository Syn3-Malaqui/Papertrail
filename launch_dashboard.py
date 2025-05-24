"""
Dashboard Launcher for Papertrail
Simple script to launch the Streamlit dashboard with optimal settings.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Check if required packages are installed."""
    required_packages = ['streamlit', 'plotly', 'pandas']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Install missing packages with:")
        print("   pip install streamlit plotly pandas")
        print("   or")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def launch_dashboard():
    """Launch the Streamlit dashboard."""
    dashboard_path = Path("dashboard.py")
    
    if not dashboard_path.exists():
        print("❌ Dashboard file not found: dashboard.py")
        return False
    
    print("🚀 Launching Papertrail Dashboard...")
    print("📊 The dashboard will open in your default web browser")
    print("🔗 URL: http://localhost:8501")
    print("\n⏹️  Press Ctrl+C to stop the dashboard")
    print("=" * 50)
    
    try:
        # Launch Streamlit with optimal settings
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(dashboard_path),
            "--server.port=8501",
            "--server.address=localhost",
            "--browser.gatherUsageStats=false",
            "--theme.base=light"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("📄 Papertrail Dashboard Launcher")
    print("=" * 40)
    
    # Check if we have classification results
    csv_files = list(Path(".").glob("*classification_results*.csv"))
    if not csv_files:
        print("⚠️  No classification results found!")
        print("💡 Run classification first: python main.py diverse_sample_documents")
        print()
        
        # Ask if user wants to continue anyway
        response = input("Continue launching dashboard anyway? (y/n): ").lower()
        if response != 'y':
            print("Exiting...")
            sys.exit(0)
    else:
        latest_file = max(csv_files, key=os.path.getctime)
        print(f"✅ Found classification results: {latest_file}")
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Launch dashboard
    success = launch_dashboard()
    sys.exit(0 if success else 1) 