#!/usr/bin/env python3
"""
System Startup Script
Launches the complete AI-Enhanced Stock Analysis System
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def check_requirements():
    """
    Check if required packages are installed
    """
    required_packages = [
        'yfinance', 'pandas', 'numpy', 'scikit-learn', 
        'fastapi', 'uvicorn', 'matplotlib', 'seaborn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Please install them using:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def setup_directories():
    """
    Create necessary directories
    """
    directories = [
        'enhanced_data',
        'models',
        'analysis_results',
        'dashboard',
        'logs'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"📁 Created directory: {directory}")

def run_initial_data_fetch():
    """
    Run the initial data fetching and model training
    """
    print("\n🔄 Running initial data fetch and model training...")
    print("This may take a few minutes...")
    
    try:
        result = subprocess.run(
            [sys.executable, 'enhanced_fetch_data.py'], 
            capture_output=True, 
            text=True,
            timeout=600  # 10 minutes timeout
        )
        
        if result.returncode == 0:
            print("✅ Initial data fetch completed successfully!")
            return True
        else:
            print(f"❌ Error in data fetch: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Data fetch timed out. You can run it manually later.")
        return False
    except Exception as e:
        print(f"❌ Error running data fetch: {e}")
        return False

def start_api_server():
    """
    Start the FastAPI server
    """
    print("\n🚀 Starting API server...")
    
    try:
        # Start the server in a separate process
        server_process = subprocess.Popen(
            [sys.executable, 'api_server.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a bit for server to start
        time.sleep(3)
        
        # Check if server is running
        if server_process.poll() is None:
            print("✅ API server started successfully!")
            print("📡 Server running at: http://localhost:8000")
            return server_process
        else:
            print("❌ Failed to start API server")
            return None
            
    except Exception as e:
        print(f"❌ Error starting API server: {e}")
        return None

def open_dashboard():
    """
    Open the dashboard in the default web browser
    """
    print("\n🌐 Opening dashboard in browser...")
    
    try:
        webbrowser.open('http://localhost:8000')
        print("✅ Dashboard opened in browser!")
    except Exception as e:
        print(f"❌ Could not open browser: {e}")
        print("Please manually open: http://localhost:8000")

def main():
    """
    Main function to start the entire system
    """
    print("🚀 AI-Enhanced Stock Analysis System Startup")
    print("=" * 50)
    
    # Check requirements
    print("\n1. Checking requirements...")
    if not check_requirements():
        sys.exit(1)
    print("✅ All requirements satisfied!")
    
    # Setup directories
    print("\n2. Setting up directories...")
    setup_directories()
    
    # Ask user if they want to run initial data fetch
    print("\n3. Initial data setup...")
    if os.path.exists('enhanced_data') and os.listdir('enhanced_data'):
        print("📊 Existing data found. Skipping initial fetch.")
        print("💡 Run 'python enhanced_fetch_data.py' to refresh data.")
    else:
        response = input("Run initial data fetch? This may take several minutes. (y/n): ")
        if response.lower().startswith('y'):
            success = run_initial_data_fetch()
            if not success:
                print("⚠️  Continuing without initial data. You can fetch data later.")
        else:
            print("⚠️  Skipping initial data fetch. Dashboard will use sample data.")
    
    # Start API server
    print("\n4. Starting system...")
    server_process = start_api_server()
    
    if server_process:
        # Wait a bit more for server to fully initialize
        time.sleep(2)
        
        # Open dashboard
        open_dashboard()
        
        print("\n" + "=" * 50)
        print("🎉 SYSTEM STARTED SUCCESSFULLY!")
        print("=" * 50)
        print("\n📊 Dashboard: http://localhost:8000")
        print("📡 API Docs: http://localhost:8000/docs")
        print("\n💡 Available endpoints:")
        print("  • /api/predictions - AI vs Traditional predictions")
        print("  • /api/market-sentiment - Current market sentiment")
        print("  • /api/prices - Real-time prices")
        print("  • /api/opportunities - Investment opportunities")
        print("  • /api/alerts - Risk alerts")
        print("  • /api/correlations - Asset correlations")
        print("\n🔄 System will auto-refresh data every 5 minutes")
        print("\n⚠️  Press Ctrl+C to stop the system")
        
        try:
            # Keep the main process running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🛑 Shutting down system...")
            server_process.terminate()
            server_process.wait()
            print("✅ System shut down successfully!")
    
    else:
        print("❌ Failed to start system. Please check the logs.")
        sys.exit(1)

if __name__ == "__main__":
    main()
