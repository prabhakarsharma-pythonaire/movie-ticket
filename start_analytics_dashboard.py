#!/usr/bin/env python3
"""
Start Analytics Dashboard - Launches both FastAPI server and Analytics UI
"""

import subprocess
import time
import os
import sys
import signal
import threading

def print_header():
    print("🎬 MOVIE BOOKING ANALYTICS DASHBOARD")
    print("=" * 50)
    print("Starting both FastAPI server and Analytics UI...")
    print("=" * 50)

def start_fastapi_server():
    """Start the FastAPI server"""
    print("🚀 Starting FastAPI server on port 8000...")
    try:
        # Kill any existing process on port 8000
        subprocess.run(["pkill", "-f", "python -m app.main"], capture_output=True)
        time.sleep(2)
        
        # Start FastAPI server
        process = subprocess.Popen(
            [sys.executable, "-m", "app.main"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a bit for server to start
        time.sleep(5)
        
        if process.poll() is None:
            print("✅ FastAPI server started successfully!")
            return process
        else:
            print("❌ Failed to start FastAPI server")
            return None
            
    except Exception as e:
        print(f"❌ Error starting FastAPI server: {e}")
        return None

def start_ui_server():
    """Start the Analytics UI server"""
    print("🌐 Starting Analytics UI server on port 8080...")
    try:
        # Kill any existing process on port 8080
        subprocess.run(["pkill", "-f", "serve_analytics_ui.py"], capture_output=True)
        time.sleep(2)
        
        # Start UI server
        process = subprocess.Popen(
            [sys.executable, "serve_analytics_ui.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a bit for server to start
        time.sleep(3)
        
        if process.poll() is None:
            print("✅ Analytics UI server started successfully!")
            return process
        else:
            print("❌ Failed to start Analytics UI server")
            return None
            
    except Exception as e:
        print(f"❌ Error starting Analytics UI server: {e}")
        return None

def check_servers():
    """Check if both servers are running"""
    import requests
    
    try:
        # Check FastAPI server
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ FastAPI server is responding")
        else:
            print("❌ FastAPI server is not responding properly")
            return False
    except:
        print("❌ FastAPI server is not running")
        return False
    
    try:
        # Check UI server
        response = requests.get("http://localhost:8080/analytics_ui.html", timeout=5)
        if response.status_code == 200:
            print("✅ Analytics UI server is responding")
        else:
            print("❌ Analytics UI server is not responding properly")
            return False
    except:
        print("❌ Analytics UI server is not running")
        return False
    
    return True

def main():
    print_header()
    
    # Start FastAPI server
    fastapi_process = start_fastapi_server()
    if not fastapi_process:
        print("❌ Cannot start Analytics Dashboard without FastAPI server")
        return
    
    # Start UI server
    ui_process = start_ui_server()
    if not ui_process:
        print("❌ Cannot start Analytics Dashboard without UI server")
        fastapi_process.terminate()
        return
    
    # Check if both servers are running
    time.sleep(2)
    if check_servers():
        print("\n🎉 ANALYTICS DASHBOARD STARTED SUCCESSFULLY!")
        print("=" * 50)
        print("📊 Dashboard URL: http://localhost:8080/analytics_ui.html")
        print("🔗 API Server: http://localhost:8000")
        print("📋 API Documentation: http://localhost:8000/docs")
        print("=" * 50)
        print("⏹️  Press Ctrl+C to stop both servers")
        print("=" * 50)
        
        try:
            # Keep the script running
            while True:
                time.sleep(1)
                # Check if processes are still running
                if fastapi_process.poll() is not None:
                    print("❌ FastAPI server stopped unexpectedly")
                    break
                if ui_process.poll() is not None:
                    print("❌ Analytics UI server stopped unexpectedly")
                    break
                    
        except KeyboardInterrupt:
            print("\n🛑 Stopping servers...")
            
    else:
        print("❌ Failed to start Analytics Dashboard")
    
    # Cleanup
    if fastapi_process:
        fastapi_process.terminate()
    if ui_process:
        ui_process.terminate()
    
    print("✅ Servers stopped")

if __name__ == "__main__":
    main()
